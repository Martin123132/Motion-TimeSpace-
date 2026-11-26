> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Finer gravity step resolves the 70.4 Mpc lapse-center sensitivity test

**24 November 2026 · Private.** Reran both the cold baseline and the heavy MTS preparation from their identical-to-prior 57.6 Mpc states through 64.0 and 70.4. Only the inner gravity time step changed. The motion of the signed lapse target between successive refinements dropped by a factor of **7.98**, from **2.9291** to **0.3669** of its one-term peak allowance. This meets the discrete resolution test that failed at the previous pair of steps. It is not a bound on the exact continuum answer or on the later physical matter source.

| Diagnostic for the MTS-minus-baseline mode | Larger → previous step | Previous → new step |
|---|---:|---:|
| Movement of the remaining lapse target, in lapse allowances | 2.92913 | **0.36692** |
| Movement of the remaining current target, in current allowances | 0.011960 | **0.001493** |

| Integrated curvature-rate discrepancy, in lapse allowances | 0.0015625 Mpc | 0.00078125 Mpc | 0.000390625 Mpc |
|---|---:|---:|---:|
| 64–70.4, baseline | 0.05474 | 0.05474 | 0.05474 |
| 64–70.4, MTS | 1.92403 | 0.27271 | **0.06882** |
| 64–70.4, signed MTS minus baseline | 1.88543 | 0.23388 | **0.03066** |
| Both blocks together, signed | 2.90435 | 0.35879 | **0.04811** |

The baseline has a small residual that is insensitive to this change of gravity step. We have not identified its origin or set it to zero. The signed result is evaluated on one common clock and kernel, not by subtracting the magnitudes in the first two rows. A separate integral using potential values and endpoint terms, without differentiating the curvature spline, agrees with the fine signed second-block result to within **0.00000040** of one lapse allowance. The measured change in curvature-rate discrepancy accounts for 0.19532 of the 0.36692 shift along its actual direction; the inherited state accounts for 0.11727, current work for 0.05481, shear for −0.00048, and the other contributions are negligible at this scale.

**The physical interpretation survived.** At the saved 273.33232 Mpc target the contribution from 64–70.4 reduces the magnitude of the future lapse cancellation required by **4.3054%** and increases the required current cancellation by **0.1078%** (previous gravity step: 4.3039% and 0.1076%). The new required signed centers are \((1.3098073-2.5746117i)10^{-13}\) for lapse and \((2.4692271-5.0479108i)10^{-16}\ {\rm Mpc}^{-1}\) for current. These are targets for the remaining production after 70.4, not a measured late-time lapse or photon spectrum.

**Verification.** The physical source inputs are the four sealed model/block banks, each with its same common source and 77 finite-momentum packets, original material grid, angular hierarchy, unchanged stress iteration and 0.5% tests. All **48 trajectory, 66 integration, and 72 time-step comparisons** passed, as did **27 absolute diagnostic cross-checks**. The 72 include both successive pairs of time steps. Largest relative discrepancy among the three groups was 0.192%, including the old control; integration and reconstruction checks on the new histories were within 0.00230%. No fitting, new observations or new physical interval. [Decision](evidence-001.zip) (archive member: `decision.json`) · [rate diagnostics](evidence-001.zip) (archive member: `rate-defects.csv`) · [complex step comparisons](evidence-001.zip) (archive member: `step-comparisons.csv`) · method (not bundled here) · [validation and source fingerprints](evidence-001.zip) (archive member: `validation.json`).

**Next:** advance the physical source from 70.4 to 76.8 Mpc using the new fine restart for each model and the previous-step restarts as controls. Carry the signed current and lapse work and recheck the absolute target movement at the same peak before accepting another interval. The new fluid and 77-bin gravitational restarts are in `to70/`; common and individual incident endpoints remain in the sealed prior stage, not in this directory. No push or external handoff.
