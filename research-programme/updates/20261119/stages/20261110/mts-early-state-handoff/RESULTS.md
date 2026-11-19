# Coupled early-state handoff verified — 2026-11-10

The retained coherent solution now crosses a tested FULL native perturbation
restart with its own matter/radiation-sourced metric. This finishes the saved
next step after the derived heavy-source interpolation repair. No physical
input, action, source bank, observation grid or tolerance was refitted.

## Saved reduced continuation

The previous endpoint is carried into the next299 intervals, rather than
resetting to the native state. Native-seeded controls remain separate.

| Model | Carried worst normalized readout error | Separately native-seeded error |
|---|---:|---:|
| Cold baseline | 1.3475077e-6 | 7.1314886e-7 |
| MTS heavy | 1.3224916e-5 | 1.6293978e-5 |

All fine2/fine4/coarse4 source, step and history checks pass the unchanged
2e-5 gate. These numbers are the fine4 maxima. The heavy carried case has
only a factor1.51 margin; do not call that high-precision physical agreement.
The separately native-seeded control is not substituted for the carried run.

## Actual coupled restart

| Control | Active / allocated coordinates | State difference | Derivative difference | Real64 observer/source difference |
|---|---:|---:|---:|---:|
| Matching window, baseline | 182 / 397 | 0 | 0 | 0 |
| Matching window, MTS | 185 / 400 | 0 | 0 | 0 |
| Earlier tight coupling, baseline | 106 / 397 | 1.68659e-10 | 1.37514e-10 | 1.49972e-12 |
| Earlier tight coupling, MTS | 109 / 400 | 1.92875e-11 | 5.88481e-11 | 1.63417e-10 |

Each number is the largest componentwise peak-normalized difference for that
category. Zeros mean bitwise parity on this trajectory, not zero continuum
error. Inactive allocated padding is excluded from physical mode counts.
Every initial state/derivative/observable/cache copy is exact. All4253 original
outputs remain bitwise unchanged by the fork. The nonzero early differences
are from a genuinely separate adaptive integration, not an echoed array.

The nonzero active photon-cache differences are3.68214e-14 for baseline and
3.18655e-13 for MTS. No photon cache was zeroed. Native G11/G30 approximate
memories are inactive here; the corresponding active hierarchy is retained.

## Action/source and constraint recovery

Full-vector recovery of scalar D/P/Q, gauge conversion, cold-state variables,
Friedmann, shear, momentum, Poisson and Weyl constraints passes the existing
1e-10 algebra gate. Worst source/constraint recovery is5.08487e-13.
The canonical readout restart differences are0 in the matching window,
4.13021e-12 for early baseline and1.63395e-10 for early MTS, all below2e-5.

The MTS matching window crosses4 field and4 velocity sign changes. The early
window crosses5 field and6 velocity sign changes. Recovery stays finite;
neither a zero-velocity division nor a new phase/averaging choice is needed.
Five retained symbolic identities pass. These source identities do not erase
the preceding stage's remaining off-shell background/metric residuals.

## Verification and ownership

`validation.json` independently recomputes1852 comparisons, verifies3231
source hashes and compiles the local Python scripts without bytecode.
It includes negative comparator controls and exact incoming-state checks.
The copied native library changes ONLY `fortran/camb_python.f90`; the retained
field action, quintic source interpolation and original libraries are intact.
The39-unit isolated build tracked136 compiler/helper identities and removed
its temporary drive mapping. Final exit and seal checks are in
`CLEANUP-VERIFIED.json` and the postseal receipt.

No GitHub, Galaxy edits, observations, fit, relay, browser, subagent or shared
service changes. No process killed. Snapshot arrays and native owner pointers
are released before exit. The actual full numerical vectors are saved, but
the native background owner remains a live-session dependency; this is not
a portable standalone checkpoint. Original external initial conditions and
abundance remain inherited. See NEXT.md for the next physical calculation.
