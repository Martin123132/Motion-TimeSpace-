# 5217 - L64 owned-direct zero confirmation

## Question

Checkpoint 5216 resolved all three grouped sums but left two
individual summands unresolved because its deliberately strict
rule included the coarse `L32` quadrature maximum. Both `L48`
maxima were already below the unchanged `1e-20` zero gate.

## Test

The two exact summands were recomputed at 120 decimal digits with
`64 x 64` contour nodes on the same six radius combinations used
by `L48`. A zero certificate requires both `L48` and `L64` below
`1e-20` and at least a `1e4` reduction from `L32` to `L48`.

## Result

- Zero certificates: `2/2`.
- Resolved grouped rows: `3/3`.
- Validation: `8/8`.
- Zero tolerance changed: `False`.
- Current checkpoint-5215 scale decision allowed: `False`.

## Consequence

The event-local grouped residues are now numerically resolved
without deleting poles or widening a tolerance. The development
event was outcome-exposed, so a new fresh run must predeclare the
general grouped classifier before any scale decision.

## Evidence

- Lock: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5217\L64_owned_direct_zero_confirmation_lock.json`
- Audit: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5217\L64_owned_direct_zero_confirmation_audit.json`
- Registry: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5217\resolved_grouped_owned_direct_registry.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5217_VALIDATION.csv`
