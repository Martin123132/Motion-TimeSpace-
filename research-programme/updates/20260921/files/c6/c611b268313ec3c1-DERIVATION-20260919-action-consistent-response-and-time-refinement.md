# Action-consistent response and temporal-refinement control

Private continuation of `DERIVATION-20260919-moving-system-Duhamel-remainder.md`, 19 September 2026. The question is whether the remaining response discrepancy is caused by the modal diagnostic, forcing interpolation, or the already saved numerical evolution. Both reference and MTS are tested. No field equation, boundary condition, coupling or previously saved result is changed.

## 1. A direct action propagation law for velocity and acceleration

For either spatial resolution let the frozen action matrices at the saved final state be M_star,K_star, and A_star=M_star^-1 K_star. Along the retained trajectory define

```text
r(theta) = a(theta)+A_star u(theta),
u''+A_star u = r,
v''+A_star v = r'.                                      (1)
```

Here theta=4e-5-t is the backward parameter used in the preceding comparison, v=u' is the reversed scalar velocity and a=v'. The action acceleration still contains all previously retained source, transport and inverse-solve terms. The new law is a derivative of the constant-operator equation in (1), not an assumption that the live geometry is constant: its changes remain inside r.

For continuous piecewise-linear r on a sampling interval, sigma=(r_right-r_left)/h is constant. Set x=(kappa v,a,c), with c'=0 and c=1 for the driven solution. Then

```text
x' = G_sigma x,
G_sigma = [ 0              kappa I    0     ]
          [ -A_star/kappa  0          sigma ]
          [ 0              0          0     ],
x(theta+h) = exp(h G_sigma) x(theta).                    (2)
```

No field jerk is required. Velocity and acceleration are propagated as the state, rather than obtaining acceleration by multiplying a reconstructed position by approximate squared modal frequencies. At each forcing node v,a are continuous; r' may jump, as permitted by this piecewise-linear control problem.

The initial driven acceleration is the evaluated action acceleration a(0). The homogeneous comparison uses a_fr(0)=-A_star u(0), with the same velocity and c=0. Keeping their initial acceleration difference is essential. The two solutions are propagated together without substituting either for the actual nonlinear trajectory.

Kappa=1e6 is a coordinate scaling, not a physical coefficient, cutoff or fitted parameter. Rescaling it to5e5 is independently checked on both branches. All558 coarse and1072 fine scalar degrees of freedom remain present.

## 2. Original operators, not an approximate eigensystem

The stiffness is applied as the original factored action,

```text
K_star w = G^T W_gradient G w + B^T W_Gram B w,
A_star w = solve(M_star, K_star w).                     (3)
```

G contains the original quadratic-element derivative evaluations; B retains all Gram rows. The original pentadiagonal mass is solved using its banded Cholesky factor. No eigenvectors or eigenfrequencies enter the new propagation. The transpose required by the exponential-action algorithm is K_star M_star^-1, not M_star^-1 K_star; this noncommuting order is independently tested.

The matrix exponential is evaluated through operator products. It is a floating-point numerical calculation of the exact piecewise-linear-forcing problem, not interval arithmetic or a new nonlinear evolution. This removes the specific modal-acceleration representation from the diagnostic while preserving the action.

For a homogeneous frozen solution,

```text
E_1 = (a^T M_star a + v^T K_star v)/2,
E_1' = 0.
```

With forcing slope sigma, E_1'=a^T M_star sigma. Conservation is checked only for the homogeneous column, not incorrectly imposed on the driven one.

The synthetic controls include dense versus operator exponentials, generator adjoints, interval subdivision, coordinate rescaling and the zero-frequency polynomial limit. On the actual actions, stiffness products are compared with the previously assembled matrices, and mass inversion, two-half-step propagation and homogeneous energy conservation are checked.

## 3. Same saved trajectory, independent propagation

The33 saved source evaluations from the preceding stage are retained. Their physical forcing is reconstructed as a+A_star u using (3), and9/17/33-node piecewise-linear controls are propagated with (2). Error is measured directly in the original fine action norm,

```text
N(delta_v,delta_a)^2 = delta_a^T M_h,star delta_a
                    + delta_v^T K_h,star delta_v,        (4)
```

after the original fixed interpolation of the coarse fields. This does not rely on a modal energy norm being exact in floating point.

At reverse offset theta=4e-5, which corresponds to the original physical time t=0:

| Branch | 9 forcing nodes | 17 forcing nodes | 33 forcing nodes | Previous arithmetic-accounted modal result,33nodes |
|---|---:|---:|---:|---:|
| Reference | 6.22788184e-7 | 1.50584730e-7 | 3.67967997e-8 | 3.67966726e-8 |
| MTS | 8.71011578e-7 | 5.98242275e-7 | 5.90891966e-7 | 5.90903714e-7 |

The direct initial error is zero by construction and verified in the output. The largest error over the33 sampled times is4.44680e-8 for reference and3.02272626e-6 for MTS. The MTS interval floor has not disappeared.

The independent action result agrees with the arithmetic-accounted modal result. This is evidence against explaining the *remaining* floor solely as an artefact of the diagnostic eigensystem. It does not undo the preceding finding that the original zero-time modal floor was numerical.

The largest actual-action half-step discrepancy is2.67e-16 in norm (4); rescaling discrepancy is at most1.97e-16. Relative homogeneous energy drift is at most1.59e-15(reference) and6.12e-16(MTS). These are floating-point controls, not certified upper bounds on every numerical error. The new action response took about41seconds on one CPU core.

The reconstructed final MTS action energy is4.80299481e-6 versus saved4.80298877e-6. Such close scalar-energy agreement still does not justify ignoring the vector response discrepancy.

## 4. Independent temporal-halving comparison

The existing larger-step trajectories are now processed using the same action and operator response, not newly evolved. Their temporal resolutions are:

| Branch | Larger-step coarse/fine | Smaller-step coarse/fine |
|---|---:|---:|
| Reference | 16 / 32 | 32 / 64 |
| MTS | 16 / 64 | 32 / 128 |

Each pair spans the same physical interval0..4e-5. The fixed action used by both temporal resolutions is the one from the smaller-step final state, so changing the response operator cannot explain their difference. Lower-resolution accelerations are recomputed from the canonical action and checked against directional velocity differences at17 matched times.

Both sets are compared using the same9/17 forcing-node grids. The existing33-node reconstruction is additional information only for the smaller-step set. This separates the size of the saved evolution step from the number of nodes used to approximate its forcing; they must not be conflated.

If the leading forcing-interpolation error scales quadratically, the diagnostic combination

```text
Y_R = (4 Y_17 - Y_9)/3                                 (5)
```

removes that leading term. Here Y contains the predicted velocity and acceleration, and the original saved Y_actual is subtracted afterwards. We compare the remaining error vectors and their factor-four relation under temporal halving, rather than merely comparing two error norms.

Equation (5) is Richardson extrapolation under a scaling assumption, not a rigorous error certificate. A factor-four relation would support second-order temporal error as an explanation; its absence would require further investigation. No such relation is imposed as an acceptance test and neither branch is exempt.

At the common17-node forcing grid, after evaluating the existing larger-step runs:

| Branch | Endpoint error,larger steps | Endpoint error,smaller steps | Maximum sampled error,larger steps | Maximum sampled error,smaller steps |
|---|---:|---:|---:|---:|
| Reference | 1.45294611e-7 | 1.50584730e-7 | 1.77786846e-7 | 1.62158213e-7 |
| MTS | 2.89200114e-6 | 5.98242275e-7 | 1.75936831e-5 | 3.00941687e-6 |

MTS endpoint error decreases by about4.83times and its maximum sampled error by about5.85times when the existing evolution steps are halved. The reference endpoint does not improve under that same operation; its strong9/17/33 forcing-node improvement is consistent with forcing-sampling error dominating at this resolution. Neither outcome is forced into a pass/fail criterion requiring an exact factor of four.

For the Richardson diagnostic (5), MTS endpoint errors are2.94434135e-6(larger evolution steps) and6.58244800e-7(smaller), a ratio of about4.47. However, the signed vector difference between the larger-step residual and four times the smaller-step residual has norm8.53438484e-7, about29% of the larger-step residual. Reference Richardson residuals are8.58633e-8 and5.37385e-8; its factor-four vector discrepancy is1.64473e-7. These results do **not** demonstrate an exact asymptotic second-order law or an error certificate. They do show that the MTS floor is materially sensitive to temporal resolution, not just the diagnostic eigensystem.

The larger-step postprocessing took about1396seconds on one CPU core. All canonical acceleration controls pass. This was evaluation of existing saved trajectories, not a new evolution.

## 5. Which level should be refined next?

We additionally retain the signed temporal telescope. Let delta_v_h,delta_a_h be the larger-minus-smaller-step difference on the fine grid, and let delta_v_H,delta_a_H be the coarse difference after the original interpolation I. In the same fine action norm,

```text
N(delta_h-delta_H)^2 = N(delta_h)^2+N(delta_H)^2
  -2 [delta_a_h^T M_h,star delta_a_H
      +delta_v_h^T K_h,star delta_v_H].                 (6)
```

The cross term is stored with its sign; the two positive norms are not falsely presented as additive error percentages.

At the saved physical endpoint t=4e-5:

| Branch | Fine-grid temporal difference norm | Interpolated coarse-grid difference norm | Combined hierarchy difference norm |
|---|---:|---:|---:|
| Reference | 3.45360e-8 | 5.49465e-8 | 5.24909e-8 |
| MTS | 1.15782e-6 | 1.70478e-6 | 2.33118e-6 |

The strongest MTS temporal difference is on the coarse grid near physical time2e-5: its norm is1.49464803e-5 versus the fine contribution1.06439748e-6. The combined norm there is1.47791766e-5 after the signed cross term. Over the17 sampled times, the largest coarse and fine contributions are1.49465e-5 and1.29351e-6 respectively. Both trajectories share their original initial data, where the temporal difference is exactly zero.

This is a localized numerical diagnostic, not a causal attribution to a particular physical coupling. It gives a concrete reason to refine the coarse *time step* first rather than blindly increasing spatial resolution or changing the action.

## Decision and next run

We now have an independent response calculation that uses the original action operators and corroborates the corrected modal calculation. The remaining MTS response error responds strongly to temporal halving, and its largest temporal contribution is on the coarse spatial grid. This narrows the next calculation substantially; it does not resolve the original spatial hierarchy-force discrepancy.

**Next:** run the same saved-initial-data coarse257/cap2e-5 discretization with64 time steps instead of32, on both MTS and reference. Keep the already qualified fine trajectories fixed at128steps(MTS) and64steps(reference). Compare the signed response and source-force diagnostics with the32-step coarse results before considering another fine-grid or spatial refinement. Preserve all earlier trajectories and reapply the same action and source conditions. This is a targeted temporal test, not a fitted correction or a change of theory.

There are747successful implementation checks:19synthetic,435original-action response,187temporal-halving and106signed-level checks. These are central-layer scalar hierarchy diagnostics of the retained annular discretization, not all components of a completed GR limit. No new failed execution occurred; the historical44 remain unchanged.

## Provenance and claim boundary

- Previous complete seal: `source-intake/navier-stokes/20260914/annular-moving-duhamel-final-integrity.json`.
- Banded-mass/factored-stiffness exponential action: `scripts/annular_action_exponential_20260919.py`.
- Independent small controls: `scripts/validate_annular_action_exponential_20260919.py`.
- Original-operator response: `scripts/derive_annular_action_exponential_response_20260919.py`.
- Existing temporal-halving comparison: `scripts/derive_annular_action_response_time_halving_20260919.py`.
- Signed level contributions: `scripts/diagnose_annular_temporal_level_contributions_20260919.py`.

This does not establish the full GR limit, a certified live envelope, refinement-uniform convergence or a new observational fit. The original **12.5718%** impulse and approximately **13.58%** instantaneous hierarchy-force discrepancies remain unchanged. The .004 interval is not rerun. Conditional bounds from earlier stages remain conditional; no numerical diagnostic is substituted for the parent action or a missing physics derivation. These are implementation checks, not independent physical validations.

All44 historical failed executions remain preserved. No GitHub, subagents, new live evolution or sibling-workbench edits. Protected-workbench verification uses mtime since2026-09-19 18:48:22UTC, not a pre-turn whole-tree hash baseline.
