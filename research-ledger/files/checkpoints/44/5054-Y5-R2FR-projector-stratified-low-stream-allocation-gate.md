# 5054 - projector-stratified low-stream allocation gate

Marker: `MTS_5054_PROJECTOR_STRATIFIED_LOW_STREAM_ALLOCATION_GATE`.

The local projection is linear,

```text
P = I - s s^T/(s^T s),
```

and each of the five raw cyclic components uses a disjoint three-argument
block. This permits exact independent low streams before applying `P`; it is not
an approximation. All 52 set partitions of the five raw components were
costed and optimized.

No partition passes the `0.8` efficiency gate within 10 hours. The best capped
choice is the unsplit full vector: four low units give score ratio `1.128` at
`9.70 h`. The first apparently efficient integer point uses 12 low units and
score `0.796`, while every split partition is worse. Therefore covariance
between raw components is valuable and projector stratification does not solve
the cost problem.

The 13.85-hour figure produced here used paired variance with one-event costs
and is superseded by 5055. Its unit-consistent paired value is `27.69 h`. The
structural result—no partition beats the full low vector—remains valid.

## Evidence

- Result: `source-intake/functional_rg/5054/projector_stratified_low_stream_allocation_gate.json`
- Partitions: `source-intake/functional_rg/5054/projector_partition_allocation_comparison.csv`
- Selected allocation: `source-intake/functional_rg/5054/selected_projector_stream_allocation.csv`
- Generator: `scripts/Y5_R2FR_5054_projector_stratified_low_stream_allocation_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5054_VALIDATION.csv`
