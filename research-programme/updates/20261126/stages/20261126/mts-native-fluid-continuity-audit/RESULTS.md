# What caused the 17 fluid–wave discrepancies?

The retained model predicts the signed difference between the heavy fluid and the projected coherent wave over the 11 supported centers, η=89.83125–89.89375 conformal Mpc. After putting both sides on consistent numerical clocks and evolving the ordinary massive-neutrino energy and current together, **all 782 modes pass separately in energy and in longitudinal current**. No coupling, preparation, amplitude or tolerance was fitted. This checks a short-window internal prediction on saved cosmological histories. It is not a comparison with observed photons and does not replace the separate photon calculation.

## The test and its controls

- The forecast starts at 89.275 Mpc. Post-cutoff native fields are used only as reference data and in a separately labelled crossed-driving diagnostic. This is a repair on an already investigated window, not an independent empirical holdout. All-mode forecasts were frozen before scoring each proposed repair.
- Each error is the largest absolute difference over the 11 centers divided by that mode's peak absolute reference contrast over those centers. No mode was discarded. The tolerance is 0.5%. Retaining the previous stage's denominators also gives 782/782 in both channels.
- The original archived comparison, undisturbed: 769 energy passes and 778 current passes, with 17 distinct exceptions. Native integration on those 17 and 17 prespecified passing neighbours satisfies both continuity and momentum. An independent calculation subtracting cold matter as a tracer of the gravitational work agrees on all 34. A denser solver-output schedule alone can move one very small current contrast by more than 1%; it is not a superior observational reference.
- The native event surface is a common physical scale factor. Different native integration blocks locate it at slightly different numerical times and sample slightly different scale factors. Using the stored event times and each mode's scale factor, including its use in the reference stress units, recovers all energy modes. It leaves three current misses, not simply a subset of the old failures. A conditional replay with the later measured perturbative metric source explains approximately 99.8–100.1% of those signed residuals. It diagnoses the error but is not the predictive repair.

| Matched preparation, 782 modes | Energy passes | Current passes | Worst energy error | Worst current error |
|---|---:|---:|---:|---:|
| Correct clock and normalization; old trace tangent | 782 | 779 | 0.0429% | 1.6635% |
| Correct clocks; evolve massive-neutrino energy and current | 782 | 782 | 0.00368% | 0.18415% |

For the three remaining current modes (k=0.93567, 1.06784, 1.49034 per Mpc), errors fall from 0.56887%, 1.66345%, 0.60945% to 0.00816%, 0.07542%, 0.18415%. Halving the integration step, changing the early derivative stencil, or holding the shear constant leaves every total-contrast test passing. None of these choices was selected by minimizing the error.

## What changed physically?

The old gravitational driving extrapolated the entire massive-neutrino active density A=(D+3P)/2 in a straight line. Instead set A=D+T, where T=(3P−D)/2. With the native rescaling and synchronous clock, conservation gives

    D′ = −2H(D+T) − kJ − (G+p)X
    J′ = −2HJ + k[(D+2T)/3 − S].

D, J are the rescaled massive-neutrino energy and current perturbations; G,p are their background density and pressure. X is the scalar metric driving, S the effective longitudinal shear. Only the small residual trace, background mass trace and shear use short-time values and slopes inferred at cutoff. See NEUTRINO.md for units and conventions. The gravitating matched heavy fluid, ordinary matter and metric evolve together; the coherent wave probes that same geometry without being counted twice.

The following comparison uses the same native modes, cutoff, equations and end time **on both** the heavy-free cold comparator and the matched MTS preparation. Each predicts its own geometry autonomously from earlier data. The end of the available cold bank is 89.65 Mpc; do not extrapolate the cold result to the later 11-center test or manufacture a heavy-wave contrast for a heavy-free comparator. Errors here are peak absolute errors divided by the peak *change* across the common time window and all modes, not per-mode pass rates.

| Preparation | Active-density error, old → new | Gravitational-driving error, old → new | Effective shear tangent error |
|---|---:|---:|---:|
| Cold | 34.7548% → 1.2890% | 0.006433% → 0.000706% | 38.81% |
| Matched MTS | 34.6654% → 1.2852% | 0.004029% → 0.000443% | 38.61% |

The shared improvement identifies an ordinary-matter modeling issue, **not an MTS advantage over the baseline**. The matched short calculation independently reproduces the corresponding longer forecasts on the overlap. The reference shear is inferred from native momentum balance, not a direct measurement of an angular multipole.

## Where the approximation breaks first

On the longer matched history to 90.45 Mpc, the peak error in the change of active density falls from 99.91% to 35.59%, not to zero. The massive current change still has a 30.91% error. The approximate shear is a concrete next candidate; these diagnostics do not establish it is the sole source of error.

The *new change* in the contrast during the 11-center window is smaller than the inherited contrast. On its own denominator, one energy mode (worst 0.5591%) and two current modes (worst 1.1491%) still exceed 0.5%. The old trace had two and five misses, respectively. Passing the total-contrast test does not erase this result or the earlier failed full-window photon substitution (~35.27% of its original reference).

Next: obtain the massive species' shear evolution from the collisionless angular and momentum hierarchy, or bound its contribution using those equations. Freeze the resulting correction and uncertainty, then propagate them to the saved photon energy and current at both gravity steps. Judge it on the original photon normalization; do not fit the three small drift residuals.

## Reproduction and provenance

- PROTOCOL.md, CLOCK-REPAIR.md, CURRENT-DIAGNOSIS.md and NEUTRINO.md describe the staged decisions. The corresponding JSON receipts pin the methods, source inputs and predictions. The corrected and legacy reference definitions are both retained.
- native-balance-scores.json and clock-scores.json record the clock controls. source-repair-all-modes.csv and neutrino-scores.json contain the mode ledger and all drift and source diagnostics. paired-scores.json records both same-window controls including native derivative sensitivity.
- Run verify_stage.py using the retained Python environment to verify this directory and upstream receipts. Replaying paired_source_control.py requires the stage's existing native banks; run its forecast action before its score action. These files are not a stand-alone survey dataset.
