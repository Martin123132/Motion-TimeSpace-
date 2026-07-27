# 3665 - Solar metal mixture expansion or unique-F2 closure

**Status:** 3665 keeps f_EM live, expands the AGSS09 listed metal mixture, and produces a complete nonclaim solar B_source_EM proxy row for the EM/gamma branch.

**Claim ceiling:** no f_EM zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed.

## Main result

The unique-`F^2` route still does not close: an independent scalar gauge-kinetic term `f_X(X_N)F_Q^2` remains legal unless a future parent theorem explicitly bans it.

The concrete advance is source-side: the solar metal term that blocked 3664 is now expanded into a numeric AGSS09 listed-metal proxy, normalized to bulk `Z=0.0142`, then combined with the existing H/He row.

`solar_B_source_EM_total = 8.256508261034e-05`.

`solar_B_source_EM_metals_proxy = 1.763554325283e-05`.

This is deliberately nonclaim: it is a source-composition scalar, not a completed gamma/local-GR/PPN pass.

## Unique-F2 closure audit
- `UF23665_0_target_theorem`: NO - `S_EM=-(C_P/4) int mu_obs <F_QT_Q,F_QT_Q>_P ; forbid DeltaS=-(1/4)int mu_obs f_X(X_N)F_Q^2`
- `UF23665_1_counterexample`: NO - `DeltaL = -(1/4) f_X(X_N) F_Q^2`
- `UF23665_2_possible_closure_contract`: NO_PARENT_SIGNATURE_FOUND - `Dq(v_X)=0 and delta_X C_P=0 and Hom(hidden residual scalars, visible F_Q^2)=0`
- `UF23665_3_verdict`: REJECT_ZERO_RETAIN_FINITE_COUPLING_INPUT - `f_EM retained; Q_X^EM_solar = B_source_EM_solar * f_EM`

## Solar metal basis
- Method: `AGSS09_LISTED_METAL_PROXY_NORMALIZED_TO_BULK_Z_NONCLAIM`.
- Listed metal rows: `28`; normalized metal mass-fraction sum: `1.420000000000e-02`.
- Largest EM-source contributors in the proxy:
  - `O`: mass_fraction=`6.088612514659e-03`, B_A_EM=`1.060279587079e-03`, contribution=`6.455631562925e-06`
  - `Fe`: mass_fraction=`1.372175917316e-03`, B_A_EM=`2.324290751276e-03`, contribution=`3.189335793742e-06`
  - `C`: mass_fraction=`2.511913410744e-03`, B_A_EM=`8.324762583379e-04`, contribution=`2.091108277445e-06`
  - `Ne`: mass_fraction=`1.334586291240e-03`, B_A_EM=`1.250365891252e-03`, contribution=`1.668721177498e-06`
  - `Si`: mass_fraction=`7.061548167300e-04`, B_A_EM=`1.627277582145e-03`, contribution=`1.149109902788e-06`
  - `Mg`: mass_fraction=`7.518325478998e-04`, B_A_EM=`1.431097605737e-03`, contribution=`1.075945759214e-06`
  - `N`: mass_fraction=`7.358183704816e-04`, B_A_EM=`9.494642347725e-04`, contribution=`6.986332260608e-07`
  - `S`: mass_fraction=`3.283893133671e-04`, B_A_EM=`1.798661237957e-03`, contribution=`5.906611289126e-07`

## Solar BsourceEM total rows
- `SOL3665_0_H`: `H` B=`0.000000000000e+00` contribution=`0.000000000000e+00` - SOURCE_BACKED_NUMERIC_NONCLAIM
- `SOL3665_1_He`: `He` B=`2.402128722068e-04` contribution=`6.492953935751e-05` - SOURCE_BACKED_NUMERIC_NONCLAIM
- `SOL3665_2_metals_listed_proxy`: `listed_metals_normalized_to_Z` B=`1.241939665692e-03` contribution=`1.763554325283e-05` - COMPLETE_LISTED_METAL_PROXY_NONCLAIM
- `SOL3665_3_solar_B_source_EM_total`: `H_plus_He_plus_listed_metals_proxy` B=`8.256508261034e-05` contribution=`8.256508261034e-05` - SOLAR_B_SOURCE_EM_TOTAL_PROXY_COMPLETE_NONCLAIM_NOT_SCORE_READY

## Gamma/EM status
- `GEM3665_0_inserted_solar_source_scalar`: SOURCE_COMPOSITION_SCALAR_FILLED_AS_PROXY_NONCLAIM - missing: f_EM; Z_X; lambda_X; k_H; k_G; gamma kernel; parent profile normalization
- `GEM3665_1_gamma_envelope`: EXECUTABLE_SOURCE_INSERTION_READY_BUT_COUPLING_PROFILE_BLOCKED - missing: f_EM; Z_X; lambda_X; k_H; k_G; gamma kernel
- `GEM3665_2_fEM_zero_route`: REJECTED_FOR_NOW_COUNTERTERM_LIVE - missing: signed parent unique-F2/no-f_XF2 theorem

## Claim gates
- `CG3665_0_unique_F2_zero`: FAILED_UNSIGNED_COUNTERTERM_LIVE - f_EM zero from unique-F2 closure
- `CG3665_1_metal_basis`: PASSED_PROXY_FILL_NONCLAIM - AGSS09 listed metal basis expanded
- `CG3665_2_solar_total`: PASSED_PROXY_TOTAL_NONCLAIM - solar B_source_EM total filled
- `CG3665_3_gamma_score`: BLOCKED_BY_COUPLING_PROFILE_INPUTS - Cassini/gamma score readiness
- `CG3665_4_no_public_claim`: ACTIVE_GUARD - no local-GR or PPN/local-source claim

## Next checkpoint

`3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md` via `scripts/Y5_R2FR_3666_solar_EM_gamma_envelope_stub_or_fEM_profile_inputs.py`.

## Sources
- `handoff_3664`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3664_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3664`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3664-Y5-R2FR-unique-F2-parent-proof-or-solar-BsourceEM-first-row.md` exists=True needle_found=True
- `uniqueF2_3664`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3664_UNIQUE_F2_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `solar_3664`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3664_SOLAR_BSOURCEEM_ROWS.csv` exists=True needle_found=True
- `doc_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md` exists=True needle_found=True
- `audit_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv` exists=True needle_found=True
- `external_AGSS09_bulk_and_metals`: `Asplund, Grevesse, Sauval, Scott 2009 solar composition; bulk X=0.7154,Y=0.2703,Z=0.0142; Table 1 log-epsilon metal basis; https://arxiv.org/abs/0909.0948` exists=True needle_found=True
- `external_SEMF_coulomb_term`: `semi_empirical_mass_formula_convention; Coulomb term E_C=a_C Z(Z-1) A^(-1/3), a_C=0.711 MeV; https://en.wikipedia.org/wiki/Semi-empirical_mass_formula` exists=True needle_found=True
- `external_CIAAW_atomic_weights`: `CIAAW/IUPAC standard atomic weights used as A_effective proxies; https://www.ciaaw.org/atomic-weights.htm` exists=True needle_found=True
