# Derived omitted transport and background-path map correction

This stage differentiates and extends the SAME retained physical source and original perturbation preparation. The accepted preceding stage is ../mts-invariant-correlated-early-transport-20261108, closeout SHA25618ef599d24a4382fe47634c2bf98eb0c3c1663de83ed0732c79017628db34a2e. It supplies the successful leading short-interval comparison, not an observational fit.

## 1. Differentiate the implicit density at fixed physical phase

Let x = ln rho, b = ln rho_bar and g be the previously derived invariant corrector. The retained candidate satisfies x = b + g(x,N,theta), b_N = -1. Here g_N denotes partial differentiation through the saved slow scalar and external source laws, holding x and theta fixed. Consequently

    x_N|theta = (-1 + g_N)/(1-g_x)
    x_theta = g_theta/(1-g_x)
    rho_N|theta = rho x_N|theta
    rho_N|path = rho_N|theta + rho_theta Omega
    Omega = omega_h/H(rho_rec) - 3 sin(2theta)/2.

The denominator is justified by the preceding contraction theorem, not a fitted regularizer. The candidate still omits the nonzero invariant drift Delta_I, which belongs to its background error. Saved slow-scalar and conformal-clock derivatives are obtained by differentiating the retained dense interpolation polynomial, not by substituting the desired exact equations.

The exterior source and all its needed derivatives are propagated through the existing source_laws.py expressions with a scalar directional jet. That jet is independent of the inner Tangent used by the physical metric-map construction: nesting them differentiates the actual generator, including derivatives of its original-flow coordinate maps. Thermal value derivatives use the original cubic's first/second derivatives at the retained cell. No bank or temperature curve is changed.

## 2. Differentiate the normalized clock measure too

For w = 1/Omega and M = sum(w A)/sum(w), the finite retained phase quadrature satisfies

    w_N = -Omega_N/Omega^2
    M_N = <A_N>_w + sum[w_N (A-M)]/sum(w)
    F = (A-M)/Omega
    F_N = (A_N-M_N)/Omega - F Omega_N/Omega.

The periodic primitive is C_theta = F with zero ordinary phase mean. Therefore its fixed-phase slow derivative is obtained by integrating F_N in phase, with zero phase mean again. To avoid losing a small phase-varying derivative beside a large constant scattering diagonal, subtract A(theta=0) and its derivative BEFORE the weighted calculation; put the constant mean terms back afterwards. This is an algebraic representation, not smoothing.

The same construction is applied to 1/H. With the complete remote hierarchy A_remote = D_remote + S_remote/H,

    C_remote = p_H S_remote
    (D_slow C)_remote = (D_slow p_H) S_remote + p_H (D_slow S_remote).

The derivative of S_remote is retained. All190 tail levels at each of five nodes and cross-boundary couplings remain. A compact-only slow derivative is not substituted for the complete primitive.

## 3. Reconstructed background versus original physical flow

The reconstructed background trajectory is not declared an exact solution. At each fixed source and phase calculate the actual retained rates and the original rates

    U_N = U + omega_s V/H
    V_N = -2V - omega_s U/H
    rho_N = (-1+3cos(2theta))rho
    tau_N = 1/H.

Their signed difference is delta_v. The relative phase obeys its own retained physical equation, so its rate defect is zero here. Source scale, fluid populations and external densities have the same N evolution in both descriptions. The conformal-clock defect is explicitly recorded; its absence from a particular coordinate map does not make it vanish from the source's clock dependence.

Let B map the original normalized variables to physical energy coordinates, R_phys be the first closed-map inverse, and S_phys = R_phys^-1. For z = R_phys B u, the additional generator caused by differentiating maps along the substituted rather than original flow is

    Delta_map = (delta_v . grad R_phys) S_phys
                + R_phys [(delta_v . grad B) B^-1] S_phys.

This sign follows directly from differentiating z, not from fitting the observed discrepancy. The source-owned physical B is derived explicitly, including gauge shifts, cold massive weights, slow field and relative heavy density/phase coordinates. Its value is checked against the retained native map. Constant native units and a fixed carrier chart cancel out of its logarithmic derivative; the physical phase is not identified with that carrier. Baseline has no invented heavy block. Setting delta_v=0 makes this map defect exactly zero, but does not erase baseline numerical errors.

## 4. Exact normal-form forcing on the chosen background

Let P = I+C and use Omega C_theta = A-M. Along the chosen background,

    P_N = A-M + D_slow C
    z_N = (A+Delta_map) z
    y_N = M y + R_total y
    R_total = P^-1 [A C - C M - D_slow C + Delta_map P].

The noncommuting order of all products is retained. The code evaluates full sparse matrix actions and a full endpoint inverse, rather than dividing entries or discarding the remote hierarchy. It checks the original chain rule at every phase on the actual saved vector. This is a generator identity ON THE CHOSEN reconstructed background; the difference between its physical source and the original reference background remains a separate error.

## 5. First propagated correction without fitting a residual

With y0 the saved leading mean solution, freeze the two derived forcings

    f_normal = P^-1 [A C - C M - D_slow C] y0
    f_map = P^-1 Delta_map P y0.

Compute them at the retained phase grid and selected saved source epochs. Keep their complete discrete Fourier coefficients. The first variation of constants is

    delta_y_N = M delta_y + f_normal + f_map
    delta_y(N_initial) = 0.

Integrate the two contributions separately, using the unchanged original collision split and an independently reproduced physical phase. The corrected output uses the SAME physical endpoint maps and original initial preparation. No late reset or reference phase is used. No observed reference residual determines a coefficient.

This first response does not include R_total delta_y or the difference between the chosen and true background sources. Its accuracy must be measured; it is not an exact re-solution by definition. Nine versus five forcing epochs and512 versus256 time-step limits are numerical controls. Report uncertainty relative to BOTH the retained physical state and the small correction; do not hide a poorly resolved correction behind its small size. Compare frozen corrected physical outputs to the same original reference, noting that this is a previously examined internal reference, not a newly held-out observational dataset.

## Verification and provenance

- Independent complex-direction calculations check the nested jet and implicit rho_N derivative, with two step sizes.
- Native physical-map values, zero-defect identity and source generator values are checked for baseline and MTS.
- Fixed-theta finite differences of the FULL re-evaluated primitive test D_slow C; a moving-endpoint difference would test a different derivative and is deliberately not used.
- Phase128/256 refinement, normalized-clock closure, complete hierarchy identity and the full chain rule use the unchanged ALGEBRA1e-10/GATE2e-5.
- REPORTING-REPAIR.md preserves an initial metadata TypeError and its diagnosed non-mathematical fix. No failed physics gate is silently called a success.

The stage remains local and preserves earlier sealed results. These derived terms are the next quantitative step toward transporting the original mode into the controlled cold/GR/Newton regime, rather than inserting an exact-zero closure for the approximation error.
