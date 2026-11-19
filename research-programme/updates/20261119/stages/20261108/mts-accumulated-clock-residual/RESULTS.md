# Accumulated clock-residual response: verified

Completed2026-11-09, local only. Parent: ../mts-clock-weighted-forcing-primitive-20261108, closeout9326810b114cd2f4758e95f0d0878eead292678358a09ebc75011bef5a690790. The broader framework goal remains active.

## Advance toward controlled GR/Newton transport

The previously derived reduction of rapid forcing now has a source-conditioned accumulated-response calculation. It is no longer justified merely by a small instantaneous oscillatory RMS.

Starting from the retained equations, set
    r=MJ-J_N,  q=fbar+a,  g=r-a.
Here a is the explicitly controlled interpolation of the derived moving-clock mean. Keeping its interpolation error inside g gives the exact retained error equation
    e_N=M e+g,  e(initial)=0,
for the difference between full and slow responses. Both use the original incoming offset eta(initial)=-J(initial) and the same final physical maps; no late initial mode is inserted.

For each physical terminal row ell, derive and solve
    lambda_N=-M^T lambda,  lambda(final)=ell.
Then
    ell e(final)=integral lambda^T g,
    abs(ell e(final)) <= integral abs(lambda^T g)
                     <= sum_chunks sqrt(DeltaN_chunk * integral_chunk (lambda^T g)^2).

The last expression supplies the reported Cauchy budget. It retains the actual full-hierarchy propagator, rather than assuming its norm small because the phase is fast. Normal-form and coordinate-map forcing remain separate until the combined physical projection.

## Quantitative result

All120 acceptance records pass: three wavenumbers, baseline/MTS, both GR and spatial-Poisson branches, allten original TERMINAL physical readouts. The readouts are Phi, Psi, D, Q, Pi, theta_c, delta_c, delta_b, delta_gamma and delta_massless.

Each value below is normalized to that channel's maximum original full-equation reference magnitude over the existing five saved probes. Different columns can have different maximizing channels. These are own-model/own-branch internal accuracy checks, not MTS-versus-baseline fits or GR-versus-Poisson equality tests.

| Family | Branch | Largest Cauchy budget | Largest observed full-minus-slow difference | Largest slow final-reference error |
| --- | --- | ---: | ---: | ---: |
| balanced | gr | 2.659362998e-7 | 2.918058173e-10 | 3.788295962e-7 |
| balanced | poisson-spatial | 1.181258800e-6 | 9.071823107e-9 | 3.790790102e-7 |
| double | gr | 1.605752290e-6 | 4.460803873e-9 | 1.628900880e-6 |
| double | poisson-spatial | 3.009178301e-6 | 1.484547551e-8 | 1.628641852e-6 |
| half | gr | 1.035940938e-7 | 1.852144534e-10 | 5.590059762e-7 |
| half | poisson-spatial | 4.298344387e-7 | 1.216020978e-9 | 5.564319060e-7 |

The largest budget is3.0091783014491323e-6 (3.009ppm), below the unchanged2e-5 (20ppm) physical gate. The largest observed omission effect is1.4845475506155858e-8 (0.01485ppm). The budget is deliberately conservative: its smallness is derived from the actual source and propagator, not fitted to that observed effect.

For baseline, the rapid-phase sector is absent: J=0,a=0,q=f and hence g=0. With the identical original source evaluation the fine slow response reproduces the saved full baseline response exactly in the tested arrays. Baseline FINAL physical reference errors remain nonzero, with maximum2.0326767687602797e-10. The zero residual budget does not assert a perfect baseline cosmology or zero overall numerical error.

The final-reference column is FINAL-EPOCH ONLY. It must not be compared as an apparent improvement to the preceding stage's maxima over allfive epochs. Earlier history and its original physical comparisons are preserved, not overwritten.

## Independent numerical evidence

- Full compact-plus-G192 transpose checked against independent sparse assembly and bilinear duality.
- All terminal rows independently checked against the existing native evaluator, with complete physical/coordinate/periodic endpoint maps.
- Mean forcing evaluated by exact degree-six convolution on the UNION of the original cubic knot sets; independent interior checks cover every product cell.
-65/33 auxiliary mean nodes,8192/4096 source quadrature intervals,4096/2048 time caps, and unchanged DOP853 rtol2e-12/atol2e-14.
-12 full numerical adjoint solves (six cases, two time controls), each in64 memory-bounded chunks:768 numerical chunks. The half-baseline repair analytically reprojects its already computed source-independent adjoints onto the exact zero source; it does not claim an extra numerical solve.
- Paired slow mean-source/time controls; signed predictions are frozen BEFORE the independent saved full-response comparison.
- All original source, bank, thermal/background history, physical grid, couplings, arithmetic gates and initial preparation remain unchanged.

Largest MTS diagnostics:
- Signed forward/adjoint discrepancy, relative to the absolute COMPONENT budget: 5.0528879633530849e-10.
- Signed discrepancy relative to the small signed component itself: 7.0086321372466623e-7; also below2e-5.
- Signed quadrature change under refinement, budget-normalized: 7.5884632044551454e-9.
- Cauchy-budget relative quadrature change: 2.4304497121554244e-8.
- Signed adjoint time-control change, budget-normalized: 1.1988758255278594e-15.
- Cauchy-budget relative time-control change: 2.9121695924224070e-14.
- Slow time-control change in physical-output normalization: 3.0118972640079329e-19.
- Slow mean-row control change in physical-output normalization: 4.0426938408837217e-21.

Original algebra gate1e-10 and numerical gate2e-5 are unchanged. The squared-projection Cauchy quadrature is well resolved under those controls. In contrast, direct absolute-value quadrature crosses nonsmooth zeros:42 of60 MTS rows do NOT meet the relative2e-5 refinement criterion (largest1.700434710351077e-4). Those diagnostics remain explicitly flagged and are NOT used as resolved integral bounds. The smooth squared-projection inequality was specified before the comparisons and avoids treating those unresolved absolute integrals as accepted evidence.

The actual full state dimensions are half1118/1116 (MTS/baseline), balanced1064/1062, double1064/1062. DERIVATION.md's shorthand1064 was representative, not a dimension restriction; every computation obtains the actual saved dimension and keeps the complete hierarchy.

## Inspected failures and root-cause repairs

Three failed process receipts are retained:
1. prepare-half-01 incorrectly assumed the nonuniform original forcing knots were a subset of the uniform auxiliary clock grid. V2 uses their exact union, without moving any knot.
2. prepare-half-02 queried the old carrier after installing the local phase accessor but before setting its local state. V3 retrieves the original chart before entering the local context, as the accepted parent readout does, and reuses the saved drift rows.
3. comparison-half-01 rejected the baseline's relative quadrature on tiny source-subtraction noise. All8193 samples were independently identified as separate evaluation roundoff (largest source-relative3.561892236946864e-13). The exact baseline q=f identity is now applied BEFORE subtraction. No residual is clipped and no tolerance is loosened.

KNOT-SUBDIVISION-REPAIR.md, CHART-ORDER-REPAIR.md and BASELINE-IDENTITY-REPAIR.md document the changes. Original sources, arrays, tracebacks and receipts remain. Accepted inputs use preparation-03, comparison-02 and audit_accumulated_v2.py.

## Scope carried into the next calculation

This is a derived inequality with numerically qualified source/propagator integrals on the retained saved interval. It is not yet a certified continuous-time enclosure. The source/mean interpolation is explicitly defined; original microscopic source interpolation uncertainty remains separate.

The accepted omission budget concerns replacing the retained FULL FIRST RESPONSE by its derived slow version, with exact endpoint restoration. It does not erase the first-response feedback R_total delta, original-background replacement error, earlier incoming uncertainty or source interpolation error. Those must be combined before extending a physical approximation to a much longer trajectory.

No new observations, calibration, fit, public claim or GitHub action occur. This advances the SAME original-preparation retained branch; it does not rebuild a different theory.

## Saved evidence and cleanup

- preparation-03/: derived mean products, terminal duals and independent validation.
- residual-path-01/: complete8193-node paired residual paths and original-phase checks; half baseline's original noise retained historically.
- slow-response-01/: paired slow controls, with half baseline superseded by baseline-identity-01/.
- adjoint-01/: numerical adjoint chunks and frozen projected predictions.
- baseline-identity-01/ (half only): qualified exact baseline limit, original-source slow controls, explicit zero-source reprojection of saved adjoints.
- comparison-02/: authoritative paired physical comparisons.
- audit/result.json: full source/hash/control/chunk audit and120 accepted physical records.
- NEXT.md: the next physical feedback calculation and its exact error identity.

All task-owned workers are checked for exit before CLEANUP.json and closeout.json are written. There are20 Python start/end receipts:17 successful and the three inspected failures above. No process was killed; no compiler, subagent, temporary app/server or GitHub action was started. Earlier research and other chats' work are untouched.
