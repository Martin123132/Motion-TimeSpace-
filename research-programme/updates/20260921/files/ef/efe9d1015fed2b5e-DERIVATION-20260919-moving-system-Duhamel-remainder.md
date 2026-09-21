# Restoring moving geometry and sources to the oscillatory bound

Private continuation of `DERIVATION-20260919-direct-forcing-and-frozen-time-bound.md`, 19 September 2026. This stage derives the exact terms omitted by the frozen control and evaluates them on the existing short numerical trajectory. It does not change the action, source condition, interpolation, couplings or saved evolution.

## 1. Exact fixed-basis moving-system identity

Keep the original fixed nodal interpolation I and define the hierarchy difference e=u_h-Iu_H, d=e_dot and a=e_ddot. The action residual satisfies

```text
M(t) a + K(t) e = R(t),
M(t) a_dot = R_dot - K_dot e - M_dot a - K d.                (1)
```

All the previously derived stiffness, source, cross-transport, mass-transport and inverse-solve residual channels belong to R. The second line requires differentiability along the actual canonical flow, not a frozen tangent direction.

Freeze only the *coordinate system* at t_star, with M_star,K_star positive and

```text
K_star U = M_star U Omega^2,   U^T M_star U = 1,
P = U^T M_star,
z = P a + i Omega P d,
E_star = (1/2) ||z||^2.
```

Unlike the physical coefficients, U and Omega are now fixed. Direct differentiation gives

```text
z_dot = i Omega z + F_star(t),
F_star = P M(t)^-1 [R_dot - K_dot e - M_dot a
                   + (M(t) M_star^-1 K_star - K(t)) d].    (2)
```

This is an identity, not an approximation or an assumption of slowly varying eigenvectors. It remains meaningful at instantaneous eigenvalue crossings because no time-dependent eigenbasis is differentiated. E_star uses the frozen metric; it is not silently identified with the instantaneous action energy.

Let z_fr be the earlier homogeneous two-grid frozen solution, including its stiffness mismatch forcing f_fr=U^T D_star v_H,fr. For w=z-z_fr,

```text
w_dot = i Omega w + eta,
eta = F_star - f_fr,
w(t) = exp(i Omega (t-t_star)) w(t_star)
     + integral exp(i Omega (t-s)) eta(s) ds.              (3)
```

Consequently ||w|| is bounded by its initial norm plus the integral of ||eta||, whenever that integral is actually controlled. Neither endpoint ||eta|| nor its sampled maximum supplies such a control automatically.

At the freeze point, (2) simplifies to

```text
eta_star = U^T [R_dot - D_star v_H - K_dot e - M_dot a].   (4)
```

The initial positions and velocities of the live/frozen scalar fields agree, but their accelerations need not:

```text
w_star = P (a_live,star - a_fr,star).                     (5)
```

This term was absent from any attempted direct transfer of the frozen bound to the live system. It is retained here. The existing nested canonical probes check (2)-(5); no new numerical jerk is generated.

## 2. A derivative-free way to evaluate the accumulated correction

The live trajectory exists on 0<=t<=t_star=4e-5, whereas the preceding frozen example was propagated forward from t_star. To compare like with like, use theta=t_star-t and propagate the frozen control *backwards*: initial scalar velocity changes sign, acceleration does not. This does not assert reversibility of a dissipative model; it is a reparameterization of the already saved canonical trajectory. The all-mode amplitude envelopes are unchanged by this velocity sign flip, but the actual frozen wave phases are recomputed.

For each level ell=H,h define A_ell,star=M_ell,star^-1 K_ell,star and

```text
r_ell(theta) = u_ell''(theta) + A_ell,star u_ell(theta).
```

Writing the actual scalar action equation as M_ell u_ell''+K_ell u_ell=b_ell gives the non-circular action evaluation

```text
r_ell = (A_ell,star - M_ell^-1 K_ell) u_ell + M_ell^-1 b_ell,
b_ell = source_kinetic - C_dot s_dot - C s_ddot
       - M_dot u_dot - inverse_residual_dot.              (6)
```

Dots in the numerical action loads refer to the original forward canonical parameter; the second derivative and products in (6) transform consistently under reversal. The code obtains the acceleration from the differentiated momentum relation and separately checks it against the canonical velocity derivative. It also retains the floating canonical-force/action-load reconstruction defect instead of setting it to zero.

Seven evaluated channels are therefore geometry/stiffness drift, source kinetic load, cross transport, source acceleration, mass transport, inverse residual and canonical/action reconstruction defect. Mass derivatives, cross derivatives and source accelerations use finite directional probes. These are numerical evaluations of (6), not exact symbolic or interval-certified coefficient derivatives.

For delta_u_ell=u_ell-u_ell,fr, both initial displacement and initial velocity vanish, and

```text
delta_u_ell'' + A_ell,star delta_u_ell = r_ell.            (7)
```

In each complete mass-normalized modal basis V_ell, put rho_ell=V_ell^T M_ell,star r_ell. The modal response obeys

```text
x_ell(theta) = integral_0^theta sin(omega_ell(theta-s))/omega_ell rho_ell(s) ds,
y_ell(theta) = integral_0^theta cos(omega_ell(theta-s)) rho_ell(s) ds,
b_ell,response = rho_ell(theta)-omega_ell^2 x_ell(theta).  (8)
```

This evaluates the correction from action acceleration without differentiating it again. The source acceleration symbol in (6) is distinct from b_ell,response in (8).

Let J=V_h^T M_h,star I V_H. In fine energy coordinates the complete correction is

```text
C(theta) = b_h,response - J b_H,response
         + i Omega_h (y_h-J y_H),
z_live(theta) = z_fr(theta)+C(theta).                     (9)
```

At theta=0, C=rho_h(0)-J rho_H(0), exactly the nonzero initial acceleration correction (5). In particular, zero initial delta_u and delta_u' do not imply zero initial differentiated-energy error.

## 3. What the sampled convolution proves, and what it does not

All33 matched saved times are used, with all558 coarse and1072 fine modes. The same retained data are reconstructed using9,17 and33 forcing nodes. On each interval rho is interpolated linearly; its harmonic-oscillator convolution is evaluated analytically, not by a timestep that must resolve every wave frequency.

For interval length h, starting force rho_0 and slope sigma, the source additions to modal position and velocity are

```text
delta_x = (1-cos(omega h))/omega^2 rho_0
        + (h-sin(omega h)/omega)/omega^2 sigma,
delta_y = sin(omega h)/omega rho_0
        + (1-cos(omega h))/omega^2 sigma.                 (10)
```

Stable sinc formulas and the zero-frequency polynomial limit avoid cancellation and division by zero. Independent quadrature and subdivision controls check (10). No mode or source row is clipped. The source interpolation is an approximation; its exact convolution is not therefore an exact live trajectory.

Let C_PL be this response and epsilon=z_live-z_fr-C_PL. At the level of a sufficiently regular exact trajectory, epsilon contains the forcing-interpolation remainder. When comparing numerical snapshots it can also contain the original evolution error, coefficient/probe error and floating arithmetic. The saved discrepancy is reported, never set to zero because the code completed.

If B_i(theta)=|z_fr,i(0)|+r_fr,i(theta) is the earlier analytic all-mode frozen envelope, the conditional live bound is

```text
sqrt(2 E_star,live) <= ||B+|C_PL|||_2 + ||epsilon||_2.     (11)
```

The table's bound omitting epsilon is explicitly conditional. A sampled point inside it is not a continuous-time pass. Adding the measured epsilon at that same point would be an a posteriori identity check, not an independently predicted bound.

### An explicit route to a certified interpolation remainder

Let k_ell=rho_ell-rho_ell,PL and I_ell,j=integral_0^T |k_ell,j(s)| ds. At interpolation nodes the ideal k_ell(T) vanishes. Using (8), a componentwise remainder bound is

```text
|epsilon_i(T)| <= Omega_h,i I_h,i
  + sum_j |J_ij| (omega_H,j+Omega_h,i) I_H,j.              (12)
```

At other times add |k_h,i(T)|+sum_j|J_ij||k_H,j(T)|. If a parent-owned regularity estimate establishes |rho_ell,j''|<=Q_ell,j on each interval of width h, linear interpolation gives

```text
integral_interval |k_ell,j| <= Q_ell,j h^3/12.             (13)
```

Equations (12)-(13) display the required norm, frequency weights and powers of the sampling width. They are a conditional theorem, not an assertion that such Q have already been bounded for MTS. Finite differences of sampled rho alone would not certify them. Numerical trajectory error requires its own contribution rather than being hidden inside an asserted continuum Q.

## Numerical results and decision

### Endpoint identity

Both saved probe sizes pass the independent fixed-basis derivative comparison. At the smaller probe5e-8:

| Branch | Frozen stiffness forcing norm | Additional eta norm | Direct action initial acceleration-gap norm |
|---|---:|---:|---:|
| Reference | 0.84335330 | 0.20564904 | 2.67752246e-6 |
| MTS | 46.06972841 | 0.42840685 | 3.49677243e-6 |

The MTS correction is about0.93% of the main stiffness-forcing norm at this endpoint; the reference ratio is about24.4%. These ratios are not a comparison of empirical theory quality: their baseline forcing norms differ substantially. Both branches receive the same test, and neither endpoint ratio is used as an interval bound.

### Matched saved trajectory

The action acceleration and all seven forcing channels were evaluated at33 matched times on each branch, at both resolutions. The canonical acceleration check passes at every point. The smaller acceleration probe is also checked at the beginning, middle and end. The single-core calculation took2793seconds, about46.6minutes; no new live trajectory was run.

At reverse offset theta=4e-5, corresponding to the **original physical time t=0**, not a forecast beyond the saved trajectory:

| Branch | Saved fixed-metric energy | Reconstructed energy | Frozen analytic envelope | Conditional envelope including C_PL but not epsilon |
|---|---:|---:|---:|---:|
| Reference | 2.88835545e-7 | 2.88835405e-7 | 4.87497247e-7 | 4.88231023e-7 |
| MTS | 4.80298877e-6 | 4.80299818e-6 | 1.56391594e-5 | 1.56641151e-5 |

All33 samples in each branch lie inside their conditional envelope. Including the computed moving/source response increases the endpoint envelope by approximately0.15%(reference) and0.16%(MTS). This is evidence that those corrections need not destroy the useful frozen estimate on this short numerical trajectory. It is **not** a certified live bound or a reduction of the original hierarchy-force error.

The unresolved response norm, unlike the scalar energy comparison, exposes an important difference:

| Branch | 9 forcing nodes | 17 forcing nodes | 33 forcing nodes |
|---|---:|---:|---:|
| Reference | 6.22789856e-7 | 1.50591727e-7 | 3.68252509e-8 |
| MTS | 3.58257268e-6 | 3.52620350e-6 | 3.52496503e-6 |

Reference shows approximately second-order improvement with forcing-grid refinement; MTS initially reaches a floor. It would be incorrect to call that a continuum failure or to hide it behind an excellent energy match.

### A numerical floor identified and retained

The actual final trajectory arrays, accepted-state arrays, canonical velocities, masses and compensated accelerations agree exactly with their previously saved counterparts. A state mix-up does not explain the floor.

The additional diagnostic compares two floating evaluations of the same ideal modal forcing:

```text
rho_action = P (a + A_star u),
rho_coordinate = P a + Omega^2 P u,
delta_rho_arithmetic = rho_coordinate-rho_action.          (14)
```

They agree in exact arithmetic for an exact generalized eigensystem. A small eigensystem backward error or small position reconstruction error does not by itself guarantee accurate acceleration after multiplication by the largest squared frequencies. This is a conditioning issue in the diagnostic representation, not a newly discovered source term of the theory.

Measured maximum modal arithmetic defects are1.44e-9(fine reference) and3.09e-6(fine MTS), with coarse maxima1.17e-10 and1.80e-6 respectively. The MTS reconstruction already has a3.47500e-6 residual at zero elapsed time; a temporal integration or source-interpolation error cannot explain a zero-time residual.

We therefore retain delta_rho_arithmetic explicitly in a separate diagnostic reconstruction, along with the measured fine modal mass Gram matrix P_h V_h rather than silently identifying it with the identity. No coefficient is fitted, no mode is discarded, and the original action forcing and previous results remain unchanged. This is an arithmetic-accounted coordinate control, not a replacement physical action.

The zero-time residual then falls to1.73e-14(reference) and2.96e-14(MTS). At theta=4e-5:

| Branch | Original unresolved norm | Arithmetic-accounted unresolved norm | Maximum accounted residual over33 samples |
|---|---:|---:|---:|
| Reference | 3.68252509e-8 | 3.67966726e-8 | 4.44680171e-8 |
| MTS | 3.52496503e-6 | 5.90903714e-7 | 3.02272953e-6 |

Thus the leading zero-time mismatch was indeed numerical, and accounting for it reduces the final MTS residual by about6times. **It does not eliminate the interval residual.** The largest remaining MTS discrepancy occurs at theta=1.625e-5; at the final offset the9/17/33-node accounted residuals are8.71012e-7,5.98245e-7,5.90904e-7. By contrast, changes in the response itself decrease from6.85717e-7(9to17nodes) to1.61855e-7(17to33nodes). Simply increasing this interpolation grid is therefore not a demonstrated cure for the remaining floor.

The exact identity (9) and the source interpolation error budget (12)-(13) remain conditional on exact operators/trajectories. Numerical spectral representation and original evolution defects must enter a rigorous computed envelope too. The new diagnostic has not certified either of them.

### Decision and next calculation

The moving/source correction has now been derived and evaluated, rather than merely listed as missing. It does not show catastrophic amplification in the saved short test, and an identifiable part of the MTS reconstruction mismatch comes from numerical modal arithmetic. However, the remainder is not fully closed and the original force discrepancy is untouched.

**Next:** perform an action-consistent frozen response comparison using the original banded mass and factored stiffness operations, without deriving acceleration by squaring approximate eigenfrequencies. Compare it with the retained modal result on both branches, then use the existing temporal-halving trajectories to separate original time-integration error from representation error. This is a bounded diagnostic before any longer evolution or claim that (11) is a certified live bound. Do not fit away the residual, delete the old bound, or infer failure of the theory from a numerical floor alone.

There are642successful implementation checks:30algebra/endpoint,537matched-trajectory and75arithmetic-diagnostic checks. The counts certify execution controls, not642independent physical tests. No new failed execution was discarded or converted into a pass.

## Provenance and scope

- Prior complete seal: `source-intake/navier-stokes/20260914/annular-direct-forcing-time-bound-final-integrity.json`.
- Direct fixed-basis and source-response helpers: `scripts/annular_moving_duhamel_20260919.py`.
- Independent oscillator/product-rule controls and saved nested endpoint comparison: `scripts/validate_annular_moving_duhamel_20260919.py`.
- Matched saved-trajectory action evaluation: `scripts/derive_annular_moving_duhamel_trajectory_20260919.py`.
- Retained modal arithmetic diagnostic: `scripts/diagnose_annular_modal_arithmetic_remainder_20260919.py`.
- Original action residual channels: `scripts/annular_wave_error_energy_20260919.py`.
- Original compensated momentum derivative: `scripts/annular_compensated_momentum_rate_20260919.py`.

The original **12.5718%** impulse and approximately **13.58%** instantaneous hierarchy-force discrepancies remain unchanged. This does not establish the full GR limit, a continuum convergence rate, nonlinear global stability, an observational/SI test or a certified live time envelope. The .004 interval is not rerun. Counts are implementation checks, not independent physical validations. All44 historical failed executions remain preserved. No GitHub, subagents, new live evolution, changed equations or sibling-workbench edits.

Protected-workbench verification uses mtime since2026-09-19 17:30:22UTC, not a pre-turn whole-tree hash baseline.
