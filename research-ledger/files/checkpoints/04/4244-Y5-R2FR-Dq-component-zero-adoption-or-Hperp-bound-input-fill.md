# 4244 - Dq component zero adoption or Hperp bound input fill

**Status:** `DQ_COMPONENT_THEOREMS_PRESENT_HL_ARGUMENT_ADOPTION_UNSIGNED_HPERP_BOUND_INPUT_FILL_SELECTED_NONCLAIM`.

## What changed

4244 separates two things that were easy to blur:

1. the componentwise theorem says `Dq_i[v]=0` for admitted q-basic/selector-safe `v`;
2. the local branch needs `Dq_i[H_L]=0` for the actual leakage direction.

The first exists conditionally. The second is not yet signed.

## Result

No local-GR claim is made. Instead, the branch now has an explicit finite residual ledger:

```text
|S_A Hperp^A|
<= C_S C_perp sqrt(sum_i w_i epsilon_i^2),
epsilon_i >= ||Dq_i[H_L]||.
```

## Files written

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md`
- `P8_Y5_R2FR_4244_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv`
- `P8_Y5_R2FR_4244_HL_ARGUMENT_GATES.csv`
- `P8_Y5_R2FR_4244_HPERP_BOUND_INPUT_FILL.csv`
- `P8_Y5_R2FR_4244_RESIDUAL_BUDGET.csv`
- `P8_Y5_R2FR_4244_DECISION.csv`
- `P8_Y5_R2FR_4244_CLAIM_FIREWALL.csv`
- `P8_Y5_R2FR_4244_STATUS.csv`
- `P8_Y5_R2FR_4244_NEXT_TARGET.csv`

## Next target

`4245-Y5-R2FR-HL-argument-qbasic-adoption-or-Dq-bound-first-input-row.md`
