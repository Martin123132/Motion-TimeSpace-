# 5221 - Scaled controlled two-stratum coefficient run

## Frozen design

The checkpoint-5212 variance and cost evidence gives
`n_top/n_full = 11.7194556826`. The design rounds this upward
to `12:1` and freezes two mandatory tranches. Each tranche
contains one paired full event and twelve controlled topological
events, with ten arguments and two epsilon values per event.

The A00 real control is the checkpoint-5220 independently
validated, symmetry-fixed unit-coefficient control. It is applied
before the physical local projection. No coefficient-dependent
stopping or threshold retuning is allowed after tranche one.

## Current state

- State: `BLOCKED_JOB_FAILURE`.
- Converged jobs: `233/520`.
- Missing jobs: `286`.
- Failed or completed-unconverged jobs: `1`.
- Complete fresh events: `1/2` full and `10/24` topological.
- Decision: `RUN_MANDATORY_REMAINING_TRANCHE`.

## Estimates

The new-only estimate is unavailable until at least two events are complete in both strata.
- Compatibility-gated pooled `K_mu=53.46217384-37.12999609 i`, real SE `445.00164` and imaginary SE `28.819647`.
- Pooled controlled-tail gate: `False`; coefficient precision gate: `False`.

## Claim boundary

This run can close only the crossed-hhh coefficient statistic.
It does not by itself close the remaining cut classes, a
canonical ultraviolet coefficient, local GR, or full MTS.
All corresponding claim flags remain false.

## Evidence

- Manifest: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5221\frozen_scaled_controlled_manifest.json`
- Allocation derivation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5221\allocation_and_stopping_derivation.json`
- Protocol lock: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5221\frozen_scaled_controlled_protocol_lock.json`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5221\scaled_controlled_two_stratum_results.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5221_VALIDATION.csv`
- Resume note: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5221\RESUME.md`
