# Correlated relative-phase mean: verified local result

Completed2026-11-07. Parent: `../mts-joint-relative-metric-20261107`.
The retained action, parameters, source bank, physical wavenumbers,
original history grids and tolerance gates remain unchanged. This stage
adds coefficient quadratures and derivative diagnostics; no new late
background, perturbation history, observational fit or GitHub operation.

## What is now derived

Gravity, the relative scalar and the remaining matter are averaged as
ONE coupled generator, B=RGS+R_N S. The phase mean uses the physical
clock weight1/[mu-(3/2)sin(2theta)], not independent averages of its
matrix factors. The exact near-identity transformation gives

    chi_N=(Bbar+E)chi,
    E=(I+Q)^-1 [BQ-QBbar-D_sigma Q f].

This retains the background drift and metric-source derivatives. The
parent's initial-state and physical-readout transformations also remain
mandatory. See DERIVATION.md for the equations, assumptions and
finite-interval error contract.

The heavy scalar rows can be evaluated directly from their already
derived equations, avoiding subtraction of large carrier/gauge terms.
This exact algebraic repair improves precision without changing a
coupling, fitting a coefficient or dropping another matter component.
See PRECISION-DERIVATION.md.

The leading self-density force is alpha^2/4-b: scalar wave pressure
opposes Newtonian attraction. At the saved early coefficient state the
three pressure terms are0.0148217846,0.2371485534,3.7943768544, while
b=0.3346518601. GR time/current/shear effects and the remaining matter
are retained in the computed mean, not replaced by this leading formula.

## Where the checks apply

The exact formulas continue the retained cold-background programme.
Numerical native qualifications here use instantaneous phase families
on the original EARLY resolved backgrounds, around N=-8.395427 and
mu=2643.515645. They do not assign a late microscopic phase or reset a
late cosmological perturbation. The parent cold inverse/transfer results
remain separate, sealed evidence.

All three inherited k values are used:
0.32497672865575244,0.6499534573115049,1.2999069146230098 Mpc^-1.
Each model retains its own saved background and preparation. Baseline
has no heavy phase, so this particular phase primitive and remainder
are zero; its ordinary matter/metric evolution is not switched off.

## Numerical results and unchanged gates

Numerical gate2e-5; algebra gate1e-10.

-180 native phase-family core-vector comparisons, followed by108
  full G192 comparisons, cover both models and both metric branches.
-Worst independent scalar-equation discrepancy2.364583e-11.
  Full native core error2.836893e-15; tail error6.594928e-16.
-30 frozen matrix predictions at unused phase angles pass. After the
  stable-row repair, the explicit triangle bound against those native
  evaluations is at most1.394150e-7 in maximum absolute matrix entry.
  These are numerical holdouts, not new observational test data.
-Final64/128/256 phase quadratures agree: worst128-to256 mean relative
  change8.662216e-16; primitive change3.475457e-13.
-Worst background-drift step comparison1.443394e-6; complete remainder
  step comparison4.819657e-9. Both pass the original gate.
-Six symbolic chain-rule/clock/covariance identities pass. The final
  audit independently recomputes the weighted means and full matrix
  chain rule from the saved packets.

The relative matrix error is maximum absolute entry difference divided
by the larger maximum absolute entry. Absolute changes are also saved.
These norms are coordinate diagnostics, not fractional cosmological
observable errors.

| k label | Q Fourier-polynomial norm bound, GR | Q bound, spatial Poisson | Sampled ||E||, GR | Sampled ||E||, spatial Poisson |
|---|---:|---:|---:|---:|
| half |6.359476e-5|6.532631e-5|0.05106582|0.05132508|
| balanced |6.337992e-5|6.349064e-5|0.10199903|0.10211713|
| double |6.334457e-5|6.335965e-5|0.20316929|0.20322973|

The computed periodic map is invertible for all phases of its Fourier
polynomial. A certificate for the exact continuum map also needs its
spectral-tail error. The E column is a sampled coefficient norm, NOT an
accumulated transfer-error bound and not a reason to discard E. A small
coordinate map alone does not imply an accurate long-time evolution.

## Two failed attempts preserved and resolved

1. `drift-half-01` fails: Poisson drift-width discrepancy2.561471e-5.
   The saved diagnostic isolates carrier/gauge cancellation in a heavy
   scalar row. No tolerance is relaxed.
2. `stable-half-01` uses the exact stable row identity. Its phase noise
   drops sharply and GR drift comparison improves to2.300656e-10, but
   Poisson still gives2.060315e-5. It remains an overall failed attempt.
3. `refined-half-01` adds only the four missing half-width directional
   families and reuses the rest. Poisson discrepancy drops by14.2741
   to1.443394e-6. This qualified method is then applied to the two
   remaining wavelengths, which also pass.

The runtime's longdouble has the same epsilon as float64; the repair's
improvement is algebraic, not a claim of extra hardware precision.
No original failed packet or receipt is deleted or promoted as a pass.

## A derived background jet ready for the cold construction

From the retained thermal density R_ext and its derivatives,

    W_ext=(2R_ext-R_ext,N)/3,
    W_ext,N=(2R_ext,N-R_ext,NN)/3.

The parent's existing Fermi-Dirac source supplies these quantities.
Checks against baseline and MTS native backgrounds agree in density
and enthalpy to better than3.14e-11. The inherited derivative differs
by up to1.31e-8 for MTS; direct differences of the smooth native
enthalpy agree with the integral derivative within4.37e-11. This
identifies a cleaner source-owned route for the next cold coefficient
jet. It is not silently substituted into this stage's accepted packets.
See EXTERIOR-JET.md and half/external-jet-01/.

## Authoritative evidence and restart

- `audit/result.json`: accepted results, source closure, independent
  recomputations and all maximum errors.
- `half/refined-01/`: accepted half-family drift/remainder; central
  operator remains in `half/stable-01/center.npz` with explicit reuse.
- `balanced/stable-01/`, `double/stable-01/`: accepted remaining families.
- Each family's `mean-01/`, `full-01/`, `heldout-01/`: original native
  phase bank, full hierarchy and frozen prediction evidence.
- `half/drift-01/`, `half/stable-01/result.json`: preserved failed
  derivative-width attempts, not accepted final results.
- `DEVELOPMENT-FILES.md`: tested entrypoints versus superseded drafts.
- `CLEANUP.json`, `closeout.json`: exact worker exits and final hashes.

Only one numerical worker/thread ran at a time, at below-normal priority
on CPU4. No subagents or unrelated processes were used or stopped.

## Next constructive step

Carry the stable coupled equations and the derived exterior thermal jet
onto the SAME accepted cold interval. Keep the residual E, or bound its
effect using the physical energy/constraint structure and retained
prepared mode; do not extrapolate the large early mixed-coordinate
logarithmic norm into a useful transfer certificate. Include background
replacement and endpoint maps, then transport the existing early
preparation for matched GR/spatial-Poisson histories. No dust closure or
new late initial condition is needed to formulate this next calculation.
