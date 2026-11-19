> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Coupled error transport derived and independently tested

Private/local, 2026-11-17. Retained parent and approximation are unchanged.
This is a new coupled-error calculation on3040..3041, not a new epoch or fit.

## New result

The known second-order heavy-field residual now drives an independently
integrated error through the full retained native perturbation hierarchy,
including the common metric and surrounding matter. It is not a discrepancy
fitted afterward. The independent parent, approximate fields, shared live
homogeneous background, K1/K2 memory and error are evolved together.
DERIVATION.md gives e'=A e-r and its stable original/change form.

Cold baseline30 and heavy35 native preflight checks pass, including exact
zero RHS/readout, additivity, homogeneity, inactive-seed affine cancellation
at three saved times, and nonzero heavy residual/source mapping. Zero affine
offsets were found on these samples. The fixed selector remains zero.
These are checks within the retained regime, not a global operator theorem.

The two unamplified32/64 replays use623 diagnostic samples across the same
0.9721649433555655 conformal Mpc. The known1051 native prefix is exact in the
1052-row owner capture; original934 normalization, bank, binary, parameters,
grids and1e-10/2e-5 gates are unchanged. No future metric or source history
drives the calculation; retained background/thermodynamic tables remain inputs.
Both physical states evolve independently, rather than reconstructing the
parent by subtracting the calculated error from the approximation.

## Original frozen test: precision failure preserved

All main physical, raw exchange/metric, original-native endpoint and full-norm
parent-comparison tests pass. The source predictions agree with the saved
direct and approximate histories. Independent numerical background differences
are reported, not assumed zero:4.799e-18 and3.359e-18 maximum absolute.

However replay-score.json retains primary_gate_pass=false. Subtraction of
nearly equal physical solutions cannot validate every tiny transported error
to the stricter error-relative gate. For the coherent branch:

| Quantity | Predicted error amplitude | Original error-relative budget |
|---|---:|---:|
| Weighted density |1.95004181335e-9|2.23207e-6 PASS|
| Weighted current |1.33986091183e-10|2.02765e-5 FAIL|
| Weighted pressure |1.55982259498e-9|1.23982e-5 PASS|
| Native velocity readout |4.25878623139e-10|2.59150e-3 FAIL|

All amplitudes use the retained native/source conventions, not SI velocities
or observational fit improvements. The gate is2e-5. Large cancelling
primitives dominate the velocity rounding allowance; independent integration
differences contribute too. Other small readouts also fail this subtraction
test. This failure is not deleted, weakened, or turned into a physical failure
of the parent theory. No3042 extension was launched by that failed gate.

## Resolving the numerical diagnosis independently

AMPLIFIED-CONTROL.md and amplified-frozen.json were saved before supplemental
controls. Four independent physical-coordinate probes use both signs at
amplitudes16384 and65536. Their equation is p'=A p+c minus the signed,
amplified residual from the UNAMPLIFIED live approximation. Their normalized
signed difference obeys the same error equation exactly in the linear regime.
No probe is reconstructed from the transported error. These are numerical
controls, not altered physical MTS models or fitted parameters.

Both32/64 controls finish and all100 comparisons pass with the same2e-5 gate:
32 error-relative source/readout comparisons,32 probe-center/parent controls,
16 cross-amplitude comparisons,20 unamplified-solution controls. The maximum
error-relative budget is1.7672644e-6; maximum cross-amplitude budget2.1913118e-6.
At65536 the coherent velocity error prediction budget is2.0509818e-8 and
density3.5532591e-11. Primitive cancellation allowances and both step errors
are included. Probe-center recovery is within3.28000e-10 of original full
norms; unamplified solutions remain within3.29630e-10 of those norms.

The separate error-parity.json compares the transported errors themselves
between unamplified and probe-augmented runs, not just the large physical
states: all16 gates pass, worst error-relative budget3.88395998e-11. Thus
these controls validate the same error prediction retained in the original
unamplified restart, rather than a different signal hidden by full-scale norms.

This supports the derived coupled error transfer numerically. It is not a
certified continuum bound on U(t,s), nor a proof about nonlinear perturbations
or arbitrary durations. The original failed subtraction gate remains false.

## Baseline, authority and restart

Baseline is treated explicitly:30 new operator/zero controls, plus the saved
cold direct32/64 physical histories from the prior stage. There is no new cold
evolution or later-time baseline result in this stage. Old/coherent labels
above are TWO heavy-model branches, not baseline versus MTS.

[Operational or machine-specific passage omitted from public reading copy.]

For matched coupled-error continuation use the complete new
`heavy-replay-64-transport-terminal.npz`, with its associated
`heavy-replay-64-parent-terminal.npz` and
`heavy-replay-64-approximate-terminal.npz` in this directory. The complete
transport file stores actual joint RHS, physical parent, approximate state,
K memory, defect work and error; its physical native checkpoint RHS alone
is the direct-control RHS, not the actual residual-modified RHS. Do not reset
K/error or silently substitute a near-equal older parent state. Amplified
probe terminals are validation controls, not canonical physical continuations.

## Verification and scope

verification.json passes165 technical checks including deterministic score
replay, full terminal/batch states, unchanged units and probe initial states.
The separate16 error-parity checks also pass. All source hashes are rechecked
at closeout. Eleven calculation/validation workers plus the separate parity
worker are accounted for by exact identities; six native owners are released.
Cleanup and the seal give final receipts. No native rebuild, browser, server,
subagent, downloads, GitHub action or unrelated process change occurred.

No new epoch, observations, parameters or quantum-measure claim. Earlier
small-baseline resolution, independent-native discrepancy, slow-sector and
source/spectrum uncertainty limitations are not removed by this error test.
The extension branch in run_transport.py is retained unexecuted scaffold;
it correctly refuses progression under the original failed replay gate.
