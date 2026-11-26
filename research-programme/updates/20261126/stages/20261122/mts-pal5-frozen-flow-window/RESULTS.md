> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Palomar 5: the saved late-time interval does not resolve the flow direction

We evolved the forward and conjugate launch states of both retained preparations under the **same** time-dependent ordinary potential. The frozen signs make different streams in this controlled experiment, but not detectably different ones. Across three distance assumptions the biggest progenitor-relative separation of a sampled track point is **0.1273 pc**. Even the largest difference in the line-of-sight velocity gradient is just **0.00566 of its published error**. This verdict applies to the 22.19 Myr contribution under the stated initial conditions; the rest of the stream history was not simulated or set to zero.

## Which history actually counts?

| Archive or experiment | Duration | Fraction of 1.94 Gyr drift time | Fraction of 5 Gyr disruption model |
|---|---:|---:|---:|
| Inherited forward preparation, 544→600 | 1,065.51 Myr | 54.92% | 21.31% |
| Common forward archive for both preparations, 572→600 | 425.18 Myr | 21.92% | 8.50% |
| Same 590 launch tested **both ways** through 600 | **22.1904 Myr** | **1.14%** | **0.44%** |

[Odenkirchen et al.](https://inspirehep.net/files/3329b4b594051c3042f68d6a9524ac72) estimate about 1.94 Gyr of drift for the distant part of their six-degree trailing debris. [Fritz & Kallivayalil](https://doi.org/10.1088/0004-637X/811/2/123) use a 5 Gyr disruption model. Neither duration is a measured age for every tracer, nor the age of the cluster's stars. The earlier common paired archive is a history of **two preparations**, not two current signs for each preparation. The earlier 0.0150 Myr forward flight is not a ceiling on the ordinary drive. The reversed histories over 22.19 Myr are new here; complex conjugating every saved forward frame would evolve the wrong problem.

## Signals versus errors

All 20 sky-track bins in Fritz & Kallivayalil Table 1 are used ([author paper, tables 1–2](https://pages.astro.umd.edu/~rmushotz/ASTRO620/Tidal_GC_2015.pdf)). They have 0.06–0.17 degree track uncertainties, not individual-star astrometric errors. Their published velocity-gradient comparison uncertainty is 0.15 km/s per degree. Observations set coordinates, reference kinematics and error scales; neither direction was fitted to observed residuals.

| At nominal 22.05 kpc | Reset | Coupled/inherited |
|---|---:|---:|
| Maximum positional separation relative to progenitor | 0.0923 pc | 0.1047 pc |
| Largest fixed-RA track displacement in units of that bin's error | 0.000346 | 0.001285 |
| Combined track separation assuming independent errors | 0.000801 | 0.003220 |
| Maximum fixed-RA line-of-sight velocity separation | 0.00332 km/s | 0.00969 km/s |
| Velocity-gradient separation / quoted uncertainty | 0.00176 | 0.00496 |

Across 20.9, 22.05 and 23.2 kpc, the largest individual bin separation is 0.00175 of its error, and the largest diagonal combined separation is 0.00438. These are full forward-minus-reverse differences, not the difference of either direction from an invented observed null. Track bins may be correlated; the diagonal combination is an illustrative error model, not a detection statistic calibrated on a joint survey likelihood. The gradient is a linear summary evaluated over the track-bin footprint, not a recreation of the per-star spectroscopic selection. We do not add the gradient to the positional score as if the inputs were independent.

## What uncertain stripping changes

A separate controlled release tests near-cluster, newly stripped tracers, not the oldest eight-degree debris. In each signed field we launch the same inner and outer offsets relative to its own moving cluster. Test releases are 1.095, 11.095 and 21.095 Myr after snapshot 590. The 10 Myr offsets borrow the **model width**, not measured dates, of the pericentric stripping prescription in [Erkal et al.](https://doi.org/10.1093/mnras/stx1208); we do not identify the middle of the FIRE window as an actual pericentre. Escape offsets and velocities are illustrative and unfitted, not a self-gravitating model of Pal 5. At 22.05 kpc in the outer coupled release:

| Observable relative to the cluster | Largest sign change at the same release | Full change from early to late release (forward) |
|---|---:|---:|
| Declination | 0.00000159 deg | 0.01494 deg |
| Line-of-sight velocity | 0.000140 km/s | 0.2896 km/s |

Even the smaller of the two signs' release-date spans exceeds the largest sign split by at least 1,845 times across these distances, components and tails. This is a sensitivity comparison, not a Gaussian error bar or posterior odds. The old track already exists at the start of our window; we cannot reconstruct its individual stripping dates by shifting a recent test release. Even assuming its starting phase space known, the late contribution is too small in this experiment.

## How it was checked

- Loaded exactly the sealed launch-590 amplitudes from the short flight and the order-64 retained forward preparation packets. Advanced the nonlinear wave and its self-gravity for each sign on the archived 590→600 ordinary drive. Recovered both saved forward endpoint wave arrays with zero numerical difference at the original step count. The opposite signs have identical launch potentials and opposite potential rates. No density normalization, force law, solar alignment, or tolerance was tuned.
- Reconstructed isolated wave potential and gradients from the underlying global finite-element mass distribution (even harmonics through degree 68), including the external and internal multipoles at each evaluation radius. Projected the same ordinary potential that drives the wave. The physically bounded radial interpolation for the stream is 12–29 kpc; it is not an extrapolation of the 5.68–8.88 kpc pulsar bank. Used snapshots of the potential **and its equation-derived time derivative**, not a straight-line extrapolation of the launch jerk.
- Used the source's Sun convention, cluster proper motion/radial velocity and mean velocity gradient with common assumed distance and proper motion across each mock track. Back-propagated the reference track in the sign-average field, then propagated both signs from identical particles. Removed bulk cluster offsets in 3-D position and velocity before sky projection, corrected the declination and velocity differences to fixed right ascension, and used the same present-day observer. This forecasts conditional track motion; it does not independently predict an old stream from its birth or identify FIRE with the Milky Way.
- On first refinement one small near-cluster reset velocity difference changed by 1.43%, above the unchanged 0.5% ceiling. That failure is retained in the tables. Refined the wave time steps and radial sampling again. All 42 final signal comparisons pass; the worst final change is 0.344%. The forward/back orbit round trips close within 1e-9 in kpc and kpc/Myr, and launch parity/occupation checks retain 1e-9. Observation errors and this numerical ceiling are separate.

**Next decision:** the 572→590 ordinary history already exists. Before a longer stream calculation, propagate the two frozen states backward over **one** earlier interval, then forward to check closure, and compare the required earlier states with the archived formation states. This separates a mathematically admissible reverse history from a formation-supported one. Only then extend tracer evolution across a longer window; do not scale the 22 Myr result up to gigayears.

[Protocol](PROTOCOL.md) · [coverage](evidence-001.zip) (archive member: `coverage.json`) · [results at all distances](evidence-001.zip) (archive member: `summary-72-192.csv`) · per-bin signals (not bundled here) · release sensitivity (not bundled here) · all refinements including the failure (not bundled here). Replay locally: run `python -B evolve.py N` for N=1,2,4; `python -B orbit.py N M` for (18,96), (36,96), (36,192), (72,192); then `python -B verify.py`. All runs are single-threaded; conflicting saved outputs are not overwritten. The earlier 36-step diagnostic tables are retained as intermediate results.
