# Live phase-stress coupling passes the paired native test

Private checkpoint, 10 November 2026. Retained MTS action and inputs, not a restart of the theory.

## What moved forward

The derived coherent moment variables now drive the actual native density/current sources, which drive the metric and other species. That live metric drives the moment variables back. The test is no longer a replay forced by saved gravity. The primitive scalar coordinates are removed from the independently evolved vector; their reconstructed values are diagnostics/plumbing, not extra hidden solutions.

Both baseline and MTS pass the unchanged 2e-5 componentwise numerical gate and 1e-10 algebra gate after explicit internal-step resolution checks. All 4253 original native output rows remain byte-identical when the new source path is disabled. The original bank, masses, G, abundance, initial physical state, background tables and observation grids are unchanged. Input/output scaling introduces only separately bounded floating-point roundoff at the initial point; see VALIDATION-REPAIRS.md.

## Four paired controls, two internal resolutions each

These are maximum componentwise discrepancies against the retained native solution at the finer window/256 maximum internal step. They measure numerical representation fidelity, not observational accuracy.

| Case/window | Active primitive / phase dimensions | State | Source/metric observables | Native derivative | Moment transverse remainder |
|---|---:|---:|---:|---:|---:|
| Baseline matching | 182 / 184 | 2.62830e-14 | 1.31889e-13 | 2.77301e-12 | 6.01384e-15 |
| MTS matching | 185 / 189 | 1.63920e-9 | 1.20617e-8 | 8.71698e-7 | 2.97734e-9 |
| Baseline active tight coupling | 106 / 108 | 2.22091e-9 | 2.57068e-11 | 1.50277e-9 | 6.99488e-13 |
| MTS active tight coupling | 109 / 113 | 4.00226e-10 | 3.88271e-9 | 5.73184e-10 | 1.03346e-9 |

The matching window is the original zero-based indices 2591–2890 (300 saved states). The early active-tight-coupling window is 512–520 (nine saved states). All other active species and the physical photon caches remain present. The 4-entry moment representation has constraints and does not add physical scalar modes.

For MTS matching, reducing maximum step from window/128 to window/256 decreases the worst derivative discrepancy from 2.86545e-6 to 8.71698e-7. Both pass; the original adaptive-only fine run's 2.43741e-5 failure is preserved. Tightening rtol alone had not produced reliable monotonic improvement. Baseline and MTS received the same step tests.

Active tight-coupling cache differences at the finer resolution are 4.01537e-13 for baseline and 7.12243e-12 for MTS. The approximate massive-neutrino memory regime is not exercised and is rejected by this bounded interface; its actual hierarchy remains included.

## Live-source tests

- A CDM perturbation changes the live metric by the predicted amount and changes the moment forcing accordingly in both cases.
- A physical heavy-field amplitude change produces the predicted change in z and the metric momentum equation without a new fitted coupling.
- A deliberately transverse, nonphysical M probe changes direct D/Q while leaving recovered primitive coordinates unchanged. The metric responds to the direct stress, proving this code path is not silently projecting M and substituting the old primitive stress. Direct metric response agrees within 4.44e-13 relative in that control.
- Repeated calls have no leaked override state; out-of-window calls are rejected.

Fifteen exact symbolic identities and 4,418 recomputed numerical comparisons pass. `validation.json` recomputes accepted packet comparisons, direct stress readout, independent phase RHS, physical-subspace drift, refinement and source controls. The unchanged historical source hashes and all declared native changes are checked. The checker also explicitly requires that the original adaptive-only failure remains a failure.

## Preserved numerical caveats

There were three receipt-level stops: the original early capture's unused polarization-index comparison; the diagnostic's deliberate SystemExit(0); and the verifier's overly strict bitwise normalized-seed comparison. Their source-specific resolutions are documented in VALIDATION-REPAIRS.md. No physical tolerance or prior result was rewritten to make these pass.

The exact derivative of the native thermal scale interpolant is retained separately from the Friedmann H in the phase-coordinate derivative. The identities in DERIVATION.md expose remaining background/source interpolation defects explicitly. This test demonstrates coupled representation fidelity; its next use is a controlled early-to-late source transfer, not a claim that interpolation errors or unknown populations have disappeared.

## Scientific scope and next use

This is a concrete coupling result within the retained model: coherent scalar stress can evolve self-consistently with the metric and radiation without a fitted pressure law or saved-metric forcing. It neither fixes galactic occupation from formation data nor supplies a new observational fit. Galaxy Lab's conditional baryonic-force work remains a separate useful input for that later state-preparation question.

Next: derive the source-complete transfer to the retained late carrier using the original signed phase projection, keeping the residual phase pressure and boundary terms. Use the live phase solution as the reference; do not simply discard its phase information or identify a signed projection with positive occupation.

Everything remains local. Exact process receipts and CLEANUP-VERIFIED.json accompany the seal. Original framework, Galaxy Lab, public repository, shared services and other chats are unchanged.
