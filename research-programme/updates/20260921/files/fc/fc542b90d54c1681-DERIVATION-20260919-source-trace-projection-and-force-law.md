# Source-trace projection and an exact two-trace force law

Private continuation of `DERIVATION-20260919-exponential-force-defect-transport.md`. This checkpoint evaluates the proposed mass-projection commutator and then derives and tests the source mechanism behind its dominant contribution. No action, boundary condition, saved evolution, coupling, mode count or physical claim is changed. The existing 12.5718% integrated and 13.58% instantaneous MTS/continuum discrepancies remain unresolved. This does not establish the full GR limit.

## 1. Scope and notation

The actual saved spatial hierarchy has 257 versus 513 base vertices, with source-cell caps 2e-5 and 1e-5. Its elements are NOT nested. The final time is T=4e-5 in the existing normalized annular units. The paired trajectories also have unequal time steps, so their field difference is not an isolated spatial truncation error. All material labels enter the reconstructed live geometry; the reported functional is its central-label explicit Gram source-force contribution, not the complete physical radiation force.

At a prescribed reconstructed geometry, let

    w[u](x) = -(c(x)/J(x)) partial_x u(x),
    b_m[u]_i = sum_q omega_m,q phi_m,i(x_q) w[u](x_q),
    v_m[u] = M_m^-1 b_m[u].

Here c is source-map motion, J the map Jacobian, and omega the positive kinetic quadrature weight. v_m is the mass projection of the field-motion factor; it is NOT the actual time-evolved scalar velocity. The source scalar degree of freedom is absent in the existing action, giving a zero Dirichlet value at the reference source. This condition is retained, not newly imposed for this calculation.

For the off-space extension from the preceding checkpoint, let

    f_m[u] = D_m samples_m(u) - r_m jump(u),
    S_m[u] = -0.5 f_m[u]^T W_b,m f_m[u],
    a_m[u] = B_m^T W_m f_m[u],
    J_G,m*[u] = S_m[u] + a_m[u]^T v_m[u].

B_m is the existing lifted Gram operator. Off-space fields retain their original piecewise gradient and source jump. The original fine quadrature is unchanged, and is NOT asserted to integrate all off-space polynomial breakpoints exactly. These comparisons are evaluations, not newly evolved counterfactual states.

## 2. Projection commutator: exact identity and tested bounds

At the SAME coarse geometry and on the SAME original coarse field u_H, with I_h denoting nodal interpolation rather than exact space inclusion,

    rho_h = b_h[u_H] - M_h I_h v_H[u_H],
    d_h = v_h[u_H] - I_h v_H[u_H] = M_h^-1 rho_h.

The projection part of the fine-functional difference is

    P_h = a_h^T M_h^-1 rho_h = z_h^T rho_h,
    M_h z_h = a_h.

Positive-definite M_h gives two useful bounds:

    |P_h| <= sqrt(a_h^T M_h^-1 a_h) sqrt(rho_h^T M_h^-1 rho_h),
    |P_h| <= sum_i |z_h,i rho_h,i|.

The first is the dual mass-norm bound. The second retains spatial localization and signs before taking absolute values. Cholesky factorization checks positivity on the actual matrices. An independent small dense-matrix validator checks band assembly, both pairings, both bounds, zero controls, and positive/negative cases saturating Cauchy-Schwarz. These are implementation checks, not physical confirmations.

The full operator/mesh term from the previous checkpoint now has the exact ordered split

    O = P_h
        + (S_h[u_H]-S_H[u_H])
        + (a_h[u_H]^T I_h v_H[u_H] - a_H[u_H]^T v_H[u_H]).

The remaining terms are measured, not discarded.

| Total MTS operator term | Initial | Final |
|---|---:|---:|
| Projection commutator P_h | 3.700928e-10 | -1.638335e-8 |
| Shape-weight difference | 2.175791e-9 | 2.175753e-9 |
| Transferred projection/stencil difference | -9.407358e-9 | 2.530105e-8 |
| Sum O | -6.861474e-9 | 1.109345e-8 |

The final projection term is substantial and cancels part of the other terms. Its global mass bound is 1.193345e-7 (7.28 times its magnitude); the localized bound is 1.888992e-8 (1.15 times). A diagnostic source window of half-width 4e-5 contributes -1.675235e-8 to z^T rho; its complement contributes +3.69000e-10. This is a declared localization window, not a fitted physical length.

Source-straddling Gram rows give P_source=-1.675311e-8, with localized bound 1.837817e-8. Remaining rows contribute +3.697591e-10. Both are retained. Reference Gram contributions are zero by construction, but its nonzero mass commutator and the independent dense fixtures still exercise the projection algebra. The earlier nonzero reference physical-force tests are not replaced by this zero-Gram control.

## 3. Deriving the source response rather than merely naming the error

Let s_minus and s_plus be the one-sided values of w at the source. Since c=1 there,

    s_minus = -partial_x u(anchor-)/J_minus,
    s_plus  = -partial_x u(anchor+)/J_plus.

Let e_minus/e_plus be the piecewise constants equal to one on their respective source side and zero on the other. Let t_m,sigma contain their values at free nodes. It is a zero-source finite-element interpolant and therefore does NOT reproduce e_sigma next to the omitted source node.

Let C_m,sigma be the mass-load column of that missing source endpoint basis function, restricted to its own side. Partition of unity gives the exact discrete identity

    b_m[e_sigma] = M_m t_m,sigma + C_m,sigma,
    R_m,sigma = P_m e_sigma = t_m,sigma + M_m^-1 C_m,sigma.

The PLUS sign follows directly from adding back the omitted endpoint basis. Each R_m,sigma is checked against a direct projection of the piecewise constant with the same quadrature. No source node, degree of freedom or action term is added to the evolution.

Now subtract the actual one-sided values, not fitted amplitudes:

    w = s_minus e_minus + s_plus e_plus + w_reg,
    w_reg(anchor-) = w_reg(anchor+) = 0,
    v_m = R_m s + P_m w_reg.

The remainder has zero source-side limits; this does NOT assert that it is smooth at every ordinary coarse element boundary. Its full original quadrature load is retained. Therefore

    d_h = (R_h-I_h R_H)s + (P_h w_reg-I_h P_H w_reg).

This is an exact two-trace decomposition of the projection commutator, not a two-mode approximation of the full MTS dynamics.

For the final MTS coarse field the actual source values are approximately

    s = (-0.0100000033285, -0.0100000042700).

The total projection force splits into

    trace response   = -1.67531048e-8,
    regular remainder = +3.69754208e-10,
    total            = -1.63833506e-8.

The trace term exceeds the signed total magnitude because the remainder partly cancels it. On source-straddling rows alone, the trace term is -1.67531046e-8 and the computed regular remainder is -5.10e-15, with localized remainder bound 3.88e-14. The latter is a floating-point evaluation of an exact-arithmetic inequality, not an interval-arithmetic certificate. Thus the measured source-local projection contribution is accounted for by the two-sided trace response to the displayed accuracy; the remainder has not simply been set to zero.

The trace contribution itself includes both nodal transfer (-1.33852011e-8) and the difference of constrained mass responses (-3.36790372e-9). This avoids wrongly assigning it wholly to one mass solve.

## 4. A numerical failure preserved and corrected

The first source-trace implementation failed its constant-projection identity check: response error 3.18634e-12 exceeded the fixed 3e-13 tolerance. It constructed the missing endpoint shape at nominal Gaussian fractions, while the existing mass matrix evaluates shapes from the rounded physical quadrature coordinates. Tiny graded cells amplify that coordinate discrepancy.

Version 2 evaluates the missing shape at those SAME actual quadrature coordinates. It does not relax the tolerance or change the mass matrix. The largest repeated response error is then 2.34e-15. The failed source and evidence are preserved. No earlier sealed calculation or legacy helper is overwritten. This is a coordinate-consistency repair in the new diagnostic, not evidence that the 12.5718% physical mismatch vanished.

## 5. The stronger exact force law and the measured sensitive channel

For each mesh, field and reconstructed geometry define the TWO force-response coefficients

    k_m,sigma[u] = a_m[u]^T R_m,sigma,
    J_reg,m[u] = a_m[u]^T P_m w_reg[u].

Then the complete explicit Gram contribution satisfies

    J_G,m*[u] = S_m[u] + k_m[u]^T s_m[u] + J_reg,m[u].

These k values are diagnostics determined by the full field and mass projection, NOT newly introduced parent coupling constants. No one has reduced all scalar/geometry dynamics to two independent physical degrees of freedom.

For two evaluations (indexed 0 and 1), the exact midpoint product identity gives

    Delta J_G = Delta S + s_bar^T Delta k
                         + k_bar^T Delta s + Delta J_reg.

It is checked in two distinct comparisons: the same coarse field at the same geometry with different spatial operators; and the actual fine versus original off-space coarse field at the same FINE geometry. The second comparison equals the preceding field/state PLUS nonnested transfer term; it is not the earlier nodal-interpolation-only difference.

### Final MTS results

| Contribution | Operator/mesh comparison | Fixed-fine-geometry field comparison |
|---|---:|---:|
| s_bar times Delta k | +1.79539248e-8 | -2.83308619e-8 |
| k_bar times Delta s | 0 | -7.24102e-14 |
| Delta S | +2.17575304e-9 | -5.01404e-16 |
| Delta J_reg | -9.03622316e-9 | -1.35191014e-9 |
| Total | +1.10934547e-8 | -2.96828450e-8 |

About 95.4% of the signed fixed-geometry field difference is in the coefficient channel, while source-value variation contributes only about 0.000244%. These ratios describe this saved pair, not a general dominance theorem. Both source and remaining rows are included. The original field/state and operator terms still partly cancel, and the pre-existing initial offset remains documented in the previous checkpoint.

**Conclusion:** merely stabilizing or equating the source values s_minus/s_plus is not enough. The field-dependent force-response coefficients k must also be controlled. The observed sensitivity is now represented by explicit computable functionals, not just a general label such as "spatial error." It is still not a proof that the continuum theory fails or converges.

## 6. Concrete next derivation

At fixed common fine geometry, R and W are fixed. For the fine/off-space field comparison,

    Delta k_sigma = (B R_sigma)^T W Delta f.

Consequently the dominant coefficient channel has the exact row representation

    s_bar^T Delta k = sum_rows W_i (Delta f)_i (B R s_bar)_i,
    |s_bar^T Delta k| <= sum_rows |W_i (Delta f)_i (B R s_bar)_i|.

The next task is to measure and bound this force-weighted lifted-field defect, including its ordinary-gradient-jump/curvature contributions, and then transport/control it under the unchanged live dynamics. This bound is derived here; its numerical sharpness has NOT yet been tested in this checkpoint. Changing geometry requires the separately retained geometry term and cannot use a fixed-R formula without correction.

This is a more specific route than another blind time-halving: control Delta k, retain Delta s and the regular/shape terms, and keep the previously derived consistency conditions in view. It is not permission to delete the source boundary response, fit away the error or declare full local GR. No new long evolution is started in this stage.

## 7. Evidence and validation

Four successful runs complete 238 implementation checks: independent algebra 32, live projection commutator 62, corrected source-trace response 50, and two-trace force identity 94. One new failed execution remains preserved, bringing the inherited failure total from 41 to 42. Numerical identities are tested at their stated tolerances; successful checks are not independent experimental confirmations of MTS.

Source implementations:

- `scripts/annular_Gram_projection_commutator_20260919.py`
- `scripts/validate_annular_projection_commutator_20260919.py`
- `scripts/derive_annular_spatial_projection_commutator_20260919.py`
- `scripts/derive_annular_projection_source_trace_20260919.py` (failed original retained)
- `scripts/derive_annular_projection_source_trace_v2_20260919.py`
- `scripts/derive_annular_Gram_two_trace_force_law_20260919.py`

Evidence:

- `source-intake/navier-stokes/20260914/annular-projection-commutator-algebra-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-spatial-projection-commutator-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-projection-source-trace-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-projection-source-trace-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-Gram-two-trace-force-law-attempt01/status.json`

All rows remain non-claim, in normalized annular units. The final seal verifies inherited hashes, cited paths, compilation, tabular identities and protected-workbench modification times. The protected scan is not a pre-turn full hash baseline. No GitHub action, subagent, or protected-workbench edit is part of this checkpoint.
