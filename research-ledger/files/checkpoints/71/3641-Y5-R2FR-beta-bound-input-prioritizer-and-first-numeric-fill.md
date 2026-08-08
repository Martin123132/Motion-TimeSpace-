# 3641 Y5 R2FR beta bound input prioritizer and first numeric fill

**Status:** 3641 fills the first source-backed observational seeds for beta_common: Cassini PPN gamma, LLR Gdot/G, and Eot-Wash/R10 short-range lambda anchor. No beta_common pass is claimed because Xdot_N, C_gamma, alpha(lambda), K_X, M_X^2, and tau_R10 remain parent/MTS inputs.

**Claim ceiling:** no beta_common bound, local-GR/Newton pass, PPN pass, Gdot pass, or R10 pass is allowed from 3641.

## What moved

This checkpoint puts real observational numbers under the `beta_common` arena map without pretending the MTS parent coefficients are known. Cassini seeds the PPN channel, LLR seeds the local drift channel, and Eot-Wash seeds the R10 short-range channel as an anchor only.

## Observational seeds

- `OBS3641_0_cassini_gamma`: `PPN_local_GR` `gamma_minus_one` limit seed `2.3e-05` `dimensionless` from https://pubmed.ncbi.nlm.nih.gov/14508481/.
- `OBS3641_1_llr_gdot`: `Gdot_clock` `dG_over_G_dt` limit seed `9e-13` `yr^-1` from https://arxiv.org/abs/gr-qc/0411113 ; https://pubmed.ncbi.nlm.nih.gov/15697965/.
- `OBS3641_2_eotwash_lambda_anchor`: `R10_short_range` `lambda_min_tested` limit seed `5.2e-05` `m` from https://link.aps.org/doi/10.1103/PhysRevLett.124.101101 ; https://www.npl.washington.edu/eotwash/inverse-square-law.

## Prioritizer

- Rank 1 `Gdot_clock`: has a direct source-normalization drift seed with units yr^-1; only needs Xdot_N/existing time profile before a beta_common inequality is executable
- Rank 2 `PPN_local_GR`: Cassini gamma seed exists and directly pressures local-GR reduction; needs PPN projection coefficient C_PPN
- Rank 3 `R10_short_range`: strong short-range empirical anchor exists, but full alpha(lambda) curve and MTS K_X/M_X/tau_R10 inputs are still needed
- Rank 4 `orbital_radial`: important for Newtonian inverse-square recovery but needs an MTS local radial profile before public residuals can bite
- Rank 5 `source_WEP_null_guard`: not a beta_common bound because common-mode coupling cancels from differential WEP

## First-fill rows

- `FILL3641_0_gdot_beta_bound_seed`: |beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|Xdot_N| | status `OBSERVATIONAL_NUMERIC_SEED_FILLED_PARENT_INPUTS_MISSING`.
- `FILL3641_1_ppn_gamma_beta_bound_seed`: |beta_common| <= sqrt(2.3e-5/|C_gamma|) if derivative terms are zero or separately bounded | status `OBSERVATIONAL_NUMERIC_SEED_FILLED_PARENT_INPUTS_MISSING`.
- `FILL3641_2_r10_lambda_anchor_seed`: |beta_common(lambda)| <= sqrt(|alpha_bound(lambda)| M_X^2/(|K_X tau_R10(lambda)|)) | status `ANCHOR_FILLED_FULL_CURVE_AND_PARENT_INPUTS_MISSING`.

## Scoreability

- `SCORE3641_0_no_beta_claim`: no — observational limits are now seeded, but every beta_common inequality still needs at least one parent coefficient/profile input
- `SCORE3641_1_best_next`: Xdot_N local time profile, then C_gamma PPN projection — Gdot has the cleanest dimensional seed; PPN has the cleanest GR-reduction pressure

## Next target

`3642-Y5-R2FR-local-XN-profile-and-PPN-projection-coefficient.md` via `scripts/Y5_R2FR_3642_local_XN_profile_and_PPN_projection_coefficient.py`.

## Sources

- `next_3640`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3640_NEXT_TARGET.csv` exists=True needle_found=True
- `bounds_3640`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3640_BETA_COMMON_BOUND_INVERSION_ROWS.csv` exists=True needle_found=True
- `ward_3640`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3640_WARD_IDENTITY_DERIVATION.csv` exists=True needle_found=True
- `cassini_gamma_pubmed`: `https://pubmed.ncbi.nlm.nih.gov/14508481/` exists=True needle_found=True
- `llr_gdot_arxiv`: `https://arxiv.org/abs/gr-qc/0411113` exists=True needle_found=True
- `llr_gdot_pubmed`: `https://pubmed.ncbi.nlm.nih.gov/15697965/` exists=True needle_found=True
- `eotwash_2020_prl`: `https://link.aps.org/doi/10.1103/PhysRevLett.124.101101` exists=True needle_found=True
- `eotwash_inverse_square_page`: `https://www.npl.washington.edu/eotwash/inverse-square-law` exists=True needle_found=True
