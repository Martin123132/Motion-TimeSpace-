# The incoming angular distribution predicts the shear; photon feedback closes the heavy drift test

Starting at η=89.275 conformal Mpc on the retained cold and matched MTS backgrounds, propagate the five massive-neutrino momentum nodes instead of extending their shear along its initial tangent. Evolving the photon intensity and polarization in the same gravitational field also removes the last failing mode of the heavy fluid–wave **change** test. No new coupling, amplitude, phase, tolerance or fit. These are internal predictions on previously investigated histories, not an independent sky detection.

## Where the shear was hiding

The incoming quadrupole gives the stress. Its *rate* depends on streaming out of, and into, the neighboring angular moments. In particular it depends on the octupole; density and current alone do not specify it. With the actual incoming moments and metric, the derived shear rate agrees with the native derivative to 0.000158% (cold) and 0.000154% (matched), relative to the respective global peak derivative. Removing the octupole term gives 73.82% and 73.67% errors. The signed terms and conventions are in EQUATIONS.md and the two shear-drive packets.

A temporary readout of the original solver recovered the starting multipoles; a separate post-forecast readout integrated pressure and shear directly over the native momentum nodes. The latter is independent of the previous practice of estimating both from derivatives of larger stresses. Native density and current provide cross-checks against the bank on every mode. Both private executable copies and temporary drive mappings were released; the installed solver and bank stayed unchanged.

| Peak error on the *change* in directly measured native shear | Initial tangent | Collisionless equations |
|---|---:|---:|
| Cold, 89.275–89.65 | 38.8126% | 0.0001664% |
| Matched MTS, same window | 38.6140% | 0.0001631% |
| Matched MTS, through 90.45 | 100.7872% | 0.0010031% |

Here “directly measured” means recorded from the numerical reference, not a telescope. Each percentage in this table is a maximum absolute error divided by the maximum absolute **change** over all modes and epochs. Both the primary angular calculation and the 16-moment and half-step controls are retained. BOUND.md also derives a conditional limit: on fixed geometry the gain from an uncertain outer angular boundary to the quadrupole over the longer window is at most 0.001511 for L=12 and 0.00000269 for L=16, times the unknown boundary amplitude. This is not an absolute bound on gravity or photons.

## What reached photons?

On the longer matched history, evolving the neutrinos while retaining a photon-shear tangent still left **354 photon-density and 567 photon-current changes** outside the original 0.5% mode-by-mode tolerance. With gravity held at the same prediction, evolving photon intensity and polarization to quadrupole order eliminated all density misses and left one current miss. Evolving their octupoles as well eliminated that last miss. The fourth-moment forcing was reconstructed from the early derivatives and carried on a tangent; it was not read from future data. On the cold control the same intervention takes the number of current misses from 197 to zero. The direct native derivative control shows that neither branch is in its tight-coupling approximation in these windows, and the summed photon–baryon momentum balance agrees to below 5e−14% on the global-peak scale.

Finally return the predicted photon density and current to the gravity equations at every internal step, rather than treating photons as passive probes. The revised calculation counts their stress only once. Both temporal resolutions pass.

| Fully coupled forecast | Modes passing density / current *changes* | Worst individual density / current error |
|---|---:|---:|
| Cold, through 89.65 | 782 / 782 each | 0.000217% / 0.00366% |
| Matched MTS, through 90.45 | 782 / 782 each | 0.00321% / 0.01826% |
| Matched minus cold, both through 89.65 | 782 / 782 each | 0.000361% / 0.00449% |

In this table the denominator is **each mode's own** peak absolute reference change in the specified channel, including for the matched-minus-cold comparison. The difference is formed first. On the common interval, the peak change of that difference is about 0.535% (photon density) and 0.684% (current) of the corresponding peak cold-only change. These are transfer functions on one retained preparation, not a claim about observable sky significance.

## The heavy-wave test, without changing its denominator

On the matched preparation's 11 supported centers (89.83125–89.89375), all **782/782** full energy and current contrasts still pass, even on the old denominators. Before revising either angular sector, the smaller change during the window missed one energy mode and two current modes. Neutrino evolution alone left one current miss (0.7512%). With photons coupled back into gravity, the change passes **782/782 in both energy and current, on both steps**. The coarser/finer worst energy drift errors are 0.02064% / 0.02890%; current 0.00637% / 0.00639%. The finer result need not have the smaller maximum because the small native-reference and solver errors also enter. Independently re-evolving the matched fluid on its predicted metric reproduces the simultaneously evolved fluid to <0.00004% of its original contrast denominator.

## What to carry forward

These are first-order species, their coupled metric, and a projected wave consistency test. They are not the second-order, scattered visibility readout, and neither of the two integration resolutions is the historical p16/p32 gravity route. The earlier ~35.27% photon-gap failure from directly replacing the complete stress is still on record. The new numbers justify moving to that observable rather than refining these same 782 mode scores again.

Next: on the overlapping post-cutoff interval, construct the **signed quadratic source difference** from the corrected linear fields on the retained Fourier triangles. Include the synchronous-to-normal metric terms and the compensating current/energy memory. Pass the incremental correction, not the entire instantaneous stress, into the two existing gravity/visibility routes; preserve the prior history and entry kick, and score the actual photon energy and current at both p16/p32 steps against their original joint normalization. Do not fill unsupported time ranges with a fitted continuation.

## Reproduce or inspect

- DESIGN.md, EQUATIONS.md, PHOTON-TRANSFER.md, FEEDBACK.md and BOUND.md give the model and controls. The imported standard physics is identified separately from the MTS application.
- snapshot.json, kinetic-forecast.json, transfer-forecast.json and feedback-forecast.json freeze the inputs and outputs by stage. native-truth.json records the separate direct readout. No halo or sky data are fitted.
- physical-readout.json separates direct stress references, inferred references, passive photon responses and collision controls. feedback-scores.json includes the signed inter-branch comparison; feedback-mode-checks.csv contains per-mode branch and heavy drift results.
- Run verify_shear.py in the retained environment for integrity and numerical checks. The manifest covers the local restart including numerical caches; it is not a request to distribute binaries or machine-specific records.
