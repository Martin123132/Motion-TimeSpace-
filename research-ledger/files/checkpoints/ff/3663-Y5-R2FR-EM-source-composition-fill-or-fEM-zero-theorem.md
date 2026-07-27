# 3663 - EM source composition fill or fEM zero theorem

**Status:** 3663 audits the f_EM=0 route against the 3649 EM-lock clauses, refuses the unsigned zero, and stages Sun/Earth/lab source-composition acquisition rows for the live EM-binding branch.

**Claim ceiling:** no f_EM zero, EM-binding pass, WEP, R10, gamma, local-GR, PPN, Newtonian, source-calibration, or EH-dominance pass is claimed.

## Main result

The clean route is still `f_EM=0`, but it is not free. From 3649, it requires unique same-frame Maxwell ownership: no independent `f_X(X_N)F_Q^2`, same Hodge/readout frame, fixed charge normalization, same current owner, and no radiative/optical leak.

Those clauses remain unsigned, so the EM-binding branch stays live. Therefore the practical fallback is source composition: `B_source_EM=sum_i w_i B_i^EM` for the Sun/Cassini gamma branch, Earth/WEP branch, and lab/R10 branch.

## f_EM theorem rows
- `FEMT3663_0_conditional_zero`: CONDITIONAL_ZERO_THEOREM_RESTATED_FROM_3649 - `unique_F2_owner and same_frame_Hodge and charge_norm_owner and current_owner and no_radiative_leak => f_EM=0`
- `FEMT3663_1_current_verdict`: FAIL_CURRENT_CLAIM_FEM_ZERO_UNSIGNED - `3649 EM-lock clauses are unsigned, so f_EM stays in the Q_X basis as B_source_EM*f_EM`

## f_EM zero audit
- `FZA3663_0_unique_F2_owner`: UNSIGNED - no independent f_X(X_N)F_Q^2 operator exists
- `FZA3663_1_same_frame_Hodge`: UNSIGNED - Hodge star/readout frame descends through the same observed coframe
- `FZA3663_2_charge_norm_owner`: UNSIGNED - charge generator and gauge kinetic normalization are fixed by one parent owner
- `FZA3663_3_current_owner`: UNSIGNED - charge current/source normalization descends from the same owner
- `FZA3663_4_no_radiative_leak`: UNSIGNED - radiative/optical readout does not regenerate an effective f_EM
- `FZA3663_5_total`: NOT_SIGNED - all EM-lock clauses hold simultaneously

## Source-composition acquisition rows
- `SCA3663_0_solar_gamma`: `solar_source_for_gamma` - SOLAR_COMPOSITION_SOURCE_REQUIRED
- `SCA3663_1_earth_WEP`: `Earth_source_for_WEP` - EARTH_COMPOSITION_SOURCE_REQUIRED
- `SCA3663_2_lab_R10`: `lab_source_for_R10` - LAB_ATTRACTOR_COMPOSITION_REQUIRED
- `SCA3663_3_generic_source`: `generic_source_body` - GENERIC_SOURCE_SCHEMA_READY_VALUES_MISSING

## Branch status
- `EBS3663_0_fEM_zero_branch`: PREFERRED_BUT_UNSIGNED - parent f_EM zero
- `EBS3663_1_source_composition_branch`: SOURCE_COMPOSITION_ACQUISITION_READY - live f_EM bound branch

## Claim gates
- `CG3663_0_fEM_zero_audit`: PASSED_AUDIT - f_EM zero theorem audited
- `CG3663_1_no_fEM_claim`: ACTIVE_GUARD - f_EM=0 not claimed
- `CG3663_2_source_composition`: PASSED_SCHEMA_GATE - Sun/Earth/lab source composition acquisition rows staged
- `CG3663_3_no_score`: ACTIVE_GUARD - EM component still not score-ready
- `CG3663_4_next`: SOURCE_BODY_OR_UNIQUE_F2_NEXT - next step should source one source-body composition or prove unique F2

## Next checkpoint

`3664-Y5-R2FR-unique-F2-parent-proof-or-solar-BsourceEM-first-row.md` via `scripts/Y5_R2FR_3664_unique_F2_parent_proof_or_solar_BsourceEM_first_row.py`.

## Sources
- `next_3662`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3662_NEXT_TARGET.csv` exists=True needle_found=True
- `theorem_3662`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3662_EM_ZERO_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `elements_3662`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3662_ELEMENTAL_EM_BINDING_ROWS.csv` exists=True needle_found=True
- `schemas_3662`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3662_SOURCE_BODY_SCHEMA_ROWS.csv` exists=True needle_found=True
- `shared_3662`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3662_SHARED_COMPONENT_ROWS.csv` exists=True needle_found=True
- `doc_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md` exists=True needle_found=True
- `theorem_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_EM_MAXWELL_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `audit_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv` exists=True needle_found=True
- `coeff_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv` exists=True needle_found=True
