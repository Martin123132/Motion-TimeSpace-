# The source-integral discrepancy is not a final-subtraction artefact

## Concrete advance

We derived the native observable covector a=T^-T lambda and evaluated the retained first-cell source through it at all257 saved points for baseline and MTS, both metric branches. We then derived and tested the exact unequal-background difference equation for the metric time-shift coordinate alpha. No new source bank, native call, physical history, coupling, grid or tolerance was introduced.

This closes two specific proposed numerical repairs: neither higher-precision subtraction/reduction of the saved rates nor the derived alpha-only cancellation law resolves the remaining MTS integration discrepancy. The algebraic alpha law remains useful; its proposed role as the present accuracy cure is rejected by calculation, not by assumption.

## Saved-rate arithmetic

At all514 points, TwoDiff finds no discarded subtraction low components. Compensated dot products agree with200 exact rational full-contraction spot checks. Maximum dual-map residuals are9.480e-16 for MTS and3.159e-16 for baseline; source-contraction backward residuals are3.011e-15 and1.879e-15, below the unchanged1e-10 gate.

| Diagnostic | MTS | Baseline |
|---|---:|---:|
| Largest compensated integral change / old source budget | 1.127759428102418e-15 | 4.437950032122359e-17 |
| Largest compensated change / old physical reference scale | 3.173739032102091e-23 | 4.338272819872424e-31 |
| Unit-roundoff native-rate-input sensitivity range | 3.4010e-11 to5.5734e-8 | 0.0022371 to0.4850774 |
| Post-subtraction dot-product arithmetic estimate, maximum / budget | 7.1798e-12 | 1.4108e-12 |
| Separate conservative product-underflow allowance / budget | 1.268e-309 | 1.365e-303 |

There are many subnormal products in the retained high-order hierarchy:1765996 in the MTS diagnostic and491938 in baseline. They were counted rather than discarded silently; the additional allowance above and exact spot checks show why these do not explain the observed discrepancy.

The input-sensitivity row is a CONDITIONAL benchmark for independent relative rate perturbations of one binary64 unit roundoff, holding the computed covector fixed. It is not a measured native error and not an error bound for the native solver. In particular, the tiny baseline source is highly conditioned with respect to rate input errors. Precision applied after those inputs have already been generated cannot recover their missing information. MTS's benchmark is much smaller, but we have not certified its native rate-input errors either.

## A derived physical difference, tested rather than assumed

The authoritative native equation is alpha_N=Psi/H-alpha in physical coordinates. At fixed encoded input and unchanged unit U_alpha,

    Delta r_alpha = [mean(1/H) Delta Psi + mean(Psi) Delta(1/H)] / U_alpha,
    Delta(1/H) = -(H_ref-H_ret)/(H_ref H_ret).

The common -alpha term cancels exactly. This alpha is the metric time-shift variable, not the electromagnetic fine-structure constant. Both gravity branches obey this equation with their own potentials.

All2056 individual native metric rates agree with the equation; maximum backward errors are2.316e-16 MTS and2.735e-16 baseline. All1028 paired product-difference identities pass exact rational arithmetic on the saved inputs. The derived alpha-only correction is propagated through the same saved adjoints and unchanged257/129 quadratures.

Largest projected changes are9.7992e-11 of the old source budget for MTS and0.0103495 for baseline; on the old physical reference scales they are only1.3823e-19 and2.2090e-19. MTS still has10/20 integration pairs passing and baseline0/20. MTS maximum signed-integration and budget changes remain8.9272e-5 and1.3831e-4 against2e-5. The candidate is a diagnostic, not a replacement source silently promoted to accepted status.

## Where the remaining work lies

Local panel differences reproduce the global refinement changes. Ninety percent of their absolute sum occupies41–45 of64 panels for MTS and41–47 for baseline. This is not a single isolated spike suited to one tiny patch. Significant cancellation among coordinate contributions is real, but the accurately accumulated source reproduces it rather than curing the quadrature discrepancy.

The next useful numerical test is one frozen513-point extension reusing all257 accepted points, not another current-history timestep reduction or repeated post-processing precision pass. Keep the unchanged pass criteria. If that extension still lacks a credible refinement trend, stop global doubling and inspect the native background/source interpolation structure. The baseline conditioning must remain visible in either outcome. This is a numerical decision within the retained GR/Newton response calculation, not a new cosmological fit.

## Evidence and scope

Accepted evidence: balanced/conditioning-01/result.json, balanced/metric-difference-01/result.json, audit/result.json, DERIVATION.md and METRIC-DIFFERENCE.md, relative to this directory. Original source packets remain in the sealed phase-response stage. The audit checks514 points,200 exact dot products,1028 metric difference identities,2056 individual metric rates and40 output/branch rows. All three owned calculations exit normally; final receipts and artifact hashes are in CLEANUP.json and closeout.json after sealing.

This remains the first original cell of the balanced family projected to the saved final epoch. The remaining interval, other wave families, output-map, bridge, response-feedback and inherited terms stay in the larger objective. Original gates, source banks and physical grids are unchanged. No GitHub action.
