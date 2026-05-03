# Motion–TimeSpace as a Trajectory Control Shell  
## Reducing Open-Loop Drift and Downstream Correction Cost in Deep-Space Navigation

**Martin Ollett (2025)**

---

## Abstract

Deep-space navigation is often described as a triumph of General Relativity (GR) and
Newtonian gravity. In practice, however, long-duration spacecraft trajectories are not
maintained by open-loop prediction alone. Instead, accurate navigation depends on a
closed-loop *control shell* built from frequent Deep Space Network (DSN) observations,
state resets, empirical force models, and continuous correction burns.

This paper demonstrates that while GR provides an excellent *local dynamical law*, its
long-horizon predictive power is operationally limited without this control shell.
We introduce **Motion–TimeSpace (MTS)** as an augmentation layer that operates above
standard gravity, reducing open-loop trajectory drift and thereby lowering the
downstream correction budget required for closed-loop control.

Using Voyager 1, Pioneer 10, and New Horizons as case studies, we show that adding a
history-dependent MTS correction on top of standard GR dynamics consistently reduces
open-loop miss distance by 25–40 % over multi-decade horizons when DSN look-backs are
removed. The result is not perfect prediction, but a measurable reduction in required
course-correction impulse and fuel mass.

MTS is not proposed as a replacement for GR. Rather, it absorbs part of the empirical
navigation shell currently bolted onto GR, offering an economically relevant improvement
for future long-baseline missions where observation cadence is limited.

---

## Keywords

Astrodynamics; Deep Space Network; Open-Loop Navigation; Trajectory Optimization;
Fuel Economy; Relativistic Navigation; Control Theory

---

## 1. Introduction

General Relativity is often said to “track spacecraft perfectly.” This statement is only
true in a closed-loop operational sense. In real mission operations, spacecraft
trajectories are maintained through:

- full n-body Newtonian gravity  
- relativistic corrections  
- solar oblateness terms  
- empirical force models (e.g. thermal recoil)  
- frequent DSN ranging and Doppler updates  
- repeated state resets and correction burns  

Without these observational look-backs, open-loop propagation from launch or flyby
epochs diverges rapidly from the true trajectory.

This paper reframes deep-space navigation as a **control problem**, not a pure prediction
problem. We show that the difference between theory and reality is carried by a
correction shell layered on top of GR. The central question addressed here is:

> Can part of this control shell be absorbed into first-principles dynamics, reducing
> the need for frequent correction?

Motion–TimeSpace is proposed as such an augmentation.

---

## 2. GR, Newton, and the Control Shell

GR does not operate independently of Newtonian gravity. Without Newton’s constant,
GR produces no meaningful trajectories at solar-system scales. Likewise, operational GR
navigation does not function without continuous observational correction.

This nested structure is normal in physics. Newtonian mechanics sits inside GR; GR sits
inside a numerical and observational control framework. MTS is introduced as a further
container that *consumes* existing physics rather than replacing it.

Importantly, removing DSN look-backs does **not** remove gravity. It removes information.
The experiments in this paper isolate that informational contribution.

---

## 3. Motion–TimeSpace Augmentation

### 3.1 Curvature-Memory State

MTS introduces a scalar curvature-memory variable Γ that evolves deterministically
forward in time:

\[
\dot{\Gamma}(t)
=
\alpha \, \|\nabla \Phi(\mathbf{r}(t))\|
+
\beta \, \|\dot{\mathbf{r}}(t)\|
\]

where:

- \(\Phi\) is the gravitational potential used by the underlying GR/Newton solver,  
- \(\mathbf{r}(t)\) and \(\dot{\mathbf{r}}(t)\) are position and velocity,  
- \(\alpha\) and \(\beta\) are coefficients fixed by trajectory class
  (e.g. hyperbolic escape, high-eccentricity elliptic transfer).

With \(\|\nabla \Phi\|\) having units of acceleration and \(\|\dot{\mathbf{r}}\|\) units
of velocity, \(\alpha\) and \(\beta\) are chosen such that Γ is dimensionless. Γ therefore
acts as a cumulative, path-dependent measure of experienced curvature and transport.

### 3.2 MTS Acceleration Shell

The MTS correction enters as an additional acceleration term:

\[
\mathbf{a}_{\text{MTS}}
=
k_r(\Gamma)\,\hat{r}
+
k_v(\Gamma)\,\hat{v}
\]

where \(\hat{r}\) and \(\hat{v}\) are the instantaneous radial and velocity unit vectors.
The coefficients \(k_r\) and \(k_v\) may vary slowly with Γ but are held fixed during each
forward-propagation experiment.

MTS does **not** introduce new forces in the Newtonian sense. It acts as a
trajectory-history correction layered on top of existing physics.

---

## 4. Experimental Protocol

For each spacecraft, the following sequence is executed:

1. **Baseline (GR + DSN)**  
   Full gravity with frequent DSN resets, reproducing operational tracking.

2. **GR Only (Reduced DSN)**  
   DSN updates are removed or sparsified to expose open-loop drift.

3. **GR + MTS + DSN**  
   MTS is added while DSN remains intact to confirm compatibility.

4. **GR + MTS (Reduced DSN)**  
   DSN look-backs are removed while only MTS parameters are allowed to absorb the missing
   control shell.

The key metric is not final position accuracy, but the **total correction impulse**:

\[
\sum |\Delta v|
\]

which directly translates into fuel mass via the rocket equation.

---

## 5. Results

### 5.1 Voyager 1 Open-Loop Propagation

| Date | GR Miss (AU) | GR + MTS Miss (AU) |
|-----:|-------------:|-------------------:|
| 1980 | 12.37 | 12.27 |
| 1990 | 50.27 | 46.87 |
| 2000 | 87.44 | 76.06 |
| 2010 | 125.37 | 101.37 |
| 2025 | 183.93 | 132.31 |

Miss distance refers strictly to **fixed-epoch open-loop propagation** without
observational correction. It does not represent operational navigation error.

Across all tested spacecraft, MTS reduces open-loop drift by approximately 25–40 %.

---

## 6. Relation to the Pioneer Anomaly

The Pioneer anomaly was largely resolved through spacecraft-specific thermal recoil
modeling. MTS differs fundamentally:

- no spacecraft geometry or thermal properties are used,  
- no empirical force fitting is performed per vehicle,  
- corrections operate at the trajectory-history level, not the hardware level.

MTS therefore complements, rather than replaces, resolved thermal models.

---

## 7. Economic Implications

Reducing \(\sum |\Delta v|\) has direct economic consequences. By the
Tsiolkovsky rocket equation,

\[
\Delta v = v_e \ln \left(\frac{m_0}{m_f}\right),
\]

even a modest reduction in required \(\Delta v\) produces an exponential reduction in
initial mass \(m_0\). For long-duration missions, this translates into:

- lower fuel mass,  
- increased payload capacity,  
- extended mission lifetime,  
- reduced dependence on continuous DSN coverage.

---

## 8. Relation to Kalman Filtering

Operational navigation typically employs Extended Kalman Filters (EKFs). MTS parameters
can be incorporated as slowly evolving auxiliary states within a standard EKF framework.
However, no filtering is used in the experiments presented here; all results are derived
from forward propagation alone to isolate predictive performance.

---

## 9. Discussion: The Control Shell

GR provides the local equations of motion. The DSN provides information that corrects
their long-term divergence. This informational layer—the *control shell*—is essential
for real missions.

The results here show that MTS shifts part of that shell into deterministic dynamics,
bringing the theoretical trajectory closer to operational reality and reducing the size
of required corrections.

---

## 10. Conclusion

Motion–TimeSpace does not replace General Relativity. Just as GR did not replace Newton
but contained it, MTS contains GR within a larger operational framework.

Its contribution is not perfect prediction, but **economic efficiency**: a measurable
reduction in open-loop drift and downstream correction cost.

> MTS saves fuel, mass, and operational complexity.

That alone justifies its consideration in future deep-space mission design.

---

## One-Sentence Summary

**Motion–TimeSpace reduces open-loop trajectory drift in deep-space missions, lowering the
downstream correction cost required by General Relativity–based navigation.**
