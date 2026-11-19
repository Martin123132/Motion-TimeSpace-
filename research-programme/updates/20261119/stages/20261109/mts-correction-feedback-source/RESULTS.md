# Correction feedback derived and checked

Completed locally on 2026-11-09. Authoritative machine-readable evidence: audit/result.json, the three family feedback-01/result.json files, and the individually hashed source packets. closeout.json is the final artifact manifest and CLEANUP.json records worker exit verification.

## What changed physically

The previously omitted correction feedback is now calculated as
    h = R_total delta_s,
    R_total = (I+C)^-1 [A C - C M - C_N + Delta_map (I+C)].
delta_s is the accepted slow first response plus its full phase primitive, evaluated at the original saved times. Normal-form and coordinate-map contributions remain separate. No fitted amplitude, replacement initial mode, reference-discrepancy correction, or new physical cutoff was introduced.

Reconstruction of A from M+Omega C_theta was checked against the actual original field-equation generator at independent angles before accepting the new source. The full endpoint inverse and the G192 hierarchy remain in use.

## Coverage and unchanged checks

All 54 source nodes pass: nine saved times, three retained wavelength choices, MTS and baseline. Each includes both GR and spatial-Poisson branches. The probe's accepted midpoint was reused, not recalculated. All five numerical workers exited successfully, including the final audit.

- 216 original-source regression checks.
- 324 independent direct-generator checks.
- 648 independent feedback prediction checks.
- 432 numerical phase-refinement comparisons.
- 108 finite-representation operator bounds, independently recomputed from the stored coefficients.
- No altered bank, physical grid, initial preparation, coupling, or acceptance tolerance.

ALGEBRA=1e-10 and GATE=2e-5 remain unchanged. Worst original-source discrepancy: 4.2843028091262436e-14. Worst direct-generator discrepancy: 3.8057243999101265e-16. Worst direct-feedback discrepancy: 1.0363152545944253e-9. Worst 128/256 phase comparison: 2.2443300955423724e-9. Worst full endpoint inverse residual: 6.404945357403434e-16.

## Calculated scale

Values below are maxima over the saved epochs and both branches. Feedback/source ratios compare the maximum phase-vector norm of each feedback component to that of its corresponding first-source component, at the same node and branch. They are not pointwise ratios near a source zero, observables, or accumulated evolution errors.

| Retained wavelength | MTS normal feedback / leading state norm | MTS map feedback / leading state norm | Largest component feedback / first source |
|---|---:|---:|---:|
| half | 1.5222153442831387e-10 | 1.7941793779441268e-14 | 1.6770731839078084e-7 |
| balanced | 1.753836020448141e-10 | 1.431489288445175e-14 | 1.6027951994789647e-7 |
| double | 1.1566498254372255e-10 | 1.637519949027214e-15 | 1.4145091673485873e-7 |

The calculated MTS feedback is small in this retained coordinate norm. Its physical accumulated effect is the next calculation, not inferred from these ratios.

Baseline: C=0 and the normal-form feedback vanishes exactly. The inherited coordinate-map defect was nevertheless evaluated, not set to zero: map feedback/state maxima are 2.624343630166832e-52, 2.7119889243153256e-52 and 2.8985573393248787e-52. Such tiny floating-point baseline values are controls of the retained implementation, not evidence of a new physical effect or meaningful relative precision at that scale.

## A useful derived bound

For the retained primitive polynomial, q bounds sup_phase ||C||_2. The largest MTS q is 0.0005185178414948041, well below one. Thus the corresponding endpoint inverse is bounded by 1/(1-q) in these coordinates. Combining this with the finite numerator's Fourier norm sum gives the following maximum fixed-epoch operator bounds:

| Wavelength | max ||R_finite||_2 bound |
|---|---:|
| half | 0.0035620007162317545 |
| balanced | 0.0021723755975881177 |
| double | 0.0017376133569666512 |

These are all-phase mathematical bounds for the defined finite numerator/primitive representation at each saved epoch. Direct physical-generator checks separately test that representation. No bound between unsampled epochs or enclosure of the unsampled analytic physical operator is supplied by this step.

MTS source times cover N=-8.368470146125201 to -8.293202925182642; baseline covers N=-8.368566039228474 to -8.293202925162689. These are retained final-interval epochs, not a new late-time restart.

## Continuation

Carry h through the saved full-hierarchy response and terminal maps, qualify its time interpolation and response resolution, and retain or bound its further self-feedback. Keep inherited source interpolation, background reconstruction and initial-state errors separate. The preceding accumulated-omission budget is preserved, not replaced or erased.

No observational fit, GitHub update, subagent, temporary app, compiler, or server was used. Crash recovery found the existing dispatcher and continued without duplicate workers or stopping unrelated processes. A read-only status display initially had a PowerShell formatting error; it was corrected without changing any numerical job or scientific output.

