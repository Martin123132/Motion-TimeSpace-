> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Palomar 5: ordinary gravity recovered from the mass source

**The negative enclosed mass was introduced in the representation of the ordinary potential; it is not in the retained mass model.** At the flagged high-latitude launch point we recovered a positive source by two independent integrations. The underlying continuous stellar and gas prescription gives **+0.00105730 solar masses** in the 19.235 pc sphere. The saved positive cells give **+0.00106156** if spread uniformly in each cell's physical volume. These are model masses, not observations of a sphere around the real cluster. The previous field gave **−0.564058**. We also obtained an actual three-dimensional Newtonian acceleration from this source at both sites, without tuning any coupling or selecting an angular cutoff.

## Which source was responsible?

All comparisons refer to snapshot 586, using the same physical location when subtracting the terminal background (snapshot 600). “Reset-forward” labels the second stored launch position, not an added wave term. No wave gravity occurs in these figures.

| Enclosed ordinary mass within 19.235 pc (solar masses) | Flagged launch | Reset-forward launch |
|---|---:|---:|
| Previous terminal background, from surface flux | −0.151053 | +697.770 |
| Previous historical increment, from surface flux | −0.413006 | −20.1014 |
| Previous full represented field | **−0.564058** | **+677.668** |
| Continuous terminal stellar/gas model | +0.000980834 | +565.474 |
| Continuous transferred increment | +0.000076467 | −2.12197 |
| Continuous full model | **+0.00105730** | **+563.352** |
| Full positive cell model, constant within physical volume | +0.00106156 | +563.806 |

The original FIRE gas/star histograms set **group growth factors**, not the Milky Way's absolute local mass. Replaying the archived transfer on sampled original potential nodes agrees to 1.1e−15 relative. The near-side group gains are 1.07796 and 0.996247. The terminal anchor's unclassified interpolation fraction is zero. We retained the original positive mass prescription (including the E3 stellar centre and the S22 stellar redistribution), taper and group gains. Under the continuous alternative the gain multiplies the source law within each group, not a velocity-selected normalization. The 19 pc spheres lie entirely within the constant-gain part of their respective groups and below the taper. Underlying source and transfer (not bundled here) · cell masses including the raw analogue separately (not bundled here) · continuous counts (not bundled here).

**Mechanism.** The old terminal potential keeps angular degrees through 68 and its historical update through 64. Independently apply those two angular truncations directly to the continuous *density*, before doing any radial interpolation. At the flagged site this gives **−19,234** solar masses/kpc³, versus **−18,927** from the original potential and **+35.47** with the density summed directly. The error left between the mixed-order calculation and the native value is 1.62% of the native density bias; it is not exact agreement at the 0.5% threshold. At the positive control the corresponding values are 22.743, 22.722 and 18.770 million solar masses/kpc³. The truncated angular representation alone therefore suffices to create the wrong sign. It is not necessary to posit negative matter or a reversed MTS force. Nor does this attribute *all* the error to angular modes: angular sampling, mass deposition and radial differentiation differ. Increasing the angular cutoff to 256 does not reliably restore positivity. Original component densities (not bundled here) · [independent projections](evidence-001.zip) (archive member: `continuous-angular-projection.csv`).

**Radial representation matters, too.** For the flagged sphere the degree-64 transferred increment gives −0.41965 solar masses with exact finite-volume radial Green functions, but −1.08320 if each radial bin is concentrated at its midpoint. Its direct, untruncated cell values are +0.00007677 and +0.00019888, respectively. At the positive control no radial midpoint intersects the primary sphere at all. An empty midpoint sphere is not evidence that the source density vanished. Independent flux and projected volume integrals agree when applied to the *same* representation. The untruncated counts and the continuous density calculation bypass both ambiguities.

## The force, not just its divergence

Two real-space constructions use Newton's isolated Green function. In the first, the field of constant-density cells reduces to integrals over faces weighted by the density jumps; the azimuthal integral is analytic. In the second, integrate the original continuous stellar and gas law on cylindrical rings, splitting at source knots, taper and transfer boundaries. Compare the full field with the source outside the transfer aperture included; this exterior contributes force but has zero enclosed mass in the two small spheres. The cell-plus-exterior comparison shares the same continuous exterior calculation, so the independent test is of the interior and the increment, not independent exterior data.

| Full acceleration at 586, (km/s)²/kpc | Previous (cylindrical R, z) | Direct continuous (R, z) | Norm of change / direct norm |
|---|---:|---:|---:|
| Flagged launch | (−220.647, −222.887) | (−221.407, −221.971) | **0.380%** |
| Reset-forward launch | (−1980.566, +842.706) | (−1981.916, +810.356) | **1.512%** |

Thus a plausible bulk acceleration at the flagged site coexists with a wrong-sign derivative. For the *smaller historical increment alone* the force-vector changes are larger: **4.70%** and **3.88%**. Do not apply those numbers to the entire galaxy or report the old and new fields as interchangeable.

Gauss's law gives an independent necessity. For ball radius A, the correction in mean outward acceleration must be −G(M_source−M_native)/A²; by Cauchy–Schwarz the rms correction cannot be smaller than the magnitude of that mean. At the flagged site **even zero enclosed mass** requires 0.006557 (km/s)²/kpc of mean inward correction. The retained continuous mass requires 0.006569. A correction that keeps the normal field fixed everywhere on that boundary cannot repair Poisson's equation. This constrains the trace, not all the independent components of the tide. Force comparisons (not bundled here) · source and flux verdict (not bundled here).

## Verification and decision

- All **18** cell-force divergence tests pass the unchanged 0.5% limit, including the weak high-latitude density and signed increment tested against *their own* densities. Worst relative error 0.00401%. Uniform-ball interior/exterior, finite-volume quadrupole, far-field and uniform aperture-volume controls also pass. The first 12-point aperture-volume trial missed the stricter 1e−9 normalization check (1.34e−9); we increased quadrature to 24 and 48, not the tolerance.
- All **36** component comparisons pass 0.5%: order refinement, extending the cylindrical integration from 80 to 160 kpc, final order refinement, and the finite-volume versus continuous constructions. Worst change on the last order refinement 0.0927%; largest cell–continuum component difference 0.0889%. These are local numerical checks, not observational error bars or a proof of global convergence. [Checks](evidence-001.zip) (archive member: `force-accuracy.csv`) · divergences (not bundled here) · [settings](PROTOCOL.md).
- **Next:** compute the full tidal tensor from the source-consistent ordinary field at these two launches, including the shear, not just the trace. Compare its eigenvalues and the already derived initial stellar-work curvature against those from the old host at fixed positions. Only after that check should the force be carried through the orbit and wave evolution on consistent fields. The frozen histories and Pal 5 direction comparison remain intact, not retroactively upgraded.

Local replay: in this directory run `python -B experiment.py`, `python -B direct_census.py`, `python -B cell_green.py`, `python -B continuous_force.py`, then `python -B verify.py`. Each stage is single-threaded and refuses to replace different numerical outputs. [Finite-volume force derivation](CELL-GREEN.md) · [full-force comparison](FULL-FORCE.md) · source provenance (not bundled here) · continuous source provenance (not bundled here).
