# 5224 - Replacement scaled controlled run

## Protocol

Checkpoint 5221 remains frozen as a failed run. This replacement
keeps its seeds, allocation, estimator and acceptance thresholds,
adds only the checkpoint-5222 sequential all-zero classifier, and
corrects topology-cache ownership.

Exactly 233 unaffected converged jobs are migrated from 5221. The
changed classifier was invoked only in the failed job, which is
instead migrated from the independently converged 5223 replay.
Every migrated numerical payload and topology payload is checked
by a metadata-independent digest.

## Current state

- State: `COMPLETE_DESIGN`.
- Converged jobs: `520/520`.
- Missing jobs: `0`.
- Failed or unconverged jobs: `0`.
- Complete fresh events: `2/2` full and `24/24` topological.
- Decision: `REJECT_CONTROLLED_SCALE_WITHOUT_RETUNING`.
- Validation passed: `True`.

## Estimate

- Provisional pooled `K_mu=-196.8269863-99.91028168 i`.
- Real/imaginary SE: `382.64473` / `64.647775`.
- Tail/precision gates: `False` / `False`.

## Claim boundary

This replacement can close only the crossed-hhh coefficient
statistic. Numeric UV, local GR and full MTS remain unclaimed.

## Evidence

- Protocol lock: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5224\frozen_replacement_protocol_lock.json`
- Job migration: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5224\converged_job_migration.json`
- Topology migration: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5224\topology_cache_migration.json`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5224\replacement_scaled_controlled_results.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5224_VALIDATION.csv`
- Resume: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5224\RESUME.md`
