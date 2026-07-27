# 5223 - Sequential-zero failed-job replay

## Result

- Frozen failed job: `TOP__E020__S522121_N0000__A03__primary24`.
- Prior status: `COMPLETED_UNCONVERGED`.
- Replay status: `COMPLETED_CONVERGED`.
- Sequential grouped-zero rows: `2`.
- Relative value change: `6.57580335694e-09`.
- Change in frozen integration-tolerance units: `0.000131516067139`.
- Replacement scaled run authorized: `True`.

The replay uses the unchanged absolute `1e-20` zero gate,
requires both adjacent level reductions, and accepts a
grouped zero only because every constituent pair is
independently zero. It also corrects topology-cache ownership
so the replay no longer writes into checkpoint 5220.

## Claim boundary

This repairs the numerical execution path only. It does not
promote a coefficient, local-GR result, or full-MTS claim.

## Evidence

- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5223\sequential_zero_failed_job_replay.json`
- Classifier audit: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5223\sequential_zero_runtime_audit.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5223_VALIDATION.csv`
