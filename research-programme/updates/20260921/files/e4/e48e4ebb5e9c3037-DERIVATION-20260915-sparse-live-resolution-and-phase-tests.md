# Sparse live resolution, a derived interpolation law, and source-cell phase tests

Private continuation of `DERIVATION-20260915-independent-live-continuum-GR-oracle.md`.
The previous executed sources, successes and failures remain immutable. No GitHub action.

## Question and fixed experiment

Can the repaired finite action approach the independently evolved spherical continuum reference when the field grid is actually resolved, rather than merely conserving its own energy?

Both reference and MTS use the same original compact-quintic preparation, domain [5.2,6.8], central mass .7, source rest parameter .03, coupling .1, positive material width .02, initial source position 6.03, initial velocity .03, and duration .02. These are normalized benchmark inputs, not derived physical MTS coefficients or observational data. Nine material collocation labels remain continuously averaged with weight 6(z+.5)(.5-z) in the geometry equations. This is not an exact finite-label Galerkin theorem.

The independently assembled live characteristic reference is the already qualified degree512 trajectory in `source-intake/navier-stokes/20260914/annular-live-continuum-degree512-attempt01/status.json`. Its actual saved fields, moving source and geometry are reused; there is no fitted target waveform. The previous degree384 comparison found a maximum physical relative field difference of 9.17e-6 across three sampled material labels and five times. This is a resolution diagnostic, not a rigorous interval error bound or a proven bound over every label. Here reported maximum errors are evaluated at the five saved times 0/.005/.010/.015/.020, with material quadrature checks, not certified suprema between times.

## Exact sparse rearrangement, not a changed theory

Implementation: `scripts/annular_sparse_live_repaired_20260915.py`.

At any regular quadrature point the split piecewise-linear scalar basis has at most two nonzero nodal entries. Store those entries and their indices instead of a full quadrature-by-node array. For material interpolation B_ai and a selected spatial node j(a), evaluate

    q_j(a)(z_a) = sum_i B_ai q_ij(a).

This gathers only the selected columns; it does not approximate or reduce the material polynomial. For a nodal Gram density, gather exactly the Gram rows with nonzero sampling weight at that node, and every column in those rows. Evaluate the original lifted factors

    F = G q - (G rho)(j_b q),       rho_j = max(R_j-b,0),
    Z_node = sum_r sampling_r,node F_r^2/(2h).

No Gram factor is dropped or fitted. Continuous averaging precedes nonlinear metric products exactly as before. Quadrature still splits node/source bands; floating-point endpoint bookkeeping need not create identical zero-width sliver arrays. Actual densities and forces are tested, rather than assuming that equal array shapes establish equivalence.

The field velocity matrix is tridiagonal. Banded solves replace dense inversion in the same strictly monotone canonical source equation:

    P_b - d^T M^-1 pi = S V/(U^2 sqrt(N^2-V^2/U^2))
                         + (I-d^T M^-1 d) V.

The radial/canonical fixed point and tolerances are unchanged. Its density sampling table depends on coordinates, not rates, so within one fixed-coordinate inversion it is constructed once and then reloaded with updated rates. It is not reused across different evolving coordinates without reconstruction.

`scripts/verify_annular_sparse_live_20260915.py` tests 17/33/65 nodes, both branches, initial and actually evolved states, action components, canonical rates, geometry, covectors, complex directional derivatives, independently sampled density components and physical radiation force. All 44 implementation checks pass. Largest recorded force-covector difference is 5.36e-15; largest complex directional component difference is 1.04e-14. Measured 65-node solve-plus-force speedup is about fivefold. The field-shape array is about 36 times smaller in those measured states; this is not a claim of 36-fold whole-process memory reduction or globally linear complexity. Exact positive-width label quadrature grows as more node bands overlap at finer spacing.

Evidence: `source-intake/navier-stokes/20260914/annular-sparse-live-equivalence-attempt01/status.json`.

Nonaffine material/source controls add eight checks in `source-intake/navier-stokes/20260914/annular-sparse-live-transport-controls-attempt01/status.json`, produced by `scripts/verify_annular_sparse_live_transport_20260915.py`. The common geometry, fields and rates agree independently; positive material weights sum to one within 8.89e-16. `scripts/annular_sparse_live_tangent_20260915.py` replaces only dense regular-current sampling, with agreement below 2.11e-19. The moving-interface Noether term is retained: residual below 1.22e-19 versus about 6.93e-7 if that term is omitted. These deliberately perturbed states are implementation controls, not substituted physical preparations for the accuracy runs.

## Derived origin of the initial waveform gap

Let f(x) be the unchanged initial scalar, x=R-b_0-epsilon*z. At time zero H=f' and W=-V_0 f'. Let H_h be the derivative of its nodal linear interpolant. On an uncut cell H_h is exactly the cell average of f'. Taylor expansion about its midpoint gives

    H_h-H = -f''(midpoint)(R-midpoint) + O(h^2),
    integral_cell C(H_h-H)^2 dR
        = C(midpoint) f''(midpoint)^2 h^3/12 + o(h^3).

Here A=R^2/(NU), C=R^2 NU, and the metric is the common continuum reference used to define the comparison norm. Integrating all cells and material labels gives

    E_h^2 = h^2 C_init^2 + o(h^2),
    C_init^2 = <integral C (f'')^2 dR> /
                   [12 <integral (A V_0^2+C)(f')^2 dR>].

Angle brackets mean the fixed positive material average. The prepared scalar is affine throughout a neighbourhood of every initial source cut; its cut-cell spatial and transported temporal traces are therefore exact there. Away from the cut, interpolation of W is O(h^2) and contributes subleading squared error. The compact preparation is piecewise smooth with the matching regularity required for this leading integrated estimate. No cell-crossing or evolving-error theorem follows from this initial result.

This explains why both branches had the same worst initial error: the comparison sees their common preparation and the common target metric, before different dynamics act. It is not evidence that evolved reference and MTS fields are identical.

`scripts/derive_annular_initial_resolution_law_20260915.py` derives the cell variance factor and preparation derivative, then evaluates the coefficient with independent quadrature:

    C_init = 3.12215486511748 per radial coordinate unit.

The asymptotic estimate requires roughly 1001 nodes for an initial error below 0.5%; it is not a rigorous sufficient-grid bound. Direct analytic-profile comparisons give:

| Nodes | Initial relative field error |
|---:|---:|
| 65 | 7.77931% |
| 129 | 3.89933% |
| 253 | 1.98187% |
| 513 | 0.975619% |
| 1025 | 0.487830% |
| 2049 | 0.243917% |

At 2049 nodes the measured E_h/h differs from the derived coefficient by 3.53e-6 relative. The analytic initial-profile comparison is explicitly different from treating the degree512 polynomial as mathematically exact. Two additional checks show that the new sparse evolved-field comparator reproduces the previous dense physical norm to within 1e-12. Eight checks pass in `source-intake/navier-stokes/20260914/annular-initial-resolution-law-attempt01/status.json`.

## Live accuracy and phase tests

Runner: `scripts/run_annular_sparse_live_refinement_20260915.py`.

The physical integration splits both source positions, so a displaced jump contributes its actual gap rather than being masked or incorrectly compared with a global supremum norm. Final physical wave force is

    F_h = L_b^wave - d_t zeta_h,       P_b=p_s+zeta_h,

including the live-metric tangent. Although zeta_h=O(h), its derivative is not generally O(h) and cannot be discarded. A halved tangent-difference step checks this diagnostic independently of the time integrator.

Prespecified waveform threshold remains 0.5%. Source position/velocity/clock thresholds remain 5e-7/2e-5/2e-7; radial residual 2e-8; exterior mass drift 2e-9; source-cell margin .15. Force qualification requires both absolute error below 2e-7 and relative error below 2%. Accuracy failures are recorded as false gates, even when a numerical suite completes successfully.

Paired nearby grids 119/129/139/149 give initial phases .2125/.4/.5875/.775 at the same physical source and domain. Thus this varies phase AND spacing slightly, not an isolated fixed-spacing phase experiment. Every branch is retained; a favourable force result cannot stand in for the phase envelope. The subsequent 253/513/1025 grids refine further without changing the preparation. Grid257 was not selected because its predicted final margin is below the unchanged .15 safeguard. This is an explicit no-crossing restriction, not proof of phase-independent or arbitrarily long-time convergence.

The complete paired trajectories are recorded in `source-intake/navier-stokes/20260914/annular-sparse-live-phase-refinement-attempt01/status.json` (62 numerical/diagnostic checks) and `source-intake/navier-stokes/20260914/annular-sparse-live-fine-refinement-attempt01/status.json` (26). Relative force percentages alone are not the force gate: the absolute requirement is also enforced.

| Nodes | Worst field error, both branches | Reference final force error | MTS final force error | Force gate, reference/MTS |
|---:|---:|---:|---:|:---|
| 119 | 4.22893% | 0.91650% | 1.20029% | fail / fail |
| 129 | 3.89933% | 6.07901% | 0.70194% | fail / fail |
| 139 | 3.61708% | 4.33766% | 0.54889% | fail / pass |
| 149 | 3.37302% | 5.83328% | 5.12909% | fail / fail |
| 253 | 1.98187% | 2.56767% | 3.19499% | fail / fail |
| 513 | 0.975619% | 1.81678% | 0.87911% | fail / fail |
| 1025 | 0.487830% | 0.031322% | 0.053173% | pass / pass |

The field maximum occurs at the common initial preparation. Evolved 1025-node final field errors differ: reference 0.4704126%, MTS 0.4704219%. Thus neither equality of the worst number nor a more favourable force at one coarse resolution is used to equate the dynamics or claim superiority. All listed finite-grid field gates fail except 1025. The coarse phase force errors are plainly nonmonotone and preserved.

At 1025 nodes the largest reference/MTS source-position errors are 1.0305e-10/1.0405e-10, velocity errors 7.3130e-9/6.0054e-9, and proper-clock errors 2.6545e-11/2.6577e-11. Final force absolute errors are 9.061e-9/1.5381e-8, passing the unchanged 2e-7 requirement as well as the 2% relative requirement. Independent off-grid radial residuals are below 4.83e-11, off-grid canonical residuals below 4.83e-11, and measured exterior-mass drift at most 1.12e-16. A reported zero is floating-point resolution, not a theorem of exact discrete conservation.

Halving the force diagnostic's difference step changes the 1025 force by at most 1.09e-16; changing material quadrature from 6 to 10 changes the final field error by less than 8.47e-13. Every evaluated integration-stage source stays in its initial cell with margin at least .2 at 1025. This is a stage check, not interval-arithmetic certification between stages. All trajectories save immutable accepted intervals at .005 spacing.

`source-intake/navier-stokes/20260914/annular-sparse-live-halfstep-controls-attempt01/status.json` records another 14 checks for paired 129-node trajectories with half the time step. Direct whole-state comparison and the high-resolution independent mass-current/reference controls are performed by `scripts/verify_annular_sparse_live_precision_20260915.py`.

All 21 checks in `source-intake/navier-stokes/20260914/annular-sparse-live-precision-controls-attempt01/status.json` pass:

- Whole 129-node trajectory differences after halving the time step are below 8.37e-15 (reference) and 3.86e-13 (MTS). This control is not claimed to have been repeated at every resolution.
- Switching the independent comparison from degree512 to degree384 changes the reported field error by at most 1.52e-8 across the four fine cases. Both 1025-node branches still pass the 0.5% field gate against degree384, with maximum 0.48783094%.
- This small change in the error norm is only reference-switch sensitivity, not an upper bound on the reference-vector error: norm differences can be smaller than differences of vectors. The separately measured three-label reference-vector discrepancy of 9.17e-6 is also well below the approximately 1.22e-4 margin between the 1025 error and the gate, but remains a sampled estimate rather than an exact continuum certificate.
- Independent temporal mass/current residuals at three fixed radii, including the source band, are below 8.54e-12 for the 513/1025 cases. At 1025 the on-shell values are 3.46e-12 (reference) and 5.19e-12 (MTS). This does not replace the waveform tests; both now independently succeed in the selected fine case.
- The full moving-interface Noether residual remains below 1.70e-18. Omitting that interface term would leave roughly 8.4e-7. Cached sparse current calculations are separately checked against the uncached expression before use.

All own numerical jobs are finished. In total, 192 current symbolic/implementation/numerical/diagnostic checks pass, while the table's failed accuracy flags remain failed. Earlier sealed failed attempts are inherited without alteration. Final provenance validation is performed by `scripts/seal_annular_sparse_live_resolution_20260915.py`; a successful integrity seal is an evidence-integrity result, not an additional physics theorem.

## An additional derived result: why a radiation force starts at all

The force diagnostic exposed a useful question: with equal initial slopes on both sides, why is the later pressure force nonzero? For this original affine preparation the initial zero-trace condition and its first time derivative hold, but the second compatibility condition does not. This is not repaired by changing the test data.

Put s=NU, a=dV/dt, r=V/s. A subscript t on s below means derivative at fixed R, not along the moving source. The wave equation implies

    W_t = (s_t/s)W + s^2 H_R + (2s^2/R+s s_R)H.

Differentiating phi(t,b(t))=0 twice gives

    W_t + 2V W_R + V^2 H_R + a H = 0.

Initially H=H_0=.01, W=-V_0 H_0 and H_R=W_R=0 near the source. The residual of the second trace condition is therefore H_0 B, where

    B = a + 2s^2/b + s s_R - V s_t/s.

The source acceleration a is computed from the same canonical source and live-metric equations; it is not a new tuning parameter. Initial pressure force vanishes because H_minus=H_plus, but B need not vanish. For the outgoing characteristic on each side, chi_plus=W/s+H and chi_minus=W/s-H give at the initial boundary

    D_b chi_minus(left) = D_b chi_plus(right)
                       = H_0[(1+r^2)s_R+2s/b],
    D_b r = a/s-r(s_t+V s_R)/s.

Applying the moving Dirichlet relations chi_minus=-(1+r)H on the left and chi_plus=(1-r)H on the right yields

    D_b H_minus = -H_0[(1+r^2)s_R+2s/b+D_b r]/(1+r),
    D_b H_plus  =  H_0[(1+r^2)s_R+2s/b+D_b r]/(1-r).

Consequently the one-sided initial pressure-force slope is

    dF_phi/dt |_(0+) = -2 b_0^2 H_0^2 B.

This is a derived initial-time law, not a fit to the later trajectory. `scripts/derive_annular_initial_force_onset_20260915.py` checks it symbolically and against independent live characteristic/source directional evolution. Nine checks pass in `source-intake/navier-stokes/20260914/annular-initial-force-onset-attempt01/status.json`. The exact finite-characteristic differentiation identity agrees within 5.59e-12. The analytic affine-limit slope discrepancy falls from 0.491% at degree384 to 0.106% at degree512. The middle layer has B about .18493945 and predicted initial force slope about -0.001344913. Initial equal-pressure force is below 1.14e-18.

Thus the original experiment launches a compatibility transient. Smoothness through the initial source corner must not be assumed in a future convergence proof; piecewise/weak evolution is not automatically invalidated. This does not by itself explain every later grid-phase error, nor is it evidence for a novel MTS force: even flat spherical space with constant speed s=1 and a=0 gives B=2/b and force slope -4b H_0^2. The benchmark preparation, spherical propagation and moving zero-trace boundary already generate this response. The correct next analysis must separate that shared response from finite-grid errors and genuinely parent-derived predictions.

## Scope and next decision

Conditional continuum interior angular completion was already derived in the preceding checkpoint; it is not being replaced with another audit here. The present bridge is numerical convergence to that chosen spherical GR-coupled scalar/material interior. It does not derive the unrestricted MTS parent, select the source action uniquely, resolve exterior reflecting-wall support, prove global black-hole regularity, derive Newton's constant, or validate galaxies observationally.

The 1025-node run closes the previously measured waveform/final-force accuracy gap for this selected finite-width, short-time experiment, subject to the independent controls above. It does not prove convergence for every mesh phase or through a source crossing. The next bounded numerical extension should compare nearby fine grids such as 1031 and 1037 against the same 1025 result: they alter the initial phase substantially while changing spacing by only about 1%, keep the physical source/domain unchanged, and leave predicted source margins above .15. These are not yet executed results. That tests whether the favourable fine force survives rather than selecting it as a universal result.

The next structural extension is a derived source-cell transfer or source-fitted variational discretization, with its full field/source momentum and current accounting retained. A longer run cannot silently cross cells using the presently qualified noncrossing formulas. The newly derived second-compatibility condition may also define an additional smooth-preparation control later, but must not replace this harder original experiment or be imposed without recomputing the live constraints. The parent/global bridge remains separate. Conservation, finer initial interpolation and attractive individual force points must not be promoted into full GR.
