> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Palomar 5 with measured stellar distances and proper motions

The earlier sign pattern survives replacing uniform geometry by actual RR Lyrae distances and proper motions **at the historically measured line-of-sight gradient**. The velocity difference shrinks; the sky pattern changes shape, rather than simply shrinking. The two directions have not been distinguished with observations. This experiment conditions the trajectories on present-day data and forecasts *differences*; the unmeasured starting velocities still matter.

## Matched comparison

All rows use precisely the same 17 tail-star positions, current frozen waves, 111.158776 Myr, observer, cluster registration and historical initialization of radial velocity. The number in each column is the forward-minus-reverse slope of line-of-sight velocity versus right ascension, in km/s per degree, corrected to fixed RA. Reset and inherited are different saved physical preparations, not baseline versus a fit.

| Distances and proper motions | Reset | Inherited |
|---|---:|---:|
| Legacy uniform 22.05 kpc and legacy uniform motion | +0.05392 | −0.06885 |
| Updated cluster distance and motion applied uniformly | +0.04539 | −0.07704 |
| Actual stellar distances; updated uniform motion | +0.04574 | −0.07720 |
| Updated uniform distance; actual stellar motions | +0.03524 | −0.04389 |
| Actual distances **and** motions | **+0.03450** | **−0.04566** |

Most of the change relative to the updated uniform calculation comes from proper motions, not from the distance gradient alone. Against the matched legacy control the full signal shrinks by 36%/34%. The last row amounts to 0.23/0.30 of the **historical** 0.15 gradient uncertainty; this is not a measured uncertainty on these 17 pulsating stars. Maximum individual fixed-RA velocity splits are 0.56/0.68 km/s and cluster-relative positions separate by up to 58.5/62.0 pc. Removing one star from the computed slope gives +0.03325 to +0.03963 / −0.05450 to −0.04288; this is an influence diagnostic, not retraining or independent validation. [Both samples and all controls](evidence-001.zip) (archive member: `scores.csv`).

Only nine of these stars lie within the separate leading/trailing RA ranges where the earlier track slope is defined. On those nine, the measured-geometry declination splits at fixed RA have RMS **0.0276°/0.0366°**, of which a single tilt about the cluster explains **11.4%/16.5% of squared signal**. We did not give these stars the old binned centroid errors. In particular this is not directly comparable to the earlier 1.26 diagonal position score or its 98% tilt fraction: footprint, conditioning, weighting and object type all differ. On the *same nine positions* the updated uniform cluster geometry gives 83.5%/95.1% tilt. The departures from a tilt here could reflect conditioning on noisy individual velocities or actual tracer variation; they are not nine measurements of a new physical ripple.

## Data and exposure

- [Price-Whelan et al.](https://arxiv.org/abs/1910.00595), [CDS release J/AJ/158/223, table 2](https://doi.org/10.26093/cds/vizier.51580223): 3,300 entries. The joint probability-above-0.5 and in-track cut gives 27 unique Gaia DR2 IDs; none in the track rounded exactly to 0.50. One duplicated Gaia ID in the unselected field has distinct PS1 entries and probability zero. Used the table's Dist (kpc) rather than using parallax or recomputing distances from the original distance modulus. Matched all 27 by integer/string source ID to the [Gaia DR2 archive](https://gea.esac.esa.int/archive/) and verified coordinates, PMs and both errors against the tabulation. Used its per-star PM correlation. Membership uses motion and distance, and the track cut uses sky location; none is withheld evidence.
- With the literal 11 arcmin cut there are 9 cluster + 18 tail stars. One at **11.1999 arcmin** changes this to 10+17 using the 11.2 arcmin value labelled in the [authors' notebook](https://github.com/adrn/pal5-rrl/blob/335db89ba108f8968d3111517243172b26983a36/notebooks/Pal5-membership-prob.ipynb). The 17 tail stars comprise 13 RRab and 4 RRc, matching the paper's tail counts; the ingested cluster labels are 3/7 rather than its narrative 2/8. We have not changed any labels to match the prose. The 18-star measured results are +0.03440/−0.04543. The actual selected positions, rather than a nominal sky-span quotation, set the calculation.
- [Kuzma et al., complete Table 4 supplement](https://arxiv.org/src/2202.04548v1/anc): compared sky positions only for all 109 (including legacy and repeated-study origins) to all 27. No candidate within 2 or 5 arcseconds; nearest separation is 8.03 arcseconds. No spectroscopic measurement was entered into a star's trajectory or scored. Absence of positional overlap does not make the published velocity sample a blind validation set: it shares literature gradients/selection, uses kinematic membership cuts and includes stars from previous studies. Overlap ledger (not bundled here) · per-star nearest matches (not bundled here).

## What uncertainty was propagated?

For fixed sky positions write the gradient difference as g = sum_i w_i s_i, with w_i=(RA_i−mean RA)/sum_j(RA_j−mean RA)^2 and s_i the sign difference after subtracting the reference sky gradient. Each test tracer is dynamically passive. Perturbing all stars along one covariance direction at once, holding the progenitor fixed, thus recovers each star's derivative separately, **not** an assumption that all stars have the same noise draw. Factor each two-dimensional Gaia PM covariance, use independent 1% distance perturbations, then add the squares of w_i times each directional derivative over stars/directions. Separately change the common distance scale by ±2%, including the progenitor. These distance components follow the paper's approximate uncertainty split; they are not exact per-star calibration posteriors.

Estimated **random input** uncertainty in the historical-reference gradient difference: **0.00172/0.00387 km/s per degree**, dominated by PM error. The signed linear responses to a common +2% distance rescaling are +0.00046/+0.00330. These are not observational errors on a stream velocity-gradient measurement. The calculation excludes cross-star astrometric systematics, cluster PM uncertainty, intrinsic stream width, stripping uncertainties, uncertain parent occupation, and uncertainty in the Galactic potential. The earlier stripping-time experiment was not reinterpreted as an error bar here. Full-to-half derivative steps changed the inherited random standard-error estimate by 0.59% on the 17-star sample, above 0.5%; retained. Half-to-quarter steps give 0.14%/0.36% change. Initial error comparison (not bundled here) · quarter-step results (not bundled here).

## Does the direction depend on how the missing radial velocities are supplied?

In the 17 stars the following are *signed differences between waves*, not fitted absolute velocity gradients.

| Radial initialization | Input slope | Reset | Inherited |
|---|---:|---:|---:|
| Common cluster radial velocity in every sightline | 0 | +0.02836 | −0.03491 |
| Historical slope − its quoted error | +1.05 | +0.03384 | −0.04434 |
| Historical central value | +1.20 | +0.03450 | −0.04566 |
| Historical slope + its quoted error | +1.35 | +0.03514 | −0.04697 |
| Same +1.20 slope, with curvature of the projected cluster velocity | +1.20 | +0.03011 | −0.03681 |
| Cluster bulk velocity projected on each sightline, with no tail slope input | −6.98 | −0.00590 | −0.01884 |

All use the same measured PMs and distances. In the last row the initialization is v_ref = n·v_cluster,hel; it is only a prescription for LOS speed, not for transverse stellar velocities. Cancel the changing projected reference by taking the signed difference of v_los−v_ref(n) at the two output directions. With straight references this reduces to fixed-RA subtraction. The raw same-star gradient *also* changes sign for reset (+0.03388 to −0.00461), so the reversal is not an artifact of subtracting the perspective term. Crucially, the last control differs from the legacy LOS input by **68.3 km/s RMS** and has a slope far outside the observational range. It shows non-identifiability from five coordinates alone, not a competing good fit or destruction of the sign within the measured range. Control table including same-star readout (not bundled here).

There is a simple reason five coordinates do not close this problem. In heliocentric sky coordinates let D(n,t) be a local distance surface for the stream, and let e be a star's distance offset from that surface. The kinematic identity is

    v_los = (∂D/∂t)_n + (dn/dt)·∇_sky D + de/dt.

Distances and proper motions at one epoch do not determine the first or last term. An arbitrary local change to the time slope of D leaves the instantaneous distance map unchanged. The two signed MTS fields determine accelerations *given initial states*, not those missing radial velocities by themselves.

**Next physical test:** construct the 3-D stream tangent from RR Lyrae geometry. In an inertial Galactic frame, for direction n(λ), heliocentric distance D(λ), solar velocity v_s and measured proper-motion vector, the transverse velocity is w = D dn/dt + (I−nnᵀ)v_s. If stars locally follow a stationary 3-D track, the inferred rate is u = (w·n′)/(D |n′|²), and v_los = u D′ − n·v_s. Test the **measured transverse residual w−u D n′** before adopting that extra assumption. Zero transverse residual is necessary, not sufficient (radial slip and time evolution remain possible). Freeze the geometric prediction and supported sky interval before comparing with spectroscopic stars; keep conditioning samples and target velocities separate. Do not pick the velocity law or host that flatters the MTS sign.

## Numerical and source receipts

Used the sealed [111.16 Myr potentials and orbit equations](../mts-pal5-joined-flow-586-600/RESULTS.md), not a field recomputed from these observations. Each sign pair starts with identical stars in a common mean-field back-initialization. All 160 central field/orbit comparisons, 52 supplementary checks and 48 bracket checks pass the retained 0.5% ceiling on their specified quantities. Mean orbits close inside 1e−9; no radial extrapolation. Raw source files have URL/query/hash receipts. Reproduce centrally with catalogue.py; replay.py for (2,1,central), (4,1,central), (4,2,central/errors/half); overlap.py; references.py for (2,1,reference/bracket), (4,2,reference/bracket/quarter); verify_stage.py. Bytecode off, one numerical thread per worker, no external score or publication.
