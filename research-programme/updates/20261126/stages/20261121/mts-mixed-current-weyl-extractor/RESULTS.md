> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A mixed stress–current measurement that isolates the photon–curvature coupling

Private parent stage, 21 November 2026. **Three shear readings suffice in the continuum at leading local order.** Starting from their kinetic operators, a charged scalar and a charged Dirac field independently give the expected two different coefficients. A discretized charged scalar on a four-torus checks the actual source derivatives and shows why one lattice size is not enough. This takes the 4946 matching contract (not bundled here) from a specified projector normalization to executable momentum and polarization choices. The response is a third derivative of the generating functional, not the ordinary two-current polarization. No new MTS parameter, galaxy fit or QCD number is used.

## What to measure

Use W_E=−log Z, incoming momenta (q,p,k)=ε[(2,0,0,0),(−1,n,0,0),(−1,−n,0,0)], flat Euclidean metric, positive scalar curvature on spheres. Both covariant photon polarizations point in direction 2; differentiate with respect to the covariant metric shear h₂₂=1,h₃₃=−1. Write G_n for the coefficient differentiated once in each of these three amplitudes, with the overall volume delta removed; coincident p=k still needs both derivatives. Polarization and metric amplitudes here are unit sources, not normalized helicity states. In a continuous translationally invariant calculation one may obtain the real coefficient by four times the corresponding three-real-cosine derivative when only the opposite-sign triplet also conserves momentum.

| Local action density | Contribution to G_n at ε=1, t=n² |
|---|---:|
| F²/4 | 1−t |
| RF² | 0 |
| Ric_ab F_ac F_bc | −4(1−t) |
| C_abcd F_ab F_cd | −8(1+t) |
| (∇_a F^ab)² | 6+4t−2t² |

The Maxwell response scales as ε²; the four curvature/derivative responses scale as ε⁴. The Maxwell variation comes from the inverse metric in F²; the full covariant divergence includes a metric derivative, not just −p²A. At this shear R=0, Ric= q²h/2, R_0202=q²h₂₂/2. The full-index identity CFF=RiemFF−2RicFF+RF²/3 fixes the Weyl normalization.

Thus the two independent choices **of readout design** (sharing some measurements) are

    c_E = lim ε⁻⁴ (−3G₀+G₁−G₂)/48
        = lim ε⁻⁴ (−35G₁+8G₂−3G₃)/480 .

These projectors reject arbitrary coefficients multiplying the other listed operators. The second uses only noncollinear nonzero photon momenta. They need not agree at finite ε. At fixed q the matrix has rank three; the scalar curvature column vanishes and the Ricci column is −4 times the Maxwell column in dimensionless units. Do not infer five separate coefficients from that design. Adding conformal metric probes and a second metric momentum gives rank five within the retained local, parity-even basis. The reverse test is important: an arbitrary finite counterterm multiplying CFF itself passes the projector with unit gain. Only a specified microscopic action/renormalization prescription or one physical calibration can fix that component. This is not a projector removing all contact terms.

Exact operator rows and weights (not bundled here) · frozen design (not bundled here). In [vertices.py](evidence-001.zip) (archive member: `vertices.py`) arbitrary vector/metric checks enforce Bose exchange, both photon Ward contractions and the **inhomogeneous** metric Ward identity. For h_ab=q_a ξ_b+q_b ξ_a the Maxwell and divergence-squared contractions cancel the variations of the two photon sources (the two flat two-point pinches); setting those metric contractions themselves to zero would be wrong. These are tests of the local vertices, not of a measured QCD stress tensor. For a general finite-momentum QCD amplitude there are nonlocal form factors; the table is not a complete nonlocal decomposition.

## Independent continuum calibrations

The reference was frozen from [Bastianelli, Dávila & Schubert](https://arxiv.org/abs/0812.4849). Their Γ=log Z uses the opposite overall sign to W_E here. Units below are e²/[(4π)²m²] per species. Our scalar and spinor calculations use different vertices of different microscopic operators; the known effective coefficients are used for comparison, not to generate their signals.

| Source | Euclidean Weyl coefficient recovered exactly at ε→0 | Finite-momentum check |
|---|---:|---|
| One charged complex scalar | +1/180 on both banks | At ε/m=1/32, two-scale extrapolation differs by 1.7 and 4.1 parts per million or less |
| One charged Dirac fermion | −1/90 on both banks | Same check differs by 2.4 and 55 parts per million or less |
| Scalar with only the triangle, after subtracting its own low orders | +7/180 on both | Wrong even though the two banks agree |

The full leading responses also match the Ricci and divergence terms on six kinematics, including unequal photon virtualities. The first scalar bank has next coefficient −1/360 multiplying (ε/m)²; the second has +13/5040. For Dirac those terms are +1/90 and +19/252. One common mass-dependent slope for all fields or banks would not be justified. [Loop derivation](LOOPS.md) · scalar results (not bundled here) · Dirac results (not bundled here) · scalar contact-removal control (not bundled here).

## Discretization is measurable, not an accuracy assumption

The scalar lattice uses the gauge link exp(ieaA_y) and the determinant-one shear metric. Differentiate the scalar action on the links, including metric–photon and two-photon vertices. A direct coordinate-space log determinant for three real waves at 8⁴ sites, independent of the Fourier diagram sum, agrees to ≤1.31 × 10⁻⁹ in the unnormalized vertex. The coarser n=0 stencil misses the original 2 × 10⁻⁸ absolute gate and is retained. Direct check (not bundled here).

At fixed mL=24, ε/m=2π/24, compare to the **infinite-volume continuum at the same momentum**, not its zero-momentum value. The original nearest-neighbor lattice differs by about −54%/−48% at 16⁴, −9.22%/−8.55% at 96⁴, and −6.17%/−5.74% at 128⁴ on the two designs. The calculation is an exact sum on each discrete torus, not Monte Carlo noise. In a separate constant am=0.5 volume check with the physical momentum fixed at ε/m=2π/12, the difference between mL=24 and 48 is below 2 × 10⁻⁷ of the matched continuum reading. mL=12 is visibly different; that comparison is a volume control at its own momentum, not a rigorous bound at all momenta.

An a²-only extrapolation from 64⁴/80⁴ missed all four held-back measurements at 112⁴ and 128⁴ by 1.03–1.61%. A three-term constant + a² + a² log(a²m²) forecast from 48⁴/64⁴/80⁴ passed all four frozen 0.5% **finite-spacing** gates (0.12–0.20% errors); its intercept still misses the infinite-volume value by 0.81–0.86%. These fits diagnose the numerical regulator only. Good prediction of the next lattice spacing is not a precision continuum determination. Frozen forecasts (not bundled here) · [observed errors](evidence-001.zip) (archive member: `spacing-test.csv`).

## Signed transport to the previous sky result

With the same curvature convention and physical metric (−+++), a static purely spatial magnetic contraction has the same CFF value before and after Wick rotation, whereas W_E=−∫L_Lorentz,static dτ. Therefore the mostly-plus Lagrangian −F²/4+c_W CFF has **c_W=−c_E** in this convention. The electron sign also follows directly in the explicit mostly-plus action in [Goon & Hinterbichler](https://arxiv.org/abs/1609.00723). This is separate from the numerical sign in the retained GRSMEFT threshold register, which chose the negative Dirac convention.

We checked the actual Schwarzschild curvature routine used by the preceding results: C_0i0j=diag(−2,1,1)q_tid, and the null-screen eigenvalues are (−3,+3)q_tid (radial in-plane, perpendicular). Hence for positive mostly-plus c_W the perpendicular polarization is slower and K for t_perpendicular−t_in-plane is positive. In these named labels the free lepton contribution is positive, not the previously transported negative register sign. Enveloping the same small W/parent terms gives approximately **+5.46 × 10⁻⁵² s** for the known non-QCD part centrally; reversing the readout labels reverses the sign. This corrects signed transport, not the earlier absolute sensitivity, magnitude or orbit. The total still contains an unknown finite QCD term. Old files are preserved. [Static convention check](evidence-001.zip) (archive member: `static-wick-check.csv`) · signed receipt (not bundled here) · [earlier timing result](../mts-binary-polarization-rays/RESULTS.md).

## A test of the interacting matter sector that need not guess the contact

The [light-mass derivation](CHIRAL-TEST.md) gives an identifiable conditional prediction: in the ordinary two-light-flavour chiral regime the leading inverse-pion-mass-squared part of the QCD coefficient comes from the one charged Goldstone pair. A four-mass difference cancels an arbitrary mass-independent intercept and all polynomials up to quadratic order in the chiral mass logarithm. It does **not** determine the physical-mass intercept. We checked the algebra exactly and the free-loop response numerically; this is not a hadron simulated as a point scalar at physical mass.

**Next:** implement the source derivatives of the quark link and the gluon/sea stress, including contacts and disconnected cumulants. Test these on the *same* noncommuting gauge fields against direct background variations and a conserved-current Ward test, then use genuine independently sourced dynamical ensembles or comparable off-forward data. A forward photon matrix element at q=0 kills the curvature vertex. Don't run another pure-scalar grid series in place of that interacting check.
