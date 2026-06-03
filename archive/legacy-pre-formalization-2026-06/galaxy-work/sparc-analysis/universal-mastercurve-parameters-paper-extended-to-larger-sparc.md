# Catalogue-Scale Mastercurve Collapse of SPARC Rotation Curves under Motion–TimeSpace Scaling

Author: Martin Ollett
Year: 2026

---

## Abstract

We perform a catalogue-level test of the Motion–TimeSpace (MTS) rotation-curve mastercurve using the SPARC rotmod dataset. The MTS framework predicts that galaxy rotation curves collapse onto a universal functional form when expressed in scaled variables

    x = r / R_s
    y = V / V_inf

where R_s and V_inf are galaxy-specific scale parameters.

Using a fixed mastercurve

    y(x) = 1 - exp(-(x/x0)^nu)

with universal parameters

    (x0, nu) = (0.966, 0.942),

we fit only the scaling parameters (V_inf, R_s) per galaxy across the SPARC rotmod catalogue.

Out of 175 rotmod files, 124 loaded successfully and 92 passed quality control criteria ensuring meaningful radial leverage and stable scale parameters.

For the QC-pass subset the rescaled curves collapse around the universal mastercurve with

    RMS scatter ≈ 0.057
    Mean absolute deviation ≈ 0.036

Tightening statistical quality cuts further reduces scatter to ≈ 0.048.

These results provide a reproducible catalogue-scale benchmark for the MTS rotation-curve scaling hypothesis.

---

## 1. Introduction

Galaxy rotation curves exhibit systematic structure that cannot be explained by simple Newtonian predictions using visible baryonic mass alone. Various frameworks attempt to describe these dynamics, including dark-matter halo models and modified dynamical laws.

The Motion–TimeSpace (MTS) framework introduced in:

    Motion–TimeSpace Gravity:
    A Geometric Stiffness-Memory Description of Galactic Dynamics

and

    Cumulative Stiffness Control of Energy Horizons
    in Spatially Screened Curvature Systems

proposes that galaxy dynamics are governed by a spatial stiffness field whose cumulative behaviour determines the effective gravitational response.

A key empirical prediction emerging from that framework is the existence of a universal rotation-curve mastercurve. When galaxy radii and velocities are expressed in scaled coordinates

    x = r / R_s
    y = V / V_inf

rotation curves are predicted to follow a common functional form independent of galaxy mass.

Initial demonstrations of this collapse were performed on curated subsets of galaxies. The purpose of the present work is to test this prediction across the entire SPARC rotmod catalogue, providing a catalogue-scale benchmark.

---

## 2. Data

We use the publicly available SPARC rotmod dataset, which provides rotation-curve measurements for nearby galaxies.

Each rotmod file contains radial samples

    (r_i, V_i, sigma_i)

representing radius, circular velocity, and observational uncertainty.

From the full set of 175 rotmod files:

    124 files contained sufficient valid data to load successfully
    92 galaxies passed quality control requirements described below

---

## 3. Mastercurve Model

The MTS rotation-curve form is given by

    y(x) = 1 - exp(-(x/x0)^nu)

where

    x = r / R_s
    y = V / V_inf

The universal parameters are fixed to values determined in earlier work:

    x0 = 0.966
    nu = 0.942

Thus each galaxy requires only two scaling parameters:

    asymptotic velocity V_inf
    scale radius R_s

Predicted velocities are therefore

    V(r) = V_inf * [1 - exp(-( (r/R_s)/x0 )^nu)]

---

## 4. Fitting Procedure

For each galaxy:

1. Load the rotation curve (r_i, V_i, sigma_i)
2. Fit V_inf and R_s using weighted least squares
3. Compute model velocities V_model(r)
4. Compute residuals relative to the universal mastercurve

The fitting was implemented using scipy.optimize.curve_fit with bounds

    5 <= V_inf <= 600 km/s
    0.05 <= R_s <= 80 kpc

---

## 5. Quality Control Criteria

Not all fitted curves provide meaningful information about universal scaling.

We therefore applied objective QC criteria:

1. Radial leverage requirement

       r_max / R_s >= 2

2. Scale collapse rejection

       r_max / R_s <= 50

3. Stable fit parameters

       fits hitting parameter bounds were rejected

Applying these criteria resulted in:

    Total rotmod files:     175
    Loaded successfully:    124
    QC-pass galaxies:       92
    Rejected fits:          32
    Load failures:          51

---

## 6. Catalogue-Level Mastercurve Collapse

For the QC-pass subset we compute

    x_i = r_i / R_s
    y_i = V_i / V_inf

and measure deviations from the universal mastercurve.

The resulting collapse statistics are

    RMS scatter  ≈ 0.057
    Mean |Δ|     ≈ 0.036

The collapse is illustrated by plotting all scaled curves against the universal function.

---

## 7. Sensitivity to Statistical Quality

To test robustness, we recomputed collapse statistics under progressively stricter statistical criteria.

QC-A (baseline):

    galaxies used = 92
    RMS scatter   ≈ 0.057

QC-B (chi^2_red < 10):

    galaxies used = 85
    RMS scatter   ≈ 0.049

QC-C (chi^2_red < 5):

    galaxies used = 83
    RMS scatter   ≈ 0.048

The reduction in scatter under stricter criteria indicates that the observed collapse is not driven by a small number of poorly fitted galaxies.

---

## 8. Parameter Distributions

Across the QC-pass sample the median parameters are

    R_s ≈ 2.66 kpc
    V_inf ≈ 117 km/s

with broad distributions reflecting the diversity of galaxy masses and sizes.

The median radial leverage

    r_max / R_s ≈ 5.3

indicates that most curves extend several scale radii beyond the characteristic transition region.

---

## 9. Discussion

The catalogue-level analysis demonstrates that a fixed mastercurve with two per-galaxy scaling parameters produces a consistent collapse across a substantial subset of the SPARC rotmod catalogue.

The observed scatter levels (~0.05–0.06) are comparable to those typically reported for empirical universal rotation-curve descriptions.

Importantly, the collapse remains stable under stricter statistical cuts, suggesting that the scaling behaviour is not dominated by pathological fits.

Within the MTS framework, this behaviour is interpreted as a manifestation of curvature-memory governed by the cumulative stiffness field discussed in earlier work.

---

## 10. Conclusion

Testing the Motion–TimeSpace rotation-curve mastercurve across the SPARC rotmod catalogue yields:

    92 galaxies passing quality control
    RMS collapse scatter ≈ 0.057
    Reduced scatter ≈ 0.048 under stricter statistical cuts

These results provide a reproducible catalogue-scale benchmark supporting the existence of a universal rotation-curve scaling under the MTS rescaling variables.

Future work may extend this analysis to additional rotation-curve catalogues and explore connections between the scaling parameters and baryonic galaxy properties.

---

## References

Lelli, F., McGaugh, S., Schombert, J. (2016)
SPARC Database




import zipfile, os

zip_path = "/content/Rotmod_LTG (3).zip"
extract_path = "/content/SPARC_data"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)

print("Unzipped to:", extract_path)



import numpy as np
import glob
import matplotlib.pyplot as plt

DATA_DIR = "/content/SPARC_data"

X0 = 0.966
NU = 0.942

MIN_POINTS = 8

def mastercurve(x):
    return 1 - np.exp(-(x/X0)**NU)

def load_rotmod(fp):

    data = np.loadtxt(fp)

    if data.shape[0] < MIN_POINTS:
        return None

    r = data[:,0]
    v = data[:,1]
    e = data[:,2]

    mask = (r>0) & (v>0) & (e>0)

    if mask.sum() < MIN_POINTS:
        return None

    return r[mask], v[mask], e[mask]

files = sorted(glob.glob(DATA_DIR + "/*_rotmod.dat"))

print("Files found:", len(files))

curves = []

for f in files:

    res = load_rotmod(f)

    if res is None:
        continue

    r,v,e = res

    Vinf = np.max(v)

    Rs = r[np.argmax(v >= 0.5*Vinf)]

    x = r/Rs
    y = v/Vinf

    curves.append((x,y))

print("Usable galaxies:", len(curves))

all_residuals = []

plt.figure(figsize=(7,5))

for x,y in curves:

    plt.plot(x,y,alpha=0.08,color="blue")

    y_m = mastercurve(x)

    all_residuals.extend(y - y_m)

xx = np.linspace(0,4,300)

plt.plot(xx, mastercurve(xx), color="red", lw=3)

plt.xlabel("x = r / Rs")
plt.ylabel("y = V / Vinf")
plt.title("SPARC Mastercurve Collapse")

plt.xlim(0,4)
plt.ylim(0,1.4)

plt.show()

res = np.array(all_residuals)

print("RMS scatter:", np.sqrt(np.mean(res**2)))
print("Mean |Δ|:", np.mean(np.abs(res)))


import os, glob, zipfile, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =========================
# USER SETTINGS
# =========================
ZIP_PATH = "/content/Rotmod_LTG (3).zip"   # change if needed
DATA_DIR = "/content/SPARC_rotmod"
OUT_DIR  = "/content/mts_mastercurve_results"

MIN_POINTS = 10

# Universal mastercurve parameters (paper)
X0_UNIV = 0.966
NU_UNIV = 0.942

# Choose fit mode:
#   "A" = fit only (Vinf, Rs) with (x0, nu) fixed universal
#   "B" = fit (Vinf, Rs, nu) with x0 fixed universal (nu varies per galaxy)
FIT_MODE = "A"

# Bounds (keep sane, avoid corner nonsense)
VINF_BOUNDS = (5.0, 600.0)     # km/s
RS_BOUNDS   = (0.05, 80.0)     # kpc
NU_BOUNDS   = (0.3, 3.0)

# =========================
# SETUP
# =========================
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Unzip if no rotmod files present
if len(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat"))) < 10:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)

files = sorted(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat")))
print("Files found:", len(files))

# =========================
# MODEL
# =========================
def y_master(x, x0=X0_UNIV, nu=NU_UNIV):
    x = np.maximum(x, 0.0)
    return 1.0 - np.exp(- (x/x0)**nu )

def model_A(r, Vinf, Rs):
    x = r / np.maximum(Rs, 1e-6)
    return Vinf * y_master(x, X0_UNIV, NU_UNIV)

def model_B(r, Vinf, Rs, nu):
    x = r / np.maximum(Rs, 1e-6)
    return Vinf * y_master(x, X0_UNIV, nu)

def load_rotmod(fp):
    try:
        data = np.loadtxt(fp)
        if data.ndim != 2 or data.shape[0] < MIN_POINTS or data.shape[1] < 3:
            return None
        r = data[:,0].astype(float)
        v = data[:,1].astype(float)
        e = data[:,2].astype(float)
        m = (r>0) & (v>0) & np.isfinite(r) & np.isfinite(v) & np.isfinite(e)
        # If errors are missing/zero, replace with median nonzero or 5 km/s fallback
        if np.any(e[m] <= 0):
            e2 = e.copy()
            good_e = e2[m] > 0
            fallback = np.median(e2[good_e]) if np.any(good_e) else 5.0
            e2[(m) & (e2<=0)] = fallback
            e = e2
        if m.sum() < MIN_POINTS:
            return None
        return r[m], v[m], e[m]
    except Exception:
        return None

# =========================
# FIT LOOP
# =========================
rows = []
all_residuals = []   # y - y_master(x) using fitted params
curves_for_plot = [] # (x,y) for QC-pass curves

n_total = 0
n_loaded = 0
n_fit_ok = 0
n_qc_ok  = 0

for fp in files:
    n_total += 1
    name = os.path.basename(fp).replace("_rotmod.dat","")
    dat = load_rotmod(fp)
    if dat is None:
        rows.append({"Galaxy": name, "status":"load_fail"})
        continue

    n_loaded += 1
    r, v, e = dat

    # Initial guesses
    V0 = np.percentile(v, 95)  # robust "almost flat" guess
    V0 = float(np.clip(V0, VINF_BOUNDS[0], VINF_BOUNDS[1]))
    # Rs guess: radius where velocity reaches half of V0 (if exists), else r_median
    try:
        idx = np.where(v >= 0.5*V0)[0]
        Rs0 = r[idx[0]] if len(idx)>0 else np.median(r)
    except Exception:
        Rs0 = np.median(r)
    Rs0 = float(np.clip(Rs0, RS_BOUNDS[0], RS_BOUNDS[1]))

    fit_status = "fit_fail"
    Vinf_fit = np.nan
    Rs_fit   = np.nan
    nu_fit   = np.nan
    rmse     = np.nan
    chi2red  = np.nan

    try:
        if FIT_MODE == "A":
            popt, pcov = curve_fit(
                model_A, r, v,
                p0=[V0, Rs0],
                sigma=e, absolute_sigma=True,
                bounds=([VINF_BOUNDS[0], RS_BOUNDS[0]],
                        [VINF_BOUNDS[1], RS_BOUNDS[1]]),
                maxfev=20000
            )
            Vinf_fit, Rs_fit = map(float, popt)
            nu_fit = NU_UNIV
            vpred = model_A(r, Vinf_fit, Rs_fit)

        else:
            popt, pcov = curve_fit(
                model_B, r, v,
                p0=[V0, Rs0, NU_UNIV],
                sigma=e, absolute_sigma=True,
                bounds=([VINF_BOUNDS[0], RS_BOUNDS[0], NU_BOUNDS[0]],
                        [VINF_BOUNDS[1], RS_BOUNDS[1], NU_BOUNDS[1]]),
                maxfev=30000
            )
            Vinf_fit, Rs_fit, nu_fit = map(float, popt)
            vpred = model_B(r, Vinf_fit, Rs_fit, nu_fit)

        n_fit_ok += 1
        fit_status = "fit_ok"
        rmse = float(np.sqrt(np.mean((v - vpred)**2)))

        # Reduced chi^2
        dof = max(len(r) - (2 if FIT_MODE=="A" else 3), 1)
        chi2 = float(np.sum(((v - vpred)/e)**2))
        chi2red = chi2 / dof

        # QC: reject if hugging bounds (means unconstrained / pathological)
        bound_hit = False
        if abs(Vinf_fit - VINF_BOUNDS[0]) < 1e-6 or abs(Vinf_fit - VINF_BOUNDS[1]) < 1e-6: bound_hit = True
        if abs(Rs_fit   - RS_BOUNDS[0])   < 1e-6 or abs(Rs_fit   - RS_BOUNDS[1])   < 1e-6: bound_hit = True
        if FIT_MODE=="B":
            if abs(nu_fit - NU_BOUNDS[0]) < 1e-6 or abs(nu_fit - NU_BOUNDS[1]) < 1e-6: bound_hit = True

        # Additional QC: need some tail leverage: r_max / Rs_fit
        tail = float(np.max(r) / max(Rs_fit, 1e-6))
        tail_ok = tail >= 2.0

        qc_ok = (not bound_hit) and tail_ok and np.isfinite(rmse) and np.isfinite(chi2red)

        if qc_ok:
            n_qc_ok += 1
            # Build collapse data
            x = r / Rs_fit
            y = v / Vinf_fit
            y_m = y_master(x, X0_UNIV, nu_fit)
            all_residuals.extend((y - y_m).tolist())
            curves_for_plot.append((x, y))

    except Exception:
        pass

    rows.append({
        "Galaxy": name,
        "status": fit_status,
        "N": len(r),
        "Vinf_fit": Vinf_fit,
        "Rs_fit": Rs_fit,
        "nu_fit": nu_fit,
        "rmse_kms": rmse,
        "chi2red": chi2red,
        "rmax_over_Rs": float(np.max(r) / max(Rs_fit, 1e-6)) if np.isfinite(Rs_fit) else np.nan
    })

df = pd.DataFrame(rows)
csv_path = os.path.join(OUT_DIR, "mastercurve_fit_results.csv")
df.to_csv(csv_path, index=False)

print("\nLoaded galaxies:", n_loaded)
print("Fit OK:", n_fit_ok)
print("QC-pass:", n_qc_ok)
print("CSV saved:", csv_path)

# =========================
# MASTER CURVE STATS + PLOT
# =========================
res = np.array(all_residuals, dtype=float)
if res.size == 0:
    print("\nNo QC-pass residuals produced. Loosen QC or check data.")
else:
    rms = float(np.sqrt(np.mean(res**2)))
    mean_abs = float(np.mean(np.abs(res)))
    print("\nMastercurve collapse (QC-pass only):")
    print("RMS scatter:", rms)
    print("Mean |Δ|:", mean_abs)

    # Plot
    plt.figure(figsize=(7,5))
    for x,y in curves_for_plot:
        plt.plot(x, y, alpha=0.08, lw=0.6)
    xx = np.linspace(0, 4, 400)
    plt.plot(xx, y_master(xx, X0_UNIV, NU_UNIV if FIT_MODE=="A" else np.median(df.loc[df.status=="fit_ok","nu_fit"].dropna())),
             lw=3)
    plt.xlim(0,4)
    plt.ylim(0,1.4)
    plt.xlabel("x = r / Rs_fit")
    plt.ylabel("y = V / Vinf_fit")
    plt.title(f"SPARC Mastercurve Collapse | mode {FIT_MODE} | QC-pass={n_qc_ok}")
    plot_path = os.path.join(OUT_DIR, "mastercurve_collapse.png")
    plt.savefig(plot_path, dpi=160, bbox_inches="tight")
    plt.show()
    print("Plot saved:", plot_path)


import os, glob, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# USER SETTINGS
# =========================
ZIP_PATH = "/content/Rotmod_LTG (3).zip"   # adjust if needed
DATA_DIR = "/content/SPARC_rotmod"
OUT_DIR  = "/content/mts_mastercurve_results_full"
MIN_POINTS = 10

# Universal mastercurve parameters
X0_UNIV = 0.966
NU_UNIV = 0.942

# Reasonable bounds / sanity checks
VINF_BOUNDS = (5.0, 600.0)    # km/s
RS_BOUNDS   = (0.10, 80.0)    # kpc  (note: 0.10 not 0.05, to avoid tiny-Rs silliness)

# QC checks
MIN_TAIL_XMAX = 2.0           # require rmax/Rs >= this (enough radial leverage)
MAX_TAIL_XMAX = 60.0          # reject absurd rmax/Rs (usually indicates Rs collapse)
MAX_CHI2RED   = 25.0          # keep, but don’t be too aggressive (rotmod errors vary)

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# =========================
# UNZIP
# =========================
if len(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat"))) < 10:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)

files = sorted(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat")))
print("Files found:", len(files))

# =========================
# MODEL
# =========================
def y_master(x, x0=X0_UNIV, nu=NU_UNIV):
    x = np.maximum(x, 0.0)
    return 1.0 - np.exp(- (x/x0)**nu )

# constant used for Rs from r50
K_HALF = X0_UNIV * (np.log(2.0) ** (1.0 / NU_UNIV))

def load_rotmod(fp):
    try:
        data = np.loadtxt(fp)
        if data.ndim != 2 or data.shape[0] < MIN_POINTS or data.shape[1] < 3:
            return None
        r = data[:,0].astype(float)
        v = data[:,1].astype(float)
        e = data[:,2].astype(float)

        m = (r > 0) & (v > 0) & np.isfinite(r) & np.isfinite(v) & np.isfinite(e)
        if m.sum() < MIN_POINTS:
            return None

        r, v, e = r[m], v[m], e[m]

        # Replace missing/zero errors
        if np.any(e <= 0):
            good = e > 0
            fallback = np.median(e[good]) if np.any(good) else 5.0
            e = np.where(e <= 0, fallback, e)

        return r, v, e
    except Exception:
        return None

def weighted_best_Vinf(r, v, e, Rs):
    """
    Fit Vinf in: v ≈ Vinf * y_master(r/Rs)
    Weighted least squares: Vinf = (Σ w y v)/(Σ w y^2)
    """
    x = r / max(Rs, 1e-12)
    y = y_master(x)
    w = 1.0 / (e**2)

    denom = np.sum(w * y * y)
    if denom <= 0:
        return np.nan
    return float(np.sum(w * y * v) / denom)

def chi2_red(r, v, e, Vinf, Rs):
    x = r / max(Rs, 1e-12)
    vpred = Vinf * y_master(x)
    chi2 = float(np.sum(((v - vpred)/e)**2))
    dof = max(len(r) - 1, 1)  # only Vinf fitted
    return chi2 / dof, vpred

# =========================
# FIT LOOP
# =========================
rows = []
all_residuals = []
curves_for_plot = []

n_total = 0
n_loaded = 0
n_ok = 0

for fp in files:
    n_total += 1
    name = os.path.basename(fp).replace("_rotmod.dat","")

    dat = load_rotmod(fp)
    if dat is None:
        rows.append({"Galaxy": name, "status":"load_fail"})
        continue

    n_loaded += 1
    r, v, e = dat

    # Robust Vinf guess = high percentile of v
    V0 = float(np.clip(np.percentile(v, 95), VINF_BOUNDS[0], VINF_BOUNDS[1]))

    # Estimate r50 = first radius where v >= 0.5*V0
    idx = np.where(v >= 0.5 * V0)[0]
    if len(idx) == 0:
        rows.append({"Galaxy": name, "status":"no_r50"})
        continue

    r50 = float(r[idx[0]])
    Rs = float(r50 / K_HALF)

    # Bound Rs
    if not np.isfinite(Rs):
        rows.append({"Galaxy": name, "status":"Rs_nan"})
        continue
    Rs = float(np.clip(Rs, RS_BOUNDS[0], RS_BOUNDS[1]))

    # Fit Vinf (1-parameter)
    Vinf = weighted_best_Vinf(r, v, e, Rs)
    if not np.isfinite(Vinf):
        rows.append({"Galaxy": name, "status":"Vinf_nan", "Rs_fit": Rs})
        continue
    Vinf = float(np.clip(Vinf, VINF_BOUNDS[0], VINF_BOUNDS[1]))

    chi2r, vpred = chi2_red(r, v, e, Vinf, Rs)
    rmse = float(np.sqrt(np.mean((v - vpred)**2)))
    tail = float(np.max(r) / max(Rs, 1e-12))

    # QC
    qc_ok = (tail >= MIN_TAIL_XMAX) and (tail <= MAX_TAIL_XMAX) and (chi2r <= MAX_CHI2RED)

    status = "ok" if qc_ok else "reject"

    rows.append({
        "Galaxy": name,
        "status": status,
        "N": len(r),
        "Vinf_fit": Vinf,
        "Rs_fit": Rs,
        "nu_fit": NU_UNIV,
        "rmse_kms": rmse,
        "chi2red": chi2r,
        "rmax_over_Rs": tail,
        "r50_kpc": r50
    })

    if qc_ok:
        n_ok += 1
        x = r / Rs
        y = v / Vinf
        y_m = y_master(x)
        all_residuals.extend((y - y_m).tolist())
        curves_for_plot.append((x, y))

df = pd.DataFrame(rows)
csv_path = os.path.join(OUT_DIR, "mastercurve_fit_results_full.csv")
df.to_csv(csv_path, index=False)

print("\nTotal files:", n_total)
print("Loaded:", n_loaded)
print("QC-pass:", n_ok)
print("CSV saved:", csv_path)

# =========================
# MASTER CURVE STATS + PLOT
# =========================
res = np.array(all_residuals, dtype=float)
if res.size == 0:
    print("\nNo QC-pass residuals produced. Try relaxing QC thresholds.")
else:
    rms = float(np.sqrt(np.mean(res**2)))
    mean_abs = float(np.mean(np.abs(res)))
    print("\nMastercurve collapse (QC-pass):")
    print("RMS scatter:", rms)
    print("Mean |Δ|:", mean_abs)

    plt.figure(figsize=(7,5))
    for x,y in curves_for_plot:
        plt.plot(x, y, alpha=0.06, lw=0.6)
    xx = np.linspace(0, 4, 400)
    plt.plot(xx, y_master(xx), lw=3)
    plt.xlim(0,4)
    plt.ylim(0,1.4)
    plt.xlabel("x = r / Rs_fit")
    plt.ylabel("y = V / Vinf_fit")
    plt.title(f"SPARC Mastercurve Collapse (stable Rs from r50) | QC-pass={n_ok}")
    plot_path = os.path.join(OUT_DIR, "mastercurve_collapse_full.png")
    plt.savefig(plot_path, dpi=160, bbox_inches="tight")
    plt.show()
    print("Plot saved:", plot_path)



import pandas as pd
import numpy as np

CSV = "/content/mts_mastercurve_results_full/mastercurve_fit_results_full.csv"  # change if needed
df = pd.read_csv(CSV)

print("Status counts:")
print(df["status"].value_counts(dropna=False))
print()

# Basic diagnostics for ok vs reject
for s in ["ok", "reject"]:
    sub = df[df["status"] == s].copy()
    if len(sub) == 0:
        continue
    print(f"--- {s} (n={len(sub)}) ---")
    print("Rs_fit: median =", np.nanmedian(sub["Rs_fit"]), "  (16–84% =", np.nanpercentile(sub["Rs_fit"], [16,84]), ")")
    print("Vinf_fit: median =", np.nanmedian(sub["Vinf_fit"]), " (16–84% =", np.nanpercentile(sub["Vinf_fit"], [16,84]), ")")
    print("rmax/Rs: median =", np.nanmedian(sub["rmax_over_Rs"]), " (16–84% =", np.nanpercentile(sub["rmax_over_Rs"], [16,84]), ")")
    print("chi2red: median =", np.nanmedian(sub["chi2red"]), " (16–84% =", np.nanpercentile(sub["chi2red"], [16,84]), ")")
    print()

# Identify common reject modes
rej = df[df["status"] == "reject"].copy()
if len(rej):
    # You can tune these thresholds to match your QC logic
    low_tail  = rej["rmax_over_Rs"] < 2.0
    scale_collapse = rej["rmax_over_Rs"] > 50.0   # typical "Rs too small" signature
    huge_chi2 = rej["chi2red"] > 10.0

    print("Reject-mode counts (non-exclusive):")
    print("  rmax/Rs < 2:", int(low_tail.sum()))
    print("  rmax/Rs > 50:", int(scale_collapse.sum()))
    print("  chi2red > 10:", int(huge_chi2.sum()))

    # Show a few most extreme scale-collapses
    worst = rej.sort_values("rmax_over_Rs", ascending=False).head(10)
    print("\nTop 10 rmax/Rs rejects:")
    print(worst[["Galaxy","Rs_fit","rmax_over_Rs","chi2red","rmse_kms","r50_kpc"]].to_string(index=False))

# ============================================================
# SPARC FULL-CATALOG MASTER CURVE COLLAPSE (MTS)
# Fit universal shape y(x)=1-exp(-(x/x0)^nu) with fixed (x0,nu)
# Fit only per-galaxy (Vinf, Rs) using SPARC rotmod files.
#
# Outputs:
#   - CSV of per-galaxy fit/QC results
#   - mastercurve collapse plot
#   - optional "QC strictness" scatter table (QC-A/B/C)
#
# Works in Colab / local Python (needs numpy/pandas/matplotlib/scipy)
# ============================================================

import os, glob, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =========================
# USER SETTINGS
# =========================
ZIP_PATH = "/content/Rotmod_LTG (3).zip"      # <-- change if needed
DATA_DIR = "/content/SPARC_rotmod"           # where *_rotmod.dat will live
OUT_DIR  = "/content/mts_mastercurve_results_full"

MIN_POINTS = 10

# Universal mastercurve parameters (your paper)
X0_UNIV = 0.966
NU_UNIV = 0.942

# Fit mode:
#   "A" = fit only (Vinf, Rs) with (x0, nu) fixed universal
#   "B" = fit (Vinf, Rs, nu) with x0 fixed universal (nu varies per galaxy)
FIT_MODE = "A"

# Bounds (keep sane)
VINF_BOUNDS = (5.0, 600.0)     # km/s
RS_BOUNDS   = (0.05, 80.0)     # kpc
NU_BOUNDS   = (0.3, 3.0)

# QC thresholds
QC_MIN_TAIL = 2.0              # require rmax/Rs >= this
QC_MAX_TAIL = 50.0             # optional: reject if rmax/Rs is insane (scale collapse)
QC_CHI2_MAX = np.inf           # keep as inf for "QC-A"; use 10 or 5 for stricter

# Collapse plot settings
X_PLOT_MAX = 4.0

# =========================
# SETUP
# =========================
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Unzip if rotmod files not present
if len(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat"))) < 10:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)

files = sorted(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat")))
print("Files found:", len(files))

# =========================
# MODEL
# =========================
def y_master(x, x0=X0_UNIV, nu=NU_UNIV):
    x = np.maximum(x, 0.0)
    return 1.0 - np.exp(- (x / x0)**nu)

def model_A(r, Vinf, Rs):
    x = r / np.maximum(Rs, 1e-9)
    return Vinf * y_master(x, X0_UNIV, NU_UNIV)

def model_B(r, Vinf, Rs, nu):
    x = r / np.maximum(Rs, 1e-9)
    return Vinf * y_master(x, X0_UNIV, nu)

def load_rotmod(fp):
    """
    SPARC rotmod format is typically columns:
      r[kpc], V[km/s], err[km/s], (then other columns we ignore)
    """
    try:
        data = np.loadtxt(fp)
        if data.ndim != 2 or data.shape[0] < MIN_POINTS or data.shape[1] < 3:
            return None
        r = data[:, 0].astype(float)
        v = data[:, 1].astype(float)
        e = data[:, 2].astype(float)

        m = (
            np.isfinite(r) & np.isfinite(v) & np.isfinite(e) &
            (r > 0) & (v > 0)
        )
        if m.sum() < MIN_POINTS:
            return None

        r, v, e = r[m], v[m], e[m]

        # If errors are missing/zero, patch them
        if np.any(e <= 0):
            e2 = e.copy()
            good = e2 > 0
            fallback = float(np.median(e2[good])) if np.any(good) else 5.0
            e2[e2 <= 0] = fallback
            e = e2

        return r, v, e
    except Exception:
        return None

def r50_of_v(r, v):
    """Radius where v first reaches 50% of V95 (robust)."""
    if len(r) == 0:
        return np.nan
    v95 = np.percentile(v, 95)
    target = 0.5 * v95
    idx = np.where(v >= target)[0]
    if len(idx) == 0:
        return float(np.median(r))
    return float(r[idx[0]])

# =========================
# FIT LOOP
# =========================
rows = []
curves_for_plot = []    # (x,y) for QC-pass curves
all_residuals = []      # y - y_master(x) for QC-pass

n_total = 0
n_loaded = 0
n_fit_ok = 0
n_ok = 0
n_reject = 0
n_load_fail = 0

for fp in files:
    n_total += 1
    name = os.path.basename(fp).replace("_rotmod.dat", "")

    dat = load_rotmod(fp)
    if dat is None:
        n_load_fail += 1
        rows.append({"Galaxy": name, "status": "load_fail"})
        continue

    n_loaded += 1
    r, v, e = dat
    r50_kpc = r50_of_v(r, v)

    # Initial guesses
    V0 = float(np.clip(np.percentile(v, 95), VINF_BOUNDS[0], VINF_BOUNDS[1]))
    # Rs guess: r where v reaches half of V0 else median r
    idx = np.where(v >= 0.5 * V0)[0]
    Rs0 = float(r[idx[0]] if len(idx) > 0 else np.median(r))
    Rs0 = float(np.clip(Rs0, RS_BOUNDS[0], RS_BOUNDS[1]))

    Vinf_fit = np.nan
    Rs_fit = np.nan
    nu_fit = np.nan
    rmse = np.nan
    chi2red = np.nan
    rmax_over_Rs = np.nan

    try:
        if FIT_MODE == "A":
            popt, pcov = curve_fit(
                model_A, r, v,
                p0=[V0, Rs0],
                sigma=e, absolute_sigma=True,
                bounds=([VINF_BOUNDS[0], RS_BOUNDS[0]],
                        [VINF_BOUNDS[1], RS_BOUNDS[1]]),
                maxfev=20000
            )
            Vinf_fit, Rs_fit = map(float, popt)
            nu_fit = float(NU_UNIV)
            vpred = model_A(r, Vinf_fit, Rs_fit)

        else:
            popt, pcov = curve_fit(
                model_B, r, v,
                p0=[V0, Rs0, NU_UNIV],
                sigma=e, absolute_sigma=True,
                bounds=([VINF_BOUNDS[0], RS_BOUNDS[0], NU_BOUNDS[0]],
                        [VINF_BOUNDS[1], RS_BOUNDS[1], NU_BOUNDS[1]]),
                maxfev=30000
            )
            Vinf_fit, Rs_fit, nu_fit = map(float, popt)
            vpred = model_B(r, Vinf_fit, Rs_fit, nu_fit)

        n_fit_ok += 1

        rmse = float(np.sqrt(np.mean((v - vpred) ** 2)))
        dof = max(len(r) - (2 if FIT_MODE == "A" else 3), 1)
        chi2 = float(np.sum(((v - vpred) / e) ** 2))
        chi2red = float(chi2 / dof)

        rmax_over_Rs = float(np.max(r) / max(Rs_fit, 1e-9))

        # Bound-hugging check
        bound_hit = False
        if abs(Vinf_fit - VINF_BOUNDS[0]) < 1e-9 or abs(Vinf_fit - VINF_BOUNDS[1]) < 1e-9:
            bound_hit = True
        if abs(Rs_fit - RS_BOUNDS[0]) < 1e-9 or abs(Rs_fit - RS_BOUNDS[1]) < 1e-9:
            bound_hit = True
        if FIT_MODE == "B":
            if abs(nu_fit - NU_BOUNDS[0]) < 1e-9 or abs(nu_fit - NU_BOUNDS[1]) < 1e-9:
                bound_hit = True

        # QC
        tail_ok = (rmax_over_Rs >= QC_MIN_TAIL)
        tail_not_insane = (rmax_over_Rs <= QC_MAX_TAIL)
        chi_ok = (chi2red <= QC_CHI2_MAX)

        qc_ok = (not bound_hit) and tail_ok and tail_not_insane and chi_ok \
                and np.isfinite(rmse) and np.isfinite(chi2red) and np.isfinite(Vinf_fit) and np.isfinite(Rs_fit)

        status = "ok" if qc_ok else "reject"
        if qc_ok:
            n_ok += 1
            x = r / Rs_fit
            y = v / Vinf_fit
            y_m = y_master(x, X0_UNIV, nu_fit)
            all_residuals.extend((y - y_m).tolist())
            curves_for_plot.append((x, y))
        else:
            n_reject += 1

    except Exception:
        status = "fit_fail"
        # treat as reject-like for counts but keep explicit label
        n_reject += 1

    rows.append({
        "Galaxy": name,
        "status": status,
        "N": float(len(r)),
        "Vinf_fit": Vinf_fit,
        "Rs_fit": Rs_fit,
        "nu_fit": nu_fit,
        "rmse_kms": rmse,
        "chi2red": chi2red,
        "rmax_over_Rs": rmax_over_Rs,
        "r50_kpc": r50_kpc
    })

df = pd.DataFrame(rows)

csv_path = os.path.join(OUT_DIR, "mastercurve_fit_results_full.csv")
df.to_csv(csv_path, index=False)

print("\nTotal files:", n_total)
print("Loaded:", n_loaded)
print("OK (QC-pass):", n_ok)
print("Reject:", n_reject)
print("Load fail:", n_load_fail)
print("CSV saved:", csv_path)

# =========================
# MASTER CURVE STATS + PLOT
# =========================
res = np.array(all_residuals, dtype=float)
if res.size == 0:
    print("\nNo QC-pass residuals produced. Loosen QC or check data.")
else:
    rms = float(np.sqrt(np.mean(res ** 2)))
    mean_abs = float(np.mean(np.abs(res)))
    print("\nMastercurve collapse (QC-pass):")
    print("RMS scatter:", rms)
    print("Mean |Δ|:", mean_abs)

    plt.figure(figsize=(7, 5))
    for x, y in curves_for_plot:
        plt.plot(x, y, alpha=0.08, lw=0.6)

    xx = np.linspace(0, X_PLOT_MAX, 400)
    plt.plot(xx, y_master(xx, X0_UNIV, NU_UNIV), lw=3)

    plt.xlim(0, X_PLOT_MAX)
    plt.ylim(0, 1.4)
    plt.xlabel("x = r / Rs_fit")
    plt.ylabel("y = V / Vinf_fit")
    plt.title(f"SPARC Mastercurve Collapse | mode {FIT_MODE} | QC-pass={n_ok}")

    plot_path = os.path.join(OUT_DIR, "mastercurve_collapse_full.png")
    plt.savefig(plot_path, dpi=160, bbox_inches="tight")
    plt.show()
    print("Plot saved:", plot_path)

# =========================
# OPTIONAL: QC STRICTNESS TABLE (QC-A/B/C)
# =========================
def collapse_stats(mask):
    dd = df[mask].copy()
    # We need residuals; recompute from stored params by reloading each galaxy file.
    # (This is reliable + keeps the table honest.)
    resids = []
    curves = 0
    for fp in files:
        name = os.path.basename(fp).replace("_rotmod.dat", "")
        row = dd[dd["Galaxy"] == name]
        if row.empty:
            continue
        row = row.iloc[0]
        if not np.isfinite(row["Vinf_fit"]) or not np.isfinite(row["Rs_fit"]):
            continue
        dat = load_rotmod(fp)
        if dat is None:
            continue
        r, v, e = dat
        Vinf_fit = float(row["Vinf_fit"])
        Rs_fit = float(row["Rs_fit"])
        nu_fit = float(row["nu_fit"]) if np.isfinite(row["nu_fit"]) else NU_UNIV
        x = r / max(Rs_fit, 1e-9)
        y = v / max(Vinf_fit, 1e-9)
        y_m = y_master(x, X0_UNIV, nu_fit)
        resids.extend((y - y_m).tolist())
        curves += 1
    resids = np.array(resids, dtype=float)
    if resids.size == 0:
        return curves, np.nan, np.nan
    return curves, float(np.sqrt(np.mean(resids**2))), float(np.mean(np.abs(resids)))

# QC-A: exactly status=="ok"
mask_A = (df["status"] == "ok")

# QC-B: ok + chi2red < 10
mask_B = (df["status"] == "ok") & (df["chi2red"] < 10)

# QC-C: ok + chi2red < 5
mask_C = (df["status"] == "ok") & (df["chi2red"] < 5)

curA, rmsA, madA = collapse_stats(mask_A)
curB, rmsB, madB = collapse_stats(mask_B)
curC, rmsC, madC = collapse_stats(mask_C)

tab = pd.DataFrame({
    "QC_level": ["A (ok)", "B (ok & chi2red<10)", "C (ok & chi2red<5)"],
    "galaxies_used": [int(mask_A.sum()), int(mask_B.sum()), int(mask_C.sum())],
    "curves_recomputed": [curA, curB, curC],
    "RMS_scatter": [rmsA, rmsB, rmsC],
    "MeanAbs_scatter": [madA, madB, madC],
})

tab_path = os.path.join(OUT_DIR, "qc_strictness_table.csv")
tab.to_csv(tab_path, index=False)
print("\nQC strictness table saved:", tab_path)
print(tab)




