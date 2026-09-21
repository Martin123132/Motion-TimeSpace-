# Nested quadratic action and crossing-force refinement

Private continuation of `DERIVATION-20260915-source-fitted-crossing-and-fine-phase-robustness.md`.
Turn start: 2026-09-15T21:04:59Z. Four-hour safe check-in: 2026-09-16T01:04:59Z.

## The target is numerical force accuracy, not an invented coupling

The preceding source-fitted flat-background test crossed old grid-node locations without an energy projection, but its 1025-node reference/MTS forces missed the unchanged 2e-7 absolute gate despite .0687%/.0903% relative errors. The present step compares an unchanged 2049-node linear refinement and a derived nested quadratic representation. It does not alter the physical initial profile, source mass, duration, reference solution or force gates.

All results are conditional spherical fixed-background controls in the benchmark's internal units. This is not a full GR limit, a derived value of Newton's constant, a parent-uniqueness theorem, an observational prediction, or an evolved live-quadratic gravity solution.

## 1. Enrich the old action instead of discarding it

Keep every original reference vertex and the fixed zero-trace source anchor. On each reference interval add one midpoint degree of freedom, with local coordinate xi in[0,1] and basis

    B_left=(1-xi)(1-2xi), B_mid=4xi(1-xi), B_right=xi(2xi-1).

These are the standard quadratic nodal functions, independently checked symbolically; [DefElement's degree-two interval definition](https://defelement.org/elements/examples/interval-lagrange-gll-2.html) provides the basis convention. The source-anchor value is still eliminated as exactly zero. With n original vertices this construction has2n scalar degrees of freedom; comparisons must not confuse original vertex counts with total unknown counts.

The source-fitted physical map, Jacobian J and mesh factor k are unchanged. For phi_tilde=Bq,

    H=(B_r q)/J, W=B qdot-k V H,
    L_wave=integral dr [A J W^2-(C/J)(B_r q)^2]/2,
    L_source=-S sqrt(N_b^2-V^2/U_b^2).

The consistent mass matrix is now pentadiagonal. The global field-carried source momentum remains

    zeta=-integral dr A k (B_r q) W,
    P_b=p_s+zeta.

Its time derivative is retained. The complete positive field/source velocity Hessian is inverted by a banded solve and scalar Schur complement, not by replacing P_b with mechanical momentum.

## 2. Preserve the Gram action, including the actual source gradient jump

Let P_v select the original vertex values from the quadratic unknowns. Keep the original G and sampling rows with their original weights and reference spacing h. Let rho_i=(r_i-b_star)_+ at those vertices. The lifted factor is

    F_2=G P_v q-(G rho) j_2 q,

where j_2 q is the **actual quadratic one-sided reference derivative jump** at the source, not a chord approximation. If L,D are the two source-adjacent reference interval lengths, and q_l,q_r and m_l,m_r their endpoint/midpoint values,

    j_2 q = (4m_l-q_l)/L + (4m_r-q_r)/D.

The Gram potential remains

    V_Gram=sum_alpha sampling(C(R_i)/J_i)_alpha (F_2)_alpha^2/(2h).

No fitted coefficient or extra fundamental field is added. Midpoint degrees of freedom improve the representation of the existing field. Metric sampling remains at the original vertices; added midpoints do not silently create new Gram sampling atoms.

### Exact preservation theorem for the old finite action

Let E insert the linear midpoint averages into the quadratic nodal vector, including the zero source value. E is independent of time, b and the metric because both bases live on the same fixed reference partition. Then

    B_2 E=B_1, (B_2)_r E=(B_1)_r, P_v E=I, j_2 E=j_1,
    F_2 E=F_1,
    L_2(Eq,E qdot,b,V)=L_1(q,qdot,b,V).

Consequently the old field momenta and covectors are the E-transpose pullbacks of the new ones, and the full source momentum and source covector also agree on the embedded subspace. This is stronger than agreement only at a static source or in the continuum limit. It does not say unconstrained quadratic evolution is identical to linear evolution; enrichment adds admissible field shapes.

This gives an explicit, nested numerical extension, not a proof of unique parent-theory ownership of all finite terms. The old calculations remain intact and directly recoverable.

## 3. Initial error law derived from the original profile

For a smooth cubic Taylor term on an interval of length h, quadratic interpolation has leading derivative error

    e_H=(h^2 f'''/6) d_xi[xi(xi-1/2)(xi-1)],
    integral_0^1 {d_xi[xi(xi-1/2)(xi-1)]/6}^2 dxi=1/720.

With the original initial W=-V0 f', the moving-grid interpolation also contributes delta W=-k V0 delta H+O(h^3). Therefore for the flat-background energy norm,

    E_initial=h^2 K+o(h^2),
    K^2=integral dR R^2(1+k^2 V0^2)(f''')^2
        /[720 integral dR R^2(1+V0^2)(f')^2].

The compact-quintic profile is piecewise smooth with continuous first two derivatives; the taper breakpoints do not justify assuming globally smooth higher derivatives. The check integrates each piece separately. The source-adjacent preparation is affine, so the cut interval introduces no initial interpolation error. This law predicts **initial** spatial accuracy only. It cannot certify evolving force accuracy, especially with the previously documented second trace incompatibility.

## 4. Independent force decomposition for quadratic elements

The earlier element-by-element source variation still applies, but now H_R is nonzero inside an element. Define dot H_refchart as the time derivative of H at fixed reference coordinate, and w=kV. Then

    dot H_refchart=(B_r qdot)/J-H J_t/J,
    H_R=(B_rr q)/J^2,
    W_t|R=B qddot-k bddot H-2w dot H_refchart+w^2 H_R,
    E_smooth=C_R H+C H_R-A_t W-A W_t|R.

At internal element vertices, continuous pulled nodal rate u implies

    Q_±=A u^2/2+(C-A w^2)H_±^2/2.

Thus the exact finite-action source force is the physical-source pressure plus interior vertex shape pressures, minus the smooth bulk-residual projection, plus the Gram shape force. Midpoints are not element interfaces and must not be inserted into that boundary sum. The precision runner checks this decomposition independently against L_b-dot zeta on evolving states. It also reports the force at all nine saved times, distinguishing the inherited **final-time** gate from a stricter sampled-trajectory test.

## 5. Derive the remaining force-error budget

Write c_h=b_h^2(1-V_h^2)/2 and let L_h,R_h be the two source gradient traces. A star denotes the independently computed continuum-reference state at its own source position. The measured finite-force identity gives the exact algebraic split

    F_h-F_star = (c_h-c_star)(L_star^2-R_star^2)
               + c_h (L_h-L_star)(L_h+L_star)
               - c_h (R_h-R_star)(R_h+R_star)
               + mesh_pressure - bulk_projection + Gram_shape_force.

Taking absolute values term by term gives a conservative triangle envelope. Its evaluations are not a certified bound on the unknown exact continuum solution: the star here is the degree-512 numerical reference. The identity and the envelope are checked at all nine saved times in all 14 new linear/quadratic cases, with identity residual at most 7.60e-15.

There is a precise reason not to equate good bulk waveform accuracy with good pressure-force accuracy. For a degree-one derivative polynomial p on a quadratic element of physical length ell,

    |p(endpoint)|^2 <= (4/ell) integral_element |p|^2 dR.

The constant 4 is sharp: for the unit-interval Gram matrix of {1,s}, endpoint evaluation has squared dual norm 4. With an R^2-weighted norm, the bound is 2/(R_min sqrt(ell)) times that norm. It applies to polynomial differences; comparing to a general exact gradient additionally requires a projection/trace remainder. It is not a uniform trace bound inferred from bulk energy alone.

A constructive counterexample makes the limitation explicit. On the right of the source take delta_phi=epsilon*eta((R-b)/epsilon), eta(s)=s(1-s)^2 on [0,1], zero outside. The source value stays zero; the one-sided gradient trace remains 1 while its squared unweighted gradient norm is 2*epsilon/15 and its weighted norm also tends to zero. Choosing delta_W=-V*delta_H preserves first moving-trace compatibility. This is a kinematically admissible counterexample to a norm implication, NOT a new on-shell solution or a claim that the tested trajectory develops such a layer.

The actual finest quadratic MTS final-force error, against degree 512, splits as follows:

| Contribution | Signed force error |
| --- | ---: |
| Source position/velocity coefficient | +4.68e-13 |
| Left gradient trace | +1.03859389e-6 |
| Right gradient trace | -8.41478004e-7 |
| Interior mesh pressure minus bulk projection | +4.10550781e-7 |
| Direct Gram shape variation | -6.21448e-12 |
| Total | +6.07660918e-7 |

Thus the net mesh/bulk term is about 68% of this signed final discrepancy; the net trace term is the other substantial part. The direct Gram shape derivative is tiny here, but that does NOT show the Gram action has no indirect effect on the evolved field. Dropping the mesh term or substituting trace pressure would change the actual action-derived force and manufacture a favourable number.

At t=0 both finest quadratic branches already have about -2.2503e-7 canonical force error, almost entirely mesh/bulk, despite matching source gradient traces to roughly 6e-14. This establishes a shared finite-action preparation/projection defect in this control, not an MTS-only missing physical coupling. The previously derived second trace incompatibility remains relevant, but has not been proved to explain the complete later-time error.

## 6. Results and decision

The quadratic nesting/action suite passes 47 checks. The interpolation-law suite passes 3: K=7.525306913756658 and the observed last initial-error order is 2.00654. The leading estimate reaches 0.5% initial error near 63 base vertices; that is not a prediction for the evolved force. Crossing implementation suites pass 26 coarse plus 14 fine checks. Physical-accuracy flags are separate.

Maximum field errors below use independently recomputed order-24 comparison quadrature. The original trajectory files, order-6 comparisons and their flags are preserved. Force errors use the unchanged degree-512 reference and require BOTH absolute error <2e-7 and relative error <2%.

| Quadratic base vertices | Scalar DOFs | Reference max field % | MTS max field % | Reference final force abs. | MTS final force abs. | Final force gates ref/MTS |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 33 | 66 | 2.13159 | 12.5545 | 1.72544e-5 | 1.35730e-3 | fail/fail |
| 65 | 130 | 0.512784 | 3.07134 | 3.40401e-6 | 5.28034e-4 | fail/fail |
| 129 | 258 | 0.143533 | 0.770599 | 1.60685e-6 | 4.49107e-5 | fail/fail |
| 257 | 514 | 0.0365440 | 0.194278 | 8.48963e-7 | 3.09945e-6 | fail/fail |
| 513 | 1026 | 0.00950213 | 0.0493863 | 3.65636e-7 | 1.89635e-6 | fail/fail |
| 1025 | 2050 | 0.00247934 | 0.0127030 | 1.04528e-7 | 6.07661e-7 | pass/fail |

At comparable scalar counts, the unchanged linear 2049 comparison gives maximum field error 0.243752% for both branches. Its final-force errors are 2.94076e-7 (reference: fail) and 1.60066e-7 (MTS: pass). The quadratic MTS field error is about 19 times smaller at essentially the same scalar DOF count, but its final force is not more accurate than the linear MTS force. We do not combine a quadratic reference pass with a linear MTS pass and call that a paired success.

Both finest quadratic source/velocity/clock comparisons pass: maxima <=4.984e-11, <=2.092e-8 and <=2.876e-12 respectively. Fifteen original vertices are crossed, J remains >=0.96969, and the finest MTS energy drift is 1.08e-15. Those conservation/trajectory results do not replace the failed force gate.

### Independent checks and the retained diagnostic failure

- A new degree-768 characteristic oracle passes 12 checks. The maximum 512/768 force difference over nine times is 1.71603e-8; the maximum energy-norm field-vector difference is 9.84392e-6. Final force is -0.0017138947185949137. These are observed resolution differences, not a rigorous error certificate.
- The first precision attempt correctly fails: reference33 order-6 versus order-10 final field norm differs by 3.08861e-8, above the unchanged 2e-8 check. Its script, executed snapshot and failed status remain immutable.
- A NEW v2 precision attempt uses order 16 versus 24 at all nine times. Maximum disagreement is 3.23539e-9; original order-6 versus recomputed order-24 disagreement reaches 1.30930e-6 at one coarse saved time. No physical field-pass classification changes. This correction increases quadrature, not the acceptance tolerance.
- All 49 v2 precision checks pass. Independent shape-force identities agree within 7.60e-15. Halving the time step and removing interval restarts at base129 changes full states by at most 4.17e-11. This temporal control was not rerun at every fine grid.
- Both reported final-force passes survive comparison to 384, 512 and 768: quadratic reference1025 and linear MTS2049. The latter is very close to the 384 boundary (1.97868e-7 versus 2e-7), so it is not a comfortable certified-continuum margin.
- No new case passes the stricter absolute-force test at ALL nine saved times. Quadratic reference1025 reaches 2.25035e-7 initially; quadratic MTS1025 reaches 6.07661e-7 finally. Linear MTS2049 reaches 2.79711e-7 initially. Nine samples would still not establish a uniform-in-time theorem even if they all passed.
- Finest quadratic accumulated mechanical-impulse errors are <=4.943e-11 (reference) and <=6.308e-10 (MTS). These follow from the exact mechanical momentum derivative, not sparse nine-point force quadrature. They do not establish pointwise force accuracy.

**Decision:** the nested action and bulk-field improvement are established for this controlled problem; a robust paired moving-source force pass is NOT established. The new force budget identifies the next mathematical target quantitatively rather than merely listing a missing ingredient. There are 190 successful current checks across eight suites, plus the explicitly retained failed precision attempt; successful implementation checks must not be called 190 passed physics tests.

## Scope and next step

The exact nesting identity, canonical momentum, sharp polynomial endpoint bound and shape-force/error identities are mathematical results conditional on the stated action and spaces. Numerical refinement and pass flags are measured controls, not blanket proofs. Conservation alone never replaces field or force accuracy tests.

Next: derive an interface-consistent spatial projection/source reaction or an on-shell residual estimate that controls BOTH the mesh/bulk term and the gradient traces, beginning with the shared t=0 residual. Keep the original physical profile and action-derived full source force; any revised finite projection must be derived from them, not an imposed force-zero correction or a new physical preparation. The measured budget is the comparison target for that construction. Once a paired trajectory force control is qualified, implement the already-derived continuously averaged live density/current and radial/canonical solve. The live-gravity bridge remains separate from the flat crossing benchmark and from the still-unproved full parent GR limit.

## Files and preservation

- Prior seal: `source-intake/navier-stokes/20260914/annular-source-fitted-crossing-final-integrity.json`.
- Linear refinement: `scripts/refine_annular_source_fitted_force_20260915.py`.
- Quadratic action: `scripts/annular_quadratic_source_fitted_action_20260915.py`.
- Action/nesting qualification: `scripts/verify_annular_quadratic_source_fitted_action_20260915.py`.
- Crossing runner: `scripts/run_annular_quadratic_crossing_20260915.py`.
- Initial error derivation: `scripts/derive_annular_quadratic_initial_error_20260915.py`.
- Independent precision/decomposition: `scripts/verify_annular_quadratic_crossing_precision_20260915.py`.
- Corrected independent precision: `scripts/verify_annular_quadratic_crossing_precision_20260915_v2.py`.
- Independent reference refinement: `scripts/verify_annular_crossing_oracle768_20260915.py`.
- Force-error identity, endpoint bound and counterexample: `scripts/derive_annular_crossing_force_error_budget_20260915.py`.
- Qualified precision evidence: `source-intake/navier-stokes/20260914/annular-quadratic-crossing-precision-attempt02/status.json`.
- Retained failed diagnostic: `source-intake/navier-stokes/20260914/annular-quadratic-crossing-precision-attempt01/status.json`.
- Force-budget evidence: `source-intake/navier-stokes/20260914/annular-crossing-force-error-budget-attempt01/status.json`.
- Final integrity record: `source-intake/navier-stokes/20260914/annular-quadratic-crossing-final-integrity.json`.

All numerical workers are finished before 23:00 UTC, within the four-hour window. Integrity is recorded separately in the linked seal. Only post-checkpoint-work is changed. No GitHub action, no subagents, no edits to formalization-workbench and no replacement of executed or sealed sources. At most two own BelowNormal one-core workers were used; accepted interval states are preserved. Five inherited failed attempts plus the new diagnostic failure and all false physical-accuracy flags remain in the evidence.
