import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# 3D PRIME CURVATURE LANDSCAPE
# ==========================================================

N = 20000  # keep smaller for performance
primes = list(sp.primerange(3, N))
prime_set = set(primes)

P = []
Q = []
ERR = []

# scan near-90° curvature for threshold
threshold = 300

for i in range(0, len(primes), 5):  # subsample to keep plot light
    p = primes[i]
    for j in range(i, len(primes), 5):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p)
            Q.append(q)
            ERR.append(err)

P = np.array(P)
Q = np.array(Q)
ERR = np.array(ERR)

# 3D plot
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(P, Q, ERR, s=5)  # default color scheme

ax.set_xlabel("Prime p")
ax.set_ylabel("Prime q")
ax.set_zlabel("Curvature Imbalance |p²+q²−r²|")
ax.set_title("3D Prime Curvature Landscape – Near-90° Geometry")

plt.tight_layout()
plt.show()



import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# 3D PRIME CURVATURE LANDSCAPE
# ==========================================================

N = 20000  # keep smaller for performance
primes = list(sp.primerange(3, N))
prime_set = set(primes)

P = []
Q = []
ERR = []

# scan near-90° curvature for threshold
threshold = 300

for i in range(0, len(primes), 5):  # subsample to keep plot light
    p = primes[i]
    for j in range(i, len(primes), 5):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p)
            Q.append(q)
            ERR.append(err)

P = np.array(P)
Q = np.array(Q)
ERR = np.array(ERR)

# 3D plot
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(P, Q, ERR, s=5)  # default color scheme

ax.set_xlabel("Prime p")
ax.set_ylabel("Prime q")
ax.set_zlabel("Curvature Imbalance |p²+q²−r²|")
ax.set_title("3D Prime Curvature Landscape – Near-90° Geometry")

plt.tight_layout()
plt.show()



import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# ==========================================================
#  OPTION A — GUARANTEED SUCCESS (FAST + CLEAN)
#  Rotating 3D Prime Curvature Landscape (MP4)
# ==========================================================

# Generate small prime dataset
N = 5000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 300

# Light sampling for speed
for i in range(0, len(primes), 12):
    p = primes[i]
    for j in range(i, len(primes), 12):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# ==========================================================
# Create 3D figure (small + simple)
# ==========================================================
fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(P, Q, ERR, s=4, c=ERR, cmap="inferno")
ax.set_xlabel("Prime p")
ax.set_ylabel("Prime q")
ax.set_zlabel("|p²+q²−r²|")
ax.set_title("3D Prime Curvature Landscape – Rotation (Fast Mode)")

# ==========================================================
# Animation function
# ==========================================================
def rotate(frame):
    ax.view_init(elev=22, azim=frame)
    return (sc,)

anim = animation.FuncAnimation(fig, rotate, frames=120, interval=40, blit=False)

# ==========================================================
# Save MP4
# ==========================================================
output_path = "/mnt/data/prime_curvature_rotation_fast.mp4"
anim.save(output_path, writer="ffmpeg", fps=30)

output_path




import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# ==========================================================
# 3D SURFACE OF PRIME CURVATURE ERROR (Gravitational-like)
# ==========================================================

# Generate primes
N = 3000  # keep small for surface interpolation
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

# sample pairs
for i in range(0, len(primes), 5):
    p = primes[i]
    for j in range(0, len(primes), 5):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# grid for surface
grid_x, grid_y = np.mgrid[min(P):max(P):200j, min(Q):max(Q):200j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# ==========================================================
# Plot surface
# ==========================================================
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap="inferno", linewidth=0, antialiased=True)

ax.set_xlabel("Prime p")
ax.set_ylabel("Prime q")
ax.set_zlabel("Curvature Error |p²+q²−r²|")
ax.set_title("3D Surface – Prime Curvature Error Field (Gravity-like Potential)")

plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==========================================================
# 2D CONTOUR MAP — Prime Curvature Potential
# ==========================================================

N = 2000  # smaller for safety
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

# light sampling
for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# surface grid
grid_x, grid_y = np.mgrid[min(P):max(P):200j, min(Q):max(Q):200j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

plt.figure(figsize=(10,8))
cp = plt.contourf(grid_x, grid_y, grid_z, 40, cmap="inferno")

plt.colorbar(cp, label="Curvature Error |p²+q²−r²|")
plt.title("Prime Curvature Potential – 2D Contour Map")
plt.xlabel("Prime p")
plt.ylabel("Prime q")

plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==========================================================
# OPTION A — LAPLACIAN OF THE PRIME CURVATURE POTENTIAL
# ==========================================================

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# Grid
grid_x, grid_y = np.mgrid[min(P):max(P):200j, min(Q):max(Q):200j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# Compute Laplacian
dx = grid_x[1,0] - grid_x[0,0]
dy = grid_y[0,1] - grid_y[0,0]

laplacian = (
    (np.roll(grid_z, -1, axis=0) - 2*grid_z + np.roll(grid_z, 1, axis=0)) / dx**2 +
    (np.roll(grid_z, -1, axis=1) - 2*grid_z + np.roll(grid_z, 1, axis=1)) / dy**2
)

# ==========================================================
# Plot Laplacian
# ==========================================================

plt.figure(figsize=(10,8))
cp = plt.contourf(grid_x, grid_y, laplacian, 40, cmap="coolwarm")
plt.colorbar(cp, label="Laplacian( Curvature Potential )")

plt.title("Laplacian of Prime Curvature Potential – Curvature Hotspots Map")
plt.xlabel("Prime p")
plt.ylabel("Prime q")

plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==========================================================
# OPTION B — GRADIENT VECTOR FIELD OF PRIME CURVATURE POTENTIAL
# ==========================================================

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# interpolation grid
grid_x, grid_y = np.mgrid[min(P):max(P):150j, min(Q):max(Q):150j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# compute gradients (negative gradient = "curvature flow")
dx = grid_x[1,0] - grid_x[0,0]
dy = grid_y[0,1] - grid_y[0,0]

grad_x = -(np.roll(grid_z, -1, axis=0) - np.roll(grid_z, 1, axis=0)) / (2*dx)
grad_y = -(np.roll(grid_z, -1, axis=1) - np.roll(grid_z, 1, axis=1)) / (2*dy)

# ==========================================================
# Plot gradient vector field
# ==========================================================

plt.figure(figsize=(10,8))
plt.contourf(grid_x, grid_y, grid_z, 40, cmap="inferno", alpha=0.6)
plt.colorbar(label="Curvature Error |p²+q²−r²|")

# quiver (vector field)
skip = (slice(None,None,5), slice(None,None,5))
plt.quiver(grid_x[skip], grid_y[skip], grad_x[skip], grad_y[skip], 
           color="white", scale=2000, width=0.002)

plt.title("Prime Curvature Gradient Field – (Negative Gradient = Curvature Flow)")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==========================================================
# OPTION B — GRADIENT VECTOR FIELD OF PRIME CURVATURE POTENTIAL
# ==========================================================

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# interpolation grid
grid_x, grid_y = np.mgrid[min(P):max(P):150j, min(Q):max(Q):150j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# compute gradients (negative gradient = "curvature flow")
dx = grid_x[1,0] - grid_x[0,0]
dy = grid_y[0,1] - grid_y[0,0]

grad_x = -(np.roll(grid_z, -1, axis=0) - np.roll(grid_z, 1, axis=0)) / (2*dx)
grad_y = -(np.roll(grid_z, -1, axis=1) - np.roll(grid_z, 1, axis=1)) / (2*dy)

# ==========================================================
# Plot gradient vector field
# ==========================================================

plt.figure(figsize=(10,8))
plt.contourf(grid_x, grid_y, grid_z, 40, cmap="inferno", alpha=0.6)
plt.colorbar(label="Curvature Error |p²+q²−r²|")

# quiver (vector field)
skip = (slice(None,None,5), slice(None,None,5))
plt.quiver(grid_x[skip], grid_y[skip], grad_x[skip], grad_y[skip], 
           color="white", scale=2000, width=0.002)

plt.title("Prime Curvature Gradient Field – (Negative Gradient = Curvature Flow)")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==========================================================
# OPTION C — DIVERGENCE & CURL MAPS OF PRIME CURVATURE FIELD
# ==========================================================

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

# light sampling
for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# Grid
grid_x, grid_y = np.mgrid[min(P):max(P):150j, min(Q):max(Q):150j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# Compute gradients
dx = grid_x[1,0] - grid_x[0,0]
dy = grid_y[0,1] - grid_y[0,0]

grad_x = -(np.roll(grid_z, -1, axis=0) - np.roll(grid_z, 1, axis=0)) / (2*dx)
grad_y = -(np.roll(grid_z, -1, axis=1) - np.roll(grid_z, 1, axis=1)) / (2*dy)

# Divergence: dFx/dx + dFy/dy
div = (
    (np.roll(grad_x, -1, axis=0) - np.roll(grad_x, 1, axis=0)) / (2*dx) +
    (np.roll(grad_y, -1, axis=1) - np.roll(grad_y, 1, axis=1)) / (2*dy)
)

# Curl (z‑component): dFy/dx − dFx/dy
curl = (
    (np.roll(grad_y, -1, axis=0) - np.roll(grad_y, 1, axis=0)) / (2*dx) -
    (np.roll(grad_x, -1, axis=1) - np.roll(grad_x, 1, axis=1)) / (2*dy)
)

# ==========================================================
# PLOT — DIVERGENCE
# ==========================================================
plt.figure(figsize=(10,8))
plt.contourf(grid_x, grid_y, div, 40, cmap="coolwarm")
plt.colorbar(label="Divergence( Curvature Flow )")
plt.title("Prime Curvature Divergence Map")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()

# ==========================================================
# PLOT — CURL
# ==========================================================
plt.figure(figsize=(10,8))
plt.contourf(grid_x, grid_y, curl, 40, cmap="coolwarm")
plt.colorbar(label="Curl_z( Curvature Flow )")
plt.title("Prime Curvature Curl Map (Vorticity of Curvature Field)")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()



import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

# ==========================================================
# OPTION D — CMB‑STYLE SMOOTHED PRIME CURVATURE HEATMAP
# ==========================================================

# Generate primes
N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

# Light sampling for speed
for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# Grid for interpolation
grid_x, grid_y = np.mgrid[min(P):max(P):250j, min(Q):max(Q):250j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# Apply CMB-style smoothing
grid_z_smooth = gaussian_filter(grid_z, sigma=6)

# ==========================================================
# Plot — CMB‑style curvature heatmap
# ==========================================================

plt.figure(figsize=(10,8))
plt.imshow(
    grid_z_smooth.T,
    extent=[min(P), max(P), min(Q), max(Q)],
    origin="lower",
    cmap="inferno"
)
plt.colorbar(label="Curvature Error |p²+q²−r²| (Smoothed)")
plt.title("Prime Curvature Potential — CMB‑Style Smoothed Heatmap")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter, sobel, binary_erosion

# ==========================================================
# OPTION E — PGF-STYLE TOPOLOGICAL SKELETON OF PRIME CURVATURE FIELD
# ==========================================================

# Generate primes (small for speed)
N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

# Sample primes
for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# Grid
grid_x, grid_y = np.mgrid[min(P):max(P):250j, min(Q):max(Q):250j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# Smooth the field
smooth = gaussian_filter(grid_z, sigma=4)

# Compute gradient magnitude to highlight structural ridges
sx = sobel(smooth, axis=0)
sy = sobel(smooth, axis=1)
grad_mag = np.hypot(sx, sy)

# Threshold to isolate strong structures
mask = grad_mag > np.percentile(grad_mag, 85)

# Morphological skeletonization alternative (simple)
eroded = binary_erosion(mask, iterations=2)

# ==========================================================
# Plot skeleton over smoothed curvature map
# ==========================================================

plt.figure(figsize=(10,8))
plt.imshow(
    smooth.T,
    extent=[min(P), max(P), min(Q), max(Q)],
    origin="lower",
    cmap="inferno",
    alpha=0.8
)
plt.imshow(
    eroded.T,
    extent=[min(P), max(P), min(Q), max(Q)],
    origin="lower",
    cmap="winter",
    alpha=0.7
)

plt.title("Prime Curvature Topological Skeleton (PGF Backbone)")
plt.xlabel("Prime p")
plt.ylabel("Prime q")
plt.tight_layout()
plt.show()

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import mpmath as mp

# ==========================================================
# OPTION F — OVERLAY RIEMANN ZEROS ON PRIME CURVATURE CMB MAP
# (using mpmath.findroot instead of unavailable zeta_zeros)
# ==========================================================

# -----------------------------
# 1. Generate prime curvature field
# -----------------------------

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# interpolation grid
grid_x, grid_y = np.mgrid[min(P):max(P):300j, min(Q):max(Q):300j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# smooth (CMB-style)
smooth = gaussian_filter(grid_z, sigma=6)


# -----------------------------
# 2. Compute first ~20 Riemann zeros using findroot
# -----------------------------

mp.mp.dps = 40

t_guesses = [
    14.134725, 21.02204, 25.01085, 30.4249, 32.9351,
    37.5862, 40.9187, 43.3271, 48.0051, 49.7738,
    52.9703, 56.4462, 59.347, 60.8317, 65.1125,
    67.0798, 69.5464, 72.0672, 75.7047, 77.1448
]

zeros = []
for g in t_guesses:
    try:
        root = mp.findroot(lambda t: mp.zeta(0.5 + 1j*t), g)
        zeros.append(complex(root))
    except:
        pass

t_vals = np.array([float(z.imag) for z in zeros])

# scale zeros to prime plot range
t_min, t_max = t_vals.min(), t_vals.max()
plot_min = min(P)
plot_max = max(P)

scaled = plot_min + (t_vals - t_min) * (plot_max - plot_min) / (t_max - t_min)

rz_x = scaled
rz_y = scaled


# -----------------------------
# 3. Plot curvature map + RZ overlay
# -----------------------------

plt.figure(figsize=(11, 9))
plt.imshow(
    smooth.T,
    extent=[min(P), max(P), min(Q), max(Q)],
    origin="lower",
    cmap="inferno",
    alpha=0.9
)

plt.scatter(rz_x, rz_y, c="cyan", s=40, edgecolor="black", label="Riemann Zeros (scaled)")

plt.legend()
plt.colorbar(label="Curvature Error |p²+q²−r²| (Smoothed)")
plt.title("Riemann Zeros Overlaid on Prime Curvature Potential Map")
plt.xlabel("Prime p")
plt.ylabel("Prime q")

plt.tight_layout()
plt.show()

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import mpmath as mp

# ==========================================================
# OPTION F — OVERLAY RIEMANN ZEROS ON PRIME CURVATURE CMB MAP
# (using mpmath.findroot instead of unavailable zeta_zeros)
# ==========================================================

# -----------------------------
# 1. Generate prime curvature field
# -----------------------------

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# interpolation grid
grid_x, grid_y = np.mgrid[min(P):max(P):300j, min(Q):max(Q):300j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# smooth (CMB-style)
smooth = gaussian_filter(grid_z, sigma=6)


# -----------------------------
# 2. Compute first ~20 Riemann zeros using findroot
# -----------------------------

mp.mp.dps = 40

t_guesses = [
    14.134725, 21.02204, 25.01085, 30.4249, 32.9351,
    37.5862, 40.9187, 43.3271, 48.0051, 49.7738,
    52.9703, 56.4462, 59.347, 60.8317, 65.1125,
    67.0798, 69.5464, 72.0672, 75.7047, 77.1448
]

zeros = []
for g in t_guesses:
    try:
        root = mp.findroot(lambda t: mp.zeta(0.5 + 1j*t), g)
        zeros.append(complex(root))
    except:
        pass

t_vals = np.array([float(z.imag) for z in zeros])

# scale zeros to prime plot range
t_min, t_max = t_vals.min(), t_vals.max()
plot_min = min(P)
plot_max = max(P)

scaled = plot_min + (t_vals - t_min) * (plot_max - plot_min) / (t_max - t_min)

rz_x = scaled
rz_y = scaled


# -----------------------------
# 3. Plot curvature map + RZ overlay
# -----------------------------

plt.figure(figsize=(11, 9))
plt.imshow(
    smooth.T,
    extent=[min(P), max(P), min(Q), max(Q)],
    origin="lower",
    cmap="inferno",
    alpha=0.9
)

plt.scatter(rz_x, rz_y, c="cyan", s=40, edgecolor="black", label="Riemann Zeros (scaled)")

plt.legend()
plt.colorbar(label="Curvature Error |p²+q²−r²| (Smoothed)")
plt.title("Riemann Zeros Overlaid on Prime Curvature Potential Map")
plt.xlabel("Prime p")
plt.ylabel("Prime q")

plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from numpy.fft import fft2, fftshift

# ==========================================================
# OPTION G — 2D POWER SPECTRUM (CMB Cl-STYLE) OF PRIME CURVATURE FIELD
# ==========================================================

# -----------------------------
# 1. Generate prime curvature field
# -----------------------------

N = 2000
primes = list(sp.primerange(3, N))

P=[]; Q=[]; ERR=[]
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P=np.array(P); Q=np.array(Q); ERR=np.array(ERR)

# Interpolation Grid
grid_x, grid_y = np.mgrid[min(P):max(P):300j, min(Q):max(Q):300j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# CMB-style smoothing
field = gaussian_filter(grid_z, sigma=6)

# -----------------------------
# 2. Compute 2D FFT power spectrum
# -----------------------------

fft_map = fftshift(fft2(field))
power = np.abs(fft_map)**2

# Create radial bins for 1D "Cl" style spectrum
ny, nx = power.shape
cy, cx = ny//2, nx//2

Y, X = np.ogrid[:ny, :nx]
R = np.sqrt((X - cx)**2 + (Y - cy)**2)

r_max = int(R.max())
radial_ps = np.zeros(r_max)
counts = np.zeros(r_max)

for r in range(r_max):
    mask = (R >= r) & (R < r+1)
    radial_ps[r] = power[mask].mean() if np.any(mask) else 0
    counts[r] = mask.sum()

# -----------------------------
# 3. Plotting
# -----------------------------

# Full 2D power spectrum
plt.figure(figsize=(10,8))
plt.imshow(np.log10(power + 1), cmap="inferno")
plt.colorbar(label="log₁₀ Power")
plt.title("2D Power Spectrum of Prime Curvature Field")
plt.xlabel("kₓ")
plt.ylabel("kᵧ")
plt.tight_layout()
plt.show()

# Radial spectrum (CMB Cl-style)
plt.figure(figsize=(10,6))
plt.plot(radial_ps, color="cyan")
plt.yscale("log")
plt.xscale("log")
plt.xlabel("Multipole ℓ (radial frequency)")
plt.ylabel("Power")
plt.title("Prime Curvature Angular Power Spectrum (CMB Cl Analogue)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter, sobel

# ==========================================================
# OPTION I — COMPOSITE FIGURE (4‑PANEL PRIME–CURVATURE SET)
# ==========================================================

# -----------------------------
# 1. Generate prime curvature field
# -----------------------------
N = 2000
primes = list(sp.primerange(3, N))

P, Q, ERR = [], [], []
threshold = 500

for i in range(0, len(primes), 7):
    p = primes[i]
    for j in range(0, len(primes), 7):
        q = primes[j]
        s = p*p + q*q
        r = int(np.sqrt(s))
        err = abs(s - r*r)
        if err <= threshold:
            P.append(p); Q.append(q); ERR.append(err)

P = np.array(P); Q = np.array(Q); ERR = np.array(ERR)

# Grid
grid_x, grid_y = np.mgrid[min(P):max(P):300j, min(Q):max(Q):300j]
grid_z = griddata((P, Q), ERR, (grid_x, grid_y), method='cubic')

# Smooth field
smooth = gaussian_filter(grid_z, sigma=6)


# -----------------------------
# 2. Gradient magnitude (for skeleton)
# -----------------------------
sx = sobel(smooth, axis=0)
sy = sobel(smooth, axis=1)
grad_mag = np.hypot(sx, sy)


# -----------------------------
# 3. Simple “skeleton mask”
# -----------------------------
mask = grad_mag > np.percentile(grad_mag, 85)


# -----------------------------
# 4. Create composite figure
# -----------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# --- Panel 1: Raw curvature map ---
axs[0,0].imshow(
    grid_z.T, origin="lower",
    extent=[min(P), max(P), min(Q), max(Q)],
    cmap="inferno"
)
axs[0,0].set_title("Prime Curvature Field (Raw)")
axs[0,0].set_xlabel("Prime p")
axs[0,0].set_ylabel("Prime q")

# --- Panel 2: Smoothed curvature map ---
axs[0,1].imshow(
    smooth.T, origin="lower",
    extent=[min(P), max(P), min(Q), max(Q)],
    cmap="inferno"
)
axs[0,1].set_title("Smoothed Curvature (CMB‑style)")
axs[0,1].set_xlabel("Prime p")
axs[0,1].set_ylabel("Prime q")

# --- Panel 3: Gradient magnitude ---
axs[1,0].imshow(
    grad_mag.T, origin="lower",
    extent=[min(P), max(P), min(Q), max(Q)],
    cmap="plasma"
)
axs[1,0].set_title("Curvature Gradient Magnitude")
axs[1,0].set_xlabel("Prime p")
axs[1,0].set_ylabel("Prime q")

# --- Panel 4: Topological skeleton ---
axs[1,1].imshow(
    smooth.T, origin="lower",
    extent=[min(P), max(P), min(Q), max(Q)],
    cmap="inferno", alpha=0.7
)
axs[1,1].imshow(
    mask.T, origin="lower",
    extent=[min(P), max(P), min(Q), max(Q)],
    cmap="winter", alpha=0.7
)
axs[1,1].set_title("PGF‑Style Skeleton Overlay")
axs[1,1].set_xlabel("Prime p")
axs[1,1].set_ylabel("Prime q")

plt.tight_layout()
plt.show()
















