> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Boundary-adapted source variables now evolve with live gravity

Private retained-parent calculation, 2026-11-10. The original 65 output times (indices 2892 through 2956), background, field parameters, scattering bank, active caches and numerical acceptance gates are unchanged. This is a new integration in derived source coordinates, not a replay of saved future perturbations.

## What was achieved

The two heavy-field source coordinates WD and WQ replace four constrained heavy moment entries while retaining their two physical degrees of freedom. Each current state reconstructs the physical perturbation through the derived regular inverse; the native equations then evolve gravity and all retained species together. The slow-field moment block remains unchanged. No phase mode or derived history term is discarded.

The heavy branch has 185 active native coordinates, 189 phase coordinates and 187 source coordinates. The baseline has 182, 184 and 184 respectively. These are representation sizes, not counts of independent physical degrees of freedom. The baseline uses its actual cold component rather than a fictitious heavy oscillator.

Both captured and independently projection-reconstructed initial states were evolved. Each has three configurations separating integration-step refinement from local metric-derivative refinement. All twelve accepted runs pass the unchanged gates. Independent verification recomputes 15,828 component comparisons from saved packets; this count is not a count of independent physical experiments.

## Numerical results

Worst component-normalized discrepancies against the retained native reference, reconstructed start, finer integration and metric-derivative steps:

| Quantity | Baseline | MTS heavy branch |
| --- | ---: | ---: |
| Active native state | 1.37022e-14 | 1.78324e-11 |
| Native readouts | 1.32068e-13 | 5.56008e-11 |
| Native state derivatives | 3.26439e-12 | 2.92718e-9 |
| Source coordinates | 1.52931e-14 | 5.56906e-11 |
| Physical phase coordinates | 1.52931e-14 | 1.78325e-11 |
| Nine selected active cache entries | 0 | 0 |

Normalization is by each reference component's peak over this window, as specified in the retained comparator. These are numerical equivalence errors, not observational uncertainties or fit improvements. The evolution comparison gate remains 2e-5 and the algebra gate 1e-10.

The reconstructed heavy derivative discrepancy decreases from 4.07311e-8 to 2.92718e-9 when the integration maximum step is halved. The separate metric-step refinement and captured-versus-reconstructed comparisons also pass. Baseline rounding-floor results are not presented as monotone convergence.

The independently assembled product-rule and full tail expressions agree: the fine reconstructed heavy tail-identity discrepancy is 8.97028e-13. Quantitative rest-to-metric feedback, heavy feedback, coordinate reconstruction and the physical rank-one moment identity pass. The finest trajectory's maximum energy-scaled inverse condition number is 1.0005641. The actual background crosses both a field sign and a velocity sign once. Separate exact-zero field/velocity algebra controls recover the perturbation at retained positive energy; these synthetic instantaneous controls are not additional cosmological solutions.

## Preserved failure and diagnostic repair

The original heavy attempt stopped at its independent coordinate-difference preflight, before integration. Its smaller check step gave 5.32965e-5, failing the unchanged 2e-5 gate. That failed receipt remains intact; it is not counted as a successful original preflight.

A separate six-step diagnostic found both large-step truncation and small-step evaluation/subtraction sensitivity. Two intermediate coordinate-check steps, span/1024 and span/2048, were then frozen and checked for both branches. Their heavy WD discrepancies are 1.99995e-6 and 7.65663e-6. These are refinements of an independent numerical checker, not changes to the physical evolution. The accepted heavy output is separately named `heavy-source-state-balanced-check`.

The physical metric-derivative steps remain span/4096 and span/8192; their mutual discrepancy is approximately 1.04e-8. No physical coefficients, integration settings, source histories, grids or tolerances were changed by the checker repair. Completed baseline integrations were reused. See STENCIL-DIAGNOSIS.md and balanced-check-contract.json for the retained diagnostic evidence. The chosen diagnostic interval is supported by this finite scan, not a certified continuum error bound.

## Derivative and interpretation boundaries

The native interface does not export H' and z'. Their partial time derivatives are evaluated locally at fixed current state, plus the exact linear state-direction contribution to z'. No saved future perturbation/metric history enters the evolved right-hand side. This is a checked numerical derivative implementation, not a newly exact native derivative port.

The homogeneous background remains the retained background. This calculation establishes a usable exact source-coordinate representation on the tested live interval; it does not select primordial or galactic occupation, activate the old averaged selector, or demonstrate that the fast component can be removed. All correction terms remain explicit. The sufficient regularity assumptions are recorded in DERIVATION.md and the preceding memory-budget derivation.

## Next derivation

Derive the slow difference-frequency and fast sum-frequency normal form directly from the retained quadratic field equations. Determine the current normalization and its relation to the existing late-carrier sound-speed coefficient before restoring expansion, gravity and representation terms. Then connect the original signed source extraction to the actual late selector/background, controlling rather than silently deleting the fast contribution. NEXT.md gives the ordered calculation.

## Provenance and ownership

Read validation.json for recomputed comparisons, frozen-inputs.json for input hashes, the two accepted result files for run receipts, and closeout.json/CLEANUP-VERIFIED.json after sealing for artifact integrity and exact process exit checks. All prior source hashes are checked during validation and sealing. The original failed heavy receipt remains part of the record.

[Operational or machine-specific passage omitted from public reading copy.]