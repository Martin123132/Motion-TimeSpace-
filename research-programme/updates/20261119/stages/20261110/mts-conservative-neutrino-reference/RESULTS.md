# Conservative neutrino reference: derived and independently checked

## New result

Background and linear perturbation stresses can be obtained from one
positive step approximation to the retained thermal distribution. Their
shared enthalpy identity and collisionless energy/current conservation
then hold algebraically, without rescaling weights to cancel the observed
metric residual. This supplies a concrete numerical remedy for the
previously derived source mismatch, not a new physical MTS coupling.

The calculation reuses the saved cold/heavy initial, midpoint and final
dimensionless masses. It adds a predeclared broad grid from the massless
case to am=1000: 15 distinct masses, four rules, 60 reference evaluations.
No saved perturbation or background evolution was rerun.

## Same gates; coarse failures retained

| Rule | Largest moment error | Largest derivative error | Continuum gate |
|---|---:|---:|---|
| Native 5 nodes | 9.78819e-5 | 2.26894e-4 | FAIL |
| Gauss 16 nodes | 2.71070e-3 | 2.71072e-3 | FAIL |
| Gauss 32 nodes | 2.02192e-7 | 5.17752e-7 | PASS |
| Gauss 64 nodes | 1.37475e-10 | 1.80338e-10 | PASS |

Gate is unchanged at 2e-5. Moment errors are relative density/pressure/
enthalpy errors. Derivative errors are scaled by density or pressure,
not by a derivative vanishing in the massless limit. The native rule's
moment error at retained backgrounds is at most 6.77128e-6, but some
derivative checks still fail: it is not promoted on that partial success.

At the saved backgrounds the 64-node moment difference is at most
1.30083e-14 relative to adaptive continuum integration. That agreement is
not a certified 14-digit physical accuracy estimate. The independent
continuum integrator's estimates and every failed mass are saved in
reference-result.json. Broad-grid accuracy is limited by the small-mass
region rather than the retained late-time backgrounds.

## Independent implementation checks

- Eight exact primitive/background identities and five exact kinetic
  identities pass.
- All four rules satisfy the shared moment/derivative identities to
  at most 7.66e-16 in the sampled floating-point evaluation.
- The step distributions are positive; their maxima are close to 0.5
  and below the fermionic bound 1.
- 36 independent 60-decimal primitive integrations, including both sides
  of the evaluation switch, differ by at most 3.90184e-13 relatively.
- 60 manufactured multipole cases conserve; altering only the background
  weight makes each negative control fail, as it should.
- Massless and high-mass limiting checks pass for all four rules.

These are implementation/identity checks, not independent observational
discoveries. Coarse continuum failures are retained despite conservation
passing. The actual machine's longdouble is double precision; only the
independent mpmath integrations use 60-decimal arithmetic.

## Preservation and interrupted save

The first reference worker completed its arithmetic but failed while
serializing a NumPy boolean. Its code, original rule packet and failed
receipt are retained. A serialization-only repair recomputed the small
reference table, reusing the exact rule packet and unchanged gates.
See SERIALIZATION-REPAIR.md. There was no failed-model retry.

The first validator also incorrectly expected only two case labels; the
inherited report includes cold, heavy, D0 and D01. All twelve case/epoch
labels had already been carried into the reference. The repaired check
requires that complete set without changing numerical results. Its
authoritative receipt is validation-complete.json; the failed validation
and its code remain available in VALIDATION-COVERAGE-REPAIR.md.

The original action, masses, G, production bank/grids and all inherited
inputs are hash-checked. No fits, publishing, Galaxy edits, relay/timer,
new native library or full evolution occurred. The separately labelled
reference grids are not replacements for the production grid.

## Next advance

Carry one shared-moment reference consistently through the background
and source interface, including the slow field and canonical carrier,
then run one short paired cold/MTS control. After that control, widen the
coupled interval or mode coverage rather than repeatedly refining these
already-small saved residuals. See NEXT.md for the fixed-scope contract.
