# All-native jump response and numerical force repair

Private continuation of the source-feedback P7 stage. Work remains inside post-checkpoint-work; no GitHub action or subagents.

## What was actually constructed

The third-derivative jump law is now imposed at every ordinary native knot, not only in the original active-force halo. It does not divide by the native field load A, so it also applies in the quiet region. The actual 15 material-vertex profiles retain native values, first and second jets, source pin, source third jets and the 1094-point interaction support. The P7 field still has 7658 coordinates per material vertex. Both branches receive their own radial geometry and full field/source acceleration solve.

The construction preserves ordinary third-derivative means except at the two neighbours of the exact-zero outer cells. There the outer-cell zero condition fixes the free mean. An initial attempt incorrectly asserted exact-zero native loads at those neighbours. The daughter keeps their actual tiny nonzero values and verifies the induced frozen point increment is below the predeclared 1e-35 budget (measured maximum about 4.93e-81), rather than deleting the terms.

Derivation: `DERIVATION-20261003-all-native-jump-response.md`. Its original exact-zero boundary sentence is superseded by the measured general-law daughter, not treated as established. Source construction: `source-intake/navier-stokes/20260914/annular-all-native-jump-construction-attempt02/status.json`.

## First live outcome: the strong-law update was insufficient

The own-gravity, full-Hessian primary solve passes the inherited initial source, curvature, point and jump gates at both quadrature rules. Its fine-rule Euler relative residual is 4.96e-16 and native energy remains 5.351617140465188e-12.

| Second-time response maximum | Previous source-corrected P7 | All-native jump update, original evaluation |
| --- | ---: | ---: |
| Shape | 7.13111e-12 | 7.13346e-12 |
| Ordinary point | 6.08408e-12 | 6.08515e-12 |
| Source slope covector U_J | 1.41270e-9 | 7.52940e-10 |
| Moving field jump | 32.5743863 | 32.3884462 |

The jump improves by only 0.57%, despite the frozen jump construction passing at every vertex. The source response improves by about 47%. The strong-versus-weak acceleration-slope gap remains about 0.83936. This makes another blind use of the same frozen strong-law update a poor next step.

Source: `source-intake/navier-stokes/20260914/annular-all-native-jump-time-response-attempt01/status.json`. Probe labels include material endpoints and nine Gauss points; they are not all independent held-out vertices. These are local second-time jets, not integrated trajectories.

## A shared numerical issue was found and repaired

Direct weak force and its integrated-by-parts equivalent initially disagree by about 1.15e-9 relative at the full low-order rule on both the primary and reference branches, failing the original 2e-10 gate. The discrepancy was not dismissed or relabelled a physics result.

Replacing cancellation-prone monomial evaluation of the degree-seven basis by the algebraically identical product form improves sampled agreement by roughly 60--500 times. Independent 75-digit exact polynomial integrals also favour the product form. Full coupled reruns, including the rebuilt Hessian and both source/native covectors, subsequently give:

| Full force comparison | Primary | Same-profile reference |
| --- | ---: | ---: |
| 12 spatial / 48 material points | 5.87975e-12 | 5.89583e-12 |
| 16 spatial / 64 material points | 2.30756e-12 | 2.30979e-12 |

All four satisfy the unchanged 2e-10 gate. Both acceleration assemblies have Euler relative residuals around 4.9e-16. The primary retains every initial gate; the empty-native reference does not satisfy the primary's nonzero-jump balance, as expected for a same-profile action control rather than a separately prepared GR solution. No observational competition is inferred from that control.

The primary direct/product-versus-integrated acceleration difference is 1.79845e-10 at the fine rule. The direct-product low/high quadrature acceleration difference remains 3.04995e-6, essentially unchanged from the original evaluation: fixing basis cancellation alone therefore does not settle every resolution question.

Derivation and oracle details: `DERIVATION-20261003-product-basis-force-repair.md` and `DERIVATION-20261003-balanced-native-force-test.md`.

Full coupled evidence:

- `source-intake/navier-stokes/20260914/annular-product-basis-live-primary-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-product-basis-live-reference-attempt02/status.json`

## Retained failures

The original boundary exact-zero assertion and both original weak/integrated force comparisons remain failed. The first two product-basis full drivers passed the force/Euler checks but failed on Python-list multiplication in an output summary; their daughter explicitly converts arrays and reruns the same equations. No failed original has been promoted and no threshold was loosened to accept the force comparison.

## Repaired time probes: tenfold jump improvement, source correction must be refreshed

Both equivalent force assemblies were tested with fresh kinetic-inclusive radial geometry at all three time-jet steps:

| Second-time response maximum | Direct product | Integrated/balanced |
| --- | ---: | ---: |
| Shape | 1.49612e-12 | 1.92904e-12 |
| Ordinary point | 4.64425e-13 | 4.71089e-13 |
| Moving field jump | 3.21650414 | 3.21650355 |
| Source slope covector U_J | 7.14858e-7 | 7.11525e-7 |
| Acceleration-slope strong/weak gap | 0.08967966 | 0.08967966 |

Thus about 90.1% of the original maximum jump drift disappears after the numerical repair, with the maximum moving from native column 572 to 609 (zero-based interior-native indexing, label -0.5). The two force forms agree closely on the remaining large jump. Its step-Richardson spread is about 5.83e-12, much smaller than its magnitude. The native-value strong/weak gap remains about 3.46377e-5. These observations do not yet distinguish spatial/material projection error from a remaining dynamical compatibility error.

The earlier source feedback was computed using the old acceleration. Its small residual does not survive the more accurate evaluation; reporting only the improved jump would conceal this. The source third-jet correction is therefore recomputed using the full coupled tangent equation H*delta(a)=delta(F)-delta(H)*a, including source inertia and the mixed block, with the new balanced acceleration as baseline. This is a derived initial-profile adjustment, not an independently fitted source acceleration.

Time-probe evidence:

- `source-intake/navier-stokes/20260914/annular-product-basis-product-time-response-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-product-basis-balanced-time-response-attempt01/status.json`

Construction script: `scripts/correct_annular_product_source_feedback_20261003.py`. Its tangent keeps the metric fixed during the linear solve; qualification requires a fresh own-geometry solve and time probe of the resulting profile.

## Source feedback rebuilt and tested live

The new 15-by-15 coupled response has condition number 1.0081024. It gives a maximum source third-jump adjustment of 0.2608757785 while retaining native values and lower jets. Its frozen predicted residual is 3.17637e-22; that number is not substituted for the subsequent live result.

Both own-geometry daughter solves pass the same force-equivalence and Euler tests. Every primary initial gate survives. Fresh time probes give:

| Final second-time response maximum | Direct product force | Integrated/balanced force |
| --- | ---: | ---: |
| Shape | 1.4962852e-12 | 1.9291235e-12 |
| Ordinary point | 4.6452803e-13 | 4.7109474e-13 |
| Moving field jump | 3.21650414 | 3.21650355 |
| Source slope covector U_J | 3.8934873e-9 | 1.7321233e-16 |

The balanced source response falls from 7.11525e-7 to 1.73212e-16 under a fresh full calculation, and the direct-product source response also falls, from 7.14858e-7 to 3.89349e-9. The point/shape/jump gains survive. **The 1.73e-16 source result is formulation-specific at the present numerical precision:** the equivalent direct force leaves 3.89e-9, so a robust source accuracy claim cannot be based on the smaller number alone. This is a force-precision/observable-sensitivity question to resolve, not a reason to fit a new physical coupling. The balanced time-step spread is 1.22e-19, but step convergence does not remove the force-assembly discrepancy.

Final primary state and both accelerations are owned by `source-intake/navier-stokes/20260914/annular-product-source-corrected-live-primary-attempt01/status.json`; matched reference is `source-intake/navier-stokes/20260914/annular-product-source-corrected-live-reference-attempt01/status.json`.

Final time evidence:

- `source-intake/navier-stokes/20260914/annular-product-source-corrected-product-time-response-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-product-source-corrected-balanced-time-response-attempt01/status.json`

The construction itself is in `source-intake/navier-stokes/20260914/annular-product-source-feedback-attempt01/status.json`.

## Where the remaining large jump comes from

At fixed measured metric response, split the second jump residual as

    R_weak = R_strong + beta * ([g_ddot]_weak - [g_ddot]_strong).

Here the weak quantity is obtained from the actual full-Hessian acceleration; the strong quantity uses the differentiated bulk equation. This is an algebraic diagnostic at the same state and metric response, not a separate converged solution.

For the final balanced case, at the maximum-jump witness (label -0.5, interior-native column 609):

    measured weak residual       = -3.21650355094
    weak/strong transfer term    = -3.21650397908
    inferred strong residual     =  4.28144523e-7

The largest remaining measured jump is therefore almost entirely in the weak/strong acceleration-derivative mismatch at that witness. However, the inferred strong residual has a larger maximum elsewhere (0.19109521), so this is not a statement that every strong jump equation is solved. Nor does the split alone prove that the mismatch vanishes under refinement. The old monomial calculation's analogous transfer maximum was 32.38928; the repaired result is not merely a renamed old failure.

Evidence: `source-intake/navier-stokes/20260914/annular-jump-projection-decomposition-attempt01/status.json`; implementation: `scripts/analyze_annular_jump_projection_20261003.py`.

## Next concrete calculation

1. Exactly prolong the final saved P7 profile onto a bisected **field** mesh while retaining all 1094 native interaction points, all 15 material vertices, the source, and the physical initial data. Do not refit the profile or add new physical interactions.
2. Recompute each branch's own gravity and full coupled acceleration with product-basis and balanced-force checks. Repeat the same time probes and weak/strong split, comparing common native knots. This tests whether spatial representation explains the remaining quiet-knot mismatch; material refinement is a separate subsequent test if spatial refinement does not settle it.
3. Add a source-observable precision check comparing the direct and balanced U_J responses. Use a high-precision or moment-exact direct-force oracle before treating the balanced 1.73e-16 as an assembly-independent accuracy level.

This is more informative than another frozen third-jet retune against the same unresolved projection. It also keeps the successful point/shape and coupled source construction in place while testing the remaining mechanism.

## Reproducibility

`scripts/seal_annular_all_native_jump_v2_20261003.py` validates the inherited hashes and all new run inputs/outputs, retains five failed originals, compiles the new scripts without bytecode, parses the four audit CSV rows, and independently replays the saved time extrapolations, force comparisons, source response and weak/strong split. The authority it writes is `source-intake/navier-stokes/20260914/annular-all-native-jump-integrity-20261003.json`.

The first sealer, `scripts/seal_annular_all_native_jump_20261003.py`, is preserved: it failed by treating this output-authority citation as an already-existing input. The daughter excludes its own output from the input hash cycle and verifies it after writing; the physics gates and inherited input hashes are unchanged.

The mutable resume bookmark is deliberately excluded from the scientific hash chain. No claim rows are promoted by this stage. All computations use at most two one-core, below-normal-priority workers; no other chat's processes are stopped.
