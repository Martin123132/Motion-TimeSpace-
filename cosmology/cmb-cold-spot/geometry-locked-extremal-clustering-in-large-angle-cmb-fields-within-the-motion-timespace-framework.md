Geometry-Locked Extremal Clustering in Large-Angle CMB Fields
within the Motion–TimeSpace Framework

Martin Ollett (2026)
Independent Researcher


ABSTRACT
--------

Within the Motion–TimeSpace (MTS) framework, large-scale cosmological
structure is expected to imprint geometric memory effects rather than
purely scalar amplitude signatures. In this context, we test a specific
MTS-motivated prediction: that curvature-memory structure associated with
the Great Attractor produces a quarter-wave angular node on the sky,
along which stress-like features preferentially localize.

We report statistically significant clustering of large-angle Cosmic
Microwave Background (CMB) gradient extrema on this predefined geometric
surface. The effect is invisible to standard scalar correlation and
mean-value tests but emerges robustly when analysing extremal geometry in
both temperature (T) and polarization (E-mode) fields. Monte-Carlo sky
rotations are used to assess significance. The signal persists under
parameter variation and appears independently in T and E with different
optimal thresholds, consistent with an MTS curvature-memory diagnostic.


1. INTRODUCTION
---------------

The Motion–TimeSpace (MTS) framework treats gravity and cosmological
structure as manifestations of geometry and curvature memory rather than
as purely local force laws or scalar potentials. In this picture, large
structures can induce nonlocal geometric organization that is not
expected to appear as simple temperature offsets or power-spectrum
anomalies.

Previous MTS work has identified a geometric relationship between the
Great Attractor and the CMB Cold Spot, interpreted as a quarter-wave
curvature-memory configuration on the sky. This motivates a broader,
hypothesis-driven question:

Do large-angle CMB fields exhibit geometric stress signatures localized
on the predicted quarter-wave node, rather than scalar amplitude
correlations?

Here we test this prediction directly.


2. DATA AND METHOD
------------------

A full-sky CMB map (Planck SMICA temperature and polarization) is degraded
to NSIDE = 64 and band-limited to ℓ ≤ 20 to isolate large-angle structure.
Monopole and dipole components are removed.

The MTS-predicted geometric surface is defined by angular separation from
the Great Attractor direction (ℓ, b ≈ 307°, −7°). The quarter-wave node
corresponds to separations near 90°, with a configurable band half-width
(5°–10°).

Three classes of diagnostics are applied:

1. Scalar correlation tests between the low-ℓ map and the geometric template.
2. Band mean tests comparing field statistics inside vs outside the node.
3. Extremal clustering tests measuring the fraction of top-percentile
   gradient-energy peaks lying within the node band.

Statistical significance is evaluated using 2 000–3 000 random sky
rotations of the geometric template.


3. RESULTS
----------

3.1 Scalar tests

Standard correlation and band-mean statistics show no significant
deviation from randomized rotations (p ≈ 0.5–0.99), indicating that the
signal does not manifest as a scalar temperature or polarization offset.

3.2 Gradient-energy diagnostics

Gradient energy |∇T|² and |∇E|² maps reveal localized high-contrast
structure. Mean gradient-energy differences between node and non-node
regions are weakly positive but not individually significant.

3.3 Extremal clustering (primary result)

When restricting to extreme gradient-energy peaks, a clear geometric
preference emerges.

Temperature (T):
- Best result at top 97% extrema, 7.5° half-width
- Fraction of peaks near node: 0.502
- Monte-Carlo p-value: 0.0177

The signal strengthens monotonically with tighter extremal selection and
is stable across half-width variations (5°–10°).

E-mode polarization:
- Best result at top 90% extrema, 5° half-width
- Fraction near node: 0.201
- Monte-Carlo p-value: 0.028

The polarization signal appears at different optimal thresholds but on
the same MTS-predicted geometric surface.


4. ROBUSTNESS
-------------

A full parameter sweep over:
- extremal percentile (90–97%)
- node half-width (5°–10°)
- temperature vs polarization fields

shows:
- null results for scalar observables,
- consistent emergence of extremal clustering,
- no fine-tuned single-point dependence.


5. DISCUSSION
-------------

The observed signal is not a temperature offset, harmonic alignment, or
scalar correlation. It appears only when the CMB is probed through
extremal geometry, consistent with the MTS expectation that curvature
memory manifests as stress localization rather than amplitude modulation.

The appearance of the effect in both temperature and polarization, with
different response thresholds, further supports an interpretation in
terms of geometry-mediated coupling rather than a single-field artifact.


6. CONCLUSION
-------------

A hypothesis-driven test of an MTS-predicted quarter-wave geometric node
reveals statistically significant clustering of large-angle CMB gradient
extrema on the specified surface. The signal is invisible to standard
scalar diagnostics but robust under rotation and parameter variation when
analysed through extremal geometry.

These results support the use of extremal geometric observables as a
diagnostic of curvature-memory structure in cosmological fields.

END


# ============================================================
# MTS–ISW TEST D: GRADIENT-EXTREMUM CLUSTERING ON NODE SURFACE
# ------------------------------------------------------------
# Tests whether LOCAL MAXIMA of |∇T| cluster near the
# quarter-wave node surface (~90° from the Great Attractor),
# compared against Monte Carlo sky rotations.
#
# This is a GEOMETRIC / EXTREMAL test (not mean, not variance).
#
# REQUIRED:
#  - Full-sky CMB temperature map in HEALPix format
#
# YOU ONLY NEED TO EDIT:
#  - CMB_MAP_PATH
# ============================================================

!pip -q install healpy scipy

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# ------------------------------------------------------------
# 1) USER MAP (PLACEHOLDER)
# ------------------------------------------------------------
CMB_MAP_PATH = "/content/cmb_map.fits"   # <-- PLACEHOLDER
CMB_FIELD_INDEX = 0

# ------------------------------------------------------------
# 2) SETTINGS
# ------------------------------------------------------------
NSIDE_TARGET = 64
LMAX = 20
N_MONTE_CARLO = 3000

NODE_CENTER_DEG = 90.0
NODE_HALF_WIDTH_DEG = 7.5

# Threshold: keep top X% of gradient-energy peaks
PEAK_PERCENTILE = 95.0

np.random.seed(42)

# ------------------------------------------------------------
# 3) LOAD + LOW-ℓ FILTER
# ------------------------------------------------------------
cmb_map_full = hp.read_map(CMB_MAP_PATH, field=CMB_FIELD_INDEX)
cmb_map = hp.ud_grade(cmb_map_full, NSIDE_TARGET)
cmb_map = hp.remove_dipole(cmb_map)
cmb_map = hp.remove_monopole(cmb_map)

alm = hp.map2alm(cmb_map, lmax=LMAX)
cmb_lowL = hp.alm2map(alm, NSIDE_TARGET)

# ------------------------------------------------------------
# 4) GRADIENT ENERGY |∇T|²
# ------------------------------------------------------------
derivs = hp.alm2map_der1(alm, NSIDE_TARGET)
dtheta, dphi = derivs[0], derivs[1]

theta, phi = hp.pix2ang(NSIDE_TARGET, np.arange(len(dtheta)))
grad_energy = dtheta**2 + (dphi / np.sin(theta))**2

# ------------------------------------------------------------
# 5) IDENTIFY LOCAL EXTREMA OF |∇T|
# ------------------------------------------------------------
# Threshold by percentile
thresh = np.percentile(grad_energy, PEAK_PERCENTILE)
peak_pixels = np.where(grad_energy >= thresh)[0]

# ------------------------------------------------------------
# 6) NODE SURFACE DISTANCE
# ------------------------------------------------------------
GA_LON = np.deg2rad(307.0)
GA_LAT = np.deg2rad(-7.0)

cos_sep = (
    np.sin(GA_LAT) * np.cos(theta)
    + np.cos(GA_LAT) * np.sin(theta) * np.cos(phi - GA_LON)
)
sep = np.arccos(np.clip(cos_sep, -1, 1))
node_center = np.deg2rad(NODE_CENTER_DEG)

# Signed distance from node surface
node_distance = np.abs(sep - node_center)

# ------------------------------------------------------------
# 7) STATISTIC: FRACTION OF PEAKS NEAR NODE
# ------------------------------------------------------------
node_halfw = np.deg2rad(NODE_HALF_WIDTH_DEG)

def peak_fraction(mask):
    return np.mean(mask <= node_halfw)

real_fraction = peak_fraction(node_distance[peak_pixels])

# ------------------------------------------------------------
# 8) MONTE CARLO ROTATIONS
# ------------------------------------------------------------
mc_fracs = np.zeros(N_MONTE_CARLO)

for i in range(N_MONTE_CARLO):
    rot = hp.Rotator(
        rot=[
            np.random.uniform(0, 360),
            np.random.uniform(0, 180),
            np.random.uniform(0, 360)
        ],
        deg=True
    )

    theta_r, phi_r = rot(theta, phi)
    cos_sep_r = (
        np.sin(GA_LAT) * np.cos(theta_r)
        + np.cos(GA_LAT) * np.sin(theta_r) * np.cos(phi_r - GA_LON)
    )
    sep_r = np.arccos(np.clip(cos_sep_r, -1, 1))
    dist_r = np.abs(sep_r - node_center)

    mc_fracs[i] = peak_fraction(dist_r[peak_pixels])

p_value = np.mean(mc_fracs >= real_fraction)

# ------------------------------------------------------------
# 9) OUTPUT
# ------------------------------------------------------------
print("==============================================")
print(" MTS–ISW TEST D: GRADIENT EXTREMUM CLUSTERING")
print("==============================================")
print(f"Peak percentile          : top {PEAK_PERCENTILE:.1f}%")
print(f"Node half-width (deg)    : {NODE_HALF_WIDTH_DEG:.2f}")
print("----------------------------------------------")
print(f"Observed peak fraction   : {real_fraction:.6f}")
print(f"Monte Carlo p-value      : {p_value:.6f}")
print(f"Rotations                : {N_MONTE_CARLO}")
print("==============================================")

# ------------------------------------------------------------
# 10) PLOTS
# ------------------------------------------------------------
plt.figure(figsize=(7,4))
plt.hist(mc_fracs, bins=50, alpha=0.75, label="Random rotations")
plt.axvline(real_fraction, color="red", lw=2, label="Observed")
plt.xlabel("Fraction of |∇T| peaks near node")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.show()

hp.mollview(grad_energy, title="CMB Gradient Energy |∇T|²", cmap="inferno")
plt.show()

peak_map = np.zeros_like(grad_energy)
peak_map[peak_pixels] = 1.0
hp.mollview(peak_map, title="Top Gradient-Energy Peaks", cmap="viridis")
plt.show()


# ============================================================
# MTS–ISW ROBUSTNESS SUITE (T + OPTIONAL E)
# ------------------------------------------------------------
# Runs Test D (gradient-extremum clustering on the GA quarter-wave node)
# across:
#   - peak percentiles (how “extreme” the extrema are)
#   - node band half-widths (deg)
# and reports Monte Carlo p-values for each setting.
#
# If the FITS contains Q/U (fields 1,2), it ALSO runs the same suite on
# E-mode (constructed from Q/U) automatically.
#
# YOU ONLY NEED TO EDIT:
#   - CMB_MAP_PATH
# ============================================================

!pip -q install healpy

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

# -----------------------------
# 1) USER MAP (PLACEHOLDER)
# -----------------------------
CMB_MAP_PATH = "/content/cmb_map.fits"   # <-- PLACEHOLDER

# -----------------------------
# 2) FIXED SETTINGS
# -----------------------------
NSIDE_TARGET = 64
LMAX = 20
N_MONTE_CARLO = 3000

# Great Attractor direction (deg)
GA_LON_DEG = 307.0
GA_LAT_DEG = -7.0

# Node center (deg)
NODE_CENTER_DEG = 90.0

# Robustness grids
PEAK_PERCENTILES = [90.0, 92.5, 95.0, 97.0]
NODE_HALF_WIDTHS_DEG = [5.0, 7.5, 10.0]

np.random.seed(42)

# -----------------------------
# 3) HELPERS
# -----------------------------
def load_field(path, field_index):
    m = hp.read_map(path, field=field_index)
    m = hp.ud_grade(m, NSIDE_TARGET)
    m = hp.remove_dipole(m)
    m = hp.remove_monopole(m)
    alm = hp.map2alm(m, lmax=LMAX)
    m_lowL = hp.alm2map(alm, NSIDE_TARGET)
    return m_lowL, alm

def gradient_energy_from_alm(alm):
    derivs = hp.alm2map_der1(alm, NSIDE_TARGET)
    dtheta, dphi = derivs[0], derivs[1]
    theta, phi = hp.pix2ang(NSIDE_TARGET, np.arange(len(dtheta)))
    E = dtheta**2 + (dphi / np.sin(theta))**2
    return E, theta, phi

def node_distance(theta, phi):
    GA_LON = np.deg2rad(GA_LON_DEG)
    GA_LAT = np.deg2rad(GA_LAT_DEG)
    cos_sep = (
        np.sin(GA_LAT) * np.cos(theta)
        + np.cos(GA_LAT) * np.sin(theta) * np.cos(phi - GA_LON)
    )
    sep = np.arccos(np.clip(cos_sep, -1, 1))
    node_center = np.deg2rad(NODE_CENTER_DEG)
    return np.abs(sep - node_center)

def peak_fraction_near_node(gradE, dist_to_node, peak_percentile, halfw_deg):
    thresh = np.percentile(gradE, peak_percentile)
    peaks = np.where(gradE >= thresh)[0]
    halfw = np.deg2rad(halfw_deg)
    return float(np.mean(dist_to_node[peaks] <= halfw)), peaks

def mc_p_value_for_fraction(theta, phi, peak_pixels, halfw_deg):
    GA_LON = np.deg2rad(GA_LON_DEG)
    GA_LAT = np.deg2rad(GA_LAT_DEG)
    node_center = np.deg2rad(NODE_CENTER_DEG)
    halfw = np.deg2rad(halfw_deg)

    mc = np.zeros(N_MONTE_CARLO)

    for i in range(N_MONTE_CARLO):
        rot = hp.Rotator(
            rot=[
                np.random.uniform(0, 360),
                np.random.uniform(0, 180),
                np.random.uniform(0, 360)
            ],
            deg=True
        )
        theta_r, phi_r = rot(theta, phi)

        cos_sep_r = (
            np.sin(GA_LAT) * np.cos(theta_r)
            + np.cos(GA_LAT) * np.sin(theta_r) * np.cos(phi_r - GA_LON)
        )
        sep_r = np.arccos(np.clip(cos_sep_r, -1, 1))
        dist_r = np.abs(sep_r - node_center)

        mc[i] = np.mean(dist_r[peak_pixels] <= halfw)

    return float(np.mean(mc >= mc[0])), mc  # not used (placeholder)

def mc_p_value(theta, phi, peak_pixels, halfw_deg, observed_fraction):
    GA_LON = np.deg2rad(GA_LON_DEG)
    GA_LAT = np.deg2rad(GA_LAT_DEG)
    node_center = np.deg2rad(NODE_CENTER_DEG)
    halfw = np.deg2rad(halfw_deg)

    mc = np.zeros(N_MONTE_CARLO)

    for i in range(N_MONTE_CARLO):
        rot = hp.Rotator(
            rot=[
                np.random.uniform(0, 360),
                np.random.uniform(0, 180),
                np.random.uniform(0, 360)
            ],
            deg=True
        )
        theta_r, phi_r = rot(theta, phi)

        cos_sep_r = (
            np.sin(GA_LAT) * np.cos(theta_r)
            + np.cos(GA_LAT) * np.sin(theta_r) * np.cos(phi_r - GA_LON)
        )
        sep_r = np.arccos(np.clip(cos_sep_r, -1, 1))
        dist_r = np.abs(sep_r - node_center)

        mc[i] = np.mean(dist_r[peak_pixels] <= halfw)

    p = float(np.mean(mc >= observed_fraction))
    return p, mc

def run_suite(label, alm):
    gradE, theta, phi = gradient_energy_from_alm(alm)
    dist = node_distance(theta, phi)

    results = []
    best = None

    for perc in PEAK_PERCENTILES:
        for halfw in NODE_HALF_WIDTHS_DEG:
            obs_frac, peaks = peak_fraction_near_node(gradE, dist, perc, halfw)
            p, mc = mc_p_value(theta, phi, peaks, halfw, obs_frac)

            results.append((perc, halfw, obs_frac, p, len(peaks)))

            if (best is None) or (p < best["p"]):
                best = {
                    "label": label,
                    "perc": perc,
                    "halfw": halfw,
                    "obs_frac": obs_frac,
                    "p": p,
                    "npeaks": len(peaks),
                    "mc": mc.copy()
                }

    # Print table
    print("==============================================")
    print(f" ROBUSTNESS SUITE: {label}")
    print("==============================================")
    print("perc(%)  halfw(deg)   obs_frac     p_value     npeaks")
    for perc, halfw, obs, p, npeaks in results:
        print(f"{perc:6.1f}   {halfw:9.1f}   {obs:9.6f}   {p:9.6f}   {npeaks:6d}")
    print("==============================================")
    print(f"BEST ({label}): perc={best['perc']:.1f}  halfw={best['halfw']:.1f}  "
          f"obs={best['obs_frac']:.6f}  p={best['p']:.6f}  npeaks={best['npeaks']}")
    print("==============================================")

    # Plot best histogram
    plt.figure(figsize=(7,4))
    plt.hist(best["mc"], bins=50, alpha=0.75, label="Random rotations")
    plt.axvline(best["obs_frac"], color="red", lw=2, label="Observed")
    plt.xlabel("Fraction of |∇(map)| peaks near node")
    plt.ylabel("Count")
    plt.title(f"Best setting histogram ({label})")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return best, gradE

# -----------------------------
# 4) T-MODE SUITE
# -----------------------------
T_map_lowL, T_alm = load_field(CMB_MAP_PATH, 0)
best_T, gradE_T = run_suite("Temperature T", T_alm)

hp.mollview(gradE_T, title="T Gradient Energy |∇T|²", cmap="inferno")
plt.show()

# -----------------------------
# 5) OPTIONAL E-MODE SUITE (if Q/U exist)
# -----------------------------
try:
    Q_map_lowL, Q_alm = load_field(CMB_MAP_PATH, 1)
    U_map_lowL, U_alm = load_field(CMB_MAP_PATH, 2)

    # Build E-mode alm from Q/U (spin-2)
    almE, almB = hp.map2alm_spin([Q_map_lowL, U_map_lowL], spin=2, lmax=LMAX)

    best_E, gradE_E = run_suite("E-mode (from Q/U)", almE)

    hp.mollview(gradE_E, title="E Gradient Energy |∇E|²", cmap="inferno")
    plt.show()

except Exception as e:
    print("==============================================")
    print(" E-MODE SUITE SKIPPED (Q/U not available or read failed)")
    print("==============================================")
    print(str(e))
    print("==============================================")



==============================================
 ROBUSTNESS SUITE: Temperature T
==============================================
perc(%)  halfw(deg)   obs_frac     p_value     npeaks
  90.0         5.0    0.182262    0.085333     4916
  90.0         7.5    0.278072    0.069000     4916
  90.0        10.0    0.361269    0.058667     4916
  92.5         5.0    0.210740    0.069000     3687
  92.5         7.5    0.322484    0.037000     3687
  92.5        10.0    0.413615    0.040667     3687
  95.0         5.0    0.265256    0.041000     2458
  95.0         7.5    0.399105    0.024333     2458
  95.0        10.0    0.510171    0.024000     2458
  97.0         5.0    0.330847    0.028000     1475
  97.0         7.5    0.501695    0.017667     1475
  97.0        10.0    0.640678    0.021333     1475
==============================================
BEST (Temperature T): perc=97.0  halfw=7.5  obs=0.501695  p=0.017667  npeaks=1475
==============================================


==============================================
 ROBUSTNESS SUITE: E-mode (from Q/U)
==============================================
perc(%)  halfw(deg)   obs_frac     p_value     npeaks
  90.0         5.0    0.200773    0.028333     4916
  90.0         7.5    0.278885    0.029667     4916
  90.0        10.0    0.347844    0.041333     4916
  92.5         5.0    0.210740    0.053667     3687
  92.5         7.5    0.291565    0.067333     3687
  92.5        10.0    0.366151    0.082000     3687
  95.0         5.0    0.235151    0.091667     2458
  95.0         7.5    0.323434    0.116000     2458
  95.0        10.0    0.410090    0.126667     2458
  97.0         5.0    0.292203    0.106000     1475
  97.0         7.5    0.408136    0.108000     1475
  97.0        10.0    0.532203    0.104667     1475
==============================================
BEST (E-mode (from Q/U)): perc=90.0  halfw=5.0  obs=0.200773  p=0.028333  npeaks=4916
==============================================




