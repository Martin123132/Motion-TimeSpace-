# 3678 - Canonical EM/Poynting transfer leg or s_EM bound

**Status:** SEM_TRANSFER_DECOMPOSED_POYNTING_STANDARD_STRESS_SEPARATED_NONCLAIM

This checkpoint makes the Poynting point precise: ordinary Maxwell/Poynting stress is real source stress, but it is already inside the total Hilbert source `T_total` and source charge `M_H`. The tested MTS leg is only the **extra vertical EM transfer** after that standard accounting.

## Main result

`s_EM = f_EM/sqrt(Z_X)` is not standard EM energy. It is the canonical coefficient for extra EM/source response to the local MTS field `X_hat`.

The private no-cancellation envelope is:

`s_EM = s_Hodge + s_XF2 + s_wEM + s_J + s_alpha_source + s_boundary_flux + s_readout + s_nonHilbert`

`|s_EM| <= sum_i |s_i|`.

Under the 3677 `|g_FXR|<=1` smoke prior: `under |g_FXR|<=1, |s_EM| must be <= 2.979212325428e-05; an equal 8-leg no-cancellation budget gives each active component <= 3.724015406785e-06`.

## Decomposition
- `SEM3678_0_definition`: DERIVED_FROM_3677_CANONICAL_PAIR - s_EM -> defines the tested transfer leg in xi_FXR=|g_FXR*s_EM|
- `SEM3678_1_minimal_poynting`: CONDITIONAL_ZERO_FOR_EXTRA_TRANSFER - ordinary minimal Maxwell/Poynting stress -> prevents double-counting ordinary EM energy as an MTS fifth-force leg
- `SEM3678_2_extra_transfer_law`: DECOMPOSITION_DERIVED_AS_ACCOUNTING_IDENTITY - canonical residual envelope -> turns the vague coupling into an executable no-cancellation vector
- `SEM3678_3_no_cancellation`: NO_CANCELLATION_GUARD - absolute envelope -> makes future tests falsifiable without hiding behind cancellations

## Zero theorem audit
- `EMZ3678_0_same_observed_hodge`: CONDITIONAL_STANDARD_FORM_NOT_PARENT_SIGNED - same observed Hodge/coframe -> s_Hodge may remain finite
- `EMZ3678_1_unique_F2_no_XF2`: NOT_DERIVED_CORE_COUPLING_TARGET - no independent F(X)F^2 or lambda_F2 -> s_XF2 remains finite
- `EMZ3678_2_no_independent_wEM`: NOT_PARENT_SIGNED - no EM action/stress multiplier -> s_wEM remains finite
- `EMZ3678_3_charge_current_owner`: SOURCE_CURRENT_OWNER_UNSIGNED - same charge/current owner -> s_J and s_alpha_source remain finite
- `EMZ3678_4_stationary_poynting_boundary`: NOT_PARENT_SIGNED - no radiative/background Poynting flux -> s_boundary_flux remains finite
- `EMZ3678_5_readout_radiative_closure`: UNSIGNED_PRESERVATION_REQUIREMENT - readout/radiative closure -> s_readout remains finite
- `EMZ3678_6_total_Hilbert_no_bypass`: CONDITIONAL_CLOSURE_NOT_SIGNED - no non-Hilbert/improvement source bypass -> s_nonHilbert remains finite
- `EMZ3678_7_verdict`: THEOREM_NOT_PROVED_CURRENT_CORPUS - s_EM theorem-zero -> s_EM is bounded/decomposed, not claimed zero

## Component rows
- `SCB3678_0_s_Hodge`: `s_Hodge` - MISSING_NUMERIC_OR_THEOREM_ZERO; target: abs(s_Hodge) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_1_s_XF2`: `s_XF2` - MISSING_PARENT_EXCLUSION_OR_BOUND; target: abs(s_XF2) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_2_s_wEM`: `s_wEM` - MISSING_UNIQUE_F2_OR_ALPHA_OWNER; target: abs(s_wEM) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_3_s_J`: `s_J` - MISSING_CHARGE_CURRENT_OWNER_OR_BOUND; target: abs(s_J) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_4_s_alpha_source`: `s_alpha_source` - MISSING_SOURCE_TEST_PROJECTION_OR_BOUND; target: abs(s_alpha_source) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_5_s_boundary_flux`: `s_boundary_flux` - MISSING_STATIONARY_FLUX_ZERO_OR_BOUND; target: abs(s_boundary_flux) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_6_s_readout`: `s_readout` - MISSING_READOUT_RADIATIVE_CLOSURE_OR_BOUND; target: abs(s_readout) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation
- `SCB3678_7_s_nonHilbert`: `s_nonHilbert` - MISSING_TOTAL_HILBERT_CLOSURE_OR_BOUND; target: abs(s_nonHilbert) <= 3.724015406785e-06 under equal 8-leg no-cancellation allocation

## Target allocations
- `ALLOC3678_0_O1_gFXR`: target `2.979212325428e-05`, equal component budget `3.724015406785e-06` under |g_FXR|<=1
- `ALLOC3678_1_4pi_gFXR`: target `2.370781840561e-06`, equal component budget `2.963477300701e-07` under |g_FXR|<=4pi

## Decisions
- `DEC3678_0_minimal_EM_not_sEM`: STANDARD_STRESS_INSIDE_HILBERT_SOURCE - ordinary Maxwell/Poynting energy is not the extra s_EM leg -> avoid double-counting standard EM energy as fifth-force/source hair
- `DEC3678_1_sEM_decomposition`: PROMOTED_TO_BOUND_VECTOR - s_EM has an executable canonical residual vector -> future work can derive/zero/bound components one at a time
- `DEC3678_2_core_next`: NEXT_BEST_TARGET - attack C_XF2/lambda_F2 first -> derive unique-F2/no-XF2 theorem or source an alpha/WEP/clock bound for s_XF2
- `DEC3678_3_claim_discipline`: BLOCKED_NONCLAIM - no Maxwell/local-GR claim -> keep private until a component theorem-zero or source-backed numeric row closes

## Claim gates
- `CG3678_0_sEM_zero`: BLOCKED_NONCLAIM - claim s_EM=0 because EMZ3678_7 theorem-zero verdict is not proved
- `CG3678_1_sEM_numeric`: BLOCKED_COMPONENT_VALUES_MISSING - score finite s_EM because component rows have MISSING_COMPONENT_VALUE
- `CG3678_2_poynting_claim`: BLOCKED_OVERCOUNT_GUARD - claim Poynting route proves source coupling because ordinary Poynting is in Hilbert stress, but extra vertical transfer channels remain
- `CG3678_3_local_GR`: BLOCKED_NONCLAIM - claim local-GR/PPN pass because source coupling and EM transfer owner clauses remain unsigned
- `CG3678_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private derivation checkpoint only

## Next target
`3679-Y5-R2FR-unique-F2-no-XF2-theorem-or-sXF2-bound.md` via `scripts/Y5_R2FR_3679_unique_F2_no_XF2_theorem_or_sXF2_bound.py`.

## Sources
- `handoff_3677`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3677_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3677`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3677-Y5-R2FR-cFXR-parent-normalization-scale-or-local-generator-elimination.md` exists=True needle_found=True
- `implications_3677`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3677_BOUND_IMPLICATION_ROWS.csv` exists=True needle_found=True
- `poynting_3463`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv` exists=True needle_found=True
- `single_current_3463`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3463_SINGLE_SOURCE_CURRENT_AUDIT.csv` exists=True needle_found=True
- `owner_3465`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv` exists=True needle_found=True
- `hodge_3504`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Hodge_flow_rule_bound_or_zero.csv` exists=True needle_found=True
- `em_bound_vector_3503`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv` exists=True needle_found=True
- `scalar_coupling_3507`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_scalar_coupling_owner_alpha_residual.csv` exists=True needle_found=True
- `source_current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `charge_current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv` exists=True needle_found=True
- `doc_3620`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md` exists=True needle_found=True
- `status_3620`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_EM_source_coupling_owner_status.csv` exists=True needle_found=True
