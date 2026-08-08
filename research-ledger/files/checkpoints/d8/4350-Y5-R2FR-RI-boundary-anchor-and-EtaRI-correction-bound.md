# 4350 Y5-R2FR RI boundary anchor and EtaRI correction bound

Marker: `PPC4161_RI_BOUNDARY_ANCHOR_AND_ETARI_CORRECTION_BOUND_4350`

Decision: `STATIC_COMPACT_ANCHORED_RI_BRANCH_GIVES_CONDITIONAL_POSITIVE_GAP_ETARI_ZERO_OR_BOUND_NONCLAIM`

## Result

4350 makes a real leap forward on the local-GR route:

```text
compact anchored residual test space + fixed static same-Hodge closed collar
=> Eta_RI,total = 0
=> lambda_RI,lower = pi^2/ell_RI^2 > 0
=> homogeneous RI adjoint multiplier Lambda = 0.
```

This is still private/nonclaim because the parent action must sign the branch clauses. But it is no longer just "missing". The clean theorem path and the finite-bound fallback are now separated.

## Next

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4351-Y5-R2FR-RI-owner-tail-zero-application-or-finite-bound-runner.md | Can the 4350 clean branch be applied to the 4347 owner-tail zero theorem, or must the owner tail remain as a finite residual bound? | apply Lambda=0 on the compact anchored static RI branch and propagate the owner-tail zero into the local GR/Newton residual vector | write the finite owner-tail bound with Eta_RI,total_bound and ell_RI source rows, keeping all arena claims false |
