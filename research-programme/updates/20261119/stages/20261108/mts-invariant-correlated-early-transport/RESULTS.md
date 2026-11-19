# Invariant-correlated early transport: the repaired comparison passes

Date: 2026-11-08. Private continuation of the retained MTS action, original perturbation preparation and saved source histories. Parent seal: ba7c097d8015ca0bad8594b4e6be1dffa7b110edbe7d85523392433590d868db.

## Main result

The positive density reconstruction derived in the preceding stage is now implemented and physically compared. All ten retained readouts pass the unchanged 2e-5 relative gate for baseline and MTS, at all three saved wavenumbers and both GR/spatial-Poisson branches. This is 120 channel comparisons across the same five saved early epochs, not a new observational fit.

The old frozen-rho approximation had changed physical stress at the INITIAL epoch despite preserving the encoded perturbation. The invariant reconstruction removes that initial physical mismatch without fitting or subtracting the measured residual. The original native perturbation is recovered to at most 7.541440e-16 relative; initial readouts differ by at most 9.560777e-16 in the comparison normalization.

The largest MTS channel discrepancy across the tested family drops from 3.2064323e-4 (0.0320643%) to 5.9152994e-6 (0.000591530%). The gate remains 2e-5 (0.002%). The ratio of these maxima is about 54.2; branchwise ratios range from 54.2 to 201.8. The identity of the worst channel changes, so these ratios are maxima comparisons, not claims that every individual channel improved by that factor.

## Physical readouts against the original saved reference

| Wavenumber family | Branch | MTS maximum relative error | Worst channel | Baseline maximum relative error |
| --- | --- | ---: | --- | ---: |
| half | GR | 1.58913542e-6 | delta_b | 2.87946528e-11 |
| half | spatial-Poisson | 5.91529940e-6 | delta_gamma | 4.91643374e-12 |
| balanced | GR | 2.18699316e-6 | delta_b | 1.11454693e-11 |
| balanced | spatial-Poisson | 1.78626408e-6 | delta_b | 2.83251343e-11 |
| double | GR | 2.48740900e-6 | delta_b | 8.23638283e-12 |
| double | spatial-Poisson | 2.40624392e-6 | delta_b | 2.00045892e-11 |

The family uses k = 0.32497672865575244, 0.6499534573115049 and 1.2999069146230098 Mpc^-1. Errors are maximum absolute differences over the five fixed epochs divided by each original channel's maximum absolute magnitude over those epochs, as in the preceding test. The maximum normalized full-state error is 4.453209e-6 for MTS; baseline maximum is 1.399253e-10. All original G192 tail entries remain.

The reconstructed physical phase is integrated from its own equation and original initial phase. Its maximum discrepancy against the saved background at these epochs is 5.868241e-9 rad; the reconstructed density's maximum relative discrepancy is 5.014928e-9. The saved carrier chart is used only for native coordinate encoding, not substituted for the physical phase evolution.

## What changed mathematically

1. Freeze the slow invariant rather than instantaneous heavy density; solve the proved positive fixed point rho = rho_bar exp[g(rho,theta)]. Keep invariant drift as an explicit bounded remainder, not an exact zero axiom.
2. Evolve theta_N = omega_h/H(rho_rec(theta)) - 1.5 sin(2theta) independently. Retain saved slow-scalar and conformal-clock histories, with their uncertainty separate.
3. Average with the corresponding variable clock. Reconstruct the FULL periodic map: the remote G192 hierarchy now has a phase-dependent S_remote/H term. Its scalar primitive is retained in both endpoint maps and the full initial inverse.
4. Retain the exact collision split kappa * <R_phys C_unit/H> and read opacity from the unchanged original thermal cubic at every RHS.

DERIVATION.md gives these equations, their assumptions, and the exact residual to derive next. No original bank, frequency/angular hierarchy, physical amplitude, source history or tolerance was altered.

## Numerical and independent checks

| Check | Largest measured discrepancy or bound |
| --- | ---: |
| Independent held-out source coefficient, absolute | 6.005177e-10 |
| Propagated time-step refinement, relative norm | 6.920055e-12 |
| Propagated source-grid refinement, relative norm | 9.310308e-16 |
| Independent phase step refinement, radians | 1.101342e-13 |
| Computed full Fourier primitive norm bound | 0.000693801017 < 1 |
| Independent 80-digit root vs float density, relative | 1.791459e-16 |
| Off-grid compact/remote primitive equation, absolute | 1.886936e-12 |
| Independent collision identity, absolute | 1.818990e-12 |

Coverage: 102 even source nodes, 96 held-out source nodes, original 256-node phase means with 128-node controls, all paired propagated source/time controls; 42 independent high-precision root and implicit-derivative fixtures, 36 off-grid branch primitive checks, and 48 opacity-difference identity checks. No phase required a retry or tolerance change. The independent Fourier controls certify the tested finite representation, not a new continuum quadrature theorem.

## Saved evidence and reuse

For each half/balanced/double family:

- source-even-01: frozen metadata, all correlated node sources/means, independent phase, five complete MTS primitive packets and full source bank.
- preparation-01: original raw/native/normalized data and newly inverted correlated initial mean state.
- source-heldout-01: predictions frozen before independent source evaluation and all 16 held-out nodes for both models.
- evolution-01: fine, coarse source and coarse time propagated full vectors.
- predictions-01: physical outputs frozen BEFORE original perturbation reference comparison.
- comparison-01: original reference and predicted physical channels, density/phase diagnostics and honest gate verdicts.
- independent-01: roots, implicit derivatives, inverse-H mean/primitive controls, sparse hierarchy and collision checks.

audit/result.json checks those sources and predictions, reconstructs verdicts, and compares the preceding preserved failure. start/end receipts preserve exact executed source hashes and worker identities. closeout.json and CLEANUP.json are written only after all work exits and hash checks pass. The prior failed frozen-rho comparison is untouched; it is the diagnostic that led to this derived repair.

## Next physical calculation

Derive and test the remaining mode-weighted averaging correction and reconstructed-background map defect on these SAVED trajectories. For the chosen background the periodic-map residual is

    R = (I+C)^-1 [A C - C Abar - D_slow C].

Keep the nonzero invariant drift and slow-history mismatch separate. Test whether this derived forcing explains the remaining baryon/photon residual without fitting it; then extend the SAME original perturbation farther toward the cold entrance. NEXT.md gives the calculation order. These results establish a successful short-interval approximation test, not a computed trajectory across the remaining early-to-cold gap.

Local only. One below-normal single-thread numerical worker at a time; no subagents, compiler, new app/server or GitHub action. The crash recovery reused the completed source-half-01 receipt rather than repeating its work. The broad research goal remains unfinished; this numerical stage is complete subject to its final seal.
