# Metric-dependent reduced action derived and tested

2026-11-10. This stage builds on the retained positive quadratic scalar,
existing Einstein coupling and saved z=10 background. No new field, fit,
mass/coupling, galaxy occupation or replacement theory was introduced.

## What the derivation adds

1. The covariant scalar expansion now retains the pure-metric quadratic
   terms and the independent shift coupling. Their lapse, spatial-trace and
   shift variations reproduce energy, pressure and momentum WITH the required
   background measure factors. These terms already belong to the parent;
   restoring them in the reduction is not adding a new force.
2. The actual canonical scalar action is pulled back onto an affine
   metric-dependent state plane. Its inherited symplectic weight, Hamiltonian,
   time-dependent coordinate connection and source shift are derived together.
   The resulting epsilon/(2Wk) term comes from variation, not a fitted fix.
3. The next response term D1=-D0'/(lambda0+lambda_k) follows from the response
   equation. Its remaining defect is D1'. A local Taylor recurrence derives
   all needed coefficients from the retained background ODE and metric cubic.
4. The free homogeneous response remains explicit. Variation of constants
   and an integration-by-parts bound separate it from the driven correction.
   The affine boundary, earlier conformal-rescaling boundary, |D|^2 term and
   pure-metric term are retained for the future joint metric variation.

DERIVATION.md gives the parent action and source map. BOUNDARY-ADDENDUM.md
includes the earlier rescaling boundary and the off-shell W2 correction.
FREE-RESPONSE-BOUND.md states the conditional norm bounds and their scope.

## Checks on the actual saved history

All399MTSmodes and399cold modes are retained. The interval is still
Delta ln a=.001 from z=10, with the original source bank, initial physical
density/current, and1e-10/2e-5 gates. The repaired8192panel microscopic
forcing integral is reused; no full scattering/native run or panel sweep.
The test lies deep in the nonrelativistic regime,k/mu<=3.67e-4. It does not
numerically validate every relativistic scale covered by the symbolic algebra.

Each conditional preparation is compared to full microscopic propagation
FROM THAT SAME preparation, not to a more convenient initial state.

| Preparation | Density difference | Current difference | Pressure energy-block difference | Failed modes |
|---|---:|---:|---:|---:|
| D0 reduced action vs full field | 2.235e-9 | 9.507e-16 | 7.454e-9 | 0/399 |
| D0+D1 reduced action vs full field | 2.217e-9 | 8.806e-16 | 3.724e-9 | 0/399 |

These use the fixed density/current scales; the pressure column is NOT a
relative pressure error or an observational fit score. Source rounding and
the previous low-k physical-reference accuracy limit still apply. The smaller
pressure difference is not evidence of a resolved asymptotic convergence order.

Both reduced preparations agree with the retained native density/current
within2.226e-9/4.126e-6 respectively. Native pressure agreement on the density
block is tiny, but no relative-pressure or exact-equality claim follows.

Cold's independently evaluated action agrees with the saved physical Euler
solution to6.167e-16; its native comparison remains9.800e-8. Rescaling the
purely conventional cold velocity-potential mass by7 changes physical outputs
by at most5.338e-16. The cold equations have not acquired a quantum mass law.

Two coordinate integrations, carrier-relative and density/current, agree
within9.846e-16. Both numerical tolerances use101RHS evaluations and return
identical stored endpoints: this is a consistency check, NOT a measured
solver-convergence order. Neither run refits any coefficient.

## Derivatives, conservation and accuracy

-13canonical/metric/source identities plus2supplementary derivative/boundary
 identities are checked exactly.
-93coefficient/preparation checks pass, including agreement of the new ODE
 Taylor derivatives with the previous independent H jets and D0' formula.
- At17saved points, max|D1/D0|=1.568e-8 and max|D1'/D0'|=2.319e-8. These
 are sampled indicators, NOT certified whole-interval bounds.
- At9trajectory samples per mode, conservation residual rates divided by H
 and the fixed source scales are at most2.786e-15 density and1.865e-8 current.
 Both conditional preparations pass the declared2e-5 sampled-rate check.
 This is not an accumulated-error or uniform conservation theorem.
-7evolution checks and28validation entries pass. Many are implementation,
 integrity and scope checks, not additional independent physical discoveries.

The first symbolic worker failed because its script extracted a polynomial
coefficient from an unexpanded mass prefactor. The deterministic variable
selection error was fixed; the separate failed/completed receipts remain.
No failed physics result or original checkpoint was overwritten.

## Physical interpretation and next step

This supplies a parent-derived reduced matter action and calibrated metric
source interface for the declared subfamily. The fast-component preparation
is still explicit and conditional; no cosmological formation population is
selected by the successful replay.

The next step is to compose this map with the EXISTING joint scalar-gravity
canonical map and total-stress constraints, then test paired metric feedback.
Earlier early-regime184/182coordinate coupled results are retained. The late
bundle does not silently become a full late hierarchy; inspect its actual
initial-state coverage before using it. Do not restart the gravity derivation
or freeze D during a metric variation. NEXT.md identifies those source owners.

Everything remains local. No GitHub, Galaxy Lab edits, communications loop,
new timer or other-agent process changes. Final artifact and process state
are in closeout.json and the post-seal cleanup receipt.
