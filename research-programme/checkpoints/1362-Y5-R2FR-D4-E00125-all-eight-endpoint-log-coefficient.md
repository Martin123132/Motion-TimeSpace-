# 5346 - D4 E00125 All-Eight Endpoint Log Coefficient

Date: `2026-08-11`

Formal marker: `MTS_5346_D4_E00125_ALL_EIGHT_ENDPOINT_LOG_COEFFICIENT`.

Private derivation checkpoint. No GitHub action, no edit to
`formalization-workbench`, and no regulator-zero, local-GR or full-MTS claim.

## Executive result

All eight source-owned D4 support events now have finite-`E00125` endpoint
logarithm coefficients. The four previously missing one-sided branch events
were evaluated on the active side fixed by the checkpoint-5334 candidate
geometry:

```text
E04, E05, E06: x = x_event - delta;
E07:           x = x_event + delta.
```

The corrected active-side extraction passes every frozen fit, support-gap,
primitive, source-provenance and diagnostic-disk gate. The coherent sum is

```text
A_E00125
 = 0.00038006208677709226
   + 0.47073718025727357 i,

|A_E00125| = 0.470737333683827,
rho_A       = 2.8629739714438195e-6,
|A|/rho_A   = 1.64422498555385e5.
```

The origin lies outside this finite-regulator diagnostic disk. This establishes
the complete eight-event coefficient at `E00125`; it does not establish that
the coefficient has a regulator-independent limit.

## 1. One-sided branch repair

The first extraction attempted the same decreasing-coordinate probe for all
four branch events. That was inconsistent with the parent candidate geometry:
`E07` has support on the increasing-coordinate side. The repaired calculation
does not select a side from the coefficient result. It requires exactly one
active candidate side before sampling and maps positive endpoint distance as

```text
delta = x_event - x  for E04-E06;
delta = x - x_event  for E07.
```

The too-close half-width stencil was also removed. The accepted parent-fit
stencil is

```text
delta / boundary_layer_scale = 1, 2, 4, 8.
```

Trace and derivative changes remain recorded as diagnostics. The acceptance
gate is the propagated event-coefficient disk itself, with relative radius at
most `0.05`; this avoids vetoing a stable final quotient merely because an
intermediate derivative is close to zero.

## 2. Branch contributions

The four newly evaluated contributions are

```text
E04:  1.5514148556130625e-11 + 3.5696248582511500e-8 i;
E05:  1.4824617728311058e-11 + 2.4151490452808285e-8 i;
E06:  1.4534316996989154e-11 + 3.7234756164787590e-8 i;
E07: -1.8780052093643680e-11 - 2.5415931999182768e-8 i.
```

They are small compared with the already-derived two-sided terms and do not
cancel their coherent sum. All eight event contracts pass, and the total
coherent-sum ratio is `0.9999998646363066`.

## 3. Validation and claim boundary

The saved result has

```text
8 unique event rows;
4 one-sided branch rows;
13/13 current source hashes;
0 failed validation gates;
0 malformed or non-finite coefficient disks;
formalization-workbench modified-file count = 0.
```

Only

```text
valid_for_D4_E00125_all_eight_endpoint_coefficients
```

is true in this coefficient artifact. Checkpoint 5343 separately signs the
finite `E00125` fixed-decay integral. The multi-regulator coefficient limit,
regulator-zero limit, decay-angle, phase-space, UV, local-GR and full-MTS
flags remain false here.

## 4. Artifacts and next gate

```text
scripts/Y5_R2FR_5346_D4_E00125_one_sided_branch_endpoint_coefficients.py
scripts/Y5_R2FR_D4_all_eight_endpoint_coefficient.py
scripts/run_D4_E00125_all_eight.ps1
source-intake/functional_rg/5346/E00125/
```

Checkpoint 5349 now owns the completed three-regulator coefficient comparison
at `E000625`, `E00125` and `E005`. Its affine compatibility test passes, while
the coefficient regulator-zero limit remains blocked pending a fourth rung or
a source-derived asymptotic remainder bound. No heavy finite-rung integration
is authorized by the coefficient result alone.
