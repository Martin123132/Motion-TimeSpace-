> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Palomar 5: a velocity forecast tested on 49 stars, and what survives for the two wave directions

**Decision.** Do not use the fitted 3-D ridge as an exact orbit to assign missing line-of-sight speeds. A velocity forecast made without the target velocities has a 22.59 km/s RMS error. Replacing those forecasts with measured velocities does **not** remove the difference between the two wave evolutions. Its slope is positive for the reset preparation and negative for the inherited one throughout four ways of initializing the same 49 tracers. These observations constrain the stellar initial conditions; they do not select which wave exists in our Galaxy. Direct spectroscopic acceleration at the locations is much too small to break the tie.

## What was predicted and then compared

Use the 17 tail RR Lyrae from [Price-Whelan et al., electronic Table 2](https://doi.org/10.26093/cds/vizier.51580223); the saved cut matches the number of RR tail members and the distant star IDs in [the paper's Table 2](https://arxiv.org/html/1910.00595v2). Use the earlier observer (Galactic Cartesian solar velocity 11.1, 251.3, 7.3 km/s). Infer a mean sky path, distance and proper motion from these stars alone. Our primary distance/declination quadratics in RA and linear PMs are simple empirical descriptions, **not** the authors' rotated-frame population model and not MTS equations.

In local east/north coordinates the derivative of the sightline with respect to RA in radians is t=(cos δ, dδ/dα). Write w=4.74047 D(μ_E,μ_N)+(v_s·e,v_s·n_N), using kpc, mas/yr, km/s. Then a star following the ridge in the inertial Galactic frame would have u=(w·t)/(D|t|²) and heliocentric v_r=u dD/dα−v_s·s, s the unit line of sight. The implementation converts derivatives per degree to match u. The signed normal speed w·(−t_N,t_E)/|t| tests the transverse part without using a measured radial velocity. A zero normal speed would not prove zero radial slip or a stationary ridge.

A synthetic Cartesian trajectory checks the projected formula to 4.3e−9 km/s. In the measured RR sample the normal RMS is 38.36 km/s versus 23.42 km/s RMS for PM measurement errors alone. Only three individual normal speeds exceed twice their PM-only errors: the three outermost trailing tracers at RA 241.73°, 246.06°, 250.34° (−83.5, −71.6, −85.7 km/s; approximately 5.3, 6.7, 5.3 quoted PM errors). Their nominal departures survive supported one-star deletions of the sky ridge. All three lie beyond the last selected spectroscopic RA, 240.342°. This does not establish that the stars are nonmembers, or that the stream has that bulk normal motion; ridge shape, stellar membership, intrinsic dispersion and correlations are not measured by this diagnostic. No exclusions were made on these grounds.

The [preregistered design](PROTOCOL.md) and prediction seal (not bundled here) fixed individual predictions, cuts and controls before decoding the spectroscopic velocity columns. Of 109 published positions, 49 distinct positions were inside the per-arm RR support outside the cluster: 15 leading and 34 trailing, with offsets up to 1.14° from the ridge. The other 60 were not scored. Coordinates were used to locate the predictions; the target PMs and velocities were not used to make them. The [Kuzma et al. catalogue](https://arxiv.org/abs/2202.04548) combines new and historical spectroscopy with kinematic membership cuts. Our previous 5 arcsec match found no objects shared with the RR sample. This is an object-disjoint comparison, **not** a survey-blind test: membership, past literature gradients and older target selection are exposed.

| Frozen sightline forecast | All 49: RMS error (km/s) | Nine exclusively K22: RMS (km/s) |
|---|---:|---:|
| Quadratic distance and sky ridge; linear PM | 22.59 | 14.39 |
| Linear distance instead | 20.78 | 32.30 |
| Cubic distance instead | 30.87 | 53.66 |
| Cubic sky ridge instead | 23.16 | 13.97 |
| Quadratic PM instead | 23.36 | 14.15 |
| Historical velocity gradient, previously exposed | 6.70 | 11.25 |

Primary predicted-minus-measured bias −20.04 km/s; median absolute error 23.22; median reported spectroscopic uncertainty 1.74. RMS error is 12.86 leading, 25.74 trailing. The literature reference is a yardstick, not an equally blind competitor; do not select a polynomial from this table. The primary curve's formal RMS random-input uncertainty is 4.39 km/s (3.55 distance, 2.58 PM); a common 2% distance shift changes the forecast by 3.33 km/s RMS. The shared-input covariance is saved. Deleting any one RR without changing polynomial degree gives 20.17–28.42 km/s RMS on the fixed 49; separate results restricted to still-bracketed positions are in [delete-scores.csv](evidence-001.zip) (archive member: `delete-scores.csv`). Full→half→quarter differencing of the marginal random uncertainties passes the 0.5% check. These are not full errors on a fitted ridge; there is no independent uncertainty for its time evolution, radial slip, intrinsic population depth, or common astrometric systematics.

One can invert the same kinematics after measuring v_r. Without any near-zero denominators, the median distance slope on the trailing arm is 0.187 kpc/deg from the frozen ridge versus 0.096 kpc/deg required by the spectra **if** the ridgeline motion and tangency assumptions are right. The median paired change is −0.092 kpc/deg. The new leading-only K22 subset gives a much smaller median paired change, −0.014 kpc/deg. This identifies the distance derivative or relative stellar motion as a real uncertainty, not a measured new distance law. Source-resolved errors, input uncertainties, shared covariance, required slopes and all frozen positions remain in the CSVs.

## Does using measured motion erase the two-direction response?

No. After scoring the forecast, [a separate conditioning experiment](CONDITIONING.md) used the spectra as initial-state information. At the same 49 actual sky positions, use RR ridge distances (not independent distances to these 49 stars), identical cluster registration and original field and time grids over the same 111.158776 Myr. Both signs start from the same inferred state backcast in their mean field, for each preparation. Nothing is fitted to favor either direction. These are repeated calculations on a Galactic analog, not integrations of a known Milky Way wave.
 
| Shared inputs to both signs | Reset | Inherited |
|---|---:|---:|
| Tangent LOS, smoothed RR PM | +0.02537 | −0.03518 |
| Measured LOS, same RR PM | +0.04005 | −0.05142 |
| Measured LOS **and** stellar PM | **+0.04164** | **−0.06208** |
| Historical LOS gradient, same stellar PM | +0.04528 | −0.06464 |

Units: km/s per degree, gradient of raw forward-minus-reverse same-star LOS differences across the original RAs. After the common historical fixed-RA correction, the fully measured-motion row is +0.04696/−0.07215. The RMS raw velocity differences in that row are 0.206/0.337 km/s; largest 3-D model separations 66.9/85.4 pc. The 112 field/orbit refinements pass the unchanged 0.5% limit (worst 0.0112%), every mean round trip <2e−13 and no radial extrapolation. Velocities used for conditioning are **not** then scored as predictions. With those velocities supplied, the uncertain release times, distances, host and wave preparation remain. In particular neither the increased separation nor the different signs across preparations imply observed flow direction.

## Independent route: observable local gravitational acceleration

For any of these sightlines, d(v_r)/dt=s·(a_star−a_sun)+|v_rel,perp|²/D. Compare fields at exactly the same present position and velocity; the perspective term cancels and so does the common ordinary source. The saved late radial grid does not include the Sun. Instead of extrapolating to it, project the 49 sightline components off the 3-column matrix of sightline unit vectors. This cancels **any** common observer acceleration; a further independent column removes a constant zero-point drift. This is the Newtonian limit evaluated on the two actual frozen wave potentials, not on the fitted velocity slope. Conditional on the sky positions and distances it does not require a chosen LOS stellar speed or stripping time.

Ten-year first-order RMS **whole forward-minus-reverse** difference in spectroscopic velocity (mm/s):
 
| Observer treatment | Reset | Inherited |
|---|---:|---:|
| Raw stellar terms; solar contribution not known | 0.0183 | 0.0331 |
| Remove arbitrary observer acceleration | 0.0000806 | 0.000297 |
| Also remove common instrumental drift | 0.0000199 | 0.0000732 |

Removing the observer eats most of the difference on the limited sky footprint. With two hypothetical independent epochs at the quoted single-epoch errors, the weighted separation of the two alternatives after observer removal is only 4.11e−10 / 1.46e−9 in noise units over a decade (half these for one sign against their midpoint). This is not an actual acceleration measurement or a constraint on all other streams. The scalar-potential derivative along each sightline reproduces the independently evaluated LOS acceleration, and coarse/fine checks pass on the small residual itself. All 20 drift checks passed. The ordinary projected components, singular-value condition numbers and precision-weighted templates are saved.

## Next physical step

Use the **tidal acceleration across the progenitor**, not its bulk acceleration: derive the local differential tensor from the same potentials, compare against finite separations and the ordinary host alone, then calculate where stars can escape under each wave preparation. Start from an independently constrained cluster mass/size. On an eccentric orbit, an instantaneous stretching scale is not an escape-time distribution; retain frame rotation, moving boundaries and competing escape/recapture if carrying that calculation into releases. This tackles the stripping uncertainty that dwarfed the sign shift without tuning a release time to favor it. Do not pursue a decades-long spectroscopic drift on the strength of this test.

Private, offline replay: freeze.py → compare.py → wave.py → drift.py → verify.py, all using the older sealed inputs and one numerical thread. No new publication, halo fit, or modification of old checkpoints.
