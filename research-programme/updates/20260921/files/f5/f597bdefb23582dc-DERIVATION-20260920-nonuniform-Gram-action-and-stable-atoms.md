# A variational nonuniform Gram candidate, with stable source-trace evaluation

Private continuation of `DERIVATION-20260920-trace-aware-Gram-force-contribution.md`.

Status: COMPLETE for the construction, primary-action derivative controls, fixed-field consistency bounds, and saved-profile probes. Not a live force repair, unique parent derivation, or GR-limit claim. The original live action and all original results remain unchanged.

## 1. What is new

We have built a positive nonuniform extension of the existing discrete Gram action, instead of subtracting another diagnostic term. It recovers the original uniform rule in ideal arithmetic, retains the original positive factor template and coefficient sampling, and has an explicit source/mesh/coefficient variation. We also derived an exact local derivative-atom evaluation which avoids the dangerous global hinge subtraction in the numerical kernel.

Two limitations are demonstrated rather than hidden:

- Uniform recovery, positivity and consistency do not uniquely select a nonuniform extension. An explicit second positive extension has the same uniform rule.
- Ordinary binary64 evaluation can corrupt the signed saved-profile pairing, even changing its sign. A 48/72-digit calculation and an independently structured 32-digit local-atom evaluation resolve the arithmetic issue for these inputs.

This is a qualified candidate numerical construction, not permission to replace the parent action silently.

## 2. Source the original rule

The positive template and original coefficient sampler are sourced from `scripts/annular_moving_collar_sparse_20260914.py` and `scripts/annular_compatible_current_restoring_20260909.py`. Write their factor template as L_N and their positive row sampler as P_N. On a uniform base grid with spacing h,

    E_G = (L_N Delta^3 w)^T diag(P_N q) (L_N Delta^3 w)/(2h),
    w(x) = u(x) - j(u)(x-a)_+.

Here a is the anchored reference source and j is its one-sided reference-coordinate derivative jump. q is the original spatial coefficient divided by the source pullback Jacobian. The reference branch has no extra Gram term.

The exact existing template bound is inherited from `DERIVATION-20260919-weak-Gram-consistency-and-fixed-field-bound.md`:

    ||L_N||^2 <= C_*,
    C_* = 59097/573104 + 2(3/392) + 1/392.

This is a sourced discrete remainder, not a new resolution-independent physical coupling.

## 3. Derive a nonuniform candidate

For strictly increasing reference knots x_i, define

    ell_i = (x_(i+3)-x_i)/3,
    U_i w = 6 ell_i^(5/2) [x_i,x_(i+1),x_(i+2),x_(i+3)] w
          = sum_(r=0)^3 a_ir w(x_(i+r)),
    a_ir = 6 ell_i^(5/2) /
           product_(s != r) (x_(i+r)-x_(i+s)).

The third divided difference annihilates every quadratic polynomial. For uniform knots it is Delta^3/(6h^3), hence U=Delta^3/sqrt(h). Therefore the candidate

    E_N = (L_N U w)^T diag(P_N q) (L_N U w)/2

recovers the old uniform functional exactly in ideal arithmetic, including its normalization. The original index-based coefficient sampler P_N is retained, not replaced with a fitted quadrature.

P_N has nonnegative entries with row sum one. Positive nodal q therefore gives a positive semidefinite quadratic form. If j is a linear functional on field coefficients, w=(S-hinge*j)u, where S evaluates the field at Gram knots. This yields a symmetric positive semidefinite Hessian without deleting field modes. The affine coordinate-rescaling check gives E_N -> E_N/scale when q and field amplitudes are held fixed and the jump rescales inversely. That is a dimensional check, not a proof of general covariance.

Choosing the span average ell_i and retaining P_N are explicit numerical-extension choices. They are not claimed to follow uniquely from the parent theory.

### Uniform recovery tests

Counts17,33,65,257 reproduce the sourced uniform factors, sampler and energy. The largest measured factor-relative difference on the saved binary64-style uniform coordinates is9.49e-14; the largest energy difference, normalized by max(1,|E|), is5.57e-14. Exact rational moment tests establish the ideal uniform identity separately. Binary64 linspace coordinates need not have exactly identical rational gaps.

## 4. Full first variation on a fixed topology

Away from source/knot crossings, with dot denoting any admissible variation,

    dot ell_i = (dot x_(i+3)-dot x_i)/3,
    dot a_ir / a_ir = (5/2) dot ell_i/ell_i
        - sum_(s != r) (dot x_(i+r)-dot x_(i+s))/(x_(i+r)-x_(i+s)),
    dot w_i = dot u_i - dot j (x_i-a)_+
        - j 1_(x_i>a)(dot x_i-dot a).

For R=L_N U w and Q=P_N q,

    dot E_N = R^T diag(Q) L_N (dot U w+U dot w)
            + (R^2)^T P_N dot q/2.

The primary implementation checks this against an independent complex-step derivative with simultaneous field, source, knot and coefficient changes. In its nonuniform fixture, the stencil, coefficient and field/trace contributions are respectively

    +0.027222475595965738,
    +0.0038852434663150357,
    -0.00004258571710940972.

Their total is0.031065133345171365 versus0.031065133345171355 independently. Dropping any of those three contributions fails a negative control. A separate field variation includes the chain rule for j(u); a Hessian test checks positivity.

This is not yet the complete coupled moving-source variation: the actual dependence of knots, q, field sampling and geometry on the parent state must be assembled consistently. Knot insertion/remeshing is a topology change and needs its own transfer/energy treatment. The current differentiable chart explicitly excludes a Gram knot touching/crossing the source.

## 5. Nonuniform consistency bounds

Let h_max be the largest knot gap and let the interval length be D. For a fixed C^3 compensated field, the divided-difference mean-value identity gives

    |U_i w| <= ell_i^(5/2) ||w'''||_infinity.

Since sum_i ell_i <= D and ell_i <= h_max,

    E_N <= (C_* q_max/2) D h_max^4 ||w'''||_infinity^2.

This does not need uniform knot spacing. It does need bounded q and a fixed smooth field; it is not a uniform estimate for the evolving parent solutions.

For a fixed continuous piecewise quadratic field,

    w(x) = p2(x) + sum_k A_k(x-b_k)_+
                  + (1/2) sum_k B_k(x-b_k)_+^2.

Let rho bound the largest/smallest gap ratio in every four-knot window. The normalized coefficients satisfy sum_r |sqrt(ell_i) a_ir| <= 8 rho^3. Only at most three windows contribute for each hinge atom. This gives

    ||U (x-b)_+|| <= 24 sqrt(3) rho^3 sqrt(h_max),
    ||U [(x-b)_+^2/2]|| <= 36 sqrt(3) rho^3 h_max^(3/2),

and therefore

    sqrt(2E_N) <= sqrt(C_* q_max) sqrt(3) rho^3
        [24 sqrt(h_max) sum|A_k| + 36 h_max^(3/2) sum|B_k|].

These are deliberately conservative sufficient bounds. They imply fixed-field consistency along a shape-regular sequence, not monotone force convergence. Both smooth and piecewise-quadratic fixture scans pass them. The smooth fixture's energy falls from2.57199e-4 at17 knots to7.07496e-8 at129; its piecewise-quadratic counterpart is not monotone at the first refinement.

## 6. Nonuniqueness is real

In each four-knot window let

    eta_i = sum_(r=0)^2 (gap_(i+r)-ell_i)^2 /
            sum_(r=0)^2 gap_(i+r)^2.

Then0 <= eta_i <1 and eta_i=0 on an ideal uniform grid. Replacing U_i by (1+eta_i)U_i leaves uniform recovery and polynomial annihilation intact, remains positive, and retains the displayed consistency rates with a larger bound. It is a distinct nonuniform action: the same fixture has energies0.358669704487328 and0.37908339738197394.

This is a witness against uniqueness, not an extra physical parameter fitted to improve agreement. The alternative has only been used for this algebraic/static sensitivity control; its additional dot eta terms must be included before any moving-force test. Only the primary action's full fixed-topology variation has been implemented and checked here.

## 7. Probe the actual saved fields, not invented front speeds

The original frozen coarse geometry is reproduced exactly at the prior comparison weights in both branches. Use the same saved coarse primal u_c(t) and fine adjoint test z_f(t)=M_f^-1 lambda_v(t), at t=0 and T. The T endpoint is the terminal force covector; the zero endpoint uses the already propagated fine adjoint. These are evaluations of A_G(z_f,u_c), not time-integrated force contributions or new evolving solutions.

The nonuniform seed uses the exact common P2 degrees of freedom:1094 knots. Its two nested refinements have2187 and4373 knots. Every common field coefficient is retained. Exact native embedding/recovery identities prove no original field mode is lost; this does not require every original native midpoint to be a common nodal location. A first attempt incorrectly required that stronger literal-coordinate condition, failed before any result, and is preserved. The corrected test checks the actual function-space identity.

The largest gaps halve from0.0015625 to0.000390625; the maximum local gap ratio remains about20. All saved P2 breakpoints are represented, but this is NOT proof that the actual evolving MTS fronts are resolved. In particular, the second-order wave cone or earlier prescribed-fixture speeds cannot be assigned to the full dispersive Gram system.

### Qualified signed pairings

72-digit accumulation, conditioned on the original binary64 inputs and saved48-digit path data:

| Gram knots | Primary, t=0 | Primary, t=T | Alternative, t=T |
|---|---:|---:|---:|
| Uniform513 comparator | -8.51760637e-8 | +1.06454030e-4 | +1.06454030e-4 |
| Common-profile1094 | -4.58237204e-8 | +8.24263361e-5 | +9.96547518e-5 |
| Refined2187 | -1.15673710e-8 | +3.15240374e-5 | +3.79124865e-5 |
| Refined4373 | -1.14741668e-8 | +1.49227897e-5 | +1.77980041e-5 |

The reference Gram baseline is exactly zero. Its nonzero mass/gradient and physical force errors have NOT been recomputed or declared absent.

The final-time primary pairing decreases, but the initial pairing has scarcely changed at the last refinement, and the two nonuniform extensions differ materially. These facts do not qualify a converged force or select the extension. No convergence order or continuum value is fitted from these three levels.

## 8. Arithmetic trap and a derived stable evaluation

The first binary64-style probe produced incorrect signed values on some saved profiles. For example, its1094-knot initial primary pairing was+1.64771106e-6; the qualified value is-4.58237204e-8. Positive-energy/Cauchy checks alone did not expose that loss of accuracy. Those raw signed values are superseded, not used to support the science.

Independent 48/72-digit accumulation agrees within4.60e-41 in all16 signed pairings, at a fixed arithmetic-only1e-24 gate. That is not a physical force accuracy claim, and high precision cannot upgrade the original geometry or coefficient inputs.

We then derived an exact local evaluation. Because U annihilates the polynomial p2, each row can be computed solely from derivative-jump atoms strictly inside its four-knot support:

    U_i w = sum_(b_k inside support)
        [A_k U_i(x-b_k)_+ + B_k U_i((x-b_k)_+^2/2)].

For native P2 pieces, A_k is the difference of adjacent first derivatives and B_k the difference of second derivatives. The source first-derivative atom is removed ONLY by the original definition w=u-j(u)hinge; the source curvature atom and all other atoms remain. This is exact evaluation of the same compensated function, not filtering modes.

Ten exact rational near-source identities and an omitted-curvature negative control check this construction. A first attempt to evaluate it entirely with binary64 still missed the unchanged arithmetic gate on one sensitive pairing; that failure is preserved. The qualified version prepares native atoms consistently at72 digits and evaluates LOCAL sums at32 digits. All16 pairings agree with the full72-digit calculation within9.98e-33. It takes about6seconds for the saved-profile suite. This qualifies the local evaluator, not a fully binary64 evolution or a general speedup benchmark.

## 9. Decision and next substantive step

Construction gate: passed for this explicit primary numerical candidate.
Unique parent-derived nonuniform action: NOT established.
Actual evolving front resolution: NOT established.
Physical force repair / local-GR or full-GR recovery: NOT established.

Next assemble the candidate's complete frozen quadratic field action on the common P2 space, including the unchanged mass/gradient sectors and the derived source/coefficient variation. Verify the resulting stiffness and source-force derivatives against the stable atom form, estimate the unfiltered frequencies, then attempt a short frozen-response pilot in both branches. Include extension sensitivity; do not choose a rule because it gives a nicer force. Do not start a long moving-source run yet. Initial-layer control, consistent remeshing and the full coupled metric/source variation remain obligations.

The original12.5718% impulse,13.5770% fine/continuum endpoint and32.5535% coarse64/fine endpoint discrepancies remain unchanged and have different denominators. The old full frozen weak remainder is also unchanged.

## Evidence and preservation

- Primary candidate: `scripts/annular_nonuniform_Gram_candidate_20260920.py`.
- Candidate controls: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-controls-attempt01/status.json`.
- Corrected saved-profile probe: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-parent-probes-attempt02/status.json`.
- Qualified signed pairings: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-precision-attempt01/status.json`.
- Stable local atom evaluation: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-atoms-attempt02/status.json`.
- Preserved literal-coordinate setup failure: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-parent-probes-attempt01/status.json`.
- Preserved insufficient binary64 atom attempt: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-atoms-attempt01/status.json`.
- Previous seal: `source-intake/navier-stokes/20260914/annular-trace-aware-Gram-final-integrity.json`.

Four completed runs contain257 scoped source/implementation checks, not257 independent physical tests. Both new failed attempts remain preserved. Work is private and post-checkpoint-work only, with one actual single-core BelowNormal worker, no subagents, no GitHub action and no change to the original live evolution.

