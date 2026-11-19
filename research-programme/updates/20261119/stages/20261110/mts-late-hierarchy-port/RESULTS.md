# Late all-species port and independent evolution — 10 November 2026

## Completed

The retained late z=10 background now has a working independently evolved
all-species interface, at k=5 and Delta ln a=.001. It carries the actual
captured initial state, rather than supplied future species histories.
The original61output times, original16mode batch context, matching table,
equations, tolerances and bank are retained. The new scalar response from
the preceding derivation is NOT inserted yet; this is its checked parent
reference and rest-species interface.

Actual late dimensions are93MTS and91cold, not the early184/182. The MTS
averaged selector is1 and is restored as discrete state in both RHS and
observer. Active neutrino preparation constants have an explicit-state
implementation; neither captured z=10case activates that approximation,
so its active-memory branch remains unvalidated numerically in this stage.

Accepted implementation: build-v3/ plus runs/heavy-v4 and runs/cold-v4.
The solver reads only present state, time, retained background and fixed
regime during independent evolution. No future source packet is used by
its RHS. Scaling uses initial state and the frozen initial operator.

## Results at unchanged gates

| Check | MTS | Cold control |
|---|---:|---:|
| Adapter/current original DLL difference, same batch |0exact|0exact|
| Historical archive, declared short interval |2.0444e-7|3.7246e-10|
| Independent base integration/state |8.2592e-8|8.3204e-8|
| Independent tighter integration/state |8.2583e-8|8.3196e-8|
| Base/tighter state difference |2.0271e-10|3.9596e-10|
| Tighter observer difference |2.2645e-8|2.2064e-8|

State differences use initial-operator normalization; observer differences
use per-column reference normalization. These are reproducibility and
integration checks, not data-fit improvements or physical error bars.
Existing numerical gate2e-5 and algebra gate1e-10 were not loosened.

Both zero evolutions are exactly zero and sign-reversed state evolutions
match exactly. Captured RHS/observer replay, matrix/zero/sign/superposition
checks pass. Gravity checks on captured and independently evolved states
include Friedmann, Hamiltonian constraint, anisotropic slip, metric
momentum equation, compensated closure and lapse acceleration. The maximum
of those endpoint/RHS identities is5.463e-16. They are not a new uniform
conservation proof or evidence that the new reduced scalar block passed.

## Failures kept visible

1. First capture read inactive, uninitialized neutrino memory and exited
   natively. v2stops reading inactive storage; active-state mapping and
   native physics are unchanged. See ADAPTER-REPAIR.md.
2. Full historical-span comparison fails for both branches:0.0036233MTS,
   0.0048920cold in some small source columns, primarily outside this
   window. The ORIGINAL DLL also exhibits this discrepancy; the adapter
   matches it bitwise. Replaying earlier batches and the original clock
   did not remove it. No whole-history archival pass is claimed, and this
   discrepancy remains an explicit separate investigation.
3. The first metric-check report hit a NumPy-boolean JSON serialization
   error. Its partial metric-result.json and failure receipt remain;
   metric-result-fixed.json is the accepted report. The helper now
   serializes before creating a new file, preventing future partial JSON
   artifacts from serialization failures. No numerical equation changed.

The short-window decision was recorded before integration in
REPLAY-SCOPE-DECISION.md. It separately requires current-native agreement,
the original short-window historical comparison and independent evolution;
it does not turn a failed whole-history gate into a pass.

## Next physical step

Compose the newly derived unrestricted canonical scalar response and
stress ports with this present-state hierarchy, keeping the existing
synchronous/Newtonian gauge map and all rest-species stress. Compare the
new D0/D01 reduction to the unrestricted parent reference, with the same
initial density/current, explicit fast component and the already derived
constraint-defect budget. Do not merely alter a fitted fluid coefficient.

No GitHub, Galaxy edits, relay, timer, fit, new coupling or halo population
selection occurred. Earlier files and outputs are unchanged. See
validation.json, closeout.json and the post-seal cleanup receipt.
