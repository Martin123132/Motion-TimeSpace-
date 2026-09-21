# Action-owned coordinate covectors on the solved candidate geometry

Private continuation of `DERIVATION-20260920-full-weighted-canonical-inverse.md`.

Status: COMPLETE for all-component coordinate-covector assembly, fixed-profile derivative controls, paired quadrature controls, and a three-direction on-shell coordinate-envelope test with re-solved gravity. All three branches pass. This is a conditional initial-state result, not a completed coupled trajectory or full GR limit.

## 1. Scope and actual target

The full 16,425-component momentum inverse is already qualified near one coherent initial configuration. This step constructs the matching coordinate derivative of the SAME continuous-material candidate action, not forces transplanted from the older collocation scheme. The reference and the primary/alternative MTS extensions receive identical tests. The reference is a numerical baseline, not a newly established GR theorem.

The result is a canonical covector, p_dot = partial L / partial q, at fixed coefficient velocities. It is not q_ddot, a proper acceleration, or a measured physical force. The annular polar/zero-shift candidate and its source normalization remain conditional. This stage does not fix the older 12.5718% impulse, 13.5770% fine/continuum endpoint or 32.5535% coarse/fine endpoint discrepancies.

## 2. Derivation, including the terms a frozen-radius shortcut loses

At material label z let r = R(xi; b,z), J = R_xi, d = R_b and d_xi = J_b. The existing source map is affine in b; its fixed reference source anchor and topology are retained. Define

    F = 1 - 2 mu/r, N = exp(ell), U = sqrt(F),
    k = r^2/(N U), C = r^2 N U,
    K = J k, G = C/J,
    m = -d Q_xi/J, W = nu + V m.

The label action is

    L_wave = integral [K W^2/2 - G Q_xi^2/2] dxi
             - (H Q)^T diag(P G_nodes) (H Q)/2,
    L_dust = -m_s sqrt(N(b)^2 - V^2/F(b)).

H is the source-backed, source-hinge-compensated reference Gram factor; P is the positive coefficient sampler. Their original spacing normalization is already included. No extra inverse mesh-spacing factor is introduced. H and P do not vary with the physical b in this fixed-reference chart; that statement does not cover remeshing or moving reference knots.

At fixed continuous metric PROFILE, values sampled at a moving physical r do vary:

    F_r = -2 mu_r/r + 2 mu/r^2,
    k_r/k = 2/r - ell_r - F_r/(2F),
    C_r/C = 2/r + ell_r + F_r/(2F),
    K_b = d_xi k + J k_r d,
    G_b = C_r d/J - C d_xi/J^2,
    m_b = -m d_xi/J.

Consequently,

    (L_wave)_b = integral [K_b W^2/2 + K W V m_b
                          - G_b Q_xi^2/2] dxi
                 - (H Q)^T diag(P (G_b)_nodes) (H Q)/2,

    (L_dust)_b = -m_s [N N_r + V^2 F_r/(2 F^2)]
                       / sqrt(N^2 - V^2/F),

    (L_wave)_Qj = -integral [K W V d/J + G Q_xi] (phi_j)_xi dxi
                  - [H^T diag(P G_nodes) H Q]_j.

The field formula is left in weak form: no unreported integration-by-parts boundary term is discarded. The anchored field value remains prescribed zero, just as in the inherited candidate. A symbolic check differentiates the unreduced kinetic/gradient and proper-clock expressions independently to verify the source and field signs.

The canonical coordinates are material-nodal coefficients, not independent unweighted labels. If L_a(z) is the inherited degree-14 cardinal polynomial and w(z)=6(z+1/2)(1/2-z), the actual components are

    force_(j,a) = integral w(z) L_a(z) (L_wave)_Qj dz,
    force_(b,a) = integral w(z) L_a(z) [(L_wave)_b+(L_dust)_b] dz.

These weights are the same action ownership used for the preceding momentum inverse.

## 3. Stationary envelope: what was derived and what was actually checked

For an exactly stationary metric with the retained gravity boundary term, the first coordinate variation of the full action equals its explicit matter variation: the implicit metric variation multiplies the metric Euler-Lagrange equations and cancels under their boundary conditions. This is the existing conditional envelope argument, not a justification for dropping the spatial gradients N_r and F_r above.

The first implementation uses the owned, coherent t=0 radial solution at degree22. Its independent complex-step tests differentiate the fixed-PROFILE matter action. A second, separate calculation then varies the coordinates, rebuilds the moving source support and radial partition, and re-solves gravity. The original velocities are held fixed. This tests the envelope cancellation numerically rather than assuming that a small constraint residual is sufficient.

The second calculation uses three native coordinate directions: initial field amplitude, source motion with a small material-label variation, and mixed field/source variation. Their common-space directions are exact rational embeddings, contracted against the first calculation's complete covectors. Centered steps 1e-3, 5e-4 and 2.5e-4 produce two fourth-order Richardson estimates. Each branch receives all three directions and all step sizes, totaling 54 solved metrics and 27 centered differences. These are coordinate perturbations in inherited units, not time steps.

The varied action includes wave, dust, gravity bulk and the outer gravitational boundary term. A constant central-mass boundary offset is removed before differencing to reduce subtractive cancellation; its derivative is zero. The action is integrated independently in the physical radial coordinate, while the tested covector was assembled in reference/material coordinates. A finite collocation residual still does not prove exact stationarity of a discretized variational functional: this is numerical evidence in the tested directions, not an all-direction or global theorem.

## 4. Independent evaluation and arithmetic discipline

All 1,094 free field coordinates and 15 material labels are retained, plus 15 source coordinates. The exact rational common-mesh embedding of the original binary64 inputs is evaluated in 64-digit Decimal arithmetic. Local P2 polynomial and derivative coefficients are prepared BEFORE conversion to binary64; tiny refined-cell differences are not formed by subtracting rounded global nodal values.

The reference quadrature is split at common P2 boundaries and at the saved metric segment boundaries pulled back separately for each material label. Local element fractions and reference subinterval lengths are formed from rational edge differences before rounding. Two paired quadratures are tested: reference/material orders (10,32) and (16,48). This is a quadrature control on one spatial mesh, not spatial convergence or an error bound on the physical theory.

Five independent coordinate directions cover a smooth field, source motion, alternating full-space field, mixed material/source variation, and the exact initial field-amplitude direction. Velocities stay fixed. Each direction is checked against a separate complex-step evaluation of the action, with wave, Gram and dust channels kept separate. A large dust term cannot mask a Gram error. Artificial quadrature partitions are held at the base point for this derivative; the underlying reference integration domain is fixed and the metric profile is evaluated at the changed radii.

The Gram contraction uses H Q prepared at high precision. The final H-transpose application and contraction are also performed at high precision. The runner's 40-versus-64-digit transpose check compares the binary64-rounded outputs. The final integrity calculation additionally compares the Decimal vectors BEFORE rounding and requires relative agreement below 1e-20 and exact recovery of the saved 64-digit vector. Neither check claims 64-digit physical input accuracy. A separate diagnostic deliberately rounds common nodal fields too early and measures the resulting H Q sensitivity. The source negative control deliberately omits the spatial metric/radius contributions and must disagree with the complete covector.

Acceptance tolerances are fixed in the runner before execution. The independent derivative gate is absolute 1e-22 plus relative 2e-8, per channel and direction. Paired quadrature diagnostics require relative max-component differences below 2e-6 for bulk/dust and 2e-5 for Gram, with source and field blocks checked separately. A failed quadrature gate is reported as an unresolved gate, not hidden by changing its tolerance or discarding a mode.

## 5. Results

The force runner completes 138 implementation/control checks in 142.35 seconds. All 90 per-channel directional comparisons pass, including the intentionally zero reference-Gram and field-only dust controls. The largest nonzero relative discrepancy is 7.85e-15 or less. All 18 paired quadrature/block comparisons pass: the largest is 3.26221e-7 in the bulk field vector; the bulk/source, Gram and dust comparisons are at approximately 1e-14 or below. This is not a spatial-convergence result.

All 16,425 components are present for each of six branch/quadrature cases. The source-clock chart stays timelike and F stays positive. The actual sampled minimum F across these force rules is 0.7302515 or larger. Omitting the radial metric/radius terms changes the WAVE source covector by 56.6378%; that percentage does not describe the total physical force or an observational discrepancy.

At the finer force quadrature, raw Euclidean covector norms are:

| Contribution | Reference field | MTS field, either extension | Reference source | MTS source, either extension |
|---|---:|---:|---:|---:|
| Bulk wave | 0.0485977128 | 0.0485977128 | 2.45779948e-4 | 2.45779948e-4 |
| Extra Gram | 0 | 3.30654124e-4 | 0 | 7.72164830e-12 |
| Proper-clock dust | 0 | 0 | 2.33287637e-4 | 2.33287637e-4 |

These norms depend on the inherited coordinate basis and normalization; they are not invariant physical magnitudes. They nevertheless show why the small extra action (-5.11835078e-11) is not a sufficient reason to erase its derivative. Primary and alternative extensions agree on this initial state to the displayed precision; that does not imply identical evolved dynamics.

The on-shell runner completes 107 implementation/control checks in 375.06 seconds. All nine refined full-action comparisons pass. The worst relative difference from the independently assembled covector is 2.323e-9; the largest absolute difference is 4.490e-12. The largest difference between successive Richardson estimates is 4.629e-12. No branch is exempted from a control. The declared gate is 2e-10 absolute plus 2e-5 relative, on both the force comparison and Richardson consistency.

| Direction | Reference full-action/covector relative difference | MTS primary | MTS alternative |
|---|---:|---:|---:|
| Field amplitude | 1.344e-10 | 5.928e-10 | 5.928e-10 |
| Source motion | 3.236e-10 | 1.683e-9 | 1.683e-9 |
| Mixed field/source | 2.323e-9 | 9.194e-10 | 9.194e-10 |

The substantive advance is that the candidate now has both an implemented full weighted momentum inverse and implemented matching coordinate covectors, with independent tests that include moving coordinates and re-solved gravity. No parameter was fitted, mode removed, boundary term dropped or gate loosened to achieve that result. A coupled time trajectory, physical-acceleration comparison, spatial convergence and the general-shift/current equations remain outstanding.

## 6. Next executable step: eliminate the midpoint momentum, not the fast modes

A concrete way to couple the qualified pieces is the implicit canonical midpoint rule. Let P(q,v) and F(q,v) denote the action-owned momentum and coordinate covector, with gravity solved at that same state. For step h and unknown midpoint velocity v,

    q_m = q_0 + h v/2,
    R(v) = P(q_m,v) - p_0 - h F(q_m,v)/2 = 0,
    q_1 = q_0 + h v,
    p_1 = p_0 + h F(q_m,v).

The same converged midpoint must be used in all four expressions. This reduces the nonlinear step to 16,425 velocity unknowns instead of independently guessing 32,850 position/momentum components. It does NOT freeze the source or geometry. Its exact formal Jacobian is

    R_v = P_v + h(P_q - F_v)/2 - h^2 F_q/4.

For a twice differentiable reduced Lagrangian, F_v = P_q^T, so the middle term is skew. In the diagnostic quadratic model L=v^T M v/2 + v^T A q - q^T K q/2,

    R_v = M + h(A-A^T)/2 + h^2 K/4.

If M is positive definite and K positive semidefinite, its symmetric part is positive definite and the skew part cannot create a null vector. The integrity script independently checks this Jacobian identity on a two-component model with nonzero skew transport. This is an algebra check and a useful preconditioner design, not a positivity result for the actual coupled MTS Hessian. Implicit stepping also does not establish time resolution: step-halving and forward/backward controls remain necessary.

The next implementation must carry the high-precision common field state and derivative atoms consistently when new coordinates leave the native embedded subspace; recompute the material geometry and live force at each midpoint trial; retain every mode; and compare equal-step reference/primary/alternative trajectories. The old frozen scalar frequency estimate is not silently reused as a bound for the full source/field/gravity Jacobian. No trajectory is started in this checkpoint because that precision-preserving moving-state step is not implemented and verified yet. The force and envelope gates needed for it are now passed rather than merely listed as missing.

## 7. Reproducible sources

- `scripts/annular_candidate_coordinate_covectors_20260921.py`
- `scripts/derive_annular_candidate_coordinate_covectors_20260921.py`
- `scripts/derive_annular_candidate_coordinate_envelope_20260921.py`
- `scripts/seal_annular_candidate_coordinate_covectors_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-coordinate-covectors-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-candidate-coordinate-envelope-attempt01/status.json`
- `scripts/annular_candidate_canonical_response_20260920.py`
- `scripts/annular_candidate_radial_constraint_20260920.py`
- `DERIVATION-20260920-candidate-radial-constraint-and-initial-metric.md`
- `DERIVATION-20260920-candidate-canonical-momenta-and-live-response.md`
- `DERIVATION-20260920-complete-frozen-candidate-and-source-response.md`
- `source-intake/navier-stokes/20260914/annular-candidate-full-canonical-inverse-final-integrity.json`

No GitHub action, subagents, galaxy work or protected-workbench edits. The calculation uses one BelowNormal single-core worker. All quantities keep the inherited parent coordinate units; no time is assigned seconds and no covector is presented as an experimentally calibrated force.
