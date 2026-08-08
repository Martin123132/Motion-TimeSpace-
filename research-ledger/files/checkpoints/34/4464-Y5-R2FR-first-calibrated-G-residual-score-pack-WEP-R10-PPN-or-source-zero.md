# 4464 - Y5/R2FR First Calibrated-G Residual Score Pack WEP R10 PPN Or Source Zero

Marker: `PPC4161_FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WEP_R10_PPN_OR_SOURCE_ZERO_4464`

Decision: `FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WRITTEN_R2_SCALAR_PRESSURED_SOURCE_ZERO_SELECTED_NONCLAIM`

## Result

4464 converts the calibrated-G local branch into an explicit residual score pack. This is the fair route: MTS does not need to predict the numerical value of Newton's constant today, but it is not allowed to hide species, range, time, frame, connection, scalar, orbital-source or EM leakage inside the calibrated `G` or fitted `GM`.

The useful new pressure is concrete. The clean branch survives as a conditional theorem branch, but the finite pure-R2 scalar branch is no longer vague: using the existing nonclaim review-candidate R10 curve near the current `lambda_R2` pressure, universal `alpha_eff=1/3` is pressured rather than silently safe. That pushes the next derivation toward a real zero/decoupling theorem for `c_R2_eff` or `C_matter`, while the coupling throat points to `Delta_C_AB=0` from source-charge universality.

## Bound Anchor Register

| anchor_id | arena | observable | bound_value | units | source_ref | source_status | extraction_method | theory_mapping | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BA4464_0_WEP_direct | MICROSCOPE_WEP | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_combined_rounded_from_stat_syst | direct geometry/WEP null row | False | MICROSCOPE Ti/Pt WEP result; maps only direct geometry/source test row, not a theorem-zero promotion |
| BA4464_1_WEP_source | MICROSCOPE_WEP | eta_WEP_source_charge | 2.8e-15 | dimensionless | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_combined_rounded_direct_WEP_proxy | source-charge proxy for Delta_C_AB product | False | Uses same WEP source as direct proxy; full source-normalization R1 channel remains retained |
| BA4464_2_clock | CLOCK_REDSHIFT | alpha_clock_redshift | 2.48e-05 | dimensionless | https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101 | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_fractional_redshift_deviation | clock/redshift source-frame row | False | Galileo eccentric satellites redshift/LPI test; clock row only |
| BA4464_3_gamma | PPN_LIGHT | gamma_minus_1 | 2.3e-05 | dimensionless | https://www.nature.com/articles/nature01997; doi:10.1038/nature01997 | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_Cassini_gamma | Cassini PPN gamma row | False | Cassini Shapiro/radio-link gamma result |
| BA4464_4_beta | PPN_ORBIT | beta_minus_1 | 7.8e-05 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_Messenger_planetary_fit_with_Cassini_gamma_prior | planetary/LLR PPN beta row | False | Will 2014 review reports beta-1=(-4.1 +/- 7.8)e-5 and Table 4 limit about 8e-5 |
| BA4464_5_alpha1 | PPN_PREFERRED_FRAME | alpha1 | 1e-04 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | SOURCE_BACKED_EMPIRICAL_BOUND | conservative_Table4_LLR_bound | preferred-frame alpha1 row | False | Will Table 4 gives 1e-4 LLR and 4e-5 PSR J1738+0333; conservative solar-system-compatible row uses 1e-4 |
| BA4464_6_alpha2 | PPN_PREFERRED_FRAME | alpha2 | 2e-09 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | SOURCE_BACKED_EMPIRICAL_BOUND | Table4_millisecond_pulsar_bound | preferred-frame alpha2 row | False | Will Table 4 alpha2 preferred-frame bound; strong-field caveat retained |
| BA4464_7_alpha3 | PPN_MOMENTUM_FLUX | alpha3 | 4e-20 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | SOURCE_BACKED_EMPIRICAL_BOUND | Table4_pulsar_Pdot_statistics_bound | momentum-flux alpha3 row | False | Will Table 4 alpha3 pulsar acceleration bound; ultratight exchange/flux lock |
| BA4464_8_xi | PPN_PREFERRED_LOCATION | xi | 4e-09 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | SOURCE_BACKED_EMPIRICAL_BOUND | Table4_millisecond_pulsar_bound | preferred-location xi row | False | Will Table 4 preferred-location xi bound; strong-field caveat retained |
| BA4464_9_Gdot | LLR_GDOT | Gdot_over_G | 9.6e-15 | yr^-1 | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | SOURCE_BACKED_EMPIRICAL_BOUND | 1sigma_LLR_current_result | time-drift of calibrated coupling row | False | LLR result Gdot/G0=(-5.0 +/- 9.6)e-15 yr^-1 |
| BA4464_10_R10_review_candidate_at_lambda_R2 | R10_YUKAWA_SHORT_RANGE | alpha_bound(lambda_R2_pressure) | 0.136485683105 | dimensionless_at_lambda_m | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | REVIEW_CANDIDATE_NONCLAIM_NOT_LIVE_CURVE | axis_calibrated_vector_path_extraction_from_fig5b1_pdf_review_candidate | nearest lambda=7.61999686401e-05 m to pressure lambda=7.63929980956e-05 m; \|C_matter\| <= 0.639888; alpha=1/3 pass=False | False | review candidate only; delta_lambda=1.93e-07 m; live_numeric_rows=0 |

## Residual Zero-Theorem Attempt

| residual_id | residual | exact_zero_condition | derivation_move | status | finite_fallback | primary_arena | bound_anchor_id | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RZ4464_0_delta_kappa | delta_kappa = D ln(kappa_eff) | topological/superselection kappa sector plus Hilbert source-measure descent gives D ln(kappa_* Z_H)=0 on the connected local domain | separate calibrated value from drift: numeric G may be fitted, but time/space variation cannot be hidden | CONDITIONAL_ZERO_IF_CONNECTED_SECTOR_AND_ZH_DESCENT_SIGNED | \|Gdot/G\| <= 9.6e-15 yr^-1 and spatial/frame drift rows | LLR_GDOT; clocks; orbital ephemerides | BA4464_9_Gdot | False |
| RZ4464_1_Delta_C_AB | Delta_C_AB = C_A - C_B | one adopted standard matter action, one Hilbert source, empty source-Hom, and source-label-forgetting for material composition | turn the coupling problem into a functorial no-extra-source-label theorem rather than a fitted material coefficient | PRIVATE_BRANCH_CONDITIONAL_ZERO_NOT_GLOBAL_PARENT_PROOF | \|Delta_C_AB*C_S*alpha_0*Y(lambda)\| <= 2.8e-15 | MICROSCOPE_WEP | BA4464_1_WEP_source | False |
| RZ4464_2_C_S | C_S - 1 or C_S source-normalization drift | the exterior source charge is the same Hamiltonian/Hilbert worldtube mass that appears in Poisson/Gauss/Newton | make source mass anti-circular: defined by H_tau/M_H before orbital GM readout | CONDITIONAL_ZERO_IF_WORLDTUBE_CHARGE_AND_BOUNDARY_SILENCE_SIGNED | WEP source response plus orbital/short-range source-charge rows | WEP; R10; orbital GM | BA4464_1_WEP_source | False |
| RZ4464_3_cD_qbar | c_D/qbar_geom shadow-frame or disformal source readout | ordinary matter, photons, clocks, rods and EM are functors of one observed coframe/metric with no second readout geometry | delete a whole family of PPN/WEP/clock leaks if the same-coframe selector is parent-owned | CONDITIONAL_ZERO_PRIVATE_SELECTOR | PPN gamma/beta/preferred-frame and clock redshift bounds | PPN_LIGHT; CLOCK_REDSHIFT | BA4464_3_gamma | False |
| RZ4464_4_DeltaGamma_WEP | DeltaGamma_WEP and connection-force leakage | connection is Levi-Civita of g_obs, or non-LC pieces are algebraic/source-silent and vanish for spinless local matter | force local acceleration to be geodesic/Newtonian instead of an independent connection force | CONDITIONAL_ZERO_IF_CONNECTION_OWNER_AND_TORSION_MARGIN_SIGNED | WEP, clocks and PPN residual vector | MICROSCOPE_WEP; PPN_LIGHT | BA4464_0_WEP_direct | False |
| RZ4464_5_alpha_R2 | alpha_eff(lambda_R2) finite curvature-scalar tail | c_R2_eff=0 by refinement/hinge owner theorem, or C_matter=0 by scalar/source decoupling | universal metric scalar gives alpha=1/3, so the clean route is a real zero/decoupling theorem, not wishful small coupling | FINITE_BRANCH_PRESSURED_BY_R10_REVIEW_CANDIDATE | alpha_eff = C_matter^2/3 <= alpha_bound(lambda_R2) | R10_YUKAWA_SHORT_RANGE; PPN_LIGHT; orbital inverse-square | BA4464_10_R10_review_candidate_at_lambda_R2 | False |
| RZ4464_6_epsilon_EM | epsilon_EM_extra_inner / standalone Poynting-background source | Maxwell-Hodge stress and Poynting flux are Hilbert-stress components on g_obs with radiative boundary routing | keep the Poynting intuition, but put it inside the stress tensor unless an extra parent coefficient is signed | FIXED_BRANCH_CONDITIONAL_ZERO_OPEN_RADIATIVE_REENTRY | EM side-channel coefficient and clock/source-energy rows | EM propagation; clocks; source energy accounting | BA4464_2_clock | False |
| RZ4464_7_PPN_preferred_frame | alpha1, alpha2, alpha3, xi preferred-frame/preferred-location tails | parent motion-frame gauge signature fixes local Lorentz/diffeomorphism structure without an extra local frame vector | A_MF-style frame closure converts preferred-frame rows into zero rows; otherwise they are brutally bounded | CONDITIONAL_ZERO_IF_A_MF_PARENT_SIGNATURE_SIGNED | alpha1<=1e-4, alpha2<=2e-9, alpha3<=4e-20, xi<=4e-9 | PPN preferred-frame/location | BA4464_5_alpha1;BA4464_6_alpha2;BA4464_7_alpha3;BA4464_8_xi | False |

## First Score Pack

| score_id | arena | branch | prediction_formula | required_theory_inputs | source_anchor | bound_value | branch_score_status | edge_dependency | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SP4464_0_clean_calibrated_GR | local_GR_Newton_clean_branch | same Hilbert source, constant calibrated G, LC connection, no scalar/frame/EM leakage | eta_AB=0; gamma-1=0; beta-1=0; Gdot/G=0; alpha(lambda)=0; orbital GM source-owned | source functor, kappa drift zero, connection owner, c_R2/C_matter zero, no shadow frame, EM-Hilbert routing | 4462/4463 local source-coupling and calibrated-G rows | not a finite bound row | THEOREM_CONDITIONAL_NOT_PUBLIC_CLAIM | parent selector signatures must be signed together | False | False |
| SP4464_1_WEP_species_source | MICROSCOPE_WEP | finite nonuniversal source charge | \|Delta_C_AB*C_S*alpha_0*(1+r/lambda)exp(-r/lambda)\| <= 2.8e-15 | Delta_C_AB, C_S, alpha_0, lambda or same-source zero theorem | BA4464_1_WEP_source | 2.8e-15 | BOUND_OPERATOR_READY_BUT_THEORY_VECTOR_MISSING | coupling/source universality is the most valuable next proof target | False | False |
| SP4464_2_R10_R2_scalar | R10_YUKAWA_SHORT_RANGE | finite pure-R2 scalar with pressure lambda_R2=76.39299809562831 um | alpha_eff=C_matter^2/3; universal C_matter=1 gives alpha=1/3; review-bound ratio=2.44226; \|C_matter\|<=0.639888 | c_R2_eff or c2 zero/finite value, C_matter, source-backed live alpha(lambda) curve | BA4464_10_R10_review_candidate_at_lambda_R2 | 0.136485683105 | UNIVERSAL_ALPHA_FAILS_REVIEW_CANDIDATE_PRESSURE | derive c_R2_eff=0, C_matter=0, screening, or a shorter/source-backed lambda | False | False |
| SP4464_3_PPN_gamma_beta | Cassini/planetary_PPN | frame/connection/scalar light-propagation residual | \|gamma-1\|<=2.3e-5; \|beta-1\|<=7.8e-5; scalar gamma(r)-1=-2 alpha_eff e^{-r/lambda}/(1+alpha_eff e^{-r/lambda}) | PPN projection matrix for DeltaGamma, c_D/qbar_geom, scalar tail and metric readout | BA4464_3_gamma;BA4464_4_beta | gamma=2.3e-05; beta=7.8e-05 | EMPIRICAL_ANCHORS_READY_PROJECTION_MATRIX_MISSING | PPN projection must be derived, not tuned after the fact | False | False |
| SP4464_4_Gdot_clock | LLR_GDOT_and_CLOCKS | time variation of calibrated coupling/source-frame readout | \|D_t ln kappa_eff\|<=9.6e-15 yr^-1; \|alpha_clock\|<=2.48e-5 | kappa/Z_H drift profile or topological zero, clock-source frame projection | BA4464_9_Gdot;BA4464_2_clock | Gdot=9.6e-15; clock=2.48e-05 | ANCHORS_READY_DRIFT_PROFILE_OR_ZERO_THEOREM_REQUIRED | calibrated G is allowed only if its drift residual is separately zero/bounded | False | False |
| SP4464_5_orbital_GM_source | orbital_GM_Newton_limit | source mass/GM readout absorption guard | Phi_N=-G_cal M_H^dress/r and a_r=-G_cal M_H^dress/r^2, with M_H defined before orbital fitting | H_tau/MHref worldtube mass, compact-exterior flux closure, no extra source charge | 4462 worldtube charge and Poisson/Newton rows | no numeric score until source mass projection is filled | THEORY_CONTRACT_READY_NUMERIC_SOURCE_PROJECTION_MISSING | prevents hiding coupling errors in fitted GM | False | False |

## Arena Score Status

| arena | current_readiness | score_ready | public_claim_ready | next_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| local_GR_Newton_clean_branch | THEOREM_CONDITIONAL_NOT_PUBLIC_CLAIM | False | False | parent selector signatures must be signed together | False |
| MICROSCOPE_WEP | BOUND_OPERATOR_READY_BUT_THEORY_VECTOR_MISSING | True | False | coupling/source universality is the most valuable next proof target | False |
| R10_YUKAWA_SHORT_RANGE | UNIVERSAL_ALPHA_FAILS_REVIEW_CANDIDATE_PRESSURE | False | False | derive c_R2_eff=0, C_matter=0, screening, or a shorter/source-backed lambda | False |
| Cassini/planetary_PPN | EMPIRICAL_ANCHORS_READY_PROJECTION_MATRIX_MISSING | True | False | PPN projection must be derived, not tuned after the fact | False |
| LLR_GDOT_and_CLOCKS | ANCHORS_READY_DRIFT_PROFILE_OR_ZERO_THEOREM_REQUIRED | True | False | calibrated G is allowed only if its drift residual is separately zero/bounded | False |
| orbital_GM_Newton_limit | THEORY_CONTRACT_READY_NUMERIC_SOURCE_PROJECTION_MISSING | False | False | prevents hiding coupling errors in fitted GM | False |

## Decision Ledger

| decision_id | finding | consequence | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC4464_0_score_result | calibrated G is fair only if residual coupling channels are theorem-zero or explicitly bounded | the local problem is now a residual vector, not a vague missing-coupling complaint | 4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | False |
| DEC4464_1_coupling_priority | the strongest route is to prove same-Hilbert/source-label-forgetting so WEP source charge vanishes | one proof can close Delta_C_AB, much of C_S, and a large chunk of fitted-G absorption risk | attack source-charge universality before chasing many isolated numeric bounds | False |
| DEC4464_2_R2_pressure | the universal metric R2 scalar at the current pressure lambda is not safe under the review-candidate R10 curve | finite c2 needs a parent zero/decoupling/shorter-range derivation or a source-backed revised curve | keep R10 as pressure, not claim, while deriving c_R2_eff=0 or C_matter=0 | False |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | detail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4464_0_sources | all local source files exist and cited needles are found | True | False | source register validates local handoff and bound files | False |
| CG4464_1_bound_anchors | WEP, clock, PPN, Gdot and R10 anchors are registered | True | False | empirical anchors are source-backed where possible; R10 remains review-candidate/nonclaim | False |
| CG4464_2_zero_theorem_attempt | residual zero theorem clauses are explicit | True | False | zero clauses are conditional; finite fallbacks are kept | False |
| CG4464_3_score_pack | first calibrated-G residual score pack is written | True | False | score pack separates clean theorem branch, WEP, R10, PPN, drift/clock and orbital source branches | False |
| CG4464_4_R10_pressure | universal R2 alpha=1/3 is not silently treated as safe | True | False | R10 status: nearest lambda=7.61999686401e-05 m to pressure lambda=7.63929980956e-05 m; \|C_matter\| <= 0.639888; alpha=1/3 pass=False | False |
| CG4464_5_public_local_GR | public local-GR/Newton pass is allowed | False | False | conditional clean branch exists but source, frame, scalar and projection signatures are not globally signed | False |
| CG4464_6_no_generated_claim_rows | no generated row is promoted to claim evidence | True | False | all 4464 rows remain private nonclaim | False |

## Decision

| checkpoint | marker | claim_id | decision | score_result | strongest_pressure | best_next_route | public_local_GR_claim | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4464 | PPC4161_FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WEP_R10_PPN_OR_SOURCE_ZERO_4464 | L-306 | FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WRITTEN_R2_SCALAR_PRESSURED_SOURCE_ZERO_SELECTED_NONCLAIM | first residual score pack separates clean theorem branch from finite WEP/R10/PPN/Gdot/clock/orbital branches | universal R2 scalar alpha=1/3 is pressured by the review-candidate R10 curve near lambda_R2 pressure | prove source-charge universality/Delta_C_AB=0 or run a WEP material vector rather than hiding residuals in calibrated G | False | 4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | False | 2026-07-05T18:00:26+00:00 |

## Status

| checkpoint | marker | claim_id | decision | calibrated_G_policy | residual_score_pack | R10_scalar_status | selected_next_target | public_local_GR_claim | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4464 | PPC4161_FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WEP_R10_PPN_OR_SOURCE_ZERO_4464 | L-306 | FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WRITTEN_R2_SCALAR_PRESSURED_SOURCE_ZERO_SELECTED_NONCLAIM | allowed_as_GR_parity_calibration | written_nonclaim | review_candidate_pressure_not_live_claim | 4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | False | False | 2026-07-05T18:00:26+00:00 |

## Next Target

| next_id | target | objective | derive_first | fallback | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4464_0 | 4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | Attack the coupling throat directly: prove same-Hilbert/source-label-forgetting gives Delta_C_AB=0, or build the first WEP material vector runner. | derive C_A=C_B from one matter action, one Hilbert source, no source-Hom, source-label-forgetting and worldtube source normalization | fill a source-backed material vector for Ti/Pt or nearest MICROSCOPE composition proxy and score the finite product against eta<=2.8e-15 | treating calibrated G as if it hides species/source coupling; relying on R10 candidate curve before live promotion | False |

## Source Register

| checkpoint | source_id | source_kind | source_ref | local_path_exists | needle | needle_found | line_number | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4464 | SRC4464_00_next4463 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4463_NEXT_TARGET.csv | True | 4464-Y5-R2FR-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md | True | 2 | 4463 selected the calibrated-G residual score pack. | False |
| 4464 | SRC4464_01_formal479 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\479-PPC4161-parent-kappa-scale-law-or-calibrated-G-residual-runner.md | True | local competitiveness does not require numeric G prediction | True | 53 | calibrated-G policy and residual runner handoff. | False |
| 4464 | SRC4464_02_runner4463 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4463_CALIBRATED_G_RESIDUAL_RUNNER.csv | True | CGR4463_3_species_charge_WEP | True | 5 | residual branches staged by 4463. | False |
| 4464 | SRC4464_03_source4462 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\478-PPC4161-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md | True | eta_AB ~= (C_A-C_B) | True | 27 | source-coupling WEP response operator. | False |
| 4464 | SRC4464_04_scalaron4461 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md | True | lambda_bound_um=76.39299809562831 | True | 36 | current pure-R2 pressure lambda used for R10 smoke pressure. | False |
| 4464 | SRC4464_05_local_bounds | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | MICROSCOPE_final_TiPt | True | 2 | WEP, clock, PPN, Gdot and symbolic R10 local bound anchors. | False |
| 4464 | SRC4464_06_r10_live_placeholder | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | MISSING_DIGITIZED_ALPHA_BOUND | True | 2 | live claim curve remains blocked/placeholder. | False |
| 4464 | SRC4464_07_r10_review_candidate | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve | True | 2 | review-candidate numeric curve for nonclaim smoke pressure only. | False |
| 4464 | SRC4464_08_gate | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\calibrated_G_residual_score_gate.py | True | def first_score_pack_rows | True | 237 | 4464 residual score gate. | False |
| 4464 | SRC4464_09_generator | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_4464_first_calibrated_G_residual_score_pack_WEP_R10_PPN_or_source_zero.py | True | CHECKPOINT = "4464" | True | 32 | 4464 generator script. | False |
