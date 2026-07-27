# 4131 - Source-Slot Tail and Common-G Calibration

## Verdict

- Decision: `SOURCE_SLOT_TAIL_SPLIT_COMMON_G_CALIBRATION_BOUND_VECTOR_FILLED`.
- The source-slot tail is now split into explicit live pieces instead of one vague coupling residual.
- `Dln w_common` is common-mode: WEP cannot kill it; it must be owned by `G_ref`/action-scale or bounded by Gdot/PPN/source calibration.
- No parent-zero theorem is claimed; bound schemas are filled for Gdot, PPN, WEP, R10, Newton/Gauss, and clock/alpha-source channels.

## Generated Outputs

- `P8_Y5_R2FR_4131_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT.csv`
- `P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE.csv`
- `P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS.csv`
- `P8_Y5_R2FR_4131_ZERO_AUDIT`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_ZERO_AUDIT.csv`
- `P8_Y5_R2FR_4131_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_DECISION_GATES.csv`
- `P8_Y5_R2FR_4131_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_STATUS.csv`
- `P8_Y5_R2FR_4131_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4131_NEXT_TARGET.csv`

## Tail Split

| symbol | status | zero_route |
|---|---|---|
| B_EM_source | MASTER_TAIL_VECTOR | exact product envelope after b_alpha invariant reduction |
| Dln c_pre | PARENT_GRAMMAR_OR_BOUND_REQUIRED | zero only if source-only current/action slots are absent from the parent matter grammar or fixed calibration data |
| Dln w_rel | FIXED_REPRESENTATION_OR_BOUND_REQUIRED | zero only if representation/species labels are fixed and no relative source weighting field exists |
| Dln kappa_A | SAME_HILBERT_SOURCE_OR_BOUND_REQUIRED | zero only if all ordinary species use the same Hilbert source coupling before readout |
| Dln R_A | READOUT_CLOSURE_OR_BOUND_REQUIRED | zero only if readout/radiative closure preserves the same source functional |
| z_rad | RADIATIVE_CLOSURE_OR_BOUND_REQUIRED | zero only if radiative closure keeps the visible matter constants fixed in the local branch |
| Dln w_common | COMMON_MODE_G_CALIBRATION_OR_BOUND_REQUIRED | not WEP-visible; must be G_ref/action-scale owned or bounded by Gdot/PPN/source calibration |

## Common-G Product

| symbol | status | meaning |
|---|---|---|
| D_A ln G_eff_obs | EXACT_PRODUCT_IDENTITY | measured coupling silence requires the whole product to be silent, not merely constant G_ref |
| z_G | CONDITIONAL_ZERO_ROUTE_NOT_NUMERIC_PREDICTION | can be zero if G_ref/kappa_ref is a fixed parent global/topological calibration label |
| z_w | COMMON_MODE_BOUND_REQUIRED | universal source prefactor is invisible to differential WEP but visible to Gdot/PPN/source-normalization |
| z_ellJ | SOURCE_DENOMINATOR_BOUND_REQUIRED | source-current normalization denominator remains the algebraic source-coupling throat |
| z_Rframe | READOUT_FRAME_BOUND_REQUIRED | same-frame/readout factor must not reintroduce source variation |
| z_extra | EXTRA_SOURCE_BOUND_REQUIRED | extra-sector source factors must be zero, universal fixed calibration, or bounded |

## Arena Bounds

| arena | observable | status |
|---|---|---|
| Gdot_clock | d ln G_eff_obs/dt | NONCLAIM_BOUND_SCHEMA_FILLED |
| PPN_source_stability | Delta_PPN_abs includes source/readout/common-G products | NONCLAIM_BOUND_SCHEMA_FILLED |
| WEP_relative_source_tail | eta_AB | NONCLAIM_BOUND_SCHEMA_FILLED |
| R10_short_range | alpha_R10(lambda) | NONCLAIM_BOUND_SCHEMA_FILLED |
| Newton_source_calibration | Phi_N source coefficient | NONCLAIM_BOUND_SCHEMA_FILLED |
| clock_alpha_source_joint | clock drift | NONCLAIM_BOUND_SCHEMA_FILLED |

## Claim Ceiling

- no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass.
- This checkpoint reduces the coupling obstruction but does not close local GR.

## Next Target

- `4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md`
