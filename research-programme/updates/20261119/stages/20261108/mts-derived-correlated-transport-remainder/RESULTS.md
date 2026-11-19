# Derived transport correction predicts the saved discrepancy

2026-11-08. Local continuation of the retained MTS framework, not a new action or fitted model. Parent: ../mts-invariant-correlated-early-transport-20261108, closeout18ef599d24a4382fe47634c2bf98eb0c3c1663de83ed0732c79017628db34a2e.

## Result

The omitted short-interval transport forcing is now derived and propagated. The largest MTS readout discrepancy against its original saved full-equation calculation falls from5.9152994e-6 to2.5782581e-9: approximately5.9 parts per million to2.6 parts per billion, a reduction of about2,294 in the family-wide maximum. This is an internal approximation-versus-original-equations test, not an observational fit.

All120 physical channel comparisons pass the unchanged2e-5 gate: ten readouts, three retained wavenumbers, baseline/MTS, GR/spatial-Poisson, across the same five fixed early epochs. No parameter was fitted to the reference residual, no initial perturbation was reset, and neither the original bank nor the G192 hierarchy was changed. The baseline maxima are unchanged from the preceding stage.

## Physical comparison

| Family | Branch | MTS before | MTS after | After: largest channel | Baseline after |
| --- | --- | ---: | ---: | --- | ---: |
| half | GR | 1.58914e-6 | 2.50910e-9 | D | 2.87947e-11 |
| half | spatial-Poisson | 5.91530e-6 | 2.50753e-9 | Phi | 4.91643e-12 |
| balanced | GR | 2.18699e-6 | 2.47549e-9 | D | 1.11455e-11 |
| balanced | spatial-Poisson | 1.78626e-6 | 2.47551e-9 | D | 2.83251e-11 |
| double | GR | 2.48741e-6 | 2.57826e-9 | Q | 8.23638e-12 |
| double | spatial-Poisson | 2.40624e-6 | 2.57821e-9 | Q | 2.00046e-11 |

Here D and Q are the retained density/current readouts; Phi is the retained metric potential. Each error uses the same per-channel normalization as the parent: maximum absolute discrepancy over the fixed five epochs divided by that reference channel's maximum absolute value over those epochs. Different rows may have different worst channels. Branchwise improvement factors range from633 to2,359; the family-wide maximum reduction is a separate statistic.

The MTS normalized full-state discrepancy is at most2.994620e-9. The largest initial physical readout difference remains9.560777e-16. The background and independent phase are unchanged from the preceding stage; the new correction explains most of the previous perturbation transport discrepancy rather than changing the background to match it.

## What was actually derived

1. The implicit density's fixed-phase derivative, rho_N|theta = rho(-1+g_N)/(1-g_x), follows from the existing invariant reconstruction. Saved slow-scalar and conformal-clock derivatives are taken from their actual retained dense histories.
2. The derivative of the phase average includes the derivative of its normalized clock measure. It yields D_slow C for the complete periodic map, including p_H S_remote and its product derivative. All190 tail levels at each of five massive nodes remain.
3. The map defect caused by the reconstructed background not following the original equations exactly is explicit:

       Delta_map = (delta_v . grad R_phys) S_phys
                   + R_phys [(delta_v . grad B) B^-1] S_phys.

   The physical energy-coordinate map B is independently reproduced from its formulas and checked against the native implementation. Original and substituted background rates are not silently equated.
4. For P=I+C, the derived omitted forcing operator is

       R_total = P^-1 [A C - C Abar - D_slow C + Delta_map P].

   Its action is computed on the saved mean solution, with normal-form and map terms kept separately. The first response solves delta_y_N=Abar delta_y+R_total y0, with delta_y_initial=0. This preserves the original preparation and physical endpoint maps.

DERIVATION.md gives the derivation, signs, noncommuting products and scope. The scripts' H is the retained conformal expansion rate, defined by tau_N=1/H; cosmic H=H/a in c=1 conventions. No new fundamental coupling coefficient or exact-zero invariant closure is introduced.

## Independent and numerical checks

| Check | Largest measured value |
| --- | ---: |
| Full normal-form chain-rule discrepancy on saved mode | 1.806724e-13 |
| Slow primitive closure | 9.480901e-14 |
| Forcing128/256 phase refinement | 1.844348e-12 |
| Independent complex directional derivative, mixed scaling | 2.411297e-15 |
| Derived physical map versus native map | 6.172607e-12 |
| Independent fixed-phase finite-difference derivative | 5.715882e-9 |
| Time refinement relative to retained state | 1.544719e-19 |
| Source refinement relative to retained state | 5.274017e-12 |
| Time refinement relative to small MTS correction | 2.991454e-13 |
| Source refinement relative to small MTS correction | 1.831464e-5 |
| Source refinement carried into physical readouts | 1.605840e-10 |
| Time refinement carried into physical readouts | 6.736317e-19 |

The largest source-grid readout variation is double-family delta_b, not the largest final D/Q residual. These are measured coarse/fine differences, not asserted rigorous continuum error bounds. Reporting both state and correction normalizations avoids concealing uncertainty in a small correction. The baseline correction itself is only around1e-28 of its state and has a relatively larger interpolation percentage at that rounding-scale level; this does not become a false physical failure or a claim of exactly zero baseline integration error.

Coverage:54 forcing nodes (nine original source epochs for each model and wavenumber), including27 MTS nodes with256 phases. The complete chain rule is checked for both gravity branches at every evaluated phase. Twelve independent complex-step source tests cover both models and both step sizes; fixed-phase finite differences check the full primitive using two widths. Source and time refinements propagate separately through the native physical readouts. All original physical gates remain ALGEBRA1e-10/GATE2e-5.

## Limits carried forward

This is the first variation of constants, not a full resummation of R_total delta_y. The true-background source difference, nonzero invariant drift, and saved slow/clock history errors remain separate. The observed short-interval agreement is evidence that the derived correction explains the previous discrepancy; it does not certify the uncomputed trajectory to the cold entrance or a continuum phase quadrature theorem.

The largest remaining discrepancies are density, metric or current readouts at the final probe, rather than the previous baryon/photon transport residual. That is useful diagnostic evidence, but it is not sufficient to assert a unique cause. With all these discrepancies far below the unchanged gate, the next default is bounded extension of the SAME original mode, carrying uncertainty, rather than repeatedly optimizing this already-passing short interval.

## Saved artifacts and execution

- remainder_source.py / directional.py: nested source derivative, implicit reconstruction rates and explicit physical map defect.
- build_forcing_v2.py / each family forcing-02: all derived phase/Fourier force packets, complete periodic primitive and slow derivative, background defects and checks.
- probe_remainder.py / probe-01 and validate_slow_rate.py / slow-rate-validation-01: independent derivative/native-map checks.
- evolve_remainder.py / evolution-01: first response, normal/map components, original mean state and source/time controls.
- predict_remainder.py / predictions-01: corrected physical predictions frozen before reference comparison.
- compare_remainder.py / comparison-01: paired original-reference comparison and exact gate verdicts.
- control_readouts.py / control-readout-01: numerical control differences propagated linearly to all ten physical channels, avoiding subtraction of nearly equal large readouts.
- audit_remainder_v2.py / audit/result.json: accepted source hashes, recomputed comparisons and numerical-control audit. The earlier auditor draft is not the accepted audit.

One inspected implementation failure is retained: forcing-half-01 completed its first numerical packet but failed when applying Python abs to a list in the report. The v2 writer uses np.abs and a new output directory; equations, grids and gates are unchanged. Original script, packet, traceback and terminal receipt remain. REPORTING-REPAIR.md documents it. No numerical or physical gate was relaxed.

Earlier work stays intact. Local only; one below-normal, CPU4, single-thread numerical worker at a time; no subagents, compiler, app/server, process kills or GitHub action. Final closeout.json and CLEANUP.json are written after exact worker identities have exited and the source/artifact hashes verify. NEXT.md specifies the continuation without a late reset. The broad research goal remains active.
