# Cancellation-aware canonical driver and conditional energy law

Private continuation, 19 September 2026. The action, source condition, all scalar modes, live geometry and both comparison branches are unchanged. No new trajectory was evolved. This stage does not establish the full GR limit, continuum force convergence or observational agreement.

## What changed

The previously isolated instantaneous hierarchy driver is not an independent canonical-momentum effect. At the saved final MTS pair its momentum contribution is **+4745.491977622051** and its source kinetic cross contribution is **-4745.475910785766**. Their combined result, including both inverse residuals and the nonnested transfer jump, is **+0.016066836279768248**. Bounding or explaining either large contribution on its own loses the central cancellation.

We have now derived and tested the combined momentum-minus-source-motion evolution, its changing-functional driver rate, and a conditional kinetic-error energy inequality. This replaces the previous untested residual-driver target with actual source-backed calculations. It is not a new physical coupling, modified action, or proof that the remaining force error is harmless.

The old **12.5718%** integrated-impulse and approximately **13.58%** instantaneous reduced-force hierarchy discrepancies remain unchanged. The comparison covers normalized annular time T=4e-5, not the older full interval .004. The spatial pair also uses unequal saved time resolutions; its difference is not isolated spatial truncation error.

## 1. Exact finite-system driver, with the cancellation retained

Use coarse/fine subscripts H/h. Each system has its own actual live scalar mass matrix M, scalar canonical momentum p, scalar velocity v, kinetic source cross covector b and source velocity V. Let

    r = p - M v - b V

be the measured inverse-solve residual; it is not silently set to zero. I is fixed reference nodal interpolation of fields/velocities. Momentum covectors are NOT interpolated as nodal values.

    rho = p_h - b_h V_h - M_h I v_H
    d = v_h - I v_H = M_h^(-1) (rho-r_h).

The equivalent separated load is

    rho_p = p_h - M_h I M_H^(-1) p_H
    rho_b = -b_h V_h + M_h I M_H^(-1) b_H V_H
    M_h d = rho_p + rho_b + M_h I M_H^(-1) r_H - r_h.

The map M_h I M_H^(-1) compares induced velocities. This is NOT a statement that I or that covector map is a canonical/symplectic intergrid transfer.

With fine lifted operator B_h=D_h-r_lift,h j_h, define the transfer jump

    J = j_H v_H - j_h I v_H.

The off-space coarse extension retains the original coarse jump. For a row covector g,

    D = g^T [B_h d + r_lift,h J]
      = ell^T d + beta J,
    ell = B_h^T g, beta = g^T r_lift,h.

Here g is built from the existing fine response and Gram weights; left, right and mean-trace-weighted functionals are each checked. No source or remaining Gram rows are discarded.

With z=M_h^(-1)ell and c=rho-r_h,

    |D| <= sum_i |z_i c_i| + |beta J|
    |D| <= ||ell||_(M_h^-1) ||c||_(M_h^-1) + |beta J|

where the second displayed right-hand side is a separate Cauchy bound, not an assertion that the first bound is always smaller in every problem.

### Actual final MTS result

| Quantity | Normalized value |
|---|---:|
| Direct driver D | +0.016066836279768248 |
| Momentum contribution | +4745.491977622051 |
| Source-cross contribution | -4745.475910785766 |
| Coarse inverse-residual contribution | -1.8394e-13 |
| Fine inverse-residual contribution | -1.3381e-13 |
| Transfer-jump contribution | -5.6242e-12 |
| Five-channel reconstruction error | 6.4731e-13 |
| Combined localized absolute bound | 0.2830388105514879 |
| Broad mass-norm bound | 220.58057184249236 |
| Residual pairing near source | +0.016322864755463014 |
| Residual pairing away from source | -0.0002560284695704667 |

Near source means reference nodal distance <=4e-5, for localization only. The localized bound is about17.62 times the actual driver, not a sharp continuum estimate. The actual inverse momentum residual is at most2.71e-20 across these saved comparisons; velocity reconstruction errors are below1.6e-19.

The initial MTS driver is only about7.09e-12 after cancellation of terms of magnitude4745.56. The conservative separated-channel checking tolerance exceeds this initial value: no physically resolved initial growth is inferred from it. Reference Gram quantities are identically zero, so those zeros are NOT a nontrivial physical reference-force validation. Independent nonzero fixtures test both omitted inverse residuals and omitted transfer jumps.

## 2. Derive the coupled evolution, not two unrelated large bounds

Along the unchanged canonical evolution, write F=dot(p), A=dot(V). Differentiating the actual mass relation gives

    M dot(v) = F - dot(b) V - b A - dot(M) v - dot(r).

Every term matters. In particular dot(b) includes scalar/source motion and live geometry; dot(M) includes the complete geometry response. The source acceleration is not arbitrarily fixed. Retaining dot(r) distinguishes an exact numerical inverse from the actual iterative solve.

For the lifted driver D=ell^T d+beta J on fixed reference grids,

    dot(D) = ell^T [dot(v_h)-I dot(v_H)]
           + dot(ell)^T d + beta dot(J) + dot(beta) J,
    dot(J) = j_H dot(v_H) - j_h I dot(v_H).

The changing ell/beta include the fine mass response, Gram weights and, for the trace-weighted functional, the changing mean source trace. Thus the calculation does not freeze the live geometry or omit the nonnested jump rate.

### What was actually tested

At the saved final state, perturb the COMPLETE joint canonical state in its full RHS direction, recomputing all-label live geometry at both signs. Probe sizes are2e-7,1e-7,5e-8,2.5e-8. These are symmetric tangent probes, not evolved neighboring trajectories. All geometry, source-acceleration and inverse-residual rates here are finite-difference estimates, not certified derivatives.

An independent centered-product check uses the exact finite-difference product identity with arithmetic-mean M,b,v,V. That check is deliberately identified as algebraic: differentiating a measured inverse relation and recovering its derivative is NOT independent validation of the underlying physical equations. Separate dense analytic fixtures and omission controls test the formula; actual full-state probes establish its numerical implementation on these saved systems.

At the finest final MTS probe, the mean-trace-weighted driver rate is:

| Contribution | Approximate normalized rate |
|---|---:|
| Canonical scalar-force contrast | +54710.66377572 |
| Cross-covector transport | -389.55298390 |
| Source acceleration | +2332.31141380 |
| Mass transport | -0.001961865 |
| Inverse-residual derivative | -0.000034987 |
| Changing response/weight/trace functional | +0.001290448 |
| Transfer-jump rate | -0.000002124 |
| Combined predicted rate | +56653.42149710 |
| Direct tangent-probe rate | +56653.42151783 |
| Localized absolute bound | 66726.58623683 |

The trace-weighted direct/composed comparison errors across probe refinement are approximately4.17e-6,1.94e-6,2.76e-6,2.07e-5: **NOT monotone**. The finest maximum error over all left/right/trace-weighted partitions is approximately.001184. The stored acceptance tolerances are conservative; the finest trace-weighted tolerance is11.33, much larger than its observed error. Do not treat pass flags as sharper certificates than the numerical evidence warrants.

The finest vector acceleration reconstruction errors are below4.6e-12, on a scalar-acceleration scale about.1226. Very small channels, especially differentiated inverse residuals, remain roundoff-sensitive. Neither their sign nor many quoted digits should be interpreted as physics. The large instantaneous driver rate is NOT the total reduced-force acceleration, nor an extrapolation of D over the full time interval.

## 3. A cancellation-aware conditional energy estimate

Define the combined force covector and comparison map

    C_a = F_a - dot(b_a) V_a - b_a A_a - dot(r_a),
    T = M_h I M_H^(-1).

Then the actual velocity difference obeys

    M_h dot(d) + dot(M_h) d = L,
    L = C_h - T C_H + [T dot(M_H) - dot(M_h) I] v_H.

The bracket is the mass-transport commutator; omitting it is false in the independent noncommuting-matrix controls. No derivative of I appears because these reference interpolation grids are fixed. Time-dependent remeshing would require another term and is outside this statement.

For positive M_h,

    E = (1/2) d^T M_h d,
    dot(E) = d^T L - (1/2) d^T dot(M_h) d.

If |x^T dot(M_h) x| <= gamma x^T M_h x, then

    |dot(E)| <= sqrt(2E) ||L||_(M_h^-1) + gamma E.

For symmetric strictly row-diagonally-dominant M, a sufficient computable bound is

    margin_i = M_ii - sum_(j!=i) |M_ij| > 0,
    gamma = max_i [sum_j |dot(M)_ij| / margin_i].

This follows by quadratic-form row bounds; it does not need a dense generalized eigensolve. All actual fine mass margins are positive in these probes.

Writing R=sqrt(2E), the corresponding conditional time-interval estimate is

    R(t) <= exp((1/2) integral_0^t gamma) R(0)
          + integral_0^t exp((1/2) integral_s^t gamma) ||L(s)||_(M_h(s)^-1) ds.

This requires positive mass, the necessary regularity and valid bounds along the entire interval. Sampled finite-difference inputs are NOT such a time-uniform certificate. Moreover L depends on the coupled systems, including their source accelerations; it is not yet closed in terms of a controlled error norm. The derived inequality is conditional, not a proved stability theorem for MTS.

### Actual finest-probe energy diagnostics

| Quantity | Reference | MTS |
|---|---:|---:|
| E | 3.31746e-16 | 8.54327e-15 |
| dot(E) | +1.46156e-11 | +4.00319e-10 |
| ||L||_(M^-1) | 0.000758980 | 0.00309863 |
| Sampled row-based gamma | 0.31207910 | 0.31207916 |
| Bound on abs(dot(E)) | 1.95502e-11 | 4.05042e-10 |
| sqrt(2E) | 2.57583e-8 | 1.30715e-7 |

The MTS energy-rate bound is relatively tight at this endpoint. That is a mathematical bound on this sampled diagnostic, not an improvement of the unresolved12.5718% physical hierarchy discrepancy. The same protocol is applied to the reference branch rather than calling reference Gram zeros a robustness baseline.

## 4. Why growing kinetic error is not yet instability; next concrete calculation

The scalar wave force exchanges kinetic and potential error energy. An independent unit-frequency oscillator control has positive kinetic-energy rate sqrt(3)/4 and negative potential-energy rate -sqrt(3)/4, with zero total rate. Calling its kinetic growth instability would be wrong.

Let e=u_h-I u_H, so dot(e)=d, and let K_h be the existing symmetric nonnegative scalar stiffness at the current live geometry. Define

    E_wave = (1/2) d^T M_h d + (1/2) e^T K_h e,
    R_wave = M_h dot(d) + K_h e.

Exactly,

    dot(E_wave) = d^T R_wave
               + (1/2) d^T dot(M_h) d
               + (1/2) e^T dot(K_h) e.

The conservative -K_h e work cancels instead of being counted twice as growth. Independent dense controls verify this identity and reject omission of the potential-energy rate. Its actual MTS trajectory bound has NOT been evaluated here; positivity/coercivity must be checked on the retained space, and this scalar energy is not automatically the total source-plus-gravity Hamiltonian.

**Next substantive step:** evaluate the kinetic-plus-potential hierarchy error on the same saved pairs, split R_wave into conservative stiffness-transfer mismatch and retained source/geometry/transport terms, then test whether the dominant force work is reversible exchange or a persistent consistency defect. Keep dot(K), live geometry, inverse residuals, original source constraint, nonnested transfer and both branches. No mode clipping, fitted coupling, blind long rerun or general missing-input survey is justified by this stage.

## Evidence and reproducibility

Successful new implementation checks:300 (20 static algebra,86 actual driver,28 derivative algebra,120 actual tangent-rate controls,46 energy/commutator controls). They are implementation/finite-diagnostic checks, not300 independent physics confirmations. No failed execution occurred in this stage; all43 previously failed executions remain preserved in the inherited evidence chain.

- Previous seal: `source-intake/navier-stokes/20260914/annular-coefficient-bounds-rate-final-integrity.json`
- Driver algebra: `source-intake/navier-stokes/20260914/annular-canonical-driver-algebra-attempt01/status.json`
- Actual driver: `source-intake/navier-stokes/20260914/annular-live-canonical-driver-attempt01/status.json`
- Derivative algebra: `source-intake/navier-stokes/20260914/annular-compensated-rate-algebra-attempt01/status.json`
- Actual rates: `source-intake/navier-stokes/20260914/annular-live-compensated-rate-attempt01/status.json`
- Energy bounds: `source-intake/navier-stokes/20260914/annular-compensated-energy-bound-attempt01/status.json`
- Driver helper: `scripts/annular_canonical_driver_residual_20260919.py`
- Rate helper: `scripts/annular_compensated_momentum_rate_20260919.py`
- Rate runner: `scripts/derive_annular_live_compensated_rate_20260919.py`
- Energy runner: `scripts/derive_annular_compensated_energy_bound_20260919.py`

Only post-checkpoint-work is used. No GitHub or subagents. Computations used one actual single-core BelowNormal worker at a time; Windows venv launcher/child pairs are not separate jobs. The final integrity seal must hash inherited and new evidence, validate sourced nonclaim CSVs and source compilation, and snapshot the continuation note. Its protected-workbench check is an mtime scan since13:37:35UTC, not a pre-turn whole-tree hash baseline.
