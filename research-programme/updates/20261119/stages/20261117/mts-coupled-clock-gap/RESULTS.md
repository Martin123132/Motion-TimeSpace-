# Full coupled evolution across the first coarse output-clock gap

Completed on17 November2026. Baseline and MTS both reach original native
epoch3039 from the complete3038 states, without replaying the coupled origin.
The interval is about0.660145 Mpc in conformal time, roughly3.6 initial
principal heavy-field periods; coherent redshift decreases from4401.45 to4364.66.

## Main result

The full live hierarchy passes pressure, integrated density/current exchange,
common-metric constraints and32/64 refinement at the unchanged2e-5 gate.
Independent original-native-solver controls also pass at the two report
endpoints. They are not available at every intermediate diagnostic.

Original table boundaries supply169 baseline and421 MTS diagnostic samples,
not a replacement native report grid. MTS has7 sampled perturbation-field
turning points and15 pressure-source sign changes. The321 turning points in
the much smaller coherent-minus-original velocity correction are NOT321
field cycles; do not confuse a difference history with the physical field.

Selected full-history relative checks:

| Check | Baseline | MTS |
|---|---:|---:|
| Coherent trace | 4.40576e-8 | 4.45964e-8 |
| Coherent shear | 4.40576e-8 | 4.53257e-8 |
| Coherent density exchange | 3.57049e-14 | 4.88234e-11 |
| Coherent current exchange | structural zero | 7.84457e-12 |
| Original native velocity control | 4.22487e-10 | 1.61651e-6 |

These checks retain the finite-neutrino implementation floor and the original
normalization. No residual was subtracted to obtain a pass.

## Frozen forecasts reveal a real approximation limit

Both constant and linear surrounding-source forecasts were frozen before
the live calculation. No coefficient was fitted or updated afterward.

| Coherent forecast error / original norm | Baseline | MTS |
|---|---:|---:|
| Constant density source | 1.57301e-7, pass | 4.56602e-3, fail |
| Linear density source | 4.81018e-8, pass | 3.28631e-5, fail |
| Linear metric eta_k | 5.35474e-5, fail | 1.38564e-4, fail |
| Linear pressure source | structural zero | 3.25180e-6, pass |

The linear MTS density error remains about139 times smaller than the constant
forecast, but it no longer meets2e-5. MTS metric error first exceeds the raw
threshold at a sampled elapsed0.28727 Mpc, its density at0.53623 Mpc;
baseline metric error crosses at0.41320 Mpc. These are sampled crossings,
not exact continuous roots. Old/coherent branches show the same failure
pattern. The successful preceding short-window forecast is therefore local,
not a replacement for the surrounding matter/radiation evolution.

## Precision distinctions retained

MTS velocity correction spans[-2.56553e-7,+2.97238e-7], ending-2.25296e-7.
Its paired32/64 difference plus primitive rounding estimate is5.21175e-6
of its maximum amplitude and passes the same2e-5 gate. The baseline correction
is still unresolved at its own tiny scale.

The separate MTS original-native control discrepancy is1.11891e-8, about3.76%
of that correction amplitude, despite passing the full-output gate. This is
a solver/control discrepancy, not a rigorous error bound on the paired
correction. The5.21e-6 refinement figure must NOT be called total physical
accuracy or a complete source/spectrum uncertainty. No sky likelihood or
MTS-versus-LambdaCDM observational comparison was performed.

## Field-level derivation for the next physical test

PRESSURE-IDENTITY.md derives the exact scalar pressure decomposition from the
retained Klein–Gordon and metric equations, including old representation
contacts. It also connects the weighted pressure integral directly to the
saved density-exchange work. Eight symbolic checks pass, including tests
showing that boundary, gradient, metric and contact terms cannot generically
be discarded. Numerical evaluation of that new identity is the next step;
there is no assumed pressureless-matter closure.

## Recovery and verification

The first MTS32 run stopped after complete boundary48 because recomputing an
integration boundary returned the terminal time twice. The zero-length
segment reproduced the recorded solver-interface failure in a manufactured
test. Deduplicating integration endpoints gives a bitwise match to the clean
manufactured solve. Original requested samples and internal maximum steps
are unchanged.

The first three MTS32 batches were preserved and restored exactly. The rest
resumed from their full boundary48 state; the failed receipts remain intact.
MTS64 uses the same endpoint repair. Baseline runs were retained unchanged.
See boundary-diagnosis.json, repair-plan.json and resume_gap.py. No original
research code, bank, parameters, tolerances or native binary was edited.

287 technical verification checks pass, including every saved batch join,
complete terminal, native signature, stress readout and frozen-source check.
All scientific tests are deliberately NOT marked passing: the forecast and
baseline-response failures remain explicit.

The reusable final states are cold-live-64-terminal.npz and
heavy-live-64-terminal.npz at3039. Closeout and cleanup receipts record all
task-worker exits and the five native-owner releases, including the failed
attempt. All work remains local; no publication or other-chat action.
