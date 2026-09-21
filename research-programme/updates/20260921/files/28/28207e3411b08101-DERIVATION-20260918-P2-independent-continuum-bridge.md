# P2 against the independent live spherical continuum

Private completed numerical/derivation checkpoint, 2026-09-18. This follows the sealed radial-conditioning/error-budget checkpoint and does not alter its equations or evidence. All six new trajectories and all physical comparisons finish; the source-force accuracy target remains FAILED, separately from successful execution and waveform checks.

## Plain-language result

- On the finest tested mesh, the sampled physical waveform error is0.4558% for the reference branch and0.4888% for MTS. Both meet the unchanged0.5% waveform target over the short interval.
- Neither meets the source-force accuracy target. Maximum errors are5.8136e-7 reference and4.4756e-7 MTS, or10.7635% and8.2863% of the sampled reference peak force. These are NOT uniform relative errors at each instant and are not observational exclusions.
- We derive a moving-element virtual-work identity that explains the finite force discrepancy. It passes both evolved-state and off-shell checks without correcting the force or deleting the MTS term.
- This is evidence of numerical approach to the stated spherical continuum branch, not a full GR limit, a unique parent-action proof, or a physical victory of MTS over GR.
- Next use saved states to control the finest force's material/quadrature uncertainty, then attack its signed virtual-work residual. Do not jump straight to another expensive long trajectory or impose the desired pressure force.

## Actual question

Does the source-fitted quadratic finite action, with and without its original Gram contribution, approach the independently discretized live spherical scalar/source system in physical waveforms and in the force delivered to the material source? Conservation inside one implementation is not sufficient to answer this.

The comparison keeps the finite source width0.02, central mass0.7, material mass0.03, coupling0.1, initial source position6.03, initial source velocity0.03, initial analytic wave, outer lapse normalization and normalized interval0..0.004 fixed. Polynomial material-label quadrature is a numerical representation of the same distributed source, not a new fit. The two representations sample the same analytic preparation; their discrete initial fields and momenta are not asserted identical. Initial representation error is INCLUDED in the reported waveform error.

## Force: derive the quantity before comparing it

Write a layer action as L=L_wave(q,qdot,b,bdot;g)+L_material(b,bdot;g), with the constrained live metric supplied by the same branch. Define zeta=partial L_wave/partial bdot and p_material=partial L_material/partial bdot. The source Euler equation is

    d/dt(p_material+zeta)=partial_b L_material+partial_b L_wave.

Consequently the wave force delivered to the material source is

    F_wave=partial_b L_wave-dzeta/dt,
    dp_material/dt=partial_b L_material+F_wave.

This is an exact splitting of this finite action's source equation, not an added correction chosen to match GR. The moving-coordinate wave inertia, metric time dependence and Gram terms remain in the calculation. A raw canonical source covector, or the raw wave covector alone, is not the same observable. Neither is a coordinate force a proper-time acceleration.

For the specified minimally coupled spherical continuum with zero source trace on each side, the previously derived moving-boundary pressure law is

    F_wave,continuum=R^2 N U [1-V^2/(N^2 U^2)](H_minus^2-H_plus^2)/2,

where U^2=1-2m/R, N is the lapse, V=dR/dt and H is the one-sided physical radial scalar gradient. Its derivation keeps the temporal boundary flux as well as the moving-domain term. This continuum law is a reference for the proposed limit, not an identity silently imposed on the finite MTS action.

The new comparison obtains the finite F_wave from the evolved canonical state and its vector-field tangent. It checks the material momentum balance and repeats the tangent extraction with half the finite-difference interval at the endpoints. It does not replace the finite force with the continuum formula. An existing independently derived proper-acceleration identity checks the continuum implementation; it is not a new P2 acceleration comparison.

## Independent representation and physical norm

The reference is the existing live characteristic solver, using two radial domains per material label and its own radial metric construction. It does not call the P2 force, mass matrix or finite Gram operator. Shared parameters and basic polynomial utilities are explicit; this is an independent discretization, not an independent research group's validation.

Use characteristic degrees384 and512 at material degree8, radial degree18, radial spacing0.025 and label quadrature12. Both are evolved anew to the exact five saved times0,0.001,0.002,0.003,0.004. The degree384 initial state is hash-read from an earlier run whose FINAL accuracy test failed; that failure is preserved, and that earlier run is not called qualified. The newly evolved384/512 comparison must pass its own controls before it can support the new numerical comparison.

P2 starts with the already sealed base-count17 trajectories and matched base-count33 runs, material degree14, radial degree18, action quadrature32 and label quadrature20. Both reference and MTS retain the same physical initialization. Every finite MTS Gram term remains enabled. Further refinement, if required, uses separate saved runs rather than replacing an unsuccessful result.

For each sampled material label -0.25,0,0.25, evaluate both solutions at the SAME physical radius. Integrate

    E_difference^2 = integral dR [R^2/(N_ref U_ref)(T_P2-T_ref)^2
                                  +R^2 N_ref U_ref(H_P2-H_ref)^2],

and divide by the corresponding reference norm. T=partial_t phi at fixed physical radius, not a moving-mesh nodal velocity. The reported waveform is this temporal/radial derivative pair. Quadrature splits every P2 element boundary and both continuum domains, including the actual interval between displaced source positions; aligning away a source gap is forbidden. The maximum across these three labels is a sampled norm, not an integral over every label or a supremum theorem. Quadrature order4 is checked against order8 at the endpoint.

Source positions, velocities, instantaneous proper-clock rates, radial mass and lapse are also compared. Accumulated proper clock and full proper acceleration are not claimed. Central-label reduced forces are sampled at the five times, not asserted to bound the continuous-time peak.

## Predeclared gates and honesty about uncertainty

Independent oracle refinement gates: physical relative waveform norm0.001, aligned field difference2e-6, source gap1e-8, reduced-force absolute difference2e-7 and peak-normalized relative difference0.02. Its current and acceleration identities retain2e-8 and2e-7 controls respectively.

New short-interval comparison targets, identical for both P2 branches: waveform relative error0.005, reduced-force absolute error2e-7 AND peak-normalized error0.005, source-position error5e-7, velocity error2e-5, instantaneous clock-rate error2e-7. Normalize force errors by the peak reference magnitude over all five samples, not by its zero initial value. Finite-difference force extraction control2e-9. These are short-interval numerical targets; they do not replace the old failed full-horizon force gates.

The prior count17 material/time/readout differences remain measurements, not rigorous global error bars and not automatically transferable to finer spatial counts or to the newly reduced force. Oracle384-to512 differences likewise are refinement estimates, not a certified infinite-resolution bound. Passing a diagnostic execution is not passing its scientific accuracy targets: each target has an explicit boolean, and failed targets remain in the result.

## Results

### Separating the remaining force error

The independently sampled force can be decomposed without fitting or changing it. Define

    A_h=R_h^2 N_h U_h [1-V_h^2/(N_h^2 U_h^2)]/2,
    P_h=A_h(H_h,minus^2-H_h,plus^2),
    r_h=F_h-P_h.

Then the exact signed identity is

    F_h-F_ref = r_h + (P_h-F_ref).

The first term is the finite-action traction defect relative to its own local boundary traces. The second is the difference in trace pressure and geometry between the finite and continuum solutions. We do NOT set r_h to zero or replace the actual force with P_h. That would impose the answer rather than test it.

For either side s, a useful sufficient error estimate follows from factoring the difference of squares:

    |F_h-F_ref| <= |r_h| + |A_h-A_ref| sum_s |H_ref,s|^2
                   + |A_h| sum_s (|H_h,s|+|H_ref,s|)|H_h,s-H_ref,s|.

This is a bound at corresponding source traces, conditional on controlling those terms. A small bulk energy error alone does not supply a bound on one-sided gradient traces, and it does not control r_h. This explains why the waveform and source-force gates must remain separate. The new diagnostic evaluates exact one-sided P2 endpoint derivatives, not finite differences straddling the moving source, and keeps the signed terms so cancellation is visible. It identifies which term needs a derivation/control next; it is not itself a convergence theorem.

### A derived expression for the finite-action traction defect

The residual r_h above can be evaluated from an independent broken-domain integration-by-parts identity; it need not remain an unexplained subtraction. Let C=R^2 N U, K=R^4/C, W=partial_t phi, H=partial_R phi, and c=partial_b R at fixed reference mesh coordinate. On each open P2 element define

    E=partial_t(K W)-partial_R(C H).

An internal mesh edge moves with v_j=c_j V. The scalar is continuous there, and W_left+v_j H_left=W_right+v_j H_right is its common moving-node time derivative. Varying b at fixed nodal scalar coordinates gives delta phi=-c H delta b. Integration by parts on each moving spacetime element gives the endpoint expression

    L+(C H+v K W)H
      = K(W+vH)^2/2+(C-Kv^2)H^2/2.

The first term cancels between two adjoining elements. The fixed outer endpoints have c=0. At the moving zero-trace source, c=1 and the remaining jump gives precisely P_h. Therefore, for the piecewise integral action,

    r_h = sum_elements integral c H E dR
          + sum_internal_edges_except_source c_j(C_j-K_j v_j^2)
                      (H_left,j^2-H_right,j^2)/2
          + F_Gram,shape.

For the existing fixed-reference lifted Gram action, let f be its retained factor vector, h_g its original spacing, w_j=(sampling^T f^2)_j/(2h_g), J_j=partial_reference R and s_j=partial_b J_j. Direct source variation, without varying the reference factor coefficients, gives

    F_Gram,shape = -sum_j w_j [C_R(R_j)c_j/J_j-C(R_j)s_j/J_j^2].

There is no Gram velocity momentum in this action; the Gram force nevertheless enters the ACTUAL evolved acceleration used in E. Removing it from E as well as from the explicit shape force would be a different model. The live metric and its time tangent here are those of the existing constrained branch: this identity does not derive an unrestricted covariant parent action.

The continuous piecewise-integral identity has been derived analytically. Numerical quadrature and the differentiated live solution introduce measured implementation errors. Eight checks (initial/final states, both branches, counts17/33) reproduce r_h to at most2.74e-11; changing integration order32 to48 changes the derived residual by less than5.2e-17. The symbolic moving-endpoint identity also passes. No force was corrected, projected or replaced.

Four additional evolved-state cases at count65 close the identity to2.101e-10, still below its2e-9 gate. This larger residual is retained, not rounded down to the count17/33 figure. Changing the quadrature in the independent integral does not remove it; the existing finite action quadrature and numerical live tangent remain distinct implementation approximations. Across all comparisons, halving the tangent finite-difference interval changes the extracted force by less than1.98e-15. That is an extraction control, NOT a time-refinement test of the evolved trajectory.

A separate OFF-SHELL test uses arbitrary accelerations, a deformed moving mesh and an analytically time-dependent prescribed metric, without solving either the scalar or metric equations. Four reference/MTS count17/33 cases close the same identity to2.82e-17. Deliberately omitting moving internal-edge terms, omitting the MTS Gram shape term, or substituting the raw wave covector all produces detectable failures. These14 controls show that the identity is not obtained merely by substituting the equations whose residual it is meant to diagnose. The manufactured metric is a test fixture, not an MTS solution or an additional physical assumption.

At the count33 final MTS state, the terms are:

| Term | Signed value, normalized units |
| --- | ---: |
| Bulk Euler virtual work | 1.7515003e-5 |
| Internal moving-edge work | 7.8928868e-6 |
| Explicit Gram shape force | -6.6968955e-6 |
| Sum, derived traction defect | 1.8710994e-5 |
| Directly measured traction defect | 1.8710967e-5 |
| Remaining trace/geometry difference | 4.0971798e-6 |

Thus the discrepancy is predominantly the finite-action traction defect here, not an inaccurate continuum benchmark or a raw-covector/pressure comparison mistake. The analogous defect is also nonzero in the reference branch. A triangle-inequality estimate using absolute local contributions is very loose (about0.00395 for this MTS state). A useful convergence argument must control the COMBINED signed weak residual and moving-edge/Gram terms, rather than asserting every local residual vanishes or treating cancellations as forbidden. That bound is not yet proved.

### Completed numerical results

The independent continuum384/512 comparison passes: maximum sampled physical relative waveform difference9.1373e-6, central force difference6.1119e-10. Both new oracle trajectories complete to0.004. The count17 and33 P2 trajectories and comparisons also complete, but the scientific accuracy gates fail at these resolutions:

| Branch/base count | Maximum relative waveform error | Maximum sampled reduced-force error | Peak-normalized force error |
| --- | ---: | ---: | ---: |
| Reference17 | 0.0648403 | 3.3905645e-5 | 6.27743 |
| MTS17 | 0.0672908 | 1.3637858e-3 | 252.497 |
| Reference33 | 0.0173850 | 2.1969310e-6 | 0.406749 |
| MTS33 | 0.0180928 | 2.4629301e-5 | 4.55997 |
| Reference65 | 0.00455765 | 5.8135712e-7 | 0.107635 |
| MTS65 | 0.00488768 | 4.4755699e-7 | 0.0828626 |

The count33 final MTS force is positive1.7406950e-5 while the independent continuum force is negative5.4011962e-6. At count65 the MTS final force has the correct sign and is-5.7622499e-6; reference65 gives-5.6217266e-6. The sign correction and substantial refinement improvement do not make either a force pass. Reference65 has its maximum discrepancy at the initial sample; MTS65 has its maximum at0.001. Neither that initial error nor the later samples are excluded from the peak calculation.

Both finest branches also pass the predeclared source-position, velocity and instantaneous clock-rate smoke checks. Their maximum source-position errors are4.30e-11/5.87e-11, velocity errors1.99e-8/2.66e-8 and clock-rate errors1.33e-9/3.40e-8 (reference/MTS). These short-horizon trajectory readouts can agree much more closely than the instantaneous force; they do not imply the force gate passes.

The MTS maximum sampled force discrepancy decreases by about55-fold from17 to33 and another55-fold from33 to65. This is an observed trend over these meshes, not a certified convergence order or a license to extrapolate to arbitrary resolution. MTS65 having a smaller maximum error than reference65 does NOT establish better physics: both are being compared with the same continuum target and have different finite discretization errors.

### Important cancellation at the finest MTS endpoint

At count65 and time0.004, the action traction defect is-5.3325164e-6 and the trace/geometry difference is+4.9714628e-6. Their sum is the actual total error-3.6105367e-7. This cancellation is part of the computed equations, not a fitted subtraction. It must be preserved and controlled in a useful estimate, not forbidden; equally, the relatively small sum is not proof that its constituents converge uniformly.

The derived broken-traction terms for that state are bulk Euler work-6.8855035e-6, internal moving-edge work+2.0630592e-6 and explicit Gram shape force-5.0986757e-7. They reproduce the measured traction defect to2.046e-10. The direct local pressure alone is only-4.2973349e-7, so replacing the action force with the local pressure would substantially CHANGE this finite solution, not repair a mere reporting error.

### Why the finest run is slower

A separate frozen-source/frozen-metric scalar eigenproblem, checked against the existing action stiffness, finds maximum angular frequencies about1545/1882 at count17,2319/2501 at33, and9272/14851 at65 (reference/MTS). All tested scalar pencils are positive. The finest MTS period is about0.000423 normalized time, shorter than the requested maximum step0.0005; the adaptive solver must resolve those modes rather than taking that maximum step indiscriminately. This diagnoses a more demanding numerical problem; it is neither a full coupled stability theorem nor evidence for a physical new frequency. No mode is deleted to accelerate or improve the force result.

The finest reference/MTS integrations use248/740 RHS evaluations and about2176/4719seconds before final readouts. Every0.001 interval is checkpointed. Both finish inside the7200-second per-run safety budget. At most two owned single-core BelowNormal workers run at once, with no subagents or GitHub action.

## What is actually closed and what comes next

261 successful implementation/identity checks complete in this checkpoint. They are not261 independent physical validations. All six combined scientific comparison rows remain false because their force target fails; the finest two nevertheless pass their separately recorded waveform and source/clock targets. No new failed execution attempt is introduced; all33 previously retained failed attempts and the4 original failed full-horizon flat-force gates remain preserved.

The new result closes the planned first independent comparison and derives a usable expression for the remaining force error. It does not close the continuum source-force limit. The next concrete calculation should use the saved worst-force states (reference65 at0, MTS65 at0.001), holding their physical state fixed while raising material-label and action-quadrature resolution. This isolates the remaining force-readout uncertainty before spending another hour on an integration. The earlier count17 material/time estimates cannot automatically certify count65, and the tangent-interval check cannot substitute for trajectory time refinement.

After that, derive a bound or a consistently varied numerical improvement for the COMBINED virtual-work residual and trace/geometry term. Preserve the original action, its moving-field momentum and its Gram contribution; any alternative mesh-motion map or approximation must have an explicit action-consistency check, not an imposed pressure-law replacement. Only then extend the horizon and return to the older force tests. Conservation precision, a positive frozen scalar spectrum, this short waveform pass and a successful algebraic identity are not interchangeable with a full GR/PPN result.

## Local sources

- `scripts/run_annular_P2_continuum_bridge_20260918.py`
- `scripts/compare_annular_P2_continuum_bridge_20260918.py`
- `scripts/diagnose_annular_P2_traction_gap_20260918.py`
- `scripts/derive_annular_P2_broken_traction_identity_20260918.py`
- `scripts/verify_annular_P2_broken_traction_offshell_20260918.py`
- `scripts/diagnose_annular_P2_frozen_frequencies_20260918.py`
- `scripts/annular_P2_primitive_geometry_20260918.py`
- `scripts/annular_live_P2_current_20260918.py`
- `scripts/annular_live_barycentric_20260915.py`
- `scripts/annular_live_continuum_characteristics_20260915.py`
- `scripts/derive_annular_continuum_radiation_force_20260915.py`
- `scripts/run_annular_live_continuum_evolution_20260915.py`
- `source-intake/navier-stokes/20260914/annular-P2-tight-error-budget-final-integrity.json`
- `source-intake/navier-stokes/20260914/annular-P2-continuum-comparison-17-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-continuum-comparison-33-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-continuum-comparison-65-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-broken-traction-offshell-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-broken-traction-65-attempt01/status.json`

No GitHub action, no external data fit, no unrestricted GR/PPN or complete-parent-action claim. The original failed evidence remains immutable.
