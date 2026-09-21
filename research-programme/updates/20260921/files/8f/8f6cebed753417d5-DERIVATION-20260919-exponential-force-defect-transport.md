# Exponential transport and the spatial source-force defect

Private continuation of `DERIVATION-20260919-live-Gram-force-error-transport.md`. The purpose is to resolve the numerical transport integral without deleting the fast modes or freezing the actual geometry. The existing 12.5718% integrated and 13.58% instantaneous MTS/continuum discrepancies are unchanged. This stage does not establish the full GR limit.

## 1. Exact split, not replacement dynamics

Use the already saved initial canonical basis of the SAME finite model. With positive scalar generalized frequencies Omega and M-orthonormal modes V, encode the central scalar differences as

    x_q = Omega V^T M delta_q,
    x_p = V^T delta_p.

The source coordinate/momentum form an additional zero-frequency block. All 1072 scalar modes remain. In these coordinates the constant reference generator is

    A = [[0,Omega],[-Omega,0]],   A^T=-A.

The full finite-element state, including all material labels and the moving sources, still determines the geometry and central canonical RHS. At each saved state the complete live geometry/inverse-momentum solve is repeated. The central block is not asserted to be a closed subsystem independent of the other labels.

For two actual temporal refinements let e be their encoded central-state difference and define

    Delta_R = encode(F_central(full_fine_state)-F_central(full_coarse_state)) - A e.

Consequently e'=A e+Delta_R for exact trajectories, with an additional path-defect term for approximate reconstructed paths. The constant A is only a computational split; all changing metric, source and nonlinear feedback stays in Delta_R. Setting that remainder to zero would change the equations and is not done here.

## 2. The terminal force covector and its exact linear pullback

For the explicit Gram functional at the fine terminal geometry, the midpoint gradient from the preceding checkpoint gives the exact quadratic secant

    J_f(T)-J_c(T) = c^T e(T) + d_theta(T).

The scalar-coordinate part of c is Omega^-1 V^T g, its scalar-momentum/source entries are zero, and d_theta is the separately evaluated terminal geometry/source-position correction. This specific observable is the explicit Gram field contribution, not the entire physical radiation force. Initial-state differences remain in the transport formula even though the tested temporal refinements share the same initial data.

Let z(t)=exp(A^T(T-t)) c=exp(-A(T-t)) c. Then

    c^T e(T) = z(0)^T e(0) + integral z(t)^T Delta_R(t) dt

for exact paths, adding integral z^T delta_r for approximate paths. This is an exact identity with a constant linear pullback and the full nonlinear remainder. It is not the full nonlinear adjoint of the live Jacobian, and is not labeled as such. It avoids assuming that the fast part of the actual force defect can be integrated accurately with an ordinary trapezoid rule.

## 3. Integrate the oscillatory kernel exactly

On an interval of length h, linearly interpolate the sampled remainder R_0,R_1. The convolution with the retained rotation is

    Q = h phi_1(hA) R_0 + h phi_2(hA) (R_1-R_0),
    phi_1(z)=(exp(z)-1)/z,
    phi_2(z)=(exp(z)-1-z)/z^2.

For one rotation block, theta=h omega and J=[[0,1],[-1,0]],

    phi_2(theta J)
       = (1-cos(theta))/theta^2 I + (theta-sin(theta))/theta^2 J.

The implementation uses sinc for the diagonal, a Taylor expansion for the small-angle off-diagonal, and the exact zero-frequency limit phi_2(0)=I/2. No eigenvalue threshold removes a mode.

The independent validator compares this kernel with augmented matrix exponentials for affine forcing at frequencies from zero through 1e4. It checks the backward-dual sign and norm-preserving rotation. In the oscillatory fixture, ordinary weighted trapezoids fail while the exponential convolution remains exact to numerical precision on the same sampled forcing.

There is a useful conditional bound independent of the size of omega. If the true remainder is twice differentiable and ||R''||<=M_R on an interval, the linear interpolation error is bounded by M_R*s*(h-s)/2. Since exp(tA) is unitary,

    ||integral exp(A(h-s)) [R(s)-I_1 R(s)] ds|| <= M_R h^3/12.

The corresponding terminal-output error is at most ||c|| M_R h^3/12. No exp(omega h) factor appears. This is a derivation, not a claim that M_R has already been certified for the actual parent. The analytic quadratic-forcing control tests the bound, including high frequency.

## 4. Keep the unresolved defect visible

For each saved interval define

    eta_n = e_(n+1)-exp(h_n A)e_n-Q_n.

The discrete budget is exactly

    c^T e_end = z_start^T e_start
                + sum z_(n+1)^T Q_n + sum z_(n+1)^T eta_n.

The two sums are recorded separately, along with ordinary weighted trapezoid quadrature of the SAME remainder and absolute interval bounds. The endpoint-defined eta combines path/evolution defects, unresolved remainder interpolation and numerical reconstruction. It is NOT automatically the time integrator's error. A vanishing reconstruction error of this telescoping budget is not evidence that the remainder integral or the physical limit is resolved.

The live calculations use all available common saved knots: 65 for MTS64/128-step trajectories, 33 for reference32/64. Each provides nested sampling controls beginning at eight intervals. Source-straddling, remaining and total Gram covectors are tested separately. A nonzero unit-modal covector is also tested in both branches so the zero-Gram reference does not make every implementation check vacuous; that extra covector has no physical interpretation.

## 5. Completed temporal results

The independent algebra validator completed 33 checks, the MTS reconstruction 153, and the reference reconstruction 85. These use 65 and 33 actual saved states respectively, producing 28 transport budgets. No new trajectory was evolved. All numbers below use the existing normalized annular units, not calibrated SI forces or observational constraints.

For the MTS total Gram covector, the fixed-geometry terminal pairing is 1.72072878571e-10. Its modal norm is 523.9304. The actual initial-state pairing is zero.

| Sample intervals | Exponential remainder integral | Unresolved weighted defect | Ordinary weighted trapezoid |
|---|---:|---:|---:|
| 8 | -3.25818e-13 | 1.72399e-10 | -1.93369e-12 |
| 16 | -1.20328e-14 | 1.72085e-10 | 1.61263e-13 |
| 32 | 2.91574e-14 | 1.72044e-10 | -2.82973e-14 |
| 64 | -4.48636e-14 | 1.72118e-10 | -7.35319e-14 |

The analytically integrated rotation removes one known quadrature difficulty, but does NOT certify the live remainder integral: its estimate still changes sign. On the finest sampling its magnitude is about 0.0261% of the terminal pairing; the 32-to-64 sampling change is about 0.0430%. Almost all that pairing therefore remains in eta, whose interpretation is still unresolved. The finest absolute interval bounds are 2.22655e-12 for the forcing and 7.05755e-9 for eta; cancellations remain substantial. The discrete telescope closes to about 3e-24, an implementation result rather than a physical-error certificate.

The reference Gram covector vanishes by construction. Its additional nonzero unit-modal control has terminal pairing 1.73113e-15 and exponential estimates -1.07067e-17, -2.00349e-17 and -2.16945e-17 on 8/16/32 intervals. This exercises the nontrivial transport algebra without pretending that the probe is a physical force. Independent affine-forcing tests agree with augmented matrix exponentials, including high-frequency and zero-frequency cases; their largest absolute difference is 1.33e-11 at large rotation angle. The curvature estimate remains conditional on actual derivative control.

These terms use a different decomposition from the preceding momentum-channel budget. Their smaller size is NOT an orders-of-magnitude improvement in the physical theory. The preceding 12.5718% integrated and 13.58% instantaneous continuum discrepancies are unchanged.

## 6. A failed assumption caught in the spatial comparison

The first spatial attempt failed its nesting assertion. The 513-grid source-fitted mesh does not contain every 257-grid element boundary: eleven coarse edges are unmatched, with maximum nearest-fine-edge distance 0.00125. The failed script and evidence are preserved, not patched or deleted. Small nodal round-trip errors do not prove equality of the piecewise-polynomial functions between nodes.

Accordingly, the preceding phrase "embedded coarse field" must be read as a nodally interpolated coarse field, not an exact inclusion of the entire coarse P2 space. Existing saved numerical differences are unchanged; any inference of exact nesting is withdrawn. The earlier interpolant consistency theorem does not require nesting, so this finding does not by itself invalidate that theorem.

The corrected calculation defines an explicit off-space extension J_h* of the original fine-grid functional. It samples the original coarse P2 field at the fine nodes, but evaluates its ORIGINAL piecewise gradient at the original fine quadrature nodes. Its original source-gradient jump is also retained. In particular,

    b_h[u_H]_i = sum_quadrature w_h phi_i (-c/J) partial_x u_H,
    v_h = M_h^-1 b_h[u_H],
    f_h = D_h samples(u_H) - r_h jump_H(u_H),
    J_h*(u_H) = -0.5 f_h^T W_b,h f_h + f_h^T W_h B_h v_h.

Here w_h is the positive kinetic quadrature weight, c the source-map motion, J its Jacobian, and B_h the existing lifted Gram operator. No mass, action coefficient or quadrature rule is changed. On the fine finite-element space this extension reproduces the original functional, as directly tested. When a coarse breakpoint cuts a fine element, the existing quadrature is NOT asserted to integrate the off-space field exactly. J_h* is a declared discrete comparison functional, not an independent continuous-integral oracle or evolved counterfactual.

Writing theta for the reconstructed geometry and source position, the exact ordered telescope is

    J_h(u_h;theta_h)-J_H(u_H;theta_H)
      = [J_h(u_h;theta_h)-J_h(I_h u_H;theta_h)]             field/state
      + [J_h(I_h u_H;theta_h)-J_h*(u_H;theta_h)]            transfer
      + [J_h*(u_H;theta_h)-J_h*(u_H;theta_H)]               geometry/source
      + [J_h*(u_H;theta_H)-J_H(u_H;theta_H)].               operator/mesh

This comparison path is explicit but is not a unique causal decomposition. Geometry is reconstructed from the full saved state of each branch; only the counterfactual evaluations hold it fixed. Both reference and MTS, at initial and final time, are checked with all Gram rows retained and source/remaining rows reported separately. The corrected attempt completes 31 checks and yields 12 partition rows.

## 7. What the spatial split actually finds

The endpoint is T=4e-5, with the actual saved 257/32-step and 513/128-step MTS states (reference uses 513/64). Their time discretizations differ as well as their spatial discretizations. This is a hierarchy diagnostic, NOT an isolated spatial truncation error or an unknown continuum error.

| Total Gram difference contribution | Initial time | Final time |
|---|---:|---:|
| Field/state | -1.353268e-9 | -2.970155e-8 |
| Nonnested transfer | 1.870884e-11 | 1.870903e-11 |
| Geometry/source | 3.651157e-19 | -5.721873e-18 |
| Operator/mesh | -6.861474e-9 | 1.109345e-8 |
| Direct fine-minus-coarse | -8.196033e-9 | -1.858939e-8 |

The transfer correction is real, but about 0.101% of the final direct hierarchy difference, so it does not explain the main discrepancy. Geometry/source effects are also small in this particular comparison, not proven small in general. The field/state and operator terms are much larger and partially cancel. The initial discrepancy is already appreciable; it would be wrong to assign the whole final difference to evolution error.

Subtracting the initial budget from the final one gives about -2.834829e-8 field/state growth, 1.85950e-16 transfer growth and 1.795493e-8 operator change, for a net -1.039336e-8. This increment comparison removes the initial diagnostic offset algebraically; it does NOT remove the dynamical influence of initial discretization errors. The source-straddling endpoint field/state term is -2.834955e-8; its operator term is +1.795392e-8. Remaining rows and their cancellation are retained.

Reference Gram terms are all zero, as expected with that Gram sector disabled. This is a fair same-pipeline control but not a nonzero test of the entire physical reference force. The independently measured reference impulse mismatch remains about 0.1889%. Neither branch is promoted to a physical or full-GR pass here.

## 8. The next computable law, not another missing-input survey

The spatial split points to a precise next calculation: separate the operator/mesh term into a mass-projection commutator and the remaining Gram stencil/weight terms on the SAME coarse field and geometry. Define

    v_H = M_H^-1 b_H[u_H],
    rho_h = b_h[u_H] - M_h I_h v_H,
    v_h - I_h v_H = M_h^-1 rho_h.

The last identity is exact; I_h is nodal interpolation, not an assumed nested embedding. For fixed f_h and positive-definite M_h, set a_h=B_h^T W_h f_h. The corresponding fine-functional projection contribution is exactly

    delta_J_projection = a_h^T M_h^-1 rho_h,
    |delta_J_projection|
       <= sqrt(a_h^T M_h^-1 a_h) sqrt(rho_h^T M_h^-1 rho_h).

Subtracting the fine functional evaluated with I_h v_H from the fine functional evaluated with v_h isolates this term. The rest of the operator difference remains explicitly in the changed stencil, weights and fine-versus-coarse evaluation; it is not silently discarded. This follows from the mass equations and Cauchy-Schwarz and supplies a concrete residual to measure next, rather than another large evolution or an assertion that an L2 field norm controls the source force. The numerical usefulness of this bound has NOT yet been tested.

After qualifying that split on saved states, the target is a source-force-stable spatial approximation and evolving-error estimate, keeping the existing action and full feedback. Another time-halving alone is not the preferred response to the present spatial sensitivity. No mode clipping, fitting away the force, altered physical action, or public claim is justified.

## 9. Reproducibility and limits

Successful implementation checks total 302 across four completed evidence folders. One new failed execution records the rejected nesting assumption; all earlier failures remain preserved. All new evidence is private and non-claim. Implementation checks test the stated finite calculations, not 302 independent confirmations of MTS. No new evolution, GitHub action, subagent, or protected-workbench edit was performed.

Implementations and evidence:

- `scripts/annular_exponential_transport_20260919.py`
- `scripts/validate_annular_exponential_transport_20260919.py`
- `scripts/run_annular_live_exponential_transport_20260919.py`
- `scripts/derive_annular_spatial_Gram_defect_split_20260919.py` (failed assumption retained)
- `scripts/derive_annular_spatial_Gram_transfer_split_v2_20260919.py`
- `source-intake/navier-stokes/20260914/annular-exponential-transport-algebra-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-exponential-transport-MTS-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-exponential-transport-reference-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-spatial-Gram-defect-split-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-spatial-Gram-defect-split-attempt02/status.json`

The final integrity seal additionally verifies inherited source hashes, source compilation without bytecode, CSV parsing and the protected-directory modification-time scan. That scan is not a pre-turn complete hash baseline. No full-interval or continuum convergence theorem is asserted.
