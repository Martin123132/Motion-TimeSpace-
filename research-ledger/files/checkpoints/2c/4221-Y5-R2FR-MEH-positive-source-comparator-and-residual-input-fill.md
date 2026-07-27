# 4221 - M_EH Positive Source Comparator And Residual Input Fill

**Status:** `MEH_POSITIVE_LOWER_BOUND_LAW_DERIVED_RESIDUAL_INPUTS_FILLED_AS_SCHEMA_PARENT_SIGNATURE_VALUES_MISSING_NONCLAIM`.

## What moved

This checkpoint turns the vague `M_EH>0` demand into a scoreable lower-bound law:

```text
M_EH >= c^-2 E_plus(1-epsilon_E).
```

with:

```text
epsilon_E=(E_neg_abs+E_open_abs+E_ref_abs+E_vir_abs+E_nonEH_abs+E_frame_abs)/E_plus.
```

Thus:

```text
E_plus>0 and epsilon_E<1 => M_EH>0.
```

## Why this is a forward move

The old route only said "need positive energy." The new route states exactly which source rows must be filled and how they are combined. It also prevents three common cheats:

- orbital `GM` cannot define the source mass;
- Tolman/Komar pressure cannot be ignored;
- Poynting flux cannot be both hidden force and Hilbert EM energy.

## Generated rows

- `P8_Y5_R2FR_4221_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4221_MEH_COMPARATOR_LAW.csv`
- `P8_Y5_R2FR_4221_SECTOR_SIGNATURE_MATRIX.csv`
- `P8_Y5_R2FR_4221_RESIDUAL_INPUT_SCHEMA.csv`
- `P8_Y5_R2FR_4221_BOUND_CANDIDATE.csv`
- `P8_Y5_R2FR_4221_DECISION.csv`
- `P8_Y5_R2FR_4221_CLAIM_FIREWALL.csv`
- `P8_Y5_R2FR_4221_STATUS.csv`
- `P8_Y5_R2FR_4221_NEXT_TARGET.csv`

## Decision

No local-GR/Newton denominator claim is made. The law is derived, but the values/signature rows are not filled.

Next: `4222-Y5-R2FR-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md`.
