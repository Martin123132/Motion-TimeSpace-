# Direct stiffness forcing and a controlled time envelope

Private continuation of `DERIVATION-20260919-action-test-energy-and-transfer-stability.md`, 19 September 2026. Original moving dynamics, source condition, interpolation and force results remain unchanged. The purpose is to replace a numerical jerk in the leading residual by an explicit operator law, then test how much time control it actually provides.

## 1. Direct derivative, with all terms retained

Let I be the original fixed, nonnested nodal interpolation, and let K_H,s and K_h,s be the coarse and fine stiffness in sector s (gradient, Gram, or their sum). Define

```text
T = M_h I M_H^-1,
D_s = T K_H,s - K_h,s I,
S_s = D_s u_H.
```

Differentiating the mass inverse, not commuting operators, gives

```text
T_dot = M_h_dot I M_H^-1 - T M_H_dot M_H^-1,
D_s_dot = T_dot K_H,s + T K_H,s_dot - K_h,s_dot I,
S_s_dot = D_s v_H + D_s_dot u_H.                     (1)
```

Its expanded form has six terms:

```text
 + M_h_dot I M_H^-1 K_H,s u_H          fine-mass transport
 - T M_H_dot M_H^-1 K_H,s u_H          coarse-mass transport
 + T K_H,s_dot u_H                    coarse-stiffness transport
 - K_h,s_dot I u_H                    fine-stiffness transport
 + T K_H,s v_H                        coarse trial velocity
 - K_h,s I v_H                        fine trial velocity.          (2)
```

Source traces and source motion enter the original compensated stiffness and its mapped weights; nothing is clipped or set to zero. The reference has no additional Gram operator, but its gradient forcing is nonzero and is tested with the same calculation. The total-stiffness result is checked against the sum of the two sector results.

Equation (1) needs coarse field velocities and mass/stiffness derivatives, **not a newly calculated field jerk**. Geometry derivatives are still finite directional estimates in the numerical evaluation; this is not an assertion that every coefficient derivative has become analytic.

## 2. A conditional coarse-energy bound

For positive action mass/stiffness matrices, define

```text
C_s = ||M_h^(-1/2) D_s K_H^(-1/2)||,
G_s = ||M_h^(-1/2) D_s_dot K_H^(-1/2)||.
```

Then

```text
||S_s_dot||_(M_h^-1) <= C_s ||v_H||_(K_H) + G_s ||u_H||_(K_H).      (3)
```

Here K_H is the full coarse action stiffness, not just its possibly singular Gram component. Numerical constants come from the complete whitened matrices, with an eigenvalue estimate and a row-sum upper bound. Cancellations are retained inside D_s and D_s_dot before taking norms.

These are **coarse background norms**, not error norms E_0 or E_1. A homogeneous bound solely in the hierarchy error is not justified: a nonzero stiffness mismatch can force an initially matched pair of fields. In terms of coarse action energies, ||u_H||_K <= sqrt(2 E_H,0) and ||v_H||_K <= sqrt(2 E_H,1), assuming the corresponding positive kinetic terms. Closing their evolution is a further requirement, not a free assumption.

Substituting (3) for the stiffness portion of F=||R_dot||_(M_h^-1) in the previous energy inequality yields an explicit *conditional* time estimate. The other source/transport residual derivatives remain in R_dot. Endpoint values of C_s,G_s or coarse energies are not uniform-in-time envelopes. Finite-grid constants do not establish a refinement-uniform continuum estimate.

Three bounds are kept separate in the calculation:

1. the sum of the norms of all six terms in (2);
2. the paired-vector bound ||D_s v_H|| + ||D_s_dot u_H||;
3. the background-energy bound (3).

All have the same mass-dual norm. Their relative sizes diagnose what is lost by taking absolute values, not alternative physical predictions.

## 3. Numerical comparison and the preserved failed attempt

The actual final coarse/fine states and canonical directions are reused, on both branches, at outer probe sizes1e-7 and5e-8. The direct law is compared with a symmetric derivative of the original stiffness residual and with the preceding nested canonical channel work/maxima. No new live trajectory is integrated and no new nested jerk is computed.

The first runner used assembled dense stiffness-matrix products also for the tiny endpoint secant. At reference step5e-8 it failed the strict old-channel comparison: work disagreement9.57827e-10 and maximum-component disagreement3.36084e-8. That failed execution and its partial outputs remain immutable.

The replacement runner restores the **same factored action-load arithmetic used by the saved comparison**, including the original nodal interpolation and banded mass action. It does not relax that comparison threshold or change the equations. Dense-versus-factored secant differences are explicitly recorded: tiny force-level rounding differences can be magnified by division by a small time probe. Matrix operators remain independently checked against the factored secants with the original derivative-control tolerance. This numerical correction is not a correction to the physical force discrepancy.

## 4. A genuinely all-time bound in a sharply limited control problem

To distinguish loose estimates from an impossible control mechanism, consider the homogeneous scalar quadratic action with **frozen mass, stiffness, geometry and source position**, and prescribed zero source velocity. This is not the actual moving system. The initial scalar positions and velocities are taken from the final saved state, but the control's momenta obey the frozen scalar mass relation; they are not asserted to equal the original source-coupled canonical momenta.

For the coarse complete generalized eigensystem,

```text
K_H V = M_H V Omega^2,      V^T M_H V = 1,
q = V^T M_H u_H(0),        p = V^T M_H v_H(0),
v_H(t) = V [p cos(Omega t) - Omega q sin(Omega t)].
```

Every mode is retained, including the fastest. Put a_j=sqrt(p_j^2+omega_j^2 q_j^2) and h_s,j=M_h^(-1/2)D_s V_j. Since the normalized phase coefficient has absolute value at most1,

```text
||D_s v_H(t)||_(M_h^-1) <= sum_j a_j ||h_s,j||,       for every t.   (4)
```

A fixed partition into consecutive blocks of16 modes, chosen before results, can tighten this without filtering. For each block b define H_b with columns a_j h_s,j. Its contribution is bounded by either its column-norm sum or sqrt(n_b)||H_b||_2. Summing the smaller of these **two valid upper bounds** over all blocks gives B_s. No mode, phase contribution, or energy is discarded.

The alternative conserved coarse differentiated-energy bound is C_s sqrt(2 E_H,1(0)). Both are legitimate in the frozen homogeneous control. Their minimum is denoted F_s. The numerical samples are checks of an analytically all-time inequality, rather than the reason it is claimed for all times. Floating eigenvalues and constants are not interval-arithmetic error certificates.

For the two frozen coarse/fine systems and the unchanged I,

```text
M_h a + K_h e = D_total u_H,
E_1_dot = a^T D_total v_H,
sqrt(2 E_1(t)) <= sqrt(2 E_1(0)) + t F_total.          (5)
```

Thus we obtain an explicit finite-time error-energy envelope without taking another field-time derivative. Equation (5) is derived for this control, not the live MTS trajectory. Forty-one sampled offsets0..4e-5 check it in both branches using complete modal propagation; these offsets are **not new observed physical times**. Earlier modal-step evidence already validated frozen scalar propagation; the new object here is the two-grid forcing and differentiated-error envelope.

Returning to the actual moving system would reintroduce D_dot, changing modal bases/frequencies, source forces and their derivatives. None are assumed small merely because the frozen control works.

## 5. Integrating the waves instead of bounding them as a persistent push

The first all-mode force envelope still proved very loose for MTS. We therefore derive the oscillatory response itself, without altering the action, the interpolation or the frozen initial data.

Use complete mass-normalized fine modes U, frequencies Omega_i, coarse modes V and frequencies omega_j. With d=e_dot define

```text
z_i = U_i^T M_h a + i Omega_i U_i^T M_h d,
E_1 = (1/2) sum_i |z_i|^2,
H_ij = U_i^T D_total V_j,
z_i_dot = i Omega_i z_i + sum_j H_ij v_j(t).
```

Here v_j(t)=p_j cos(omega_j t)-omega_j q_j sin(omega_j t). For b_j=(p_j+i omega_j q_j)/2, define the entire function

```text
J(nu,t) = integral_0^t exp(i nu s) ds
        = t exp(i nu t/2) sinc(nu t/2),
|J(nu,t)| <= min(t,2/|nu|),     J(0,t)=t.                (6)
```

The sinc in (6) means sin(x)/x. The implementation converts to NumPy's normalized sinc. The exact frozen response is

```text
z_i(t) = exp(i Omega_i t) [z_i(0)
  + sum_j H_ij {b_j J(omega_j-Omega_i,t)
             + conjugate(b_j) J(-omega_j-Omega_i,t)}].   (7)
```

Thus a component response envelope is

```text
r_i(t) = sum_j |H_ij| a_j/2 [min(t,2/|omega_j-Omega_i|)
                            +min(t,2/(omega_j+Omega_i))],
E_1(t) <= (1/2) sum_i (|z_i(0)|+r_i(t))^2.              (8)
```

The first minimum equals t at exact resonance. No resonant mode is discarded and no small gap is divided by zero. The r_i are nondecreasing envelopes, so their values at T also give a uniform bound on 0<=t<=T. Unlike t times a force norm, (8) retains the suppression from oscillatory integration. Every coarse/fine mode pair is included.

There is also an exact total-stiffness identity,

```text
H_ij = (omega_j^2-Omega_i^2) (U_i^T M_h I V_j).          (9)
```

This follows from the two generalized eigenproblems and the definition of D_total. In the ideal frozen problem, exactly equal frequencies have zero total mismatch forcing. We verify (9) against the directly assembled H, but use the direct H and the nonsingular expression (6) in (7)-(8). We do not zero nearly resonant numerical couplings. Identity (9) need not hold sector by sector, or after changing to the live moving problem.

The homogeneous part of (7) has exactly constant energy because the fine frozen generator is skew in these energy coordinates. This is a finite-dimensional, positive quadratic-action statement, not a proof of nonlinear GR or MTS stability.

## Results and decision

### Direct action derivative

Both steps, both branches and all three sectors pass. At step5e-8, in the same normalized annular mass-dual units:

| Branch / sector | Actual direct forcing norm | Paired-vector bound | Coarse-energy bound |
|---|---:|---:|---:|
| Reference / total | 0.84335245 | 0.84385565 | 1741.50 |
| MTS / gradient | 2.40412746 | 2.40462894 | 1892.43 |
| MTS / Gram | 46.61815985 | 46.61827491 | 43324.62 |
| MTS / total | 46.06973576 | 46.07025075 | 43311.27 |

The direct signed MTS Gram contribution is -8.37651689e-4, compared with the saved nested-channel -8.37652152e-4. This is agreement within the numerical controls, not an exact-arithmetic equality. The old factored secant work/maxima are reproduced exactly by the revised comparison runner. The assembled operator derivative is independently checked at both probe sizes; largest reconstruction error among six-term sums is at rounding level.

MTS total geometry-rate contribution has norm0.00052234 versus velocity contribution46.06972841 **at this one state**. This locates the dominant endpoint forcing in D v, not D_dot u; it does not bound geometry transport over an interval. The background-energy constants are too loose for a useful live closure on either branch. The reference has a genuine nonzero gradient mismatch; it has not been exempted from the test.

### Frozen time control and its improvement

All558 coarse modes and1072 fine modes are retained. The block force envelope is19.5093 for reference and6217.8422 for MTS; the more generic conserved coarse-energy force bounds are69367.5 and1792764.8. Those force envelopes are not force predictions.

At frozen offset T=4e-5:

| Branch | Initial error energy | Actual frozen error energy at T | Force-times-time energy bound | Oscillatory response energy bound |
|---|---:|---:|---:|---:|
| Reference | 2.88718636e-7 | 2.89004249e-7 | 1.18620972e-6 | 4.87497247e-7 |
| MTS | 4.80596262e-6 | 4.80342683e-6 | 3.17051450e-2 | 1.56391594e-5 |

The MTS energy bound improves by approximately2027 times and is about3.26 times its actual frozen final energy. Reference improves by approximately2.43 times and its bound is about1.69 times the actual frozen final energy. These are improvements to an **upper bound**, not reductions of measured force error or improvements in a data fit.

Independent modal propagation and the forced-response formula (7) agree at all41 sampled offsets in both branches. Maximum energy-coordinate reconstruction errors are3.40e-14(reference) and3.47e-11(MTS); identity (9) relative residuals are8.74e-15 and7.38e-15. These floating-point checks support the implementation of the analytic identities; they are not a rigorous enclosure of roundoff or a continuum proof.

**Decision:** a useful finite-time energy envelope is available in the frozen quadratic control once the wave response is integrated, rather than treated as a persistent unsigned force. This is a real bounded subproblem, not full live closure. The direct forcing law also removes the need for a new numerical jerk in the dominant stiffness channel.

**Next derivation:** retain this fixed energy basis and derive the exact Duhamel remainder for the actual moving mass/stiffness and full source residual. Bound that accumulated remainder on the saved short trajectory, with the same reference comparator. Account for M_dot, K_dot, source acceleration and the difference between frozen and live initial accelerations; do not simply reuse the frozen envelope for the live state or assume the remainder is small. A fixed basis avoids importing unproved differentiability of individual eigenvectors across crossings. Only after that remainder is controlled should a longer live run be considered.

Successful calculations contain801 implementation checks:30algebra,72direct forcing,355frozen-envelope and344oscillatory-response. The failed original comparison is additional, not counted as a successful check set. Integrity sealing separately verifies provenance and table parsing; neither count is a tally of independent physical validations.

## Sources and claim boundary

- Previous seal: `source-intake/navier-stokes/20260914/annular-action-test-energy-final-integrity.json`.
- Direct operator law: `scripts/annular_direct_stiffness_forcing_20260919.py`.
- Independent algebra controls: `scripts/validate_annular_direct_stiffness_forcing_20260919.py`.
- Preserved first runner: `scripts/derive_annular_direct_stiffness_forcing_20260919.py`.
- Factored comparison runner: `scripts/derive_annular_direct_stiffness_forcing_v2_20260919.py`.
- Frozen all-mode envelope: `scripts/derive_annular_frozen_forcing_time_envelope_20260919.py`.
- Exact oscillatory response and its envelope: `scripts/derive_annular_frozen_oscillatory_response_20260919.py`.
- Earlier modal propagation control: `scripts/verify_annular_P2_frozen_modal_step_20260919.py`.

The original **12.5718%** impulse and approximately **13.58%** instantaneous hierarchy-force discrepancies remain unchanged. This does not establish the full GR limit. Live time-uniform forcing closure, refinement-uniform convergence, observational/SI tests and the full .004 interval remain unproved/untested here. These are implementation checks, not independent physical validations. No GitHub, subagents, sibling-workbench edits, or new live trajectory. The frozen control does not explain away the original force discrepancy.

Protected-workbench verification is mtime since2026-09-19 16:59:30 UTC, not a pre-turn whole-tree hash baseline. The new failed comparison is preserved in addition to the43 historical failures.
