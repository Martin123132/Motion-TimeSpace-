# Complete coupled restart and bounded continuation

Reuse the exact retained Coupled and MetricCoupled equations. Save all active
native multipoles and coherent differences, allocated inactive seed values,
the autonomous background correction, integrated exchange work and every
normalization. Do not reconstruct unobserved hierarchy entries as zero.

The Fortran owner contains process-local pointers. Rebuild it from frozen
parameters/tables/binary; require exact original934-state/derivative/cache/
signature/readout prefix parity in a fresh942-state capture. Then load the
persistent dynamical state. This is reproducible rehydration, not a portable
serialization of arbitrary Fortran heap objects. Retained branch flags must
remain unchanged, including absence of tight coupling and massive-nu closure.

Replay original64 full evolution with identical divisions, query times and
arithmetic; additional files do not alter the solve. Store full states at
existing queries and checkpoints2916/2924. A later fresh process restarts2916
and compares to uninterrupted2924, including the complete normalized state,
common-metric readouts and exchange work. Freeze2e-5 full-output and1e-10
algebra gates before scoring. Tiny response-relative limitations stay separate.

Only when both model restart gates pass, continue the physical one-mode
trajectory through eight native-clock epochs2925..2932 at32/64 step settings.
This is not a902-translated-preparation-window extension or full sky forecast.
No new scattering/source fit or table extrapolation is permitted. The future
source-budget projection requires its own correctly supported histories.

Terminal checkpoints are reusable physical states, not selected observables.
Each segment also saves a bounded latest-state cursor for interruption safety.
Immutable saved checkpoints are never overwritten. No rebuild of native DLL,
no public publication, no process interference, one numerical worker/thread.
