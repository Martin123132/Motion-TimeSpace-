# Parent-kernel trace projection and compatible MTS boundary data

Private working derivation, 11–12 September 2026 (Europe/London). All numerical values below are internal code units, not experimental errors or a local-GR certificate.

## 1. What changed

We constructed the previously missing boundary-compatible canonical projection, rather than deleting the two troublesome constraint rows. It retains the full Gram time-link force, all previous phase directions, and all previous weak equations. Two new continuous mass-coordinate directions are paired with two new momentum directions.

On the unchanged N16 MTS initial fields, the maximum constraint-rate residual falls from **7.7146899478e-6 to 1.3428868117e-13**. Independent higher quadrature gives **1.9509299039e-14**. The GR+canonical-scalar reference remains at approximately **1.8e-17**.

We then actually prepared compatible MTS initial data while retaining the prescribed inner mass drive, outer scalar drive, inner mass, scalar configuration, and natural outer clock. A two-amplitude boundary solve converges in one Newton update. This addresses the separate external-drive mismatch instead of disguising it as a projection success.

This is a finite-dimensional, initial-time construction. It is **not** a nonlinear spacetime solution, mesh-convergence result, interval proof, black-hole regularity proof, or derivation of the entire MTS-to-GR limit.

## 2. Starting point and conventions

The predecessor is `DERIVATION-20260911-canonical-rate-completion-and-two-boundary-flux-defects.md`, with immutable evidence in `source-intake/navier-stokes/20260911/annular-canonical-rate-completion-final-integrity.json`.

We retain its positive annulus, 16 scalar intervals/17 nodes, kappa=0.1, P=0 initial slice, zero scalar mass/potential parameters, natural spatial reactions, and outer clock N_out/sqrt(F_out)=C_out. Here F=1-2 mu/R, w=chi_R, and pi is the canonical scalar momentum. The previous completed phase counts are 67 mass pairs, 67 GR scalar pairs, and 68 MTS scalar pairs.

The GR physical reference is reconstructed from its formula-defined fields, not from the failed older GR boundary root. The MTS comparison initially uses the unchanged saved outer-clock root, but with the natural reactions required by the current action. This is not a comparison against the old artificially fitted reaction residual.

The canonical bulk mass velocity is

    s = kappa N F^(3/2) pi w.

With the full Gram scalar covector G_chi, the one-sided parent fluxes are

    u_in  = s_in  + kappa sqrt(F_in)  q_in  G_chi,in  / N_in,
    u_out = s_out - kappa sqrt(F_out) q_out G_chi,out / N_out.

The opposite signs are essential. The prior calculation identifies the two residual rows as minus/plus (weak flux minus parent flux)/(kappa sqrt(F)), with the interior already closed. No Gram force is set to zero here.

## 3. Derivation: the full parent kernel has a cell-family representation

Define the initial generator and a global primitive

    g(R) = kappa sqrt(F(R)) Pdot(R)/N(R),
    G(R) = integral from R_in to R of g(s) ds.

For factor f anchored at a_f, J_f(R)=exp(G(R)-G(a_f)). Its node current is

    I_fi = A_f [S_fi C_i A'_f - B_fi q_i D_f]/h,
    A_f = sum_i B_fi chi_i,
    C_i = R_i^2 N_i sqrt(F_i),
    D_f = sum_i S_fi J_fi C_i,
    A'_f = sum_i B_fi J_fi q_i.

Thus sum_i I_fi J_fi=0 for every factor, by direct cancellation of the two products. The momentum covector is

    G_P[delta P] = sum_fi I_fi J_fi
                  integral from a_f to R_i of
                  kappa sqrt(F)/(N J_f(R)^2) delta P(R) dR.

Changing to the global primitive produces its density

    G_P(R) = k(R) sum_fi I_fi exp(G(R_i)+G(a_f))
                      sign(R_i-a_f) 1_between(a_f,R_i)(R),
    k(R) = kappa sqrt(F(R))/N(R) exp(-2G(R)).

Every anchor jump cancels: its coefficient is proportional to sum_i I_fi J_fi. Only scalar-node jumps remain. Consequently, at fixed initial generator the entire parent momentum-force family lies in the span of

    f_j(R) = k(R) 1_(R_j,R_(j+1))(R),  j=0,...,15.

Endpoint values mean the physical one-sided limits. The discontinuous cell functions are force/momentum functions, not discontinuous mass coordinates. This reduction uses the full link currents and their orientations; it is not a fit to the two observed residual numbers.

Checks on the actual MTS state: factor-current cancellation 3.39e-20; cell coefficients agree at two distinct points per cell within 4.07e-20; global-primitive versus original link logs agree within 3.42e-16; one-sided kernel endpoint identity agrees to reported floating precision. Integrating the reconstructed cell density against the new momentum tests agrees with the original oriented-link covector within 5.64e-15.

These exact algebraic identities apply to the stated parent kernel. Their floating-point quadrature implementation is checked, not interval-enclosed.

## 4. Derivation: two paired trace-dual extensions

Let V and W denote the old completed mass-coordinate and momentum matrices, Q the bulk quadrature, M=W^T Q V, and E endpoint evaluation. Let B collect the 16 parent kernel functions. The old weak projection has endpoint defect functional

    L = E B - E V M^(-1) W^T Q B.

Seek two dual momentum functions T0 satisfying

    T0^T Q V = 0,       T0^T Q B = L.

An explicit construction uses the residual of B after its L2 projection onto V. Provided that residual family has full rank, its Riesz map supplies T0. We keep **all 16** kernel-family directions. After an invertible two-column normalization T=T0 A, construct two continuous coordinate functions H such that

    W^T Q H = 0,       T^T Q H = I_2,
    E H = A^(-T),      H(R_i)=0 at every interior scalar node.

We construct H from the two endpoint scalar hat functions plus continuous polynomial bubbles on the combined scalar-node/mass-face partition. The bubbles vanish at every partition knot. Four bubble modes per subcell provide the dual-moment reservoir; the actual required row rank, 69, is checked.

The enlarged canonical pairing is block diagonal:

    [W,T]^T Q [V,H] = diag(M,I_2).

For every force in span(B), its new weak projection therefore has endpoint value

    E V M^(-1) W^T Q B + A^(-T) A^T L = E B.

This preserves all previous weak equations and both endpoint traces at once. No canonical coefficient is overwritten after the solve and no new boundary force is inserted. Original coordinate and momentum maps remain bit-for-bit present as the first columns.

On both branches the complete kernel trace error is at most 2.78e-17, old-moment error at most 8.17e-18, and enlarged pairing condition below 1.66. Twelve unfitted random kernel combinations per branch pass; the old projection fails the same trace tests. The MTS projection now has 69 mass pairs and retains all 68 scalar pairs.

### Numerical false start, retained rather than hidden

`source-intake/navier-stokes/20260911/annular-canonical-trace-projection-attempt01/status.json` records a failed construction. A normal-equation Riesz implementation squared the conditioning of the nearly common carrier direction; it left a kernel trace error around 1.29e-6. No physics rejection follows from that numerical failure.

The replacement resolves the residual family by SVD, re-orthogonalizes it against V, and solves the unsquared dual moment system. The smallest retained residual singular values are 3.66e-8 (GR) and 7.89e-8 (MTS). No direction is truncated to make the test pass. Original scripts and executed snapshots are preserved alongside the corrected version.

## 5. Momentum/time-link self-consistency, not a frozen-force substitution

Adding a canonical pair can change Pdot and hence the kernel that motivated it. That change must be checked.

At the exact integral level the bulk mass Euler force on H is <E_N,H>, after integration by parts and cancellation with the natural boundary reactions/clock. The completed old momentum space contains E_N, so this is zero. Gram mass forces sample scalar nodes; H vanishes at the interior nodes and endpoint sampling weights vanish. Therefore the ideal added mass Euler force is also zero. The block-diagonal pairing then leaves the old Pdot unchanged. This is the conditional momentum-transparency argument.

The implemented calculation **reevaluates** the new Euler force, Pdot, and all link Jacobians. It does not assume that argument is numerically exact. The MTS sampled Pdot changes by 1.52e-8, the added momentum-rate coefficients are about 6.05e-10, link logs change by 1.34e-12, and the actual kernel carrier changes by 1.98e-13. The residual weak-integration/roundoff discrepancy is retained. The GR sampled Pdot change is 1.12e-8; its constraint propagation nevertheless remains near 1e-17.

The initial diagnostic sampled-Pdot threshold of 1e-8 was too tight for this already observed weak-integration discrepancy and is explicitly 1e-7 in the stable runner. Kernel-self-consistency and complete constraint-row thresholds were not loosened. This is not an assertion that Pdot is pointwise exact.

The frame is frozen at the initial physical fields. No field-dependent change of coordinates along an evolved trajectory is justified by this calculation.

## 6. Results before changing initial data

| Initial-state calculation | GR max abs(Cdot) | MTS max abs(Cdot) |
|---|---:|---:|
| Previous bulk-rate completion | 1.44674e-17 | 7.71469e-6 |
| New trace-preserving completion | 1.83605e-17 | 1.34289e-13 |
| Same frame, higher bulk/link quadrature | 1.34019e-17 | 1.95093e-14 |

MTS weak-minus-parent endpoint flux gaps become approximately (-1.087e-14,-7.063e-15), rather than (6.265e-7,2.748e-7). Interior Cdot stays below 1.8e-15.

However, the actual parent inner flux still differs from the prescribed mass drive by about -3.03566e-8, and the outer scalar drive differs by +3.97953e-10. These are distinct boundary-preparation conditions. The next subsection solves them; they are not silently redefined away.

## 7. Actual compatible boundary-data preparation

Write the auxiliary scalar momentum as xi=pi/K_seed, retaining the original frozen canonical kinetic map K_seed. For x=(R-R_in)/(R_out-R_in), use only

    xi_new = xi_saved + a_in (1-3x^2+2x^3) + a_out (3x^2-2x^3).

These are whole-annulus cubic lifts with zero endpoint derivatives, not narrow spikes or an unconstrained interior fit. Their conversion into nodal/Hermite-correction coefficients is explicit. They change xi, not directly the physical scalar velocity q.

For each trial pair of amplitudes:

1. Hold chi, the inner mass, original mass bubbles, and prescribed external drives fixed.
2. Solve all 17 radial mass-constraint rows for the remaining 17 mass-face coefficients at the actual 12-point bulk quadrature. The analytic mass Jacobian includes the Gram nodal source derivative.
3. Set the lapse normalization from N_out/sqrt(F_out)=C_out, retaining its original shape.
4. Rebuild the canonical rate completion and full parent-kernel trace extension from those actual fields.
5. Reevaluate the natural reactions, Pdot, q, all links, parent flux, and all constraint-rate rows.
6. Solve parent_inner_flux=prescribed_inner_drive and q_out=prescribed_outer_scalar_drive for the two amplitudes.

The two-by-two boundary Jacobian has condition approximately 1.00868. Independent step-size checks confirm its nondegenerate sensitivity. One Newton update gives

    a_in  = -8.91408429334396e-7,
    a_out = -3.293365316827791e-10.

The largest mass-coefficient change is 9.37756e-9. The prescribed inner mass velocity remains 0.00033578281226508903; the prescribed outer scalar velocity remains 0.015344562303521506. These are boundary-data coefficients, not new couplings or fitted observational parameters.

| Prepared MTS check | Value |
|---|---:|
| All mass constraints, max abs(C) | 2.57391e-15 |
| All constraint rates, max abs(Cdot) | 1.29016e-13 |
| Higher-quadrature max abs(C) | 2.57345e-15 |
| Higher-quadrature max abs(Cdot) | 7.07393e-14 |
| Parent inner mass-drive gap | -8.40257e-17 |
| Actual weak inner mass-drive gap | -1.05285e-14 |
| Outer scalar-drive gap | -1.45717e-15 |
| Natural outer-clock gap | 0 |
| Minimum sampled F | 0.6595720052 |
| Minimum sampled N | 0.8120644431 |

The analytic mass derivative agrees with an independent complex-step directional derivative within 1.78e-15. A fresh reconstruction replays the prepared state. All original fixed-input comparisons and archive round trips pass. Positivity here is sampled, not a new interval chart certificate.

This does not cure or certify the regularity of the inherited free momentum profile. A small boundary adjustment and tiny weak residual are not evidence of spatial convergence.

## 8. What is now solved, and the next genuinely different task

Solved at this initial finite resolution: the two boundary projection defects, the corresponding canonical paired-space construction, numerical Pdot/link self-consistency, and the retained external boundary-data compatibility. GR is not broken by the same trace-space machinery.

Next: transfer this prepared physical state onto N32 and then N64 **with the same annulus, boundary histories, scalar/free-profile prescription, and natural reactions**. Rebuild the parent kernel family at each resolution; compare actual physical profiles, first-jet norms, momentum variation and conditioning as well as every constraint row. Do not substitute independently tuned archived N32/N64 data and call that convergence. Higher quadrature is not higher spatial resolution.

Before claiming any time evolution, derive/implement the complete nonlinear Gram action away from P=0, account for any field-dependent frame transport, and solve compatible higher boundary time derivatives. No old trajectory or residence certificate transfers to this new initial datum automatically.

No reopening of the old numeric-coupling hunt is required to perform this next representation/continuum test. Conversely, this local construction does not settle the programme's other coupling, quantum, cosmology or observational questions.

## 9. Reproducibility and scope

- `scripts/annular_canonical_trace_context_20260911.py`: source-backed physical/reference context and original frames.
- `scripts/annular_canonical_trace_projection_20260911.py` and `scripts/derive_annular_canonical_trace_projection_20260911.py`: preserved failed normal-equation attempt.
- `scripts/annular_canonical_trace_projection_stable_20260911.py` and `scripts/derive_annular_canonical_trace_projection_stable_20260911.py`: successful unsquared construction and both-branch runner.
- `scripts/annular_canonical_trace_boundary_data_20260911.py`: analytic mass projection and two-amplitude preparation.
- `scripts/verify_annular_canonical_trace_and_prepare_20260911.py`: random-family controls, negative controls, source reconstruction, actual preparation, derivative checks and higher quadrature.
- `source-intake/navier-stokes/20260911/annular-canonical-trace-projection-attempt02/status.json`: 32 passed checks, unchanged initial-state comparison.
- `source-intake/navier-stokes/20260911/annular-canonical-trace-boundary-control-attempt01/status.json`: 30 passed checks and preparation history.
- `source-intake/navier-stokes/20260911/annular-canonical-trace-boundary-control-attempt01/MTS_prepared_initial_data.npz`: the new prepared physical initial datum, not an evolved solution.
- `source-intake/navier-stokes/20260911/annular-canonical-trace-boundary-control-attempt01/MTS_prepared_first_jet.npz`: its computed initial canonical rates and fields.

All work remains in post-checkpoint-work. One BelowNormal single-core Python worker at a time; no subagents, GitHub action, galaxy edits or frozen-workbench edits. Old evidence and the failed attempt remain intact.
