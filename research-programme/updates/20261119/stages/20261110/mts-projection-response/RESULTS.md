# The original projected sources recover the coherent state

Private retained-framework checkpoint, 10 November2026. This completes the saved response-map calculation rather than starting another theory or repeating the missing-phase audit.

## Main result

For this saved MTS window, the original averaged heavy density/current pair, together with the specified rest history and retained other initial values, determines the two coherent heavy initial coordinates. The measured response has rank2. Its condition is1.0013176888 after declared dimensionless row/state scaling; the raw response condition is67.3445. The forcing-subtraction cancellation factors are only about1 and1.00144, so good matrix conditioning is not concealing a large subtractive cancellation.

This refines the earlier concern about lost phase: the two projected sources are not automatically insufficient. Their ability to identify the state depends on the derived dynamical response and driving history. Both were explicitly supplied and tested here.

The baseline is tested with its proper one-dimensional CDM density state. It also passes; no artificial2x2 dust inverse or nonzero dust pressure is introduced.

## Pressure is predicted, not fitted

Eliminating the two heavy initial coordinates gives, in the original projected normalization:

    P_bar = 0.00021985207325650542*D_bar
            +0.000013854484743668138*Q_bar
            -0.0000005949823326616946.

The first two coefficients come from the action-derived response matrix. The last number is the evaluated history/known-seed term, not a new constant to fit. These coefficients belong to this finite window and specified history, not to a universal instantaneous pressure law.

The finest reconstruction predicts P_bar=-0.00022500624054861969; the saved independent pressure is -0.00022500624054007335. The pressure-relative difference is3.79826e-11. Pressure was not an inversion input. Removing the history term gives a0.2644% pressure error and fails the unchanged pressure-relative numerical check.

The separately retained legacy pressure gate,2e-6 of the original mode norm, also passes. Do not conflate that mode normalization with pressure-relative accuracy. These are numerical equation/reconstruction comparisons, not observational precision or a new cosmology likelihood improvement.

## Paired resolution checks

The real-scalar block includes BOTH retained scalars where present plus CDM, with their mutual density contribution to gravity inside the evolution operator. Baryon/radiation/neutrino densities and eta are supplied histories for this test. Initial seeds, action, masses, G, source bank, original902 epochs, signed weights and2e-5/1e-10 acceptance gates are unchanged.

| Check | Baseline | MTS |
|---|---:|---:|
| Finest forward state, worst componentwise relative difference | 9.27041e-14 | 2.37684e-11 |
| Finest recovered seed, error in declared coordinate units | 2.55351e-15 | 1.31081e-12 |
| Coarsened-history forward state difference | 8.66895e-14 | 1.14291e-10 |
| Coarsened-history recovered seed error | 2.55351e-15 | 1.38174e-11 |

All eight paired fundamental/quadrature/history configurations pass. Coarsened-history pressure reconstruction differs by6.00416e-7 relative, still below the fixed gate. The maximum observed MTS seed shift between histories is1.51282e-11; the derived finite-refinement sensitivity bound is1.56320e-11 plus a7.12e-15 rounding allowance. That bounds the measured representation change, not an unknown continuum error.

There are428 recomputed numerical checks and4 exact symbolic checks. The independent verifier reconstructs the forward/inverse source predictions and response matrix, checks a seven-point derivative of the saved fundamental solution against its differential equation, and checks its determinant against the integrated trace. Source-column algebra controls and the independent pressure row pass. Original inputs and earlier checkpoints are hash-verified.

## Boundaries of the result

This is a derived, history-dependent state/source bridge on the retained linearized background. It does not choose a galactic population, prove a positive-ensemble preparation, or evolve the other species independently in a new reduced cosmology. The projected-pressure numbers cannot be reused at arbitrary epochs as a local sound speed.

The next test is a live continuation from the reconstructed endpoint, retaining all other native state and caches and comparing with the captured-endpoint continuation. Before calling that a port to the old late carrier, its actual physical state/ensemble contract must be checked. NEXT.md gives that sequence without restarting the framework or changing direction.

## Work preservation

Two reporting interruptions and one pre-worker adapter error are documented in REPORTING-REPAIRS.md. The completed coarse heavy numerical packet was reused, not recomputed; no physics result or tolerance changed to fix logging. Completed reports are cold-response-result.json, heavy-response-resume-result.json and derived-closure.json.

Everything remains local. No GitHub action, Galaxy file changes, native rebuild, downloads, relay/timer or subagents. Exact worker receipts and final cleanup accompany the seal.
