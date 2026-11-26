# Source coupling from the phase-space stress, on the retained clock

The imported linear kinetic theory is not a new MTS force. [Ma & Bertschinger (1995)](https://arxiv.org/abs/astro-ph/9506072) give the standard synchronous-gauge species and momentum hierarchy, and [Blas, Lesgourgues & Tram (2011)](https://arxiv.org/abs/1104.2933) discuss the high-kτ fluid approximation for an ultrarelativistic species. The precise variable convention in this test comes from the retained Fortran functions Nu_Integrate_L012 and derivs, not by numerically identifying superficially similar moments in those papers. What is being tested here is how that standard species sources the geometry of the two retained preparations, with no extra coupling.

Let q be comoving momentum in present neutrino-temperature units, v=q/sqrt(q²+a²m²), w the native dimensionless phase-space quadrature weights, and K the archived relativistic density coefficient divided by a². The native scalar multipoles have streaming coefficients ℓ/(2ℓ+1) and −(ℓ+1)/(2ℓ+1), including the velocity of the actual momentum node. Then

    D=K Σw F₀/v,    J=K Σw F₁,    P=(K/3) Σw vF₀,    S=(2K/3) Σw vF₂.
    A=(D+3P)/2,    J′=−2HJ+k(P−S).

Differentiation, not a fit, gives the instantaneous shear source

    S′ = −2HS − (2HK/3) Σw v(1−v²)F₂
         + (2Kk/15) Σw v²(2F₁−3F₃)
         + (16K/45) (kσ) Σw v.

The four terms are the change in density units, particle redshifting, angular transport, and metric driving. The factor 2/3 on native anisotropic stress is required by the dipole equation, not chosen to match the old inferred shear. In flat synchronous coordinates kσ=X+3δq_total/(2k), where X=kz. The forecast computes δq_total from its own ordinary and heavy currents plus the early slow-field current and its tangent; the gravitating heavy source is counted once. The massive active density then enters X′ with the same negative sign as all the other species. Remove the octupole term to get an independently specified wrong-source control; the published ledger retains that error.

At launch, read each native momentum slot. For the slots the native solver was still treating perturbatively, initialize Fℓ=Rℓ+(m/q)²Cℓ/2 from its saved massless and mass-correction hierarchy. This is the solver's finite-mass expansion, not independent particle data. After launch evolve those nodes with their actual v, not the mass-expansion equations. For the massless species use the native high-kτ quadrupole rule where active. In the full branch retain angular orders through 12, test 16 separately and use the inherited free-streaming endpoint condition. This is a convergence control, not a proof for arbitrary multipole tails. The test with the old massless shear prescription isolates the difference between upgrading just the massive hierarchy and upgrading both. Exact native source code, build inputs and initial snapshot are fingerprinted.

The shared cold and MTS comparisons start at 89.275 conformal Mpc. Regard reconstructed native shear from momentum balance as a reference estimate, not a direct separate observation. The short-window photon density and longitudinal current are ordinary *linear*, single-mode fluid readouts; the quadratic, visibility-weighted photon observable in the parent is different and cannot be computed by substituting the maximum percentage quoted here.
