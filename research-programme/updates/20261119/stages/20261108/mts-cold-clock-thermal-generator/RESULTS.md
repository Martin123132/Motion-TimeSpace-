# Cold free evolution and clock/thermal coupling verified

## What moved forward

The free matter evolution and metric-force injection are now derived explicitly in the retained physical coordinates, rather than supplied only through numerical operator extraction. This includes dust, baryons, photons/polarization, both retained massless-neutrino branches, all five massive-neutrino nodes through G192, the slow scalar and the heavy relative-phase pair.

Two useful exact results accompany that derivation:

1. The physical Thomson collision block is symmetric negative semidefinite: its dipole sector is a negative outer product, and its quadrupole eigenvalues are -opacity/H and -3opacity/(10H). Collisions cannot be counted as positive norm growth.
2. Thermal first/second N-derivatives follow from the actual saved cubic interpolation and its scale inverse. The physical conformal clock is NOT substituted for the thermal table clock. The original clock uncertainty now enters the retained hierarchy closures explicitly.

This builds on the existing metric and coordinate-map envelopes. The original bank, grids, thermal history, parent action, initial preparation and tolerances remain unchanged. No GitHub action.

## Validation

-54 native full free-generator/injection cases: both models, three scales, three cold epochs and three phases. Worst absolute coefficient differences are3.276000e-9 for the free source and1.113332e-12 for the injection, below2e-5.
-168 full G192 native vector comparisons cover both gravity branches, both models, independent phases, full-state random probes and all five terminal momentum-node basis vectors. Worst relative difference8.100549e-9; worst absolute6.131939e-7. The original terminal condition is retained.
-409,374 independent70-digit derivative entries,90 saved-background/clock fixtures and3,060 thermal derivative checks pass. Largest fixture/enclosure ratio0.498046. Whole-window coverage follows from the interval derivation, not sampling.
-Five exact symbolic identities cover collision dissipativity, intensity/polarization streaming symmetry and the physical-clock derivative. The existing half-k predictions are preserved bit-for-bit by the accepted v2 implementation.

## Source uncertainty now quantified

These bounds apply across the saved cold interval and all phases, conditional on the retained thermal source and inherited scalar/clock tube. They are operator-coefficient errors, not fractional observational errors or completed evolution errors.

| k family | Free-source operator bound | Force-injection bound (Mpc^-1) | Clock-closure group bound |
|---|---:|---:|---:|
| half |2.613181e-3|2.697787e-6|1.312014e-4|
| balanced |5.555864e-3|5.395574e-6|1.081836e-4|
| double |1.111173e-2|1.079115e-5|1.081836e-4|

Table values are rounded upward; exact values and term-by-term splits are in `source-envelope/*-envelope.json` and `audit/result.json`. The clock-closure group includes H/scalar uncertainty as well as clock uncertainty. The inherited heavy clock radius is0.017485713632227135 Mpc. Its control counterpart has zero heavy-averaging replacement radius, not zero numerical uncertainty.

The largest bounds arise from rapid streaming and heavy micromotion. They must not be exponentiated as growth rates: streaming is largely skew, collision terms damp, and the preceding periodic averaging calculation handles the heavy oscillation. These conservative source bounds alone do not establish a2e-5 total transfer error. The retained source representation, thermal continuum integration and global ODE arithmetic remain separate budget channels.

## Preserved branch correction

The initial balanced-k attempt correctly stopped at an unsupported source signature: the retained model uses UFA there, whereas half-k uses the full massless hierarchy. The v2 derivation includes the existing UFA gauge coupling, both metric injections and its -3/(H tau) closure. It does not turn the approximation off or change the model to pass a test. The rejected attempt, logs and exact initial code remain in place; see `EXECUTION-NOTE.md`.

Accepted code: `free_math_v2.py`, `interval_jets.py`, `thermal_jets.py`, `enclose_free.py`, `validate_sources.py`, `validate_full_vectors.py`, and `audit_sources.py`. Accepted native packets: `half/free-01`, `balanced/free-02`, `double/free-02`; all three `full-vectors` folders. The incomplete `balanced/free-01` is not accepted.

## Next calculation

Carry the derived thermal jets and the preceding exact normalized-denominator jets through the full metric/map derivative. Combine G_free, F, L_phys and both coordinate maps, preserving their cancellations, then use the useful physical logarithmic norm and averaging remainder to transport the ORIGINAL early preparation. No invented late initial mode is needed. The clock-only closed-generator change already has the exact form R_phys(delta G_clock)S_phys at fixed slow state/phase.

All numerical workers finish before sealing. `CLEANUP.json` records exact owned-process absence; `closeout.json` inventories hashes and the accepted scope. No compilers, temporary apps, servers, subagents or unrelated process cleanup are started in this stage.
