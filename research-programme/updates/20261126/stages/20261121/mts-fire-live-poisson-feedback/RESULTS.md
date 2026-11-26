> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The matter moves the wave back: a reciprocal Newtonian-limit test

**Private · 21 November 2026.** Starting at the same saved snapshot, gravity now acts in **both directions** in a finite-duration test: the wave accelerates ordinary matter, the changed ordinary density sources the wave Hamiltonian, and the next matter kick uses the changed wave. Both original preparations were evolved. No force coupling, occupation, clock amplitude or observed velocity target was fitted. This pilot isolates mutual gravity from the other forces in a gas disk.

### One force law, tested from both sides

The common interaction energy fixes the returning force by differentiating with respect to each material position. It is not enough to plug the results of two independently accurate Poisson solvers into an energy budget. The original smooth-wave force and the precise derivative of the retained Hamiltonian differ by **2.04% in mass-weighted RMS** for the paired acceleration; they describe the same coupling at different numerical resolutions. The newly derived discrete force and its returning wave potential satisfy the work identity to rounding. The original continuously integrated operator remains an independent control, not a term silently replaced in earlier work. Work check (not bundled here) · [derivation](DERIVATION.md).

The previous signed clock curvature predicted what would happen to displaced matter. Recomputing the potential from all displaced source masses, rather than from the predicted clock value, gives **−2.3577662×10⁻¹³ Myr⁻² at the shortest probe**, versus **−2.3577640×10⁻¹³** predicted. The wave-grid potential changes agree to 3.61 parts per million in weighted RMS there. The full source has 39.224 billion represented solar masses; an independent exterior monopole check sees no gain or loss. Finite displacements (not bundled here).

### Actual two-way evolution

At 0.24 Myr, the finest run gives this change in the **difference between the preparations** for the outer-minus-inner fractional clock rate, relative to controls with ordinary positions held fixed:

| Source of the feedback | Fractional clock-rate change |
|---|---:|
| Moving ordinary mass | −6.7916821×10⁻¹⁵ |
| Wave response to that movement | −5.8797×10⁻²⁰ |
| **Combined** | **−6.7917409×10⁻¹⁵** |

The direct ordinary term differs by 0.072% from extrapolating its *discrete* launch curvature to this time. Both individual waves respond after their arbitrary overall phases are removed. The smaller wave-only contrast changed from −6.56 to −6.03 to −5.88 in units of 10⁻²⁰ at 4, 8, and 16 steps; its last digits are not established. This is a controlled difference between model clocks, not an observation with that precision. [Matched controls](evidence-001.zip) (archive member: `control-paired.csv`) · [last refinement](evidence-001.zip) (archive member: `control-paired-refined.csv`).

**Energy was actually counted.** At 16 steps ordinary matter gains 5.906 and 5.805 billion solar masses (km/s)² of kinetic energy in the reset and inherited arms. Its change is balanced by wave and interaction energy to **4.25×10⁻⁸ and 7.99×10⁻⁸** of that gain, respectively. Halving the step twice reduced each residual by about four each time. The reference for these fractions is the kinetic energy transferred, not a much larger background energy. The two-sided wave work and mechanical work are independently tabulated. Reset (not bundled here) · inherited (not bundled here) · [frozen pilot assumptions](RECIPROCAL-PILOT.md).

### Where the approximations matter

- The leading phase response is cubic in time; the induced wave-clock term is predominantly quartic over the tests. Simply adding a fourth-order Taylor term to the *whole wave state* is not a reliable shortcut: on pointlike radial shells at 0.24 Myr the correction makes the vector prediction worse (reset error about 193% versus 5.1%, measured against the cubic non-global signal). Giving each shell finite radial thickness reduces that quartic-prediction error to about 5.0%. Direct evolution, not this short state series, supplies the finite clock result. Frozen prediction test (not bundled here) · radial-spread control (not bundled here).
- With saved FIRE velocities in the 5.75–9 kpc guard, **460,287 gas elements and 1,471,955 stars** give a short-time moving-source comparison. At +0.24 Myr velocity changes that aperture's effective curvature by +8.80×10⁻¹⁷ Myr⁻² relative to the stationary, time-evolving-wave control. More than 20,000 trajectories cross one of the two clock radii: the readout derivative changes branch there and cannot be differentiated as a single smooth function. This is a signed partial aperture result; it cannot be added to the full-volume calculation. Measured-velocity check (not bundled here).
- The closed pilot starts ordinary matter at rest, holds the other foreground at launch, and does not supply gas pressure or stellar-return momentum. The velocity test uses actual simulation phase space, not a measured Milky Way velocity law. The separate thermal test uses the published [FIRE-2 launch internal energy](https://arxiv.org/pdf/2202.06969) and an explicit adiabatic hypothesis. It diagnoses the first material-pressure response, not the validity of a cold fluid over a full orbit.

### First data-backed pressure coefficient

All **57,075,281 launch gas elements** were indexed back to the archived mass cells. For the represented gas and a monatomic adiabatic response, the thermal-energy curvature divided by the mass-weighted squared paired acceleration is **7.4974×10⁻⁶ Myr⁻²**. Of this, 20.9% comes from tidal deformation at fixed volume and 79.1% from compression. The corresponding *opposing pressure term in that same work projection* has relative magnitude **3.60×10⁻⁸** at 0.24 Myr. Using γ=7/5 gives 1.70×10⁻⁸ instead; using raw interior FIRE gas rather than the target-weighted gas gives 1.20×10⁻⁷ at γ=5/3. These are coefficients of the short-time expansion, **not** an error bound for the clock or for all hydrodynamics. Measured thermal terms (not bundled here) · [pressure derivation and material assumptions](THERMAL-WORK.md).

During validation the old and new sums outside 500 kpc differed by 2.113 solar masses out of 326.7 billion. Replaying the identical carriers in the two original orders reproduced **each** stored mass array exactly. The difference is floating-point accumulation, not a missing carrier. The unused exterior never entered the pressure result; the largest interior bin difference was 1.49×10⁻⁸ solar masses. Reconciliation (not bundled here).

**Next:** use the measured gas-energy distribution in the mixed pressure response for the clock itself. Derive the contributions at the two probe radii explicitly instead of differentiating across a jump or introducing a fitted smoothing length. Keep stellar mass-return momentum separate from adiabatic gas pressure. [Replay](REPLAY.md) · validation (not bundled here).
