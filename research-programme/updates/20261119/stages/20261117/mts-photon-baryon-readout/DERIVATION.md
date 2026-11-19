# Photon/baryon response from the existing coupled history

This stage does not rerun evolution or introduce a collision source. It extracts the radiation and baryon states ALREADY evolved with the corrected MTS/common-metric source. Baseline and MTS use identical procedures. Their native initial-mode amplitude is inherited: results are transfer readouts, not microkelvin sky predictions.

## Physical route

The new source affects the common metric and hence the retained photon/baryon hierarchy. Native rescaled heavy-field D,Q,T are NOT interchangeable with a Compton/emission collision kernel. The angular hierarchy here is frequency-integrated. It does not contain a frequency-resolved chemical-potential/y distortion and does not close a new microscopic emission calculation.

Let B_i=kappa a^2 rho_i, D_i=kappa a^2 delta-rho_i and Q_i be the same rescaled native heat flux. Then
```
delta_b=D_b/B_b, delta_gamma=D_gamma/B_gamma
v_b=Q_b/B_b, q_gamma=Q_gamma/B_gamma, v_gamma=3q_gamma/4
T_b/B_b=the native fractional baryon pressure perturbation.
```
The photon monopole temperature-like perturbation is delta_gamma/4 at the retained linear bolometric order. This does not distinguish a temperature shift from a frequency-dependent distortion in a non-Planck spectrum.

## Relative-density and relative-velocity equations

Two frame-independent combinations at retained pressureless-baryon-background order are
```
S_bg=delta_b-3delta_gamma/4
V_bg=v_b-3q_gamma/4.
```
The native continuity equations give S_bg'=-k V_bg. Native baryon/photon Euler equations give
```
V_bg'=-H v_b+k cs2 delta_b-k delta_gamma/4+k pi_gamma/2
       -opacity [1+4B_gamma/(3B_b)] V_bg,
pi_gamma=Pi_gamma/B_gamma.
```
The drag coefficient is derived from their shared Thomson momentum exchange, not fitted or inserted as extra MTS damping. Metric terms cancel in S_bg' but influence the separately evolved states. Check both sides directly from saved D',Q',B and the actual rate r=a'/a; do not differentiate sparse reporting times.

The retained baryon thermal-pressure omission in its continuity equation remains the previously documented approximation. S_bg is a relative-density/isocurvature variable at this order, not a measured thermodynamic entropy production.

## Metric and frame map

The saved sigma is dimensionless; native eta_k=k eta_s. Conformal time is Mpc, k/r/H are Mpc^-1. On the native synchronous frame, the time shift to conformal Newtonian variables is alpha_g=sigma/k. Here alpha_g is not the background fractional correction. Kinematic potentials are
```
Phi_N=eta_k/k-r sigma/k
Psi_N=(sigma'+r sigma)/k
W=(Phi_N+Psi_N)/2=(eta_k+sigma')/(2k)
Theta_gamma,N=delta_gamma/4-r sigma/k
delta_b,N=delta_b-3r sigma/k
v_b,N=v_b+sigma.
```
Use the ACTUAL saved scale-factor rate r for a coordinate transformation; it equals H in the coherent history. In the old interpolated control they are not silently identified. sigma' is the actual derivative obtained from the coupled equations in the metric stage, not the independent spatial-pressure expression substituted to remove its old defect.

The standard gauge transformations are independently checked against the retained CAMB symbolic.py frame map. General source: Ma & Bertschinger, synchronous/conformal Newtonian perturbations, https://arxiv.org/abs/astro-ph/9506072 (1995), sections3-5. These conventions are imported established physics, not claimed MTS discoveries.

## Gas thermodynamics

The retained3500<z_scale<5000 RECFAST branch fixes homogeneous T_m=T_CMB/a and x_e=1+fHe. It does not evolve an independent delta T_m in these packets. For a_star=a(1+alpha),
```
Delta T_m/T_m=Delta cs2/cs2=-alpha/(1+alpha)
Delta opacity/opacity=-alpha(2+alpha)/(1+alpha)^2.
```
Check these maps against saved cs2/opacity and the accepted background correction. They are a background thermal response, not a resolved gas-temperature perturbation or a new recombination history.

## Small differences, norms and interpretation

For any quotient N/D, compute its response as
```
Delta(N/D)=[Delta N-(N/D)Delta D]/(D+Delta D).
```
Products use their exact finite-difference decomposition. Independently check selected rows with80-digit arithmetic applied to the saved binary64 inputs. Higher-precision reading does not recover information absent from those inputs.

Before evaluating corrected readouts, freeze each observable's norm=max absolute value over the934 ORIGINAL reference states. Term-magnitude norms and native kinetic-equation norms are separately frozen for1e-10 algebra checks. Keep2e-5 for numerical refinement and report response-relative failures even if absolute output errors are tiny. The64epsilon term-magnitude envelope is a working arithmetic allowance, not a rigorous interval guarantee.

Report old-to-coherent prediction changes against the same2e-5 numerical envelope, but distinguish repair size from solver accuracy: the old MTS pressure/geometry was inconsistent. Requiring the repaired metric to reproduce every incorrect old potential would defeat the repair. Changes outside the old output envelope must be surfaced and propagated before using those old predictions.

Use the actual final saved mode at query[-1,-1] as a physical endpoint. A secondary signed902-node projection reuses the historical preparation weights for traceability; it is NOT an observational line-of-sight kernel or a primordial probability distribution. Keep initial preparation, later increment and their sum distinct.

The window/mode does not supply a complete CMB angular spectrum, present-day lensing/growth prediction, new mass-gap result, galaxy occupation law or a bound on all future times. No new dataset, fit, spectrum file, bank change or tolerance change is authorized by this readout.

