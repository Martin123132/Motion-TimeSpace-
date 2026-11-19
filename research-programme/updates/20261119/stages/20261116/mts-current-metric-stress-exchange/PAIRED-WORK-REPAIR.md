# Paired work evaluation without changing the test

The original calculation is retained at the stage root. Its first fixture
passes all metric-source and mixed-response checks, but the force/work
finite difference at step 0.0025 misses the frozen 1e-10 gate: its normalized
discrepancy is 1.4387811076512933e-10 for both action totals. The step-0.005
discrepancy is 3.896874305007951e-11. Smaller steps worsening the discrepancy
motivates a cancellation diagnostic; it does not itself prove roundoff.

The follow-up uses exactly the same fixtures, gauge shifts, overlap operators,
step sizes, stencil weights, binary64 arithmetic and acceptance threshold.
It reproduces the original complete calculation before changing any reported
force/work evaluation. Original reports and source arrays are checked for
exact agreement. No failed result is overwritten.

## Algebraic change

For the link-only work probe, the metric, raw field probes, neutral action,
Higgs potential and barred Yukawa partners do not change. Their finite
differences vanish identically. The independent action difference can therefore
be evaluated before adding these constant terms.

More strongly, evaluate the changing bilinears as paired products:

    Delta(D psi) = D_mid Delta(psi) + Delta(D) psi_mid
    Delta(f^T B h) = Delta(f)^T B h_mid + f_mid^T B Delta(h)
    Delta(|grad H|^2) = 2 Re[(grad H)_mid^dagger Delta(grad H)].

Use Delta(psi)=(P_plus-P_minus) eta directly, not subtraction of two
already-rounded projected vectors. The Higgs gradient difference is computed
from the two link matrices before subtracting the common site field.
Complex summands are accumulated with separate compensated real and imaginary
sums. This is an action-side calculation, not integration of the analytic
current being tested.

Both matter and matter-plus-bath have the same difference here because the
neutral bath is fixed under this particular gauge probe; its nonzero metric
response is retained in all stress tests. Packet-level checks verify the
unchanged terms and agreement with the original action differences.

## Acceptance

Authoritative follow-up outputs live in paired-work-repair, not at the root.
Only the four force/work error entries may change in the 106 panel checks.
All other metrics and saved source arrays must reproduce exactly. The
follow-up retains the raw failed errors, adds 18 invariance/algebra/reproduction
checks, and must pass an exact cached replay. If the repaired independent
action derivative still misses the original tolerance, report that failure
rather than loosen it. Consult its result.json and replay-result.json for
the actual outcome. The authoritative stage acceptance is validation-v2.json,
which resolves the separate reference-reporting issue described next.

## Reference alignment and serialization receipts

The paired action derivative passes the unchanged gate at both steps.
The first repair aggregate still reports false because its exact-bit raw-error
receipt used the force stored from the PREVIOUS checked current, while the
original finite difference used this stage's independently reconstructed
current. The currents agree at approximately 6e-17 normalized error; their
contracted work references differ by 2.7951869596744664e-17. Exact equality
of errors against two slightly different references was therefore the wrong
receipt comparison, despite both scientific comparisons being within tolerance.

validate_bridge_v2.py reconstructs the ORIGINAL reference from the saved
curvature and this stage's saved reconstructed current. It reconstructs both
raw and paired derivatives from the saved work packets, with no new eigensolve.
The original failed errors then reproduce EXACTLY, not just within tolerance.
The repaired errors against that same reference are 6.488427162970265e-12
and 4.9357191759518e-12. All non-work metrics and all source arrays are unchanged.
The failed repair aggregate and its identical replay are preserved.

The first acceptance serializer encountered a NumPy boolean after writing
accepted-panels.json. validate_bridge.py, validation-start.json and
validation-failure.json preserve that attempt. The v2 serializer converts
check flags to native booleans and requires the already-written accepted
panels to match exactly. No mathematical threshold, field, operator, packet,
or test step changes. Its accepted report and cached replay match exactly.
