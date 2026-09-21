# Coupled moving-source scalar evolution: flat qualification and GR control

2026-09-14. Private post-checkpoint work. Numerical implementation of the conditional source action, not an unrestricted MTS-to-GR theorem.

## What changes in this step

The previous derivation supplied a source response law and an exact flat-space recoil solution. This step evolves the **spatial scalar field and the moving source together**. The source pressure is evaluated from the live field at its current location; no old rigid-wall force history or analytic reflected waveform drives the numerical PDE.

The exact solution is used only for independent comparison. The earlier rigid-source failure stays intact.

Predecessor:
`DERIVATION-20260914-action-consistent-moving-source.md`.
Its material law and perfect-reflection mechanism remain explicit assumptions. The present bulk is the already identified conditional spherical Einstein-scalar control, not an additional derivation of those assumptions from MTS.

**Result status:** flat-space accuracy qualification, the coupled GR run, independent field/metric checks and the interpolation-warning audit are complete: 17 + 37 + 25 + 22 + 13 checks. This is numerical validation of the declared model, not a completed MTS parent-source or full-GR claim.

## 1. Coordinates, unknowns and clock

Use \(c=1,\kappa=4\pi G\), and let the source's proper time be the numerical time \(\tau\). The inner annular boundary is fixed at \(a=3\); the source is at \(b(\tau)\). Define

\[
 R=a+Hx,\qquad H=b-a,\qquad 0\le x\le1,\qquad w=\dot b .
\]

These are new declared test data on \([3,6]\) initially. They are not a replay of the original \([5,6]\) rigid annulus and not an assertion of regularity at a centre or horizon.

For the scalar conventions inherited from the previous continuum work,

\[
 X=R\chi_R,\qquad Y=p/R,\qquad
 A=Y-X,\qquad B=Y+X,\qquad e=(A^2+B^2)/4.
\]

Here \(A,B\) denote outgoing/incoming characteristic variables, not action coefficients or old cosmological fit parameters. A spherical outgoing wave need not have \(B=0\), because of the \(1/R\) amplitude term.

The radial metric is determined afresh at every time step:

\[
 m_R=\kappa(1-2m/R)e,\quad F=1-2m/R,\qquad
 (\log L)_R={2m\over R^2F},\quad L=N\sqrt F .
\]

An integrating factor computes the first equation, with fixed inner geometric mass \(m(a)=8\kappa\). This gives \(m(a)=.8\) in the \(\kappa=.1\) run and zero in the flat control.

The boundary clock is **not** the old static midpoint prescription. Set

\[
 L_b=\beta_-=\sqrt{F_b+w^2},
\]

so \(dt_-/d\tau=1\), while separately evolving the exterior Schwarzschild time

\[
 {dt_+\over d\tau}={\beta_+\over F_+},\qquad
 \beta_+=\beta_- -{\kappa S\over b}.
\]

Both induced metrics must equal \(-d\tau^2+b^2d\Omega^2\). In flat space, \(t_+\) is inertial Minkowski time, with \(\dot t_+=\sqrt{1+w^2}\); it must not be confused with source proper time.

The implementation rejects loss of the declared regular chart, including \(F\le.15\), nonpositive \(\beta_+\), or crossing the inner boundary. It does not attempt a horizon continuation.

## 2. Derive the moving-domain characteristic PDE

Starting from \(\chi_t=Lp/R^2\) and \(p_t=(R^2L\chi_R)_R\) gives

\[
 A_t+LA_R=-L_RA+{L\over R}B,\qquad
 B_t-LB_R=L_RB-{L\over R}A.
\]

At fixed \(x\), \(R_\tau=xw\), so

\[
 A_\tau+{L-xw\over H}A_x=-L_RA+{L\over R}B,
\]
\[
 B_\tau-{L+xw\over H}B_x=L_RB-{L\over R}A.
\]

The scalar is reconstructed by integrating \(X/R\) inward from \(\chi(b)=0\). Its independent temporal consistency condition is

\[
 \chi_\tau|_x={LY+xwX\over R}.
\]

This is checked separately; defining \(\chi\) by a spatial integral is not by itself proof of the scalar evolution equation.

## 3. Source trace and mechanical evolution

Comoving reflection requires

\[
 B_b=-r_b A_b,\qquad r_b={\beta_- -w\over\beta_-+w}.
\]

The source force uses the corresponding projected normal trace,

\[
 \eta_\chi=-{(\beta_- -w)A_b\over b},\qquad
 \Pi={(\beta_- -w)^2A_b^2\over2b^2}.
\]

At finite resolution the incoming trace is weakly enforced and has a measurable mismatch. Using the stated projected trace for the source force makes the flat discrete work balance consistent. This projection is a boundary discretization, not a new physical coefficient.

The previously derived source law is then evaluated on the live field:

\[
 \dot b=w,\quad
 \dot w={b^2\Pi\beta_+\over S}
       +{2bP\beta_-\beta_+\over S}
       -{m_b\over b^2}
       -{\kappa S\beta_-\over2b^2}.
\]

The main runs use positive-rest-energy dust, \(S=.003,P=0\). This source can fall or recoil; it is not kept at a prescribed radius.

The geometric mass integral

\[
 M=m_b+\kappa S\beta_- -{(\kappa S)^2\over2b}
\]

is evaluated, **not held constant by projection**. The separate diagnostic accumulator
\(\dot W_m=-\kappa b^2\Pi w\) is also not used to overwrite the live radial mass. Agreement of \(m_b-m_b(0)\) with \(W_m\) is therefore a test.

## 4. Boundary discretization and an exact discrete energy check

Reuse the positive-norm fourth-interior/second-boundary summation-by-parts derivative whose rational identity was previously checked:

`scripts/annular_reflecting_boundary_20260914.py`,
`source-intake/navier-stokes/20260914/annular-reflecting-boundary-attempt01/status.json`.

Let \(D\) be its derivative in \(x\), with diagonal quadrature weights \(\omega\).
Put \(c=(L-xw)/H,d=(L+xw)/H\). The split-form interior update is

\[
 \dot A=-\tfrac12[cDA+D(cA)]-\tfrac12(L_R+w/H)A+LB/R,
\]
\[
 \dot B=+\tfrac12[dDB+D(dB)]+\tfrac12(L_R-w/H)B-LA/R.
\]

The split coefficient terms recover the continuum equations and account for the changing grid volume. At the fixed inner boundary add
\(-c_0(A_0-B_0)/\omega_0\) to \(\dot A_0\); at the source add
\(-d_b(B_b+r_bA_b)/\omega_b\) to \(\dot B_b\).
These are simultaneous-approximation-term (SAT) penalties on incoming characteristics.

The density energy \(E_h=H\sum\omega(A^2+B^2)/4\) obeys the discrete identity

\[
 \dot E_h={H\over4}\sum\omega L_R(B^2-A^2)
 -{w(\beta_- -w)\over2(\beta_-+w)}A_b^2-\mathcal D_h,
\]
\[
 \mathcal D_h={L_0\over4}(A_0-B_0)^2+
              {\beta_-+w\over4}(B_b+r_bA_b)^2\ge0.
\]

For flat space, \(L=\beta_-=\sqrt{1+w^2}\), \(L_R=0,F=1\); the source kinetic-energy gain exactly cancels the work term. For dust,

\[
 {d\over d\tau}\left[E_h+S\sqrt{1+w^2}
                  +\int_0^\tau\mathcal D_h ds\right]=0.
\]

Thus we record numerical boundary loss explicitly; we do not silently count it as physical absorption. Replacing moving reflection by the fixed-wall rule while retaining recoil fails a negative-control energy test.

In curved space \(E_h\) is **not** the total ADM/exterior energy. The flat corrected-energy formula must not be used to manufacture GR mass conservation. There we check \(M\), the mass-work law, and the temporal Einstein equation directly.

The 17 algebra/random-grid checks include the completed-square boundary identity, trace projection, split consistency, arbitrary flat-grid states with positive and negative source velocities, and the wrong-reflection control. This is a discrete energy statement, not a nonlinear global stability theorem.

## 5. Flat-space accuracy qualification

Incoming data use the previously declared compact profile
\(f=A_0\exp[1-1/(1-x_f^2)]\), \(|x_f|<1\), zero otherwise,
\(x_f=(u+5.5)/.3\). At initial rest,
\(X=-f'(-R)-f(-R)/R\), \(Y=f'(-R)\).

Two pulse strengths, \(A_0=.01,.02\), are evolved through the exact end-of-reflection proper times, respectively
\(1.001764117953\) and \(1.607056471813\).
Their exterior times are \(1.044383215967\) and \(2.288962040031\).
Both precede the first reflected-front arrival at the inner boundary at inertial time \(3.2\).

The target is reconstructed independently in null coordinates using
\(D'=2f'^2/S\), \(v'=D^2\), \(\tau'=D\), not by the numerical PDE.
The field norm compares corresponding normalized positions on the exact and numerical moving intervals, with radius error reported separately. It is normalized by the square root of initial incident energy, not the smaller final reflected energy.

Original acceptance threshold: maximum normalized wave error below 0.5%, source position error below .001, proper-rate error below .005, recorded boundary loss below .1% of incident energy. Those thresholds were not loosened.

| Pulse | Nodes | Maximum normalized wave error | Maximum position error | Boundary-loss fraction |
|---|---:|---:|---:|---:|
| .01 | 129 | 27.5215% | .00449784 | .00108969 |
| .01 | 257 | 13.0988% | .000648566 | .000191384 |
| .01 | 513 | 4.27324% | .0000591617 | .0000155962 |
| .01 | 1025 | .889804% | .00000423797 | \(4.32487\,10^{-7}\) |
| .01 | 2049 | .116057% | \(2.69408\,10^{-7}\) | \(7.03800\,10^{-9}\) |
| .02 | 257 | 17.7034% | .00395481 | .000210247 |
| .02 | 513 | 8.06617% | .000473524 | .0000184416 |
| .02 | 1025 | 2.44521% | .0000395028 | \(5.53649\,10^{-7}\) |
| .02 | 2049 | .377834% | \(2.60823\,10^{-6}\) | \(8.57935\,10^{-9}\) |

At 2049 nodes maximum proper-rate errors are \(7.40\,10^{-6}\) and \(3.03\,10^{-5}\). Corrected energy drifts are below \(1.65\,10^{-17}\) in these two fine runs; that conservation residual must not be confused with their nonzero waveform error.

A failed coarse-grid accuracy check was important: accurate source motion and near-roundoff energy accounting did **not** mean an accurate field. Refinement resolved the field without changing the physics or acceptance threshold.

Evidence:
`source-intake/navier-stokes/20260914/annular-moving-flat-PDE-attempt03/status.json`.

## 6. Curved-space results

The curved control uses \(\kappa=.1,m(a)=.8,S=.003,A_0=.01\) and runs to source proper time \(\tau=1.4\). Unlike the flat tests, no exact solution is available here; the field tests are successive-grid comparisons, not exact error bounds.

The incoming wave reaches the source and causes genuine recoil. In the 4097-node run:

- Source radius changes from 6 to 6.28184594360.
- Proper radial rate ends at .365289898226; this is \(db/d\tau\), not a coordinate speed or a velocity fraction of \(c\).
- Exterior Schwarzschild time reaches 1.69249168260.
- The interior geometric mass decreases by \(2.43199757877\,10^{-5}\).
- The separately integrated work law predicts \(2.43199758556\,10^{-5}\).
- Peak sampled normal scalar pressure is \(1.73953733163\,10^{-4}\).
- Minimum \(F\) is .466666666667. The fixed inner boundary remains effectively quiet during the tested interval.

| Nodes | Maximum exterior-mass drift | Maximum mass-work mismatch | Maximum source reflection mismatch |
|---:|---:|---:|---:|
| 257 | \(1.61223\,10^{-7}\) | \(1.61232\,10^{-7}\) | .00477528 |
| 513 | \(3.30066\,10^{-8}\) | \(3.30085\,10^{-8}\) | .000634653 |
| 1025 | \(2.92978\,10^{-9}\) | \(2.92995\,10^{-9}\) | .000388827 |
| 2049 | \(3.32575\,10^{-10}\) | \(3.32595\,10^{-10}\) | .0000300675 |
| 4097 | \(4.13203\,10^{-11}\) | \(4.13227\,10^{-11}\) | .00000556091 |

The maximum normalized wave differences between successive grids are
12.7933%, 4.43896%, .966650%, and .132297%. Scalar, source position, proper rate, exterior clock, mass-profile and metric-speed differences all decrease under the same refinement criterion.

The final 2049/4097 comparison has position difference \(1.85\,10^{-7}\), proper-rate difference \(3.58\,10^{-6}\), scalar maximum difference \(3.11\,10^{-7}\), mass-profile difference \(5.29\,10^{-9}\), and metric-speed difference \(1.42\,10^{-6}\).

The initial exterior mass is approximately .800328400292. Its small drift is a conservation diagnostic, **not** a claim that all fields have \(10^{-11}\) error. No conserved mass was imposed on the evolving solution.

The 4097-node run was included before starting the GR matrix, in light of the flat-space resolution findings. The same field, boundary and mass acceptance gates were retained.

Evidence: `source-intake/navier-stokes/20260914/annular-moving-GR-PDE-attempt01/status.json`.

## 7. Independent verification and preserved failures

The direct temporal Einstein test uses the moving-coordinate identity

\[
 m_\tau|_x=\kappa F(LXY+xwe).
\]

The left side is obtained by differentiating the implemented constrained metric map along its live PDE time derivative, with a complex-step check and a separate central-difference cross-check. The scalar temporal identity in section2 is tested in the same way, including all grid points and both boundaries.

| Nodes | Maximum temporal Einstein residual | Maximum scalar temporal residual |
|---:|---:|---:|
| 257 | \(2.43788\,10^{-5}\) | .000371884 |
| 513 | \(6.88226\,10^{-6}\) | .000129515 |
| 1025 | \(1.60790\,10^{-6}\) | .0000289320 |
| 2049 | \(2.11380\,10^{-7}\) | \(3.87206\,10^{-6}\) |
| 4097 | \(3.16852\,10^{-8}\) | \(5.74178\,10^{-7}\) |

These are residuals in pilot units, not direct observational bounds.

Additional checks:

- A separate adaptive radial integrator solves the original mass and log-lapse equations at \(\tau=.4,.8,1.4\), using interpolated live field density. Maximum disagreement is \(8.25\,10^{-12}\) in mass and \(2.40\,10^{-12}\) in log lapse.
- Halving the maximum time step and tightening tolerances at1025 nodes changes saved states by at most \(1.96\,10^{-14}\); this establishes temporal error is much smaller than the measured spatial-grid differences for that test.
- The induced metrics on both sides agree with shell proper time to below \(6.7\,10^{-16}\).
- Setting the wave amplitude to zero reproduces the prior dust-shell vacuum ODE within \(1.07\,10^{-14}\). The scalar stays exactly zero, and the radial metric-speed profile agrees with the Schwarzschild expression within \(8.12\,10^{-9}\) at129 nodes.

Evidence: `source-intake/navier-stokes/20260914/annular-moving-GR-independent-attempt01/status.json`.

The independent radial interpolation emitted a reciprocal-overflow warning in PCHIP's harmonic-mean slopes for densities as small as the smallest positive double. This was investigated, not suppressed or mistaken for a physical divergence. An algebraically equivalent scaled harmonic mean avoids reciprocals of subnormal numbers, without clipping any density or changing the PDE. The polynomial-coefficient comparison differs by less than \(2.7\,10^{-19}\) over any interval; sampled values differ by less than \(4.4\,10^{-19}\), with floating-point evaluation roundoff accounted for. Both interpolants remain finite. A separate synthetic subnormal test verifies that legitimate tiny positive slopes are retained.

Evidence: `source-intake/navier-stokes/20260914/annular-moving-radial-interpolation-attempt01/status.json`.

Preserved failed attempts:

- `source-intake/navier-stokes/20260914/annular-moving-flat-PDE-attempt01/status.json`: the independent exact target did not handle an empty reflected-support array at initial time. A separate helper version handles the zero reflected field. The PDE was not changed.
- `source-intake/navier-stokes/20260914/annular-moving-flat-PDE-attempt02/status.json`: 513 nodes failed the original wave-accuracy threshold despite good energy accounting. The successful continuation inherits those cases and extends resolution, rather than overwriting the failure.

Each completed evolution is saved before comparisons, so later diagnostic failure cannot erase its trajectory. Main tests run sequentially in one BelowNormal, one-core worker; no subagents or GPU jobs. No GitHub activity.

## 8. Meaning for the framework

This implements a meaningful missing piece of the **conditional continuum source model**: feedback between a wave, a moving material source and the radial geometry, with declared clocks and energy transfer.

It does not yet establish that the finite-collar MTS theory supplies this same moving boundary action. The old fixed-boundary convergence argument cannot simply be relabelled as a moving-boundary proof.

The next theory target is to vary the finite-collar source embedding and material degrees of freedom, derive their force and clock map, and compare both MTS and the reference regulator against this moving-source GR control. The same accuracy standards must apply to both.

Material coefficients and physical reflectivity remain to be justified by the parent theory. No claim here resolves a horizon, a black-hole singularity, the full GR limit, or observational viability.
