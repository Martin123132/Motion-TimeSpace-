# 3336 - PPN dominant-floor source acquisition or derivation under AX1090

Run UTC: `2026-06-28T01:43:00.647834+00:00`

## Verdict

3336 replaces one placeholder with a real source-backed candidate and turns the dominant floors into exact acquisition contracts.

The threshold candidate is Cassini's PPN gamma result:

`gamma - 1 = (2.1 ± 2.3)e-5`.

For private steering, this checkpoint uses `B_gamma_candidate=2.30e-05` as a gamma-slot candidate only. It is not a full PPN vector and not a local-GR pass.

Reranking the 3335 reduced smoke grid with that candidate gives `5` pass-like and `4` fail-like nonclaim scenarios.

The harsh response-product contract is now concrete:

`epsilon_eff_PPN <= sqrt(0.30 B_gamma/(A_PPN C_metric)) = 2.627e-09` for `A_PPN C_metric=1e12`.

The composite budget contract is also concrete:

`epsilon_composite_PPN <= 0.30 B_gamma = 6.900e-06`.

For a reference `sigma_Dpi=1e-3`, the commutator ceiling is

`delta_comm_PPN <= 6.900e-03`

before reserving other composite floors.

So the next best derivation is not broad cosmology or a new field. It is the boring-but-decisive PPN projector/smoothing commutator and contact scaling theorem.

No PPN/local-GR pass is claimed.

## Local Source Register

- `LSRC3336_0_3335_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3335-Y5-R2FR-PPN-composite-tree-envelope-first-numeric-nonclaim-under-AX1090.md` exists=true parse_ok=true role=dominant floor handoff
- `LSRC3336_1_3335_envelope`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv` exists=true parse_ok=true role=dominant term ranking from reduced smoke envelope
- `LSRC3336_2_3335_inputs`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3335_REQUIRED_SOURCE_INPUTS.csv` exists=true parse_ok=true role=missing real threshold, response, epsilon, composite, Gamma inputs
- `LSRC3336_3_3332_epsilon`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv` exists=true parse_ok=true role=tree epsilon_eff formula
- `LSRC3336_4_3332_composite`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv` exists=true parse_ok=true role=composite contact/commutator formula
- `LSRC3336_5_3331_appn`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3331_APPN_BOUND.csv` exists=true parse_ok=true role=A_PPN response formulas
- `LSRC3336_6_3331_cmetric`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3331_CMETRIC_BOUND.csv` exists=true parse_ok=true role=C_metric operator formulas
- `LSRC3336_7_3334_budget`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3334_UPDATED_REDUCED_PPN_BUDGET.csv` exists=true parse_ok=true role=Gamma-fork reduced PPN budget

## Web Source Register

- `WSRC3336_0_Cassini_Nature`: A test of general relativity using radio links with the Cassini spacecraft; url=https://pubmed.ncbi.nlm.nih.gov/14508481/; doi=10.1038/nature01997; role=primary Cassini PPN gamma source; candidate=gamma-1=(2.1±2.3)e-5
- `WSRC3336_1_Will_LRR`: The Confrontation between General Relativity and Experiment; url=https://link.springer.com/article/10.12942/lrr-2014-4; doi=10.12942/lrr-2014-4; role=review source for PPN gamma/beta context; candidate=Cassini gamma and reviewed beta/PPN constraints

## PPN Threshold Candidates

- `PPN3336_0_gamma_Cassini_1sigma`: observable=PPN gamma; source_id=WSRC3336_0_Cassini_Nature; source_value=gamma-1=(2.1±2.3)e-5; working_bound=2.300000e-05; bound_type=one_sigma_candidate_not_full_vector; use=replace B_PPN_smoke for gamma-slot sensitivity only; valid_for_claim=false
- `PPN3336_1_gamma_Cassini_abs_central_plus_sigma`: observable=PPN gamma; source_id=WSRC3336_0_Cassini_Nature; source_value=|2.1e-5|+2.3e-5; working_bound=4.400000e-05; bound_type=conservative_abs_central_plus_sigma_candidate; use=looser sanity check, not used as pass claim; valid_for_claim=false
- `PPN3336_2_beta_review_working`: observable=PPN beta; source_id=WSRC3336_1_Will_LRR; source_value=reviewed beta constraints; working envelope only; working_bound=1.200000e-04; bound_type=review_working_candidate; use=do not use until beta projection is separately sourced; valid_for_claim=false

## Dominant Floor Rerank

- `ENV3335_0_clean_lambda`: dominant_term=epsilon_composite; R_total=1.000003e-12; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=true; tree_residual=4.000008e-30; epsilon_composite=1.000003e-12; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_1_long_mode_harsh_survives`: dominant_term=tree_residual; R_total=1.004005e-06; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=true; tree_residual=1.004004e-06; epsilon_composite=1.000003e-12; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_2_equal_smoothing_tree_fail`: dominant_term=tree_residual; R_total=3.678819e-01; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=false; tree_residual=3.678819e-01; epsilon_composite=1.000003e-12; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_3_contact_composite_fail`: dominant_term=epsilon_composite; R_total=1.000000e-04; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=false; tree_residual=4.000008e-30; epsilon_composite=1.000000e-04; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_4_open_Gamma_fail`: dominant_term=R_Gamma; R_total=1.000000e-04; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=false; tree_residual=1.004004e-12; epsilon_composite=1.000003e-12; R_Gamma=1.000000e-04; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_5_Ksolar_clean`: dominant_term=tree_residual; R_total=1.004006e-12; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=true; tree_residual=1.004004e-12; epsilon_composite=2.011001e-18; R_Gamma=1.000000e-122; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_6_boundary_large_response`: dominant_term=tree_residual; R_total=1.030103e-06; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=true; tree_residual=1.020100e-06; epsilon_composite=1.000300e-08; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_7_boundary_harsh_fail`: dominant_term=tree_residual; R_total=1.020100e+00; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=false; tree_residual=1.020100e+00; epsilon_composite=1.000300e-08; R_Gamma=1.281458e-30; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false
- `ENV3335_8_commutator_warning`: dominant_term=epsilon_composite; R_total=1.000060e-07; B_gamma_Cassini_candidate=2.300000e-05; candidate_pass_like=true; tree_residual=1.004004e-12; epsilon_composite=1.000050e-07; R_Gamma=1.281458e-26; source_status=RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM; valid_for_claim=false

## Tree Epsilon Bound Contract

- `TREE3336_resp_1e+00`: quantity=epsilon_eff_PPN; A_PPN_times_Cmetric=1.000000e+00; full_gamma_slot_allowance=4.795832e-03; tree_partition_allowance=2.626785e-03; formula=epsilon_eff <= sqrt(f_tree B_gamma/(A_PPN C_metric)); derivation_status=EXACT_FROM_REDUCED_BUDGET_AND_CASSINI_CANDIDATE; still_needed=source-bound A_PPN*C_metric and derive epsilon_bg*T_grad + boundary + anisotropy; valid_for_claim=false
- `TREE3336_resp_1e+06`: quantity=epsilon_eff_PPN; A_PPN_times_Cmetric=1.000000e+06; full_gamma_slot_allowance=4.795832e-06; tree_partition_allowance=2.626785e-06; formula=epsilon_eff <= sqrt(f_tree B_gamma/(A_PPN C_metric)); derivation_status=EXACT_FROM_REDUCED_BUDGET_AND_CASSINI_CANDIDATE; still_needed=source-bound A_PPN*C_metric and derive epsilon_bg*T_grad + boundary + anisotropy; valid_for_claim=false
- `TREE3336_resp_1e+12`: quantity=epsilon_eff_PPN; A_PPN_times_Cmetric=1.000000e+12; full_gamma_slot_allowance=4.795832e-09; tree_partition_allowance=2.626785e-09; formula=epsilon_eff <= sqrt(f_tree B_gamma/(A_PPN C_metric)); derivation_status=EXACT_FROM_REDUCED_BUDGET_AND_CASSINI_CANDIDATE; still_needed=source-bound A_PPN*C_metric and derive epsilon_bg*T_grad + boundary + anisotropy; valid_for_claim=false
- `TREE3336_resp_1e+16`: quantity=epsilon_eff_PPN; A_PPN_times_Cmetric=1.000000e+16; full_gamma_slot_allowance=4.795832e-11; tree_partition_allowance=2.626785e-11; formula=epsilon_eff <= sqrt(f_tree B_gamma/(A_PPN C_metric)); derivation_status=EXACT_FROM_REDUCED_BUDGET_AND_CASSINI_CANDIDATE; still_needed=source-bound A_PPN*C_metric and derive epsilon_bg*T_grad + boundary + anisotropy; valid_for_claim=false
- `TREE3336_boundary_zero_attempt`: quantity=boundary/aniso silence; A_PPN_times_Cmetric=symbolic; full_gamma_slot_allowance=; tree_partition_allowance=; formula=epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0 if the PPN patch is interior, isotropic, and the smoothing kernel commutes with the PPN projector; derivation_status=CONDITIONAL_ZERO_ATTEMPT; still_needed=prove PPN projection/kernel commutator is zero or bound it; valid_for_claim=false
- `TREE3336_gradient_suppression_attempt`: quantity=background gradient leakage; A_PPN_times_Cmetric=symbolic; full_gamma_slot_allowance=; tree_partition_allowance=; formula=epsilon_bg_PPN T_grad(lambda_PPN) <= sqrt(f_tree B_gamma/(A_PPN C_metric)) - epsilon_boundary - epsilon_kernel_aniso; derivation_status=ACQUISITION_CONTRACT; still_needed=ell_s/lambda_PPN, epsilon_bg_PPN, and local boundary/aniso bounds; valid_for_claim=false

## Composite Contact Commutator Contract

- `COMP3336_0_total_budget`: quantity=epsilon_composite_PPN; formula=epsilon_composite <= f_comp B_gamma; candidate_bound=6.900000e-06; derivation_status=BUDGET_PARTITION_FROM_CASSINI_CANDIDATE; still_needed=replace f_comp policy with full PPN vector allocation; valid_for_claim=false
- `COMP3336_1_commutator_bound`: quantity=delta_comm_PPN; formula=delta_comm <= (f_comp B_gamma - other_composite_floors)/(A_1P sigma_Dpi); candidate_bound=6.900000e-03; assumptions=A_1P=1, sigma_Dpi=1.0e-03, other floors reserved as zero for first ceiling; derivation_status=EXACT_INEQUALITY_CEILING; still_needed=derive or source the PPN projector/smoothing commutator norm and sigma_Dpi; valid_for_claim=false
- `COMP3336_2_contact_p2`: quantity=ell_c/L_PPN for p_contact=2; formula=ell_c/L_PPN <= (f_comp B_gamma/C_contact)^(1/p_contact); candidate_bound=2.626785e-03; assumptions=C_contact=1, p_contact=2; derivation_status=CONTACT_SCALE_CEILING; still_needed=derive p_contact and C_contact from parent/local renormalization; valid_for_claim=false
- `COMP3336_3_contact_p4`: quantity=ell_c/L_PPN for p_contact=4; formula=ell_c/L_PPN <= (f_comp B_gamma/C_contact)^(1/p_contact); candidate_bound=5.125217e-02; assumptions=C_contact=1, p_contact=4; derivation_status=CONTACT_SCALE_CEILING; still_needed=derive p_contact and C_contact from parent/local renormalization; valid_for_claim=false
- `COMP3336_4_two_particle_gap`: quantity=m_gap_2pi r_PPN; formula=C_2P exp[-2 m_gap_2pi r_PPN] <= allocated two-particle budget; candidate_bound=m_gap_2pi r_PPN >= 0.5 ln(C_2P/B_2p); assumptions=gapped two-particle tail; B_2p chosen from f_comp B_gamma; derivation_status=SPECTRAL_GAP_CONTRACT; still_needed=source two-particle spectral density/gap or prove absence; valid_for_claim=false

## Response Product Acquisition Contract

- `RESP3336_0_A_PPN`: quantity=A_PPN(q_U,gauge); formula=A_PPN=max(A_gamma,A_beta,A_vector_tensor,A_gauge_residual); source_path=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3331_APPN_BOUND.csv; needed_action=choose actual PPN observable slot, q_U convention, and gauge projector; claim_gate=numeric A_PPN with source-owned q_U/gauge map; valid_for_claim=false
- `RESP3336_1_C_metric`: quantity=C_metric(lambda); formula=C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source; source_path=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3331_CMETRIC_BOUND.csv; needed_action=bound projection, gauge-fix, source-window, readout, smoothing, Hessian/Green, and source-normalization factors; claim_gate=numeric C_metric or conservative finite upper bound; valid_for_claim=false
- `RESP3336_2_product`: quantity=A_PPN*C_metric; formula=tree_residual=(A_PPN*C_metric) epsilon_eff^2; source_path=3335 placeholder grid; needed_action=replace placeholder product 1,1e6,1e12,1e16 with source-owned interval; claim_gate=interval upper bound small enough for derived epsilon_eff; valid_for_claim=false

## Required Source Inputs

- `REQ3336_0_real_PPN_vector`: quantity=full real PPN threshold vector; current_status=CASSINI_GAMMA_CANDIDATE_ONLY; next_action=add beta/preferred-frame/orbital thresholds before public local-GR claim; valid_for_claim=false
- `REQ3336_1_response_product`: quantity=source-owned A_PPN*C_metric upper interval; current_status=ACQUISITION_CONTRACT_ONLY; next_action=derive q_U/gauge map and C_metric operator factors; valid_for_claim=false
- `REQ3336_2_tree_floors`: quantity=epsilon_bg, T_grad, boundary, anisotropy; current_status=ALLOWABLE_BOUNDS_DERIVED_NOT_SOURCED; next_action=prove boundary/aniso silence or source numerical ceilings; valid_for_claim=false
- `REQ3336_3_composite_floors`: quantity=delta_comm, sigma_Dpi, contact scaling, spectral gap; current_status=ALLOWABLE_BOUNDS_DERIVED_NOT_SOURCED; next_action=derive commutator/contact theorem or source conservative upper bounds; valid_for_claim=false
- `REQ3336_4_Gamma`: quantity=Gamma_local or Gamma->K_solar map; current_status=LOWER_PRIORITY_UNLESS_GAMMA_LOCAL_SOURCED; next_action=retain Gamma fork while attacking dominant tree/composite floors; valid_for_claim=false

## Promotion Gates

- `GATE3336_0_real_gamma_candidate`: claim=real PPN gamma threshold candidate is recorded; passed=true; reason=Cassini gamma source and DOI/URL are recorded; valid_for_claim=false
- `GATE3336_1_tree_contract`: claim=tree epsilon_eff allowable bounds are derived from real gamma candidate; passed=true; reason=epsilon_eff ceilings are computed for response-product grid; valid_for_claim=false
- `GATE3336_2_composite_contract`: claim=composite contact/commutator allowable bounds are derived; passed=true; reason=delta_comm and contact scale ceilings are computed from allocated gamma candidate budget; valid_for_claim=false
- `GATE3336_3_response_contract`: claim=A_PPN*C_metric acquisition contract is explicit; passed=true; reason=A_PPN, C_metric, and product claim gates are separated; valid_for_claim=false
- `GATE3336_4_claim_ready`: claim=PPN/local-GR branch is claim-ready; passed=false; reason=only gamma candidate is sourced; response, tree, composite, Gamma, and full PPN vector are not source-owned; valid_for_claim=false

## Decision Ledger

- `DEC3336_0`: question=Did the real gamma candidate change the 3335 smoke story?; answer=not materially: 5 pass-like and 4 fail-like scenarios remain; reason=Cassini gamma candidate is close to the earlier smoke ceiling; tree/composite/open-Gamma dominance pattern survives; next_action=derive/source dominant tree and composite floors; valid_for_claim=false
- `DEC3336_1`: question=What is the best next derivation?; answer=PPN projector/smoothing commutator and contact scaling; reason=these decide whether composite floors are naturally tiny or require external fitting; next_action=attempt commutator/contact theorem before more broad theory expansion; valid_for_claim=false
- `DEC3336_2`: question=What is the best next source acquisition?; answer=A_PPN*C_metric interval and full PPN threshold vector; reason=tree allowance changes as sqrt(1/(A_PPN*C_metric)); no claim is possible with placeholder response products; next_action=bind q_U/gauge and C_metric factors, then add real PPN beta/preferred-frame/orbital thresholds; valid_for_claim=false

## Next Target

- `3337-Y5-R2FR-PPN-commutator-contact-zero-or-bound-theorem-under-AX1090.md`: target_script=scripts/Y5_R2FR_3337_PPN_commutator_contact_zero_or_bound_theorem.py; objective=attempt to prove or bound the PPN projector/smoothing commutator and contact floor that dominate composite risk in 3335-3336; must_include=condition for delta_comm_PPN=0; contact scaling epsilon_contact <= C_contact(ell_c/L)^p; spectral-gap fallback; no PPN pass claim; fallback_if_failed=retain exact composite acquisition contract and move to response-product source bounding; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- Cassini gamma is a source-backed candidate threshold, not the full PPN vector.
- All response-product values remain placeholders until `A_PPN C_metric` is bounded.
- The point of this checkpoint is to identify exact next derivations, not to announce a pass.
- `formalization-workbench` is not modified.
