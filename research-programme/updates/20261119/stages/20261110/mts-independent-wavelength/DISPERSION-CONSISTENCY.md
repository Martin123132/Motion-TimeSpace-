# Interpret the wavelength response from the retained scalar action

This is a **post-test mechanistic consistency diagnostic**, added after the two numerical results were inspected. It is not a newly frozen observational prediction, a fit, or an independent third wavelength test. No saved solution, parameter or acceptance gate changes.

## Derivation and assumptions

In a locally frozen weak-field background, write the retained massive scalar Fourier perturbation as a complex carrier times an envelope, delta_phi=exp(-i*mu*tau)*u, with mu=a*m and c=hbar=1. Its free Klein-Gordon equation gives

    u'' - 2 i mu u' + k^2 u = 0.

There are two branches. Their envelope frequencies are the slow difference and fast sum of sqrt(mu^2+k^2) and mu. For the slow branch,

    omega_s = sqrt(mu^2+k^2)-mu = k^2/(sqrt(mu^2+k^2)+mu),
    omega_s^2 + 2 mu omega_s = k^2,
    omega_s^2 = k^4/(4 mu^2) [1+O(k^2/mu^2)].

The stable rational expression is the same leading beat mechanism present in the retained canonical block. That block also retains the documented expansion/W2 corrections and the fast coordinates. Deriving the slow branch does **not** prove the actual state occupies only it; the preparation question remains independent.

Equivalently, in the coherent nonrelativistic weak-field limit, the inherited minimally coupled Schrodinger-Poisson equations imply the linear pressure-gradient term k^4/(4a^2m^2) in the density equation. The restoring term follows from the field's gradient energy, not a fitted fluid sound speed. In that conditional limit the density equation has the schematic form

    delta_h'' + H delta_h' + [k^4/(4a^2m^2) - 4 pi G a^2 rho_h] delta_h
        = the other species' gravitational source.

Here H is conformal Hubble rate, rho_h is physical background density, and other species cannot be dropped in a coupled prediction. This is an imported standard scalar-field limit of the retained action, not a derivation of the numerical value of G, a universal equation of state, or a galaxy occupation law. The actual runs use the full retained four-coordinate block and metric coupling, not this schematic equation as a replacement.

## What the two saved modes can test

For the same initial density seed and a short interval where the leading gravitational response is approximately independent of wavelength, the first dispersive density change scales as k^4. The metric constraint contributes an inverse k^2, so its **absolute** potential change relative to the cold control scales approximately as k^2. The **fractional** potential change scales approximately as k^4 only when the baseline's scaled potential k^2*Phi is itself wavelength-independent. Its small measured variation must not be hidden.

`dispersion_consistency.py` evaluates these algebraic frequencies using the retained mass/background coefficients at three positions and reads both completed mode results. It reports the absolute and fractional ratios, baseline transfer variation, and the saved time-step-difference proxy. That proxy is not a certified uncertainty interval and excludes physical approximation/initial-state uncertainties. No coefficient is estimated from the two points; the reference ratios25 and625 follow from k=5 versus1.

If the ratios agree, that is a mechanistic cross-check on this controlled example. It does not make two post-inspection points a general scaling law or establish primordial/galaxy predictions. The next step remains the early-to-late state bridge in NEXT.md, not a scan chosen to improve this pattern.
