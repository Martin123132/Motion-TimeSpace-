# One-Mpc coupled continuation: verified through original epoch3940

## Result and scope

The prospectively selected3046..3940 window completes for baseline and MTS at BOTH32/64 resolutions. All seven batch gates pass with the original bank, source knots, physical solver, normalizations and tolerances unchanged.689 technical checks pass. The follow-up physical readout and existing cancellation-safe slip calculation replay exactly.

This is a verified continuation of the retained coupled cosmological calculation, not a fitted observational result or a certified continuum error theorem. No new coupling, initial-state prescription, quantum measure, or parameter was inserted.

Start of turn11:51UTC on2026-11-17. Numerical evolution finished12:52UTC; subsequent checks and closeout occur within the four-hour limit. One numerical worker/thread at a time, below-normal priority. No GitHub or other-chat process changes.

## Window and preserved state

| Quantity | Baseline | MTS |
|---|---:|---:|
| Starting conformal time, Mpc |97.01378045482294|97.01384380237617|
| Ending conformal time, Mpc |98.01401254130049|98.01407549198478|
| Elapsed conformal time, Mpc |1.0002320864775527|1.0002316896086114|
| Original intervals retained |894|894|
| Distinct new-window samples including background knots |1130|1543|
| Accepted steps,32 resolution |67750|4009|
| Accepted steps,64 resolution |69605|7371|

Reference scale factors0.00024800796351187886..0.0002509683749992881 label reference redshifts4031.1285890971117..3983.5657844452976. These are labels on the retained reference clock, not a newly derived observational redshift mapping for corrected histories. Retained wave number k=5Mpc^-1.

Seven batch ends3174,3302,3430,3558,3686,3814,3940 preserve all original clocks and background knots. Grouping changed artifact/launch organization, not time-grid content. Each next batch started only after all four previous runs and the cumulative physical/work gate passed.

Both native compatibility inspections capture1950 rows, reproduce known1056 exactly, retain the original934 normalization/packet prefix, and restore complete parent states at both resolutions. No native hierarchy/signature switch appears in this captured window. First-segment dense-output preflights reproduce accepted clocks/states bitwise for both cases/resolutions. This does not assert a duplicate plain run of the entire window.

Complete native, coupled-field, K1/K2, inherited/generated/total error, four signed probes, pressure work and diagnostic work states carry forward without reset. Matching remains3040; error split and work accounting remain anchored at3041.

## Derived pressure-work transport survives

Previously derived equations, unchanged:

- e=h+f; J_h'=-3H B_P h, J_f'=-3H B_P f, J_e'=-3H B_P e.
- Delta Wp(t)-Delta Wp(3041)=J_h+J_f, compared to independently evolved parent/approximate work.
- Old/change products retain the deltaH cross term.
- Positive non-cancelling accumulated bounds and independently integrated split-defect work accompany the signed result.
- Accepted-step Gauss3/5/7 diagnostics retain inherited allowance and sum absolute local quadrature differences; they do not enter physical error control.

| Cumulative approximation work error | Original | Coherent | Coherent-minus-original |
|---|---:|---:|---:|
| Predicted final |-2.612808431686617e-10|-2.6128228329814035e-10|-1.4401294824140517e-15|
| Independently observed final |-2.6128084721840916e-10|-2.612822875809953e-10|-1.4403650474229053e-15|
| Working budget / physical parent-work amplitude |1.1185773576517231e-6|1.118580046702769e-6|1.3131932721981197e-6|
| Independent comparison / physical parent-work amplitude |2.6216258470700277e-11|2.623885806322894e-11|4.482204238410154e-9|
| Defect-accounted split residual |4.599298098149717e-15|4.234410424390687e-15|4.529049119493985e-15|

Work/source quantities use the retained project normalization, not an invented SI conversion.
All working physical-response budgets pass2e-5; worst margin is about15.23. Algebra tolerance remains1e-10. Largest cumulative coupled readout working envelope is1.9800368940604032e-7. Maximum inverse-safety expression is0.21240272668140825<1. These are numerical working budgets, not rigorous global enclosures.

New3046..3940 work accumulation is independently resolved: branch-change increment=-6.244321605036952e-16, with numerical comparison1.742369595436056e-9 of its amplitude. Original/coherent increments have comparisons about1.77e-11.

The TOTAL tiny branch-change approximation-error self-precision remains0.001962546616015176 and fails2e-5. Its inherited allowance1.428932389025111e-18 was not erased by subtracting a work offset. New accumulation precision does not remove inherited trajectory uncertainty.

## Physical consequences, not just gates

physical-consequences.json reuses the existing source and metric/photon projection. All responses below mean coherent-minus-original WITHIN MTS, not MTS-minus-baseline and not an observational fit.

Parent source changes are numerically resolved in density, current and pressure: relative comparisons2.7790294849626788e-8,5.326482975499282e-9 and4.0345949597153034e-9. The parent cumulative pressure-work response ends at3.156677602056608e-9 in retained work units, with precision1.901071823985503e-9 of its amplitude.

| Retained response | Approximation vs parent numerical comparison |2e-5 gate|
|---|---:|---|
| Native velocity |1.033981873296329e-5|pass|
| Native Weyl readout |4.352759280533406e-6|pass|
| Photon-density readout |9.095904741587362e-7|pass|
| Relative-density readout |5.233635577219684e-7|pass|
| Stable baryon/photon slip |9.236736833093204e-7|pass|

The parent photon-density response ends at-2.871792406471379e-10 in the retained readout normalization. Its amplitude2.9111900563816295e-10 is resolved by the paired-resolution comparison4.471488706395386e-7. This is a saved-model response, not a measured sky signal.

Use stable-consequences.json for the already-derived slip identity delta_v_b-(3/4)delta_q_gamma. The original raw packet-subtraction comparison0.0009214487610401607 still fails and is preserved, rather than rediscovered as a new physical discrepancy. Reusing the existing identity gives the passing comparison above, with80-digit arithmetic controls and no rerun of physical evolution.

Baseline is checked using the same histories/tolerances. Its owned cold current/pressure/work channel is structurally zero, as verified directly. The generic full-source density-plus-pressure rounding allowance in the follow-up report is overinclusive for that exact zero and is NOT evidence of nonzero pressure. Baseline tiny density/metric responses remain unresolved, and its stable slip amplitude1.1171927334522758e-17 has precision0.011973806108772411: retain this limitation, do not call it a detection or exact zero. No baseline/MTS direct common-redshift comparison has been manufactured from unequal clocks.

## Reproducibility and restart

- regime-inputs.json and inputs.json protect the old authority, native binary, source histories and new frozen physical scripts.
- verification.json:689 checks pass, including score replay, original-clock retention, exact state/work joins, monotone carried allowances, checkpoints, fresh-owner final RHS and retained earlier failures.
- consequences-inputs.json / consequences-verification.json and stable-consequences-inputs.json / stable-consequences-verification.json freeze and replay the saved-data analyses separately. No physical gate was changed by those analyses.
- Source preparation, all28 physical runs, all seven scoring runs and both readout workers complete without failure.
- Restart from COMPLETE epoch3940/cold-32/64-terminal.npz and epoch3940/heavy-32/64-terminal.npz plus corresponding work-terminal files; preserve both resolutions.
- Separate parent/approximate native and core transport terminals remain controls, not substitutes for complete coupled states.
- closeout.json / cleanup.json contain the artifact seal, exact worker identities and native release receipts. Independent post-closeout verification must also confirm the foreground closer exited.

The full MTS goal remains active and unfinished. Next work should finish the retained source-history endpoint and its response connection, not accumulate hundreds of tiny nominal epoch stages.
