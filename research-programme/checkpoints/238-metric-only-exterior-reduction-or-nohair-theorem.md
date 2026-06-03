# 238 - Metric-Only Exterior Reduction or Nohair Theorem

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 237 made the EH route precise:

```text
MTS earns local GR only if the compact exterior reduces to a metric-only
Einstein-Hilbert action.
```

This checkpoint audits every non-metric sector that must leave the exterior.

## 2. Machine Artifact

Script:

```text
scripts/metric_only_exterior_reduction_or_nohair_theorem.py
```

Run:

```text
runs/20260601-000055-metric-only-exterior-reduction-or-nohair-theorem
```

Command:

```text
python scripts/metric_only_exterior_reduction_or_nohair_theorem.py --timestamp 20260601-000055
```

Status:

```text
metric_only_exterior_reduction_sector_audit_partial_nohair_not_derived_no_promotion
```

Claim ceiling:

```text
sector_nohair_audit_no_metric_only_parent_reduction_or_PPN_promotion
```

## 3. Sector Audit

The metric-only exterior needs every non-metric sector to become:

```text
zero,
pure boundary,
or conserved M_eff.
```

Current readout:

| sector | current status |
|---|---|
| ordinary matter | pass as exterior-region definition |
| effective memory scalar | screened EFT, not parent no-hair |
| `Pi_M` mass class | contract; conserved `M_eff` not derived |
| `Pi_TF` shear | conditional scalar-boundary route |
| `Pi_matter` direct coupling | universal-coupling contract |
| `P_mem J_rel` | topology gate plus parent gap |
| `T_projector` | structured, not derived |
| `X` multiplier | no-hair algebra not derived |
| `V_def/P[Y]` | not derived |
| boundary primitive `A_rel` | not derived |

So:

```text
metric-only exterior reduction is not derived.
```

But it is not shapeless anymore.

## 4. Nohair Targets

The route now splits into six theorem targets:

| target | theorem needed |
|---|---|
| `N1_Meff` | mass flux becomes conserved `M_eff` only |
| `N2_no_TF` | trace-free/tangential exterior stress vanishes |
| `N3_universal_coupling` | matter/clocks couple only to metric/coframe |
| `N4_exact_relative_memory` | `P_mem J_rel` exact with pure-gauge primitive |
| `N5_projector_stress` | `T_projector` cancels or vanishes in Bianchi ledger |
| `N6_auxiliary_nohair` | `X/J_rel/V_def` carry no exterior propagating degrees |

Only after these can the EH action contract be promoted.

## 5. Consequence For Beta

The beta chain is now:

```text
N1-N6
=> metric-only exterior
=> Einstein-Hilbert/Lovelock gate
=> Schwarzschild exterior
=> beta = 1.
```

The current corpus has:

```text
several conditional gates,
but not N1-N6 as parent theorems.
```

So:

```text
beta remains conditional.
```

No local-GR promotion is allowed.

## 6. Decision

Decision:

```text
metric_only_exterior_reduction_sector_audit_partial_nohair_not_derived_no_promotion
```

Meaning:

```text
the metric-only exterior reduction does not derive yet. The audit shows one
definitional pass, several useful conditional/screened gates, and multiple
not-derived sectors.
```

Main gain:

```text
the non-metric exterior leftovers are now enumerated sector by sector.
```

Main failure:

```text
X/V_def/A_rel/projector stress and source normalization still block
metric-only reduction.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| nonmetric exterior sector audit written | pass |
| no-hair theorem targets listed | pass |
| metric-only exterior parent-derived | fail |
| beta derived | fail |
| local GR or PPN promoted | fail |

## 8. Next Target

Create:

```text
239-nohair-theorem-targets-or-local-bound-runner.md
```

Purpose:

```text
either attack the no-hair targets N1-N6 one by one,
or run an explicitly closure-flagged local-bound preflight using the current
conditional coefficients.
```

Pass condition:

```text
one N-target is parent-derived,
```

or:

```text
the local-bound runner reports closure-flagged pressure without claiming a pass.
```

Fail condition:

```text
metric-only exterior is inserted as a PPN rescue assumption.
```
