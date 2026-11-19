# Live accumulated pressure work through3046

Private/local, 2026-11-17. Completed the frozen3044..3046 continuation for
baseline/MTS32/64; the3045 cumulative gate passed before3046 launched.
The full MTS goal remains active. This stage improves the retained coupled
model's physical error accounting; it is not an observational fit or new action.

## New method without physical feedback

Both preflights compare dense output enabled/disabled at both resolutions.
Accepted clocks and physical states are bitwise identical over the tested
first source segment. Initial actual RHS and complete saved outputs are exact;
dense output agrees at solver nodes.16 MTS and12 baseline controls pass.
This is a representative non-invasive control, not a second complete plain
integration of every new segment. All new full physical gates also pass.

The derived J_h/J_f/J_e, non-cancelling and split-defect work are evaluated on
MTS DOP853 ACCEPTED-STEP dense output. Gaussian3/5/7 refinement is fixed;
local absolute order differences are accumulated rather than cancelled across
steps. Work diagnostics never enter the physical error controller or feed
back into the fields. All source/background knots are retained as boundaries.

The starting integrals include3041..3044 work and explicit prior uncertainty.
No field, work, K/error/h/f/parent/probe reset; physical matching3040 and split
anchor3041 remain unchanged. Original bank, binary, grids,934 norms and
1e-10/2e-5 gates remain. No fitted parameters, downloads or publication.

## Completed physical window

3045:654 MTS/243 baseline saved diagnostic nodes over~1.009267 conformal Mpc.
3046:360/133 nodes over~0.552662 Mpc. Native capture1056 preserves known1054
and original934 source prefixes exactly. Fine MTS uses10605 accepted dense
steps across the new window. Both cases carry their respective32/64 histories.

Both original-epoch gates pass: raw physical pressure/exchange, actual metric,
signed error controls, coupled source/readout envelopes and physical work
budgets. Maximum inverse safety quantity0.17822385336<1. Largest cumulative
source/readout working envelope1.9800297e-7, below2e-5 by about101-fold.
These are tested numerical estimates, not certified continuum enclosures.

## Accumulated work and independent comparator

Predicted approximation-minus-parent pressure-work error from3041:

| Branch | Predicted final error | Independent saved work error | Working budget relative to parent work |
| --- | ---: | ---: | ---: |
| Original | -2.29105390692e-10 | -2.29105391830e-10 | 9.0675809e-7 |
| Coherent | -2.29106206389e-10 | -2.29106207747e-10 | 9.0676085e-7 |
| Coherent minus original | -8.15697321910e-16 | -8.15903944639e-16 | 1.1167167e-6 |

All three physical-response budgets pass2e-5; worst margin about17.9-fold.
Every new saved-node budget covers both signed prediction and independently
evolved work. Branch-change inherited/newly generated contributions at the
final epoch are+9.76804880562e-18 and-8.25465370716e-16. Keep both: they
partially cancel. The full branch-change working budget is4.257365336e-15,
against a parent pressure-work response amplitude3.812395280e-9.

Raw and defect-accounted J_e=J_h+J_f identities pass. The actual numerical
split residual is independently integrated and added to the budget. Corrected
identity ratios4.58458e-15 /3.76581e-15 /3.18329e-15 are below1e-10.

Baseline owned cold pressure/work and corresponding error-work remain zero
by their structural definition, not all baseline matter/radiation pressure.
Stable MTS photon-baryon slip response amplitude now8.05208266e-12; parent
and approximate own-precision ratios4.54952e-7 /4.02416e-7 pass. The baseline
tiny slip remains unresolved at0.00931317 relative; this stage does not erase it.

## What live accumulation fixed, and what it did not

For the NEW3044..3046 branch-change integral, the summed fine-grid local
order7-versus5 and5-versus3 differences are8.82996e-28 and1.05313e-27.
New local rounding allowance2.93892e-29. These are far below the inherited
offline diagnostic allowance1.42893e-18. The latter was carried conservatively,
including both earlier stride differences and interpolation-degree comparison.

An additional cached difference-of-increments check removes ONLY the constant
3044 integral offset, which cancels exactly in this observable. It does not
erase uncertainty in physical initial states;32/64 evolved trajectories remain
independent. Include their increment difference, local quadrature/rounding on
BOTH histories and64eps subtraction allowance. Results:

| New-window work-error increment | Final increment | Numerical relative budget |
| --- | ---: | ---: |
| Original | -9.63387472268e-11 | 6.3422545e-12 |
| Coherent | -9.63393529258e-11 | 6.3392442e-12 |
| Coherent minus original | -6.05698931839e-16 | 5.0893494e-10 |

All pass2e-5 within this refinement/arithmetic diagnostic. The branch-change
increment amplitude6.32030583e-16 has absolute budget3.21662446e-25. This is
evidence that new within-step accumulation avoids the earlier reconstruction
problem, NOT a certified bound on all trajectory error.

The TOTAL tiny branch-change error from3041 remains unresolved relative to
itself:0.00339403 versus2e-5, dominated by conservative inherited uncertainty.
The full physical work-response budget passes separately. Old native,
slow-sector, source/spectrum and tiny-baseline limitations remain visible.

## Source cadence matters for the next test

Read-only original clock inspection shows a change in SAVED OUTPUT SPACING,
not evidence of a new physical regime. At3046 the MTS clock is97.0138438024
Mpc;3047 is97.0149705571 Mpc. Two more numbered epochs would advance only
~0.00225 Mpc, not another~1-Mpc test. Both source arrays have4253 entries.
The first saved index at least1 Mpc beyond3046 is3940 for both cases:
MTS98.0140754920,baseline98.0140125413 Mpc. This candidate spans894 saved
intervals. Preserve this grid, but use grouped batches instead of894 new
folders/checkpoints. Regime/signature continuity must still be checked before
new physical work; clock availability alone does not establish it.

## Verification and cleanup

233 technical checks pass: exact score replay, physical/work restart joins,
finite arrays, monotone uncertainty, source hashes, gate-before-launch order,
saved boundaries and fresh-owner final actual RHS/native sources.12 native
owners are released. No task numerical worker remains after closeout.

One preparation-only failure is retained: a source-path helper was imported
from the wrong module. It was fixed BEFORE source freeze or physical work;
the empty preparation directory was reused without deletion. No physical run
was retried. All later physical/scoring/verification jobs complete successfully.

At closeout require15 exact worker identities exited (14 completed and the
accounted failed preparer). Verify all artifact hashes and the foreground
closer's exit independently. No other chat, server, browser, scheduler or
protected process changed. All outputs stay private/local.

Restart from epoch3046 complete physical AND work-terminal files, keeping
both32/64 histories. NEXT.md selects a physically meaningful next window.
