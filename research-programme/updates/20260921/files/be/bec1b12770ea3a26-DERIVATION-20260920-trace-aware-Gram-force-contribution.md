# Source-trace contribution to the frozen Gram force difference

Private continuation of `DERIVATION-20260920-finer-test-geometry-and-Gram-force-split.md`.

Status: COMPLETE. The original-path forward and independent adjoint calculations agree. No action, coefficient, physical mode, terminal force covector or live evolution is changed. The trace-only explanation does not leave a small Gram remainder in this comparison.

## Question

The old same-geometry MTS Gram force contribution is -1.5185425785272700e-8 in the original code-unit normalization. Does the source derivative trace lost by coarse nodal evaluation explain it, or does a comparably large Gram difference remain after retaining that trace?

This is an actual force-path calculation, not an inference from the large unit-basis witness. It is still a decomposition of the frozen homogeneous operator contribution, not the complete moving-source force budget.

## Derived comparison

Retain the original stored native factors H_c,H_f, weights W_c,W_f and lifted hinge g_c. The original floating-point factor is H_c=O_c-g_c j_c. Its reproduction from the original action is checked bitwise at both resolutions for both branches, without replacing the assembled jump j_c.

On the exact common P2 space, E_c,E_f embed the native fields and R_c,R_f evaluate them. Set C=R_c E_f and J=R_f E_c. The canonical reference-coordinate derivative jumps satisfy

    ell E_c = j_c*,   ell E_f = j_f*,
    j_f* J = j_c*,    delta = j_f* - j_c* C != 0.

Here delta is the NEGATIVE of the previously saved test-defect row. It has ten nonzero entries. These are reference-coordinate traces, not unqualified physical-radius derivatives after a moving pullback.

Define the trace-aware extensions

    Hhat_c = H_c R_c - g_c (ell - j_c* R_c),
    Hhat_f = H_f R_f - g_f (ell - j_f* R_f).

Exact rational identities give

    Hhat_c E_c = H_c,
    Hhat_f E_f = H_f,
    Hhat_f E_c = H_f J,
    Hhat_c E_f = H_c C - g_c delta.

Thus each original native action is unchanged. This is an off-native comparison convention: native agreement alone does not uniquely determine an extension, and this construction is not a derivation of a new continuum action.

Let

    H_counter = H_f^T W_f|coarse H_f J,
    Q_old = H_counter - C^T K_Gram,c,
    p_c = g_c^T W_c H_c.

The trace-aware mixed coarse Gram form is C^T K_Gram,c - delta^T p_c. Therefore

    Q_trace = Q_old + delta^T p_c,
    D_Gram,old = -Q_old = delta^T p_c - Q_trace.

The two operators evaluated here are consequently

| Channel | P | Q in D=P A_c-Q |
|---|---|---|
| Lost test trace | 0 | -delta^T p_c |
| Trace-aware Gram remainder | 0 | Q_old+delta^T p_c |

The rank-one formula, its sign, and the direct weighted-factor contractions are checked independently on a full-support fixture and the source basis555 witness. Their sum reconstructs the old matrix before any propagation.

## Force calculation and controls

The original coarse trajectory obeys u_c''=-A_c u_c. For each channel,

    r_j'' + A_f r_j = M_f^-1 D_j u_c,
    r_j(0)=r_j'(0)=0,
    F_j = c^T(r_j(T),r_j'(T)),
    T = the original stored binary64 value of 4e-5.

The independent adjoint evaluates the equivalent integral of z_f^T D_j u_c, with z_f=M_f^-1 lambda_v and the original terminal force covector c. For the rank-one term this integrand is (delta z_f)(p_c u_c); no claim about its size follows from the static witness alone.

MTS is evaluated at 32-digit/order48 and 48-digit/order64 arithmetic, including the independent adjoint at the latter setting. Both use the identical saved matrices. The old moment-order32 and moment-order64 Gram matrices are exactly equal, checked explicitly, so repeating a moment quadrature for this channel would not supply an additional refinement test.

The reference branch has identically zero Gram weights, so both new operators are exactly zero. Zero initial response plus zero forcing implies zero response by uniqueness of the original finite-dimensional linear ODE. This baseline is evaluated analytically rather than adding artificial cancelling channels just to run a numerical solver. The previously qualified independent dense integrator controls remain in force.

The original literal force gates are retained: 3.002e-16 for reference and 3.06397869398973548091222937147781805346218151514e-16 for MTS. High-precision propagation conditions on the saved binary64 parent inputs; it does not upgrade their physical accuracy.

## Results

Signed contributions in the original frozen force normalization:

| Contribution | Reference | MTS |
|---|---:|---:|
| Lost test trace | 0 | +5.7679173528885195e-8 |
| Trace-aware Gram remainder | 0 | -7.2864599314157895e-8 |
| Sum / original Gram channel | 0 | -1.5185425785272700e-8 |

The lost-trace term has the OPPOSITE sign to the old Gram difference. The trace-aware remainder is about4.798 times the old channel's magnitude, not a small leftover. The split exposes cancellation, rather than removing the discrepancy. These ratios concern this specified comparison, not unique percentages of physical error.

Regrouping the lost trace with the prior mass/gradient finer-test contribution gives +4.2588333729614010e-8 for MTS. Together with -7.2864599314157895e-8 of trace-aware Gram remainder and -5.1874926684696914e-17 of unchanged closure/geometry channels, the full weak sum remains -3.0276265636418811e-8. The reference weak sum remains +1.3513359139087759e-9. Moving terms between headings does not improve either result.

The largest individual forward/adjoint difference is3.0613e-46, conditional on the fixed saved inputs. The largest arithmetic/time-order refinement change is3.6797e-30. Both sums reproduce the old Gram integral within the unchanged literal threshold; the higher-precision forward sum differs by1.3941e-46. The original fine-adjoint terminal is identical at the recorded48-digit precision. These are numerical implementation controls, not physical accuracy at those scales.

The matrix run contains57 source/algebra checks and the force run24 checks, all passed. The independent native factor pairings include the sign of the rank-one term. The reference zero is analytic, not an artificial numerical surrogate. The actual propagation took770.83seconds (about12.8minutes), using one single-core BelowNormal worker. No failed execution was added by these calculations.

## Interpretation and next calculation

This closes the targeted question: retaining the lost source trace alone does NOT make this frozen same-geometry Gram residual small. It does not disprove MTS, prove a physical source defect, or uniquely identify the remaining discrepancy as a bulk-stencil error. Off-native extensions remain comparison conventions. The restored trace is mathematically real, but treating it as a numerical repair would have been wrong.

Do not repeat trace subtraction, retune a Gram multiplier, or launch another blind source-cell halving. Earlier work already found that source-only refinement can leave bulk errors and that the whole Gram stencil, not merely the tiny source cell, must resolve the fronts in the prescribed fixture. That evidence is in `DERIVATION-20260919-localized-Gram-reaction-and-force-mesh-law.md` and `DERIVATION-20260919-joint-source-refinement-and-inertial-force-scale.md`. The fixture's front speeds must not be silently assigned to the evolving parent.

The next substantive target is an ACTION-CONSISTENT source/front-resolved spatial construction, starting with a derivation and a short frozen pilot rather than another long coupled run. It must recover the original uniform-grid rule and its normalization, retain the compensated source trace, and include the full source/metric variation. It is not yet constructed or qualified; a nonuniform rule cannot simply be substituted and called the same theory.

For any candidate retaining the positive form S_G=(H u)^T W(H u)/2 and H=O-g j, its necessary first variation is

    variation S_G = (H u)^T W [H variation u + (variation H)u]
                    + (H u)^T (variation W)(H u)/2,
    variation H = variation O - (variation g)j - g(variation j).

If g=O h for the hinge samples h, variation g=(variation O)h+O(variation h). Dependences vanish only when the corresponding reference objects are genuinely held fixed. Ignoring geometry-dependent weights, stencil coefficients or trace rows would change the source force. This algebra is a necessary contract, not a completed continuum identification or a measured force improvement.

Before a live run, require exact uniform-grid recovery, polynomial/compensated-hinge controls, positivity, independent variations, and a source/front resolution criterion tied to the actual parent paths. Then compare frozen force convergence in BOTH reference and MTS, with all physical coefficients held fixed and without removing modes. If the candidate fails those gates, preserve the failure rather than promoting it to a repair. The initial-time layer and the full moving-source budget remain separate obligations.

The original 12.5718% impulse, 13.5770% fine/continuum endpoint and 32.5535% coarse64/fine endpoint discrepancies remain unchanged. These have different denominators and cannot be merged into one error percentage. No local-GR/full-GR limit, continuum certificate, observational success or physical force repair follows from this accounting.

## Evidence

- Original construction and preceding five-way force split: `DERIVATION-20260920-finer-test-geometry-and-Gram-force-split.md`.
- Source reconstruction, exact extension algebra, and independent factor pairings: `scripts/derive_annular_trace_aware_Gram_matrices_20260920.py`.
- Matrix/source evidence: `source-intake/navier-stokes/20260914/annular-trace-aware-Gram-matrices-attempt01/status.json`.
- Original-path forward/adjoint runner: `scripts/derive_annular_trace_aware_Gram_force_20260920.py`.
- Force evidence: `source-intake/navier-stokes/20260914/annular-trace-aware-Gram-force-attempt01/status.json`.
- Independent existing channel-integrator controls: `source-intake/navier-stokes/20260914/annular-weak-channel-controls-attempt01/status.json`.
- Prior integrity chain: `source-intake/navier-stokes/20260914/annular-weak-residual-force-final-integrity.json`.

Private and post-checkpoint-work only. One actual single-core BelowNormal worker; no subagents, GitHub action, new live evolution, sibling edits, or deleted historical evidence.
