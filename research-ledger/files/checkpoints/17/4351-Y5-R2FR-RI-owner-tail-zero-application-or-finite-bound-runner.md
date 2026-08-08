# 4351 Y5-R2FR RI owner-tail zero application or finite bound runner

Marker: `PPC4161_RI_OWNER_TAIL_ZERO_APPLICATION_OR_FINITE_BOUND_RUNNER_4351`

Decision: `OWNER_TAIL_ZERO_APPLIES_ONLY_ON_FULL_CLEAN_BRANCH_OTHERWISE_FINITE_BOUND_WITH_4350_DENOMINATOR_NONCLAIM`

## Result

4351 uses the 4350 RI gap. Clean branch:

```text
C_RI=0, lambda_4350>0, R_Lambda=0, B_RI=0, I_RI=0
=> Y_owner_a=0.
```

If boundary or incoming clauses are unsigned, the sharpened fallback is:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|.
```

This means the next useful attack is not another lambda pass. It is boundary/corner silence and no-incoming RI mode control.

## Next

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4352-Y5-R2FR-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md | Can B_RI and I_RI be zeroed in the same compact static selector, or must the owner-tail branch now become a finite residual value runner? | derive stationary/no-incoming RI selector plus boundary/corner silence for the same anchored RI test space | fill finite B_RI, I_RI, R_Lambda, C_Lambda, Pi_a and lambda_4350 source rows for arena scoring |
