# Coarse time64 isolation: same action, fixed fine trajectories

Private numerical checkpoint. This does not establish the full GR limit. The test changes one evolution parameter, not a coupling or a boundary condition.

The original action is unchanged throughout this checkpoint.

## Question and controlled intervention

The preceding stage located the largest MTS temporal difference on the coarse spatial grid. This stage actually evolves that grid again, rather than only registering a missing input.

Both reference and MTS use coarse257/source-cap2e-5, the same saved initial state, all15 layers and558 scalar modes per layer, the same source coordinate and the same exponential-midpoint integrator. The normalized interval is0..4e-5. Only the number of coarse time steps changes:32 to64. The fine trajectory remains exactly the saved fine64(reference) or fine128(MTS) trajectory. No new spatial grid, fitted coefficient, spectral clipping or modified action is introduced.

The diagnostic response uses the original banded mass and factored stiffness operators. Those frozen operators and the original nonnested interpolation are also held fixed at their preceding-stage values; freezing at the new endpoint would change a second variable. The live integrator continues using its original canonical splitting. These are distinct numerical operations, not two different physical theories.

## Exact isolation identity

Write reverse time theta=T-t, with T=4e-5. For an exact smooth trajectory on either spatial level, let

```text
v = du/dtheta, a = dv/dtheta, A_star = M_star^-1 K_star,
r = a + A_star u.
Then v' = a, a' = -A_star v + r'.                 (1)
```

Piecewise-linear interpolation of sampled r makes r' constant on each interval. The retained matrix-exponential action propagates(v,a) without squaring approximate eigenfrequencies. Its initial data are the measured velocity and acceleration of each corresponding physical endpoint, not an assumption that different time resolutions share their final state.

For a trajectory and its reconstruction, define the signed residual e_L=Y_L,reconstructed-Y_L,canonical, where Y=(v,a). With interpolation I and a fixed fine trajectory,

```text
e_hierarchy,32 = e_fine - I e_coarse,32,
e_hierarchy,64 = e_fine - I e_coarse,64,
e_hierarchy,64-e_hierarchy,32 = -I(e_coarse,64-e_coarse,32).   (2)
```

Thus the fine residual cancels exactly from the *change*. It need not vanish in either residual itself. The script reconstructs the old result independently, checks this signed cancellation, and records the energy cross term instead of presenting component norms as additive percentages.

The norm and signed decomposition are

```text
N(v,a)^2 = a^T M_h,star a + v^T K_h,star v,
N(e_fine-Ie_coarse)^2 = N(e_fine)^2+N(Ie_coarse)^2
  -2<a_fine,M_h,star I a_coarse>
  -2<v_fine,K_h,star I v_coarse>.                 (3)
```

This is an algebraic identity for the saved discrete vectors. It is not a continuum convergence theorem. The canonical acceleration at each accepted state is evaluated from the action, including moving mass, cross and inverse-residual terms. It is checked against a directional derivative of the canonical velocity; the derivative probe is halved at both ends and the midpoint. Derivatives of numerical interpolants are not silently substituted for the canonical acceleration.

## Comparisons and safeguards

- Both branches get the same intervention and the same diagnostic forcing grids(9,17,33 nodes).
- Fine point data are reused byte-for-byte from the owned previous evidence. Coarse acceleration is newly evaluated at33 matching times.
- The old response is regenerated and compared against its saved vectors, not only its scalar norm.
- First-interval halfstep and coordinate-rescaling checks test matrix-exponential arithmetic at each forcing-grid size.
- All accepted evolution states are saved, with immutable output hashes and progress. One single-core BelowNormal worker is used at a time.
- An observed improvement is not an implementation acceptance condition: a larger error is retained and reported, not classified as a broken pipeline by itself.

Richardson cancellation between17 and33 forcing nodes is reported as a diagnostic only. It assumes a leading quadratic sampling error; no factor-four convergence law is imposed on the signed temporal residual.

The response endpoint is theta=T, which corresponds to physical t=0 after backward reconstruction from physical t=T. In contrast, the force table evaluates the live physical endpoint t=T. These endpoints must not be confused.

## Results

### Physical endpoint force

Both live evolutions complete, with11 implementation checks each. The reference takes approximately495seconds and MTS566seconds on one core. Endpoint canonical/radial constraints, force identities, source/scalar Euler checks and regular-domain tests pass. These are finite numerical checks, not a bound covering every point of the exact flow.

| Quantity | Reference | MTS |
|---|---:|---:|
| Old coarse32 force | -5.335180393e-8 | -4.123163465e-8 |
| New coarse64 force | -5.335011785e-8 | -4.120942082e-8 |
| Fixed fine force | -5.335852153e-8 | -6.109938885e-8 |
| Signed coarse64-minus-coarse32 force | +1.686082155e-12 | +2.221383331e-11 |
| Old coarse-fine relative difference | 0.0125896% | 32.5171079% |
| New coarse-fine relative difference | 0.0157495% | 32.5534648% |
| Fixed fine-continuum relative error | 0.8123877% | 13.5770317% |

The common continuum endpoint comparator is-5.379554995337369e-8. Coarse-fine percentages divide by the absolute fine force; fine-continuum percentages divide by the absolute continuum force. MTS's coarse-fine force difference slightly **increases**. The change is only about0.1118% of the preceding absolute coarse-fine gap, so this particular coarse time-step error cannot explain that gap. The reference's already small gap also increases; this is retained, not hidden behind a requirement that every observable improve under time refinement.

At the MTS endpoint, the old time16-to32 force change was1.350688000e-10, versus2.221383331e-11 for32-to64, a decrease by approximately6.08times. For reference the corresponding changes are6.757703338e-12 and1.686082155e-12, a ratio near4.01. These successive observed differences are not a rigorous bound on the remaining temporal error or proof of asymptotic order.

### Signed response

The response calculation completes998 implementation checks in approximately751seconds. Including the two evolutions, the three calculations complete1020 successful implementation checks without a calculation failure. The checks concern finite numerical identities and provenance, not1020 separate tests of physical validity.

At the common33-node forcing grid:

| Response diagnostic | Reference, coarse32 | Reference, coarse64 | MTS, coarse32 | MTS, coarse64 |
|---|---:|---:|---:|---:|
| Reverse-endpoint residual norm | 3.67967997e-8 | 3.29439108e-8 | 5.90891966e-7 | 4.09734773e-7 |
| Maximum sampled residual norm | 4.44680321e-8 | 4.34656014e-8 | 3.02272626e-6 | 7.30696367e-7 |

MTS's maximum response residual decreases by approximately4.14times. Its reverse-endpoint residual decreases by only1.44times, not four. This difference is explained in part by retaining the fixed fine contribution rather than assuming it is exact:

| Coarse64 response component | Reference | MTS |
|---|---:|---:|
| Fine residual norm at reverse endpoint | 3.54900824e-8 | 3.80850697e-7 |
| Interpolated coarse residual norm there | 9.78286544e-9 | 8.90762404e-8 |
| Maximum sampled fine residual | 4.37421729e-8 | 4.04847979e-7 |
| Maximum sampled interpolated coarse residual | 9.99870903e-9 | 7.25426456e-7 |

For MTS the largest combined residual is at physical t=2e-5. There the coarse residual decreases from3.06583690e-6 to7.18692589e-7, while the unchanged fine residual is3.41113431e-7. The signed cross contribution to the squared norm is-9.89602290e-14. Thus neither adding the two norms nor treating them as independent percentages gives the actual combined result. At the reverse endpoint the fixed fine contribution is instead larger than the new coarse contribution.

Forcing sampling remains a distinct uncertainty. The new MTS reverse-endpoint norms at9/17/33 forcing nodes are7.94523532e-7,4.19912613e-7 and4.09734773e-7. Reference gives6.22459078e-7,1.49620282e-7 and3.29439108e-8. The reference remains especially sensitive to forcing-node resolution. The new endpoint vector difference between17 and33 reconstructions is1.61000146e-7 for MTS, even though their scalar error norms are close. Similar scalar norms do not establish vector convergence.

The17/33 Richardson diagnostic gives MTS endpoint residuals5.98232863e-7(old coarse32) and4.20224198e-7(new coarse64). Its signed factor-four discrepancy is1.17215565e-6. Consequently the combined residual is not certified to be asymptotically second-order under this *coarse-only* refinement. Reference Richardson values are1.95271608e-8 and1.09407407e-8, also not an exact factor-four law.

Independent propagation controls give maximum halfstep error4.17e-16 and coordinate-rescaling error2.89e-16. The largest old-response reproduction error is2.88e-15; fixed-fine cancellation errors are below9.47e-17. The canonical acceleration controls and three probe-halving checks per branch pass. These arithmetic checks are much smaller than the retained response residual, but they do not certify the finite-difference acceleration or forcing interpolation uniformly between sample points.

## Next target: full source-force-weighted spatial budget

The targeted temporal intervention succeeds in reducing the large interior response error but does not repair the force discrepancy. Another blind time-halving is therefore not the preferred next step. Nor should a smaller diagnostic norm be presented as better agreement with the continuum force.

Return to the *full reduced source-force observable*, using the existing Schur law rather than just the explicit Gram term or a global scalar energy norm. For each level let J be the free wave drive, G the dust drive, and q=Q/I the projected field inertia divided by dust inertia. Then

```text
F_L = (J_L-q_L G_L)/(1+q_L),
Delta F = [Delta J-q_f Delta G-Delta q (G_c+F_c)]/(1+q_f),   (5)
Delta = fine-minus-coarse.
```

Equation(5) follows by multiplying the difference by1+q_f and substituting(1+q_c)F_c=J_c-q_c G_c. It preserves both inertia and source terms. When numerical Schur identities have residuals, their fine-minus-coarse residual must also be retained; the algebra is not permission to discard recorded floating closure errors.

The next bounded calculation should evaluate this signed spatial budget on the refined endpoints, then contract the action-consistent spatial Duhamel remainder with the force-sensitive J functional. Reuse the existing force-gradient/transport machinery, but extend the scope from its explicit Gram or temporal-only comparison to this full source-force budget. Keep initial representation error, spatial-operator mismatch, moving geometry/source terms and numerical path defect separately. Validate the budget on the now-owned coarse32/64 pair on both branches before using it as a spatial bound. No new long evolution is justified until that observable-specific budget shows which refinement can reduce the actual force error.

This is an implementation target, not a claim that the full force-weighted transport bound has already been evaluated. Equation(5) itself is an exact algebraic reduction under the stated positive-inertia Schur assumptions.

## Force interpretation and scope

Three quantities must remain separate: coarse-fine endpoint force difference, fine-continuum endpoint force difference, and integrated impulse discrepancy. A useful finite-difference bound is

```text
|F_fine-F_coarse,64| >= |F_fine-F_coarse,32|
                         - |F_coarse,64-F_coarse,32|.       (4)
```

This bounds how much this particular temporal refinement can explain; it is not an extrapolation to zero time step. The prior approximately13.58% instantaneous number is the fine-versus-continuum comparator, not the coarse-versus-fine relative difference. The prior report used the broader label "hierarchy-force discrepancy"; this checkpoint makes the denominators explicit. Since the fine trajectory and continuum comparator are fixed here, that fine-continuum number cannot change in this test. The original12.5718% impulse discrepancy is not recomputed or claimed resolved.

These are finite-annulus, central-layer scalar response diagnostics. Endpoint force/current checks do not validate all fields, the original longer.004 interval, observational/SI normalization or a completed parent action. There is no certified continuous-time error envelope or proof of local GR. Implementation checks are not independent physical validations.

## Provenance

- Previous sealed stage: `source-intake/navier-stokes/20260914/annular-action-response-refinement-final-integrity.json`.
- New live runner: `scripts/run_annular_coarse_time64_20260919.py`.
- Response and signed isolation: `scripts/derive_annular_coarse_time64_response_20260919.py`.
- Original response operator: `scripts/annular_action_exponential_20260919.py`.
- Source Schur reduction: `scripts/annular_P2_graded_source_20260919.py`.
- Earlier temporal/explicit-Gram pullback, not yet the full spatial force budget: `DERIVATION-20260919-exponential-force-defect-transport.md`.
- Coarse64 reference evidence: `source-intake/navier-stokes/20260914/annular-coarse-time64-reference-attempt01/status.json`.
- Coarse64 MTS evidence: `source-intake/navier-stokes/20260914/annular-coarse-time64-MTS-attempt01/status.json`.
- Paired signed response: `source-intake/navier-stokes/20260914/annular-coarse-time64-response-attempt01/status.json`.

The first integrity-seal attempt passes43 checks, including all inherited hashes, outputs and sourced tables, then fails its literal report-wording test because the exact phrase "original action" was absent. The report now states that fact explicitly. No calculation, numerical tolerance or physical acceptance gate changes. The failed seal and its seven CSVs remain immutable; a versioned successor verifies and inherits them rather than overwriting them. The new historical count is45 failed executions, of which this added one is a report-wording/sealing failure, not a failed physical or numerical calculation.

- Preserved first sealing failure: `source-intake/navier-stokes/20260914/annular-coarse-time64-final-integrity.json`.
- Corrected, versioned sealer: `scripts/seal_annular_coarse_time64_v2_20260919.py`.

No GitHub, subagents or sibling-workbench edits. Protected-workbench verification uses mtime since2026-09-19 20:31:36UTC, not a pre-turn whole-tree hash baseline. New live evolution is explicitly distinguished from the postprocessing-only preceding stage. All historical evidence remains immutable.
