# Predictive memory closes the saved pressure test

10 November 2026. This continues the retained carrier normal-form and phase-drift calculation; earlier checkpoints and failed controls are unchanged. Previous goal turn: verified progress. This turn implements and propagates an equation-derived correction, rather than fitting the known pressure discrepancy.

## Derived and executed

The candidate is y1=y0+delta1, with y0'=B y0+f and delta1'=B delta1+R y0+g. The new correction starts exactly at zero. R and g come from the current primitive-to-normal-to-phase coordinate maps and their derivatives. There is no new free coupling, state amplitude, pressure parameter, mass, data fit or output weight. The explicit coefficient construction is in DERIVATION.md and memory_model.py.

The separate error transport obeys e1'=(B+R)e1+R delta1. Its input is also derived from the candidate, not from an exact-reference residual. It is used only for checking the truncation error; it is NOT added to the candidate. Four exact symbolic identities verify the memory/error equations without assuming commuting operators. Preflight includes 136 numerical coefficient/chain-rule/initial/independence checks at nodes and between nodes.

Twelve integrations completed: actual cold/CDM and heavy/MTS, two retained time windows, and three fixed step/history configurations. The original 65/902 output nodes, bank, physical parameters, 2e-5 numerical and 1e-10 algebra gates, signed weights, solver tolerances and initial normalization convention remain unchanged. Integration stops at the existing Hermite knots. No native rebuilding or observational fitting occurred.

## Previously failing signed-pressure projection

Fine dense-history MTS results on the original 902-node extraction:

| Quantity | Native target | Corrected candidate | Relative error |
|---|---:|---:|---:|
| Density | -1.0259226340481824 | -1.025922634371176 | 3.14832e-10 |
| Current | 0.08228092934536191 | 0.08228092934503484 | 3.97506e-12 |
| Pressure | -0.00022500624054024466 | -0.00022500624039748169 | 6.34484e-10 |

All three now pass the unchanged 2e-5 relative gate. The old pressure discrepancy was 0.00150966 relative (0.150966%); its uncorrected control is reproduced, not overwritten. The new fine pressure absolute discrepancy is 1.42763e-13 in the retained source normalization.

The smaller-step and sparser-history checks also pass. Pressure relative error is 6.36300e-10 for dense-step1 and 2.72512e-6 for sparse-step2, versus 6.34484e-10 for dense-step2. The larger sparse-history difference demonstrates that interpolation/history uncertainty must not be confused with the tiny fine conditional-reduction error. This is a passed fixed-tolerance test, not evidence that the physical cosmos has been predicted to ten decimal places.

The actual cold baseline also passes. Its fine projected density is 59.14012963880834 against 59.140129638808325; the retained dust current and pressure readouts remain zero. No artificial scalar correction is assigned to that branch.

## Instantaneous histories and error transport

The fine MTS candidate's history-peak-normalized primitive errors against the saved native data are (7.70629e-12,1.26502e-11) on the 65-node interval and (1.11119e-10,1.08047e-10) on the 902-node extraction. Density/current/pressure source errors are respectively (7.88679e-11,7.51240e-12,1.20623e-11) and (6.08667e-10,5.78803e-11,1.13445e-10). These all pass, alongside their step/history refinements.

Against the exact conditional reference, the remaining fine density-source history error is 1.14588e-12 on the short interval and 2.13563e-11 on the extraction. On the extraction, the final two-coordinate measured residual is approximately (2.25044e-11,1.85060e-13), while the independently driven error transport gives (2.24931e-11,1.85981e-13). The strict reconstruction check uses the original coordinate scale and passes at 1e-10; it is not a relative-accuracy claim on each tiny residual itself.

The numerical componentwise envelopes enclose sampled errors, with the retained algebra-scale allowance. Their values are not converged at 2e-5 across the tested refinements. No certified numerical bound or observational uncertainty bar is claimed. The analytical comparison inequality and its assumptions are stated separately in DERIVATION.md.

## What this establishes

The saved conditional pressure discrepancy is repaired by the first explicit memory response from the existing equations. The same correction also preserves density/current and the actual baseline controls. The independently regenerated readouts and original signed projections are checked separately in packet-audit.json. validation.json records 144 numerical replay, error-transport, refinement and independence comparisons; candidate pointwise and projection gates pass for all configurations.

The background/rest histories are still prescribed. Constructing the saved rest source uses the original full state and subtracts its heavy density contribution. Mutation independence is checked AFTER that history is constructed: future comparator perturbations do not enter the evolving candidate, but this is not an independent all-species cosmological forecast or a new observational fit. No speedup, arbitrary-background theorem, population prescription or replacement of the old late selector is claimed.

## Concrete next coupling

CURRENT-STATE-MEMORY-LIFT.md derives the full current-state block operator and its remainder. The remainder has zero direct rest rows, but the correction to rest species is generally nonzero through the original heavy-to-rest coupling. Thirteen symbolic block identities pass; these check the algebraic interface, not a completed native coupled evolution. The next task is to implement and test that interface using CURRENT native source constraints and background, with the exact trajectory retained only as comparator.

All work stays in this new private stage plus the resume bookmark. No Galaxy files, browser, relay, public repository, unrelated process or shared service is changed. Worker ownership and final exits are recorded in CLEANUP-VERIFIED.json.
