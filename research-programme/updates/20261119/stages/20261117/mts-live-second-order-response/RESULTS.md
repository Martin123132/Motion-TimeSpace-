# The derived second-order response passes a new live coupled window

Completed 2026-11-17. This extends the retained parent dynamics from original
epoch3040 to3041, with no supplied future metric or perturbation/source history.
The original background/thermodynamic tables remain retained model inputs.
All native surrounding species and the coherent background correction evolve.
The direct parent remains authoritative; the second-order calculation is a
tested approximation, not a replacement action or new interaction.

## Implementation and checks that matter

The accepted slow response is implemented in original physical field coordinates
through its exactly derived residual R=E^-1 C K2 S^-1 E(f,g). This is equivalent
to the second-order rotating equation, while allowing stable old/change
arithmetic and unchanged native source coupling. Its K1/K2 memory starts at
zero once with the complete3040 physical state and is carried through the full
window, never reset or rematched at output points. No coefficient was fitted.

The changed field derivative also changes source and metric derivatives.
We explicitly derived and applied those corrections to the diagnostic, retaining
the unmodified native-equation metric in a separate array. In particular,
delta z'=delta D'/(2kH) and delta sigma'=delta z'+3delta Q'/(2k^2).
Using the old diagnostic without these terms would test the wrong equations.
Independent differentiation of the modified species stresses and constraints
passes in both preflight and the saved trajectory checks.

Six new runs cover baseline direct32/64, MTS direct32/64 and MTS second-order32/64.
They span about0.972165 conformal Mpc, with244 baseline and623 MTS diagnostic
samples on existing background-table boundaries. Original report clocks, bank,
binary, parameters,934 seed/norms and1e-10/2e-5 gates are unchanged. Fresh1051-row
native captures preserve the previous1050-row prefix exactly. Initial physical
source, metric and native RHS are exact, including a nonzero-residual preflight.

## Physical results under the frozen tests

All ratios below are relative to original frozen component norms, not observed
fit scores or fractional errors of the instantaneous signal.

| Coherent result | Baseline direct | MTS direct | MTS second order |
|---|---:|---:|---:|
| Largest raw main budget | 4.30163e-8 | 4.39453e-8 | 8.03708e-8 |
| Raw density-exchange budget | 5.58880e-14 | 4.31737e-11 | 4.30490e-8 |
| Raw current-exchange budget | structural zero | 9.45204e-12 | 7.26666e-9 |

Raw ACTUAL metric, exchange and source/refinement gates pass without subtracting
the approximation defect. Separately accounting for the independently derived
defect reduces the second-order density/current exchange budgets to
4.31701e-11/9.31361e-12, near the direct-control level. This explains a small
known approximation drift; it does not redefine it as exact conservation.

Compared directly with the live full parent, the coherent second-order density,
current and pressure budgets are4.10014e-8,1.88777e-9 and3.27033e-9. The largest
readout comparison is native velocity6.17398e-8. Both branches pass. Independent
original-native endpoint controls pass too; their largest full-output budget is
2.66247e-6. Those controls cover the two original report times only.

The actual-minus-native-equation trace correction reaches6.64716e-11 in its
native derivative units. The coefficient inverse bound reaches0.0301231<1.
The actual spatial/constraint derivatives, rather than the unmodified equation
diagnostic, are what pass the main test.

## Small corrections and cost

The full MTS coherent-minus-original velocity response reaches3.00514236e-7 in
magnitude and ends at2.06390944e-8. Its direct/reduced paired-refinement plus
primitive-rounding budgets are5.24723e-6/5.22872e-6 of the response amplitude.
The reduced-versus-direct response budget is7.92183e-6, also below2e-5. This is
not MTS minus LambdaCDM or a new observed signal.

Baseline's tiny response remains unresolved: amplitude7.25192e-14 versus
3.45059e-12 working uncertainty, relative47.58 FAIL. Preserve that separate
failure. The original-native MTS velocity discrepancy4.61700e-9 is about1.54%
of this interval's maximum small response; paired refinement is not total
physical accuracy. Earlier slow-scalar identity failures and87.5966% projected
source uncertainty remain unchanged and are not repaired by this result.

This residual-form implementation is NOT faster. Recorded heavy64 runs took
141.1s second order versus81.3s direct, with82442 versus82454 RHS evaluations.
These single-run timings include local workload effects and are not a general
benchmark. Baseline64 used1166427 evaluations and642.5s; its greater cost has not
been causally isolated. No tolerance or normalization was changed to speed it up.

## Restart and next use

The authoritative full-parent3041 restarts are cold-direct-64-terminal.npz and
heavy-direct-64-terminal.npz. The approximate physical state is saved separately
in heavy-order2-64-terminal.npz; its RHS there is the DIRECT native-control RHS
for that state, not the approximate derivative. The complete approximate state,
coefficient memory and ACTUAL RHS are in heavy-order2-64-order2-terminal.npz.
Use that pair together for approximate continuation, with known1051 capture and
original934 normalization. Do not reset memory when crossing the next epoch.

148 technical checks,72 high-precision stable-pair controls and the nonzero live
mapping/source/metric controls pass. No failed worker receipt or bytecode was
created.2412 frozen input paths remain unchanged; cleanup.json and closeout.json
record all exact worker exits/native releases and artifact hashes. Everything
remains local/private, with no GitHub, browser/server, subagent or other-chat
process changes. The fixed-forcing bound from the previous stage is still not
a general coupled/continuum error enclosure; this stage supplies actual new
live comparison evidence. NEXT.md specifies the next derived-error target.
