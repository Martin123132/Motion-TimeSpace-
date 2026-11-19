# Checked current connected to the common-metric source

16 November 2026. Completed bounded manual stage; all work remains local.
Authoritative acceptance: validation-v2.json and accepted-panels.json.
Cached acceptance replay: validation-v2-replay.json.

## What advances

The previously checked gauge current and an integrated metric response now
come from the same explicitly declared finite-background action. The new
calculation varies the volume, coframe, Wilson operator and moving chiral
projector together, instead of holding the projector fixed.

This is an interface to the existing common-metric and exchange owners,
not a replacement action. Checkpoint4916 already owns the densitized metric
source map;4904 already owns the on-shell opposite matter/gauge Lorentz forces.
Their source paths and hashes are in protocol.json. DERIVATION.md fixes the
off-shell normalization and spells out what is inherited versus tested here.

The useful new distinction is that a moving projector is not an invertible
scalar coordinate transformation. The chain term E_psi delta(P) eta must be
retained. Projected Euler stationarity alone does not make it vanish:
the explicit saved witness has E_psi P at approximately1e-16 while its omitted
metric contraction is0.00831–0.01317. This is a linear-algebra counterexample
to that inference, not a physical solution of the full coupled equations.

## Paired tests

Matter and the same matter plus the retained positive-quadratic neutral bath
are checked on the three existing synthetic fixtures. No new physical
coefficients are inferred from these dimensionless test parameters. Independent
metric/link finite differences use the first fixture, three directions
(trace, stretch, shear) and both original step sizes.

| Check | Worst accepted residual |
|---|---:|
| Previously checked link current recovered |6.9743e-17|
| Old flat Wilson/overlap operators recovered |2.3369e-15|
| Metric action derivative |3.9072e-12|
| Direct densitized-metric path derivative |1.5077e-11|
| Mixed current/metric derivative reciprocity |6.5128e-11|
| Explicit neutral-bath stress addition |2.8382e-16|
| Gauge-invariant curvature/current force readout |2.0119e-14|
| Independent paired action work derivative |6.4885e-12|
| Neutral internal exchange product identity |4.4409e-16|

The inherited normalized identity gate is1e-10; the last exchange row is an
absolute fixture-level residual. There are106 passing panel checks and30
passing acceptance/reproduction checks. Counts include controls, not106
independent physical predictions. All non-work metrics reproduce exactly
from the initial run, and all initial source arrays are unchanged.

The neutral bath adds no gauge-link current in this family, but DOES add
metric stress. Its interaction stress is required for its internal exchange:
omitting it leaves1.52–2.35 in fixture units, above the1e-6 negative-control
floor. Omitting the metric/projector chain leaves normalized response
discrepancies0.00161–0.00941 and also fails. These controls test terms that
would be lost by equating gauge neutrality with gravitational silence.

## Numerical repair, openly retained

The original small-step work residual is1.4387811076512933e-10 and fails.
Evaluating the same action difference through paired bilinear products,
before adding cancelling constant terms, reduces it to4.9357191759518e-12.
The larger-step result is6.488427162970265e-12. Step sizes, binary64 operators,
fixtures, stencil and tolerance are unchanged. This is an independently
evaluated action difference, not an integral of the current being checked.

PAIRED-WORK-REPAIR.md records the further exact-reference receipt alignment
and boolean-serialization repair. Root result.json and
paired-work-repair/result.json intentionally retain their failed statuses.
Use validation-v2.json for overall acceptance. No failures are overwritten.

## Meaning and scope

The declared regulator extension uses a CONSTANT positive Euclidean metric;
it is a diagnostic choice that reduces to the original operator at flat
metric, not a uniquely parent-derived curved-lattice construction. The stress
is an integrated variational response, not a pointwise Lorentzian energy
measurement. Mixed-source reciprocity and the force/work probe test that
interface; they do not test local lattice diffeomorphism invariance.

The parent continuum exchange relation is retained with its Euler contacts:

    nabla_mu T_m^mu_nu = F^a_numu j_a^mu + E_cov,nu.

Only with the relevant matter and gauge equations can the combined divergence
be set to zero. Arbitrary fixture fields are off shell. No cancellation is
claimed merely by defining a second force as minus the first.

The quantum measure/Jacobian remains separate. The internal gauge current
is not the cosmological momentum Q_s. No finite-cutoff fixture current is
inserted into the saved cosmology. The33 physical reports through epoch2924,
their source bank, grids, parameters and tolerances are untouched.

## Reproduction and preservation

The original full panels/source arrays and paired work packets were replayed
exactly. The corrected reference readout and all accepted panels then replayed
exactly without another eigensolve.90 frozen paths were verified:77 inherited
inputs and13 artifacts from the initial attempt. closeout.json records the
new stage artifacts and their hashes; CLEANUP-VERIFIED.json records exact
worker exits. No browser, server, subagent, GitHub or other-chat action.

NEXT.md gives the proposed return to the retained physical history.
