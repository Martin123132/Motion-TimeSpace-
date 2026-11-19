# Matching state recovered; nonzero initial memory quantified

Private bounded continuation, 11 November 2026. Original bank, masses, grids, a225-w6-d8 signed projector and tolerances unchanged. No observational fits, GitHub work, Galaxy changes or new late cosmological integration.

## Constructive result

The original k5 preparation determines a phase-corrected slow carrier AND a nonzero unresolved source contribution. Both are now saved, rather than reconstructing a unique oscillating phase from two fluid numbers or setting the fast contribution to zero. CARRIER-MATCHING-DERIVATION.md gives the explicit map; carrier-initial-state.npz retains all 902 original-node coordinates and source maps. Twelve carrier/readout checks pass. The saved density/current/pressure are recovered to component-relative differences at most 6.002e-14.

The derived normalized memory source is

    C0 = (1.3105681969083294e-08, -1.031989837643703e-06, 9.145341456793352e-07).

Discarding it changes the initial current by 0.0029885% and pressure by 0.35903%, against the unchanged 0.002% gate. This is an identified, preparation-owned correction, not a new fitted coefficient. The density-only check would miss the problem.

## Matching representative and its equation test

The separately constructed fixed-center moment representative also reproduces all three sources and supplies the previously unrecorded b*w cross moment directly from preparation. Its background scaled eigenvalues are 0.9994286699775721 and 1.0005713758234998; its normalized energy is 1.000000022900536, only 2.29e-8 from the inherited value. Nothing was renormalized. This positive factorization is a mathematical representative, not proof that the signed temporal projector is a physical ensemble. There are 429 negative weights; sum(abs(weights))=1.7024412253439902.

Simply evolving this representative with a bare local quadratic generator fails the projected-rate check. High-precision source rates, in original conformal units:

| Source rate | Projected preparation | Bare center representative | Relative discrepancy |
|---|---:|---:|---:|
| Density | -0.00038114761395 | -0.00038082970063 | 0.0834095% |
| Current | -0.00171268453028 | -0.00171268061793 | 0.000228434% |
| Pressure | 0.00000411053485 | 0.00000391023003 | 4.87296% |

The current rate passes; density/pressure rates do not. Background and cross-moment whole-matrix rate discrepancies also exceed 2e-5 (3.51634e-5 and 2.22032e-5). These are internal equation/projection discrepancies, NOT observed cosmology errors or a test of the full retained phase-corrected memory evolution.

The exact remainder is separated into coefficient correlations, rest-force correlations, background representation defects and the mass-dependent matching-map connection. The two complete residual identities pass at 60 and 90 decimal digits; no residual was fitted or frozen into an invented future law. The cold baseline uses the SAME signed projector, its own saved dust normalization and dust equation: density rate 0.631689168267089 matches its center readout to floating precision. The slow-scalar primitive/canonical maps pass in both cold and MTS branches.

## Validation and preserved failures

- Initial matching run: 42 checks. Thirty-six pass in binary64; four physical bare-rate gates fail. Two cancellation-sensitive decomposition checks fail binary64 despite absolute differences about 1.1e-15. All original results remain in matching-validation.json.
- Unchanged two decomposition identities reevaluated at both 60/90 digits pass. Maximum error is 2.7731e-52 at 60 digits; 5.9051e-84 at 90 digits. The physical rate errors agree to the 30 decimal digits stored for comparison. The recorded zero precision difference denotes equality of those serialized digits, not a bound on arbitrary unseen digits or floating input uncertainty.
- The combined interpretation is 38 accepted initial checks and four retained physical failures, plus twelve carrier checks. The three memory-omission checks are deliberate negative controls: density passes, current/pressure fail as expected. Do not count expected failures as an all-physics-pass result.
- Two implementation failures are preserved separately: initial seal hash reader used the wrong JSON level; first mpmath diagnostic used single-index matrix access. Their receipts, repair notes and frozen failed precision code are retained. Neither changed a source, equation or tolerance.

Source hashes tie the work to original October preparation and the accepted November native/general-k stages. The saved late capture is still two endpoints near z10; the present a0 preparation is not mislabelled as that late restart. Growth-based force reconstruction uses double growth with float-origin transfer density/velocity columns; no additional accuracy is claimed for those input columns.

## Decision

Do not launch a zero-memory or bare-representative late run under these failed gates. We now have the missing preparation-owned initial memory packet; the next calculation is to transport it through the existing general-k, current-rest-state memory system and check the matching source/RHS before a bounded late evolution. A constant additive pressure patch is not an acceptable substitute. All work is local and all task-owned numerical workers are closed; see cleanup receipts.
