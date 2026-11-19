# Live memory passes the original signed extraction

10 November 2026. This completes the already-running stage. Martin paused the goal while allowing this calculation to finish; no next-stage work or overnight job is authorized by this closeout.

## What changed scientifically

The earlier 902-node memory test prescribed a saved future rest-perturbation history. This test instead evolves the other species and their memory correction together with the MTS carrier, using only current perturbation states. The original homogeneous background remains the retained native background. The source coupling, physical bank, parameters, original initial state, output grid, signed weights and tolerances are unchanged.

Six full-window streams completed: baseline and MTS, each at three integration/metric-step configurations. Each stream uses four linked batches, for 24 completed batches and 902 unique original epochs per stream (native indices 1991..2892). Shared restart values agree bit for bit, and duplicate boundary rows are excluded from the final extraction. All six streams pass the frozen numerical and candidate gates.

## Signed physical-source results

The ordered triplet is density/current/pressure, using the retained normalization and original signed weights, not measured cosmological observables.

| Source | Native MTS reference | Fine live-memory prediction | Relative difference |
|---|---:|---:|---:|
| Density | -1.0259226340481824 | -1.0259226341710772 | 1.19790e-10 |
| Current | 0.08228092934536191 | 0.08228092934491955 | 5.37615e-12 |
| Pressure | -0.00022500624054024466 | -0.00022500623541830056 | 2.27636e-8 |

The fine uncorrected pressure is -0.0002246665571126751, approximately 0.00150966 relative difference from the native reference, above the unchanged 2e-5 gate. Adding the derived first memory term passes that same test with current-rest feedback. No pressure coefficient was fitted to this target.

The baseline projected density is 59.14012963880835 against 59.140129638808325 (relative 3.60437e-16). Its current and pressure are exactly zero, and the baseline memory correction remains exactly zero throughout. This is the unchanged cold control, not a claim that MTS improves an observational score over it.

## Actual evolution and refinement

Maximum componentwise history-peak-normalized discrepancies for the fine configuration:

| Comparison against native history | Cold baseline | MTS live memory |
|---|---:|---:|
| Native state | 5.83160e-14 | 1.22125e-10 |
| Source/observer readout | 2.56649e-13 | 2.56579e-10 |
| Actual physical evolution derivative | 1.03795e-11 | 1.05565e-8 |
| Coordinate equation residual | 0 | 2.54846e-9 |
| Physical source history | 5.26555e-15 | 2.59273e-10 |

The actual derivative includes the inverse-mapped reduced-equation residual, rather than simply evaluating the exact native RHS at the candidate state. See DERIVATION.md and the saved `actual_physical_derivative` arrays.

MTS signed-pressure relative discrepancies across the three configurations are 2.44513e-7, 3.28196e-8 and 2.27636e-8. The step-refinement comparison is 2.11693e-7 and the metric-step comparison is 1.00561e-8; both pass the unchanged 2e-5 gate. This is numerical stability at the tested resolutions, not an asymptotic convergence proof. The fine error is larger than the earlier prescribed-history result and is reported without substituting that earlier, more favourable number.

The current-rest correction is genuinely nonzero for MTS: its maximum absolute coordinate magnitude is 8.08910e-9 in the retained mixed-coordinate convention. This is not a dimensionless observational effect or a derived galactic population.

## Verification and scope

- Whole-window preflights pass: 393 cold checks and 410 MTS checks.
- Final validation passes 1,796 numerical/restart/readout/refinement comparisons and 3,591 candidate comparisons. These are checks on six numerical streams, not thousands of independent experiments.
- Native full-output parity and original extraction captures are preserved. Selected retained cache entries are unchanged. Source readouts are independently reconstructed from the saved packets.
- Both branches use the same comparison rules. No tolerance, initial state, physical parameter or signed weight was tuned after seeing these results.
- No current-stage worker failed. Earlier derivative-repair failures remain preserved in the preceding stage, not deleted or reclassified.
- This is the original k=1 early-regime extraction with a retained background. The distinct late k=5 native interface and its existing background/averaging contract are the next physical connection, not a result claimed here.

`validation.json` contains every comparison, exact results and packet hashes. Six `*-merged.npz` files contain the verified full streams. The original batch packets and receipts remain intact. `closeout.json` seals the stage; `CLEANUP-VERIFIED.json` records process exits and native-owner release. No task-owned continuing job is authorized.

The inbound NGC3198 conditional-force report is acknowledged separately in GALAXY-RECEIPT.md without redirecting either agent or treating missing geometry or occupation as zero. No Galaxy code, original workbench file, public repository, browser, timer, shared service or unrelated process was changed.
