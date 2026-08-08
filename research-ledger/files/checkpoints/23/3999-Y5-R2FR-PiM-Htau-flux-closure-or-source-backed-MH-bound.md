# 3999 - PiM/Htau Flux Closure Or Source-Backed MH Bound

Timestamp: `2026-07-01T19:06:35+00:00`

## Result

This rung does not merely say the mass plateau is missing. It derives the exact conditional route:

`d(Pi_M J_H[tau]) = 0`

holds in a local stationary exterior annulus if the Hilbert/Ward current closes, `tau` is stationary/Killing, `Pi_M` is parent-owned and constant on the annulus, boundary/reference terms are fixed, and no radiative/Poynting, source-crossing, memory/range, or non-EH monopole flux leaks through the annulus.

## Flux Derivation

The starting identity remains

`M_H[S2]-M_H[S1] = N_G int_A d(Pi_M J_H[tau])`.

The product rule gives

`d(Pi_M J_H)=Pi_M dJ_H + (D Pi_M) wedge J_H + [d,Pi_M]_ref J_H + boundary/exchange terms`.

On shell, the Hilbert stress Ward identity gives `nabla_mu T_H^{mu nu}=0`. Contracting with a stationary/Killing `tau` gives `dJ_H[tau]=0`, except for explicit source crossing and radiative/Poynting leakage. If the projector and reference terms also commute, the whole flux vanishes.

## Bound If Closure Fails

`|Delta M_H|/M_ref <= |N_G|/M_ref int_A (|Pi_M dJ_H| + |D Pi_M wedge J_H| + |dB_ref| + |J_rad/Poynting| + |J_nonEH| + |J_source_crossing|)`.

So a failed plateau is not a vague failure anymore. It is the vector `epsilon_MH_flux_3999`.

## Evaluator Results

- `CASE3999_0_conditional_zero_exterior`: status `CONDITIONAL_ZERO_CLAUSES_UNSIGNED`, epsilon `0.000000000000e+00`, zero=True, no_backfill=True, claim=False
- `CASE3999_1_static_EM_stress_inside_JH`: status `EM_STRESS_RETAINED_NUMERIC_SMOKE_ONLY`, epsilon `3.000000000000e-06`, zero=False, no_backfill=True, claim=False
- `CASE3999_2_radiative_Poynting_leakage`: status `RADIATIVE_FLUX_NONZERO`, epsilon `4.000000000000e-05`, zero=False, no_backfill=True, claim=False
- `CASE3999_3_projector_drift`: status `PROJECTOR_COMMUTATOR_NONZERO`, epsilon `7.000000000000e-05`, zero=False, no_backfill=True, claim=False
- `CASE3999_4_orbital_backfill_refused`: status `ORBITAL_MU_USED_AS_MH_SOURCE`, epsilon `0.000000000000e+00`, zero=False, no_backfill=False, claim=False
- `CASE3999_5_missing_parent_rows`: status `MISSING_PARENT_FLUX_COMPONENT_VECTOR`, epsilon `MISSING`, zero=False, no_backfill=True, claim=False

## Verdict

We have a real conditional local-vacuum/stationary-exterior mass plateau theorem. We do not yet have a global local-GR claim, because the parent projector, reference boundary, radiation/Poynting silence, and non-EH channel clauses still need to be signed or bounded on the same annulus with the same `tau`, `Pi_M`, and reference choice.

## Next Target

The sharpest next move is the EM/Poynting split: prove static EM stress is part of the Hilbert source current, and isolate true radiative flux as a boundable `Delta_rad_Poynting` leakage term.

- `4000-Y5-R2FR-EM-Poynting-stress-inside-Hilbert-source-or-radiative-MH-bound.md`
- `scripts/Y5_R2FR_4000_EM_Poynting_stress_inside_Hilbert_source_or_radiative_MH_bound.py`

## Source Count

- source needles found: `16/16`
