# 3328 - Local-GR residual budget and promotion map under AX1090

Run UTC: `2026-06-27T20:44:47.442848+00:00`

## Verdict

3328 assembles the local branch into one scorecard.

The branch is now structurally coherent as a **conditional measured-G local-GR closure theorem**, not an unconditional proof and not a derivation of `G`.

For each local arena `i`, the no-cancellation residual budget is

`R_i^local <= |R_Gamma_i| + C_i(lambda) epsilon_eff_i(lambda)^2 + epsilon_composite_i(lambda) + epsilon_direct_i + epsilon_G_closure_i`,

where

`epsilon_eff_i(lambda)=epsilon_bg_i T_grad(lambda)+epsilon_boundary_i+epsilon_kernel_aniso_i`,

and

`epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i`.

This is progress: the local branch has moved from loose narrative to an inspectable residual budget. But no PPN/R10/WEP/clock/orbital pass is claimed. The missing step is numeric or source-backed bounds for `C_i`, `epsilon_eff`, `epsilon_composite`, local `Gamma` leakage, and arena thresholds.

## Source Register

- `SRC3328_0_3318_Gamma`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md` exists=true parse_ok=true role=Gamma extra-sector local nonpropagation/readout branch
- `SRC3328_1_3319_psi`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md` exists=true parse_ok=true role=psi public readout split and tree residue route
- `SRC3328_2_3321_epsilon`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3321-Y5-R2FR-smoothing-kernel-scale-separation-bound-for-epsilon-grad-under-AX1090.md` exists=true parse_ok=true role=epsilon_grad smoothing transfer and threshold rows
- `SRC3328_3_3322_Ci`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3322-Y5-R2FR-Ci-projection-and-composite-contact-tail-gate-for-epsilon-grad-under-AX1090.md` exists=true parse_ok=true role=C_i operator response and arena threshold formulas
- `SRC3328_4_3324_closure`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3324-Y5-R2FR-induced-EH-coefficient-or-measured-G-closure-local-GR-theorem-under-AX1090.md` exists=true parse_ok=true role=measured-G local GR/Newton/Maxwell closure theorem
- `SRC3328_5_3325_matter`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3325-Y5-R2FR-universal-matter-no-direct-psi-vertex-and-no-tadpole-signature-gate-under-AX1090.md` exists=true parse_ok=true role=macroscopic universal matter and EM stress signature
- `SRC3328_6_3327_composite`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3327-Y5-R2FR-parent-local-fluctuation-measure-or-numeric-composite-envelope-under-AX1090.md` exists=true parse_ok=true role=CLT/mixing composite envelope and required numeric inputs
- `SRC3328_7_3324_theorem_csv`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv` exists=true parse_ok=true role=closure theorem rows
- `SRC3328_8_3322_thresholds_csv`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3322_ARENA_THRESHOLD_FORMULAS.csv` exists=true parse_ok=true role=arena residual threshold formulas
- `SRC3328_9_3327_inputs_csv`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3327_REQUIRED_NUMERIC_INPUTS.csv` exists=true parse_ok=true role=composite-envelope numeric inputs
- `SRC3328_10_3327_envelope_csv`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv` exists=true parse_ok=true role=composite residual envelope

## Local Branch Component Status

- `COMP3328_0_measured_G_closure`: component=measured-G local GR closure; status=CONDITIONAL_PASS; signed_piece=3324 formalizes local GR/Newton/Maxwell with measured G_N; remaining_gap=not a derivation of G; induced C_EH still future work; budget_symbol=epsilon_G_closure=0 if measured-G closure is declared; valid_for_claim=false
- `COMP3328_1_Newton_Poisson`: component=Newton/Poisson weak-field limit; status=CONDITIONAL_PASS; signed_piece=3324 derives nabla^2 Phi = 4 pi G_N rho plus bounded residual; remaining_gap=requires residual budget below Newton/PPN/orbital thresholds; budget_symbol=epsilon_Newton_i; valid_for_claim=false
- `COMP3328_2_matter_EM_source`: component=macroscopic matter and EM stress coupling; status=MACRO_SIGNED_CONDITIONAL; signed_piece=3325 signs standard metric L_matter and Maxwell/Poynting as T_munu^EM route; remaining_gap=microscopic matter descent from psi not derived; direct psi vertices must remain excluded; budget_symbol=epsilon_direct_i=0 only under Delta S_direct=0; valid_for_claim=false
- `COMP3328_3_Gamma_local`: component=Gamma/local saturation residue; status=CONDITIONAL_OR_BOUND; signed_piece=3318/3324 route treats local Gamma/saturation as silent or residual-bounded; remaining_gap=must keep explicit R_Gamma_i unless parent local silence is signed for each arena; budget_symbol=R_Gamma_i; valid_for_claim=false
- `COMP3328_4_psi_tree`: component=psi tree first-gradient residue; status=BOUNDED_CONDITIONAL; signed_piece=3319-3321 give first-gradient silence theorem and Gaussian T_grad transfer; remaining_gap=epsilon_bg, ell_s, boundary/aniso leakage, and local gradient scale not numeric; budget_symbol=C_i epsilon_eff_i^2; valid_for_claim=false
- `COMP3328_5_Ci_response`: component=C_i projection/propagator/source response; status=FORMULA_READY_NOT_NUMERIC; signed_piece=3322 decomposes C_i into arena projection, propagator norm, and source normalization; remaining_gap=C_PPN, C_R10, C_WEP, C_clock, C_orb not source/numeric bounded; budget_symbol=C_i(lambda,S,H_pi); valid_for_claim=false
- `COMP3328_6_composite`: component=composite/tadpole/contact tail; status=ENVELOPE_READY_NOT_NUMERIC; signed_piece=3326-3327 give centered split, CLT skew suppression, and total epsilon_composite envelope; remaining_gap=ell_c, C_mix, C3, bias, rho_P1, spectral gap, contact/boundary/aniso bounds missing; budget_symbol=epsilon_composite_i; valid_for_claim=false
- `COMP3328_7_arena_data_bounds`: component=PPN/R10/WEP/clock/orbital empirical thresholds; status=ROUTED_NOT_CLAIM_READY; signed_piece=3321/3322 define threshold formulas by arena; remaining_gap=claim-ready numeric threshold curves and response coefficients are not assembled; budget_symbol=B_i^max; valid_for_claim=false

## Residual Budget Formulas

- `BUD3328_0_master`: formula=R_i^local <= |R_Gamma_i| + C_i(lambda) epsilon_eff_i(lambda)^2 + epsilon_composite_i(lambda) + epsilon_direct_i + epsilon_G_closure_i; meaning=master no-cancellation local residual budget for each arena i; claim_gate=must satisfy R_i^local <= B_i^max for every claimed arena; valid_for_claim=false
- `BUD3328_1_epsilon_eff`: formula=epsilon_eff_i(lambda)=epsilon_bg_i T_grad(lambda)+epsilon_boundary_i+epsilon_kernel_aniso_i; meaning=first-gradient leakage after smoothing and local patch defects; claim_gate=requires epsilon_bg_i, ell_s, lambda, boundary, and anisotropy bounds; valid_for_claim=false
- `BUD3328_2_T_grad`: formula=T_grad(lambda)=(ell_s/lambda) exp[-ell_s^2/(2 lambda^2)]; meaning=3321 Gaussian smoothing transfer law; claim_gate=requires parent/phenomenological ell_s and arena lambda convention; valid_for_claim=false
- `BUD3328_3_Ci`: formula=C_i=||Pi_i W_i||^2 ||D S_ell H_pi S_ell^dagger D^dagger|| x source_normalization_i; meaning=3322 response coefficient; claim_gate=requires arena projection, propagator, and source normalization bounds; valid_for_claim=false
- `BUD3328_4_composite`: formula=epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i; meaning=3327 composite envelope; claim_gate=requires CLT/mixing and spectral/contact inputs; valid_for_claim=false
- `BUD3328_5_one_particle_composite`: formula=epsilon_1p_i <= A_i delta_mean_i sigma_Dpi_i + B_i (C3_i/sqrt(N_eff_i)+delta_bias_i) sigma_Dpi_i^2 + rho_P1_i Q2_norm_i; meaning=one-particle composite leakage after exact mean-centering and CLT skew suppression; claim_gate=requires delta_mean_i=0 or bound, N_eff_i, C3_i, bias, projection leakage, and Q2 norm; valid_for_claim=false
- `BUD3328_6_G_closure`: formula=epsilon_G_closure_i=0 only for declared measured-G closure; deriving G requires numeric C_EH^ind; meaning=separates GR-equivalence from deeper Newton-constant derivation; claim_gate=public text must not claim G is derived unless C_EH is computed; valid_for_claim=false
- `BUD3328_7_direct_vertex`: formula=epsilon_direct_i=0 only if Delta S_direct[psi,matter,EM]=0; meaning=direct psi-matter/psi-EM/Poynting vertices are excluded from clean local branch; claim_gate=any direct vertex must be bounded separately; valid_for_claim=false

## Arena Promotion Map

- `PPN_local_GR`: residual_test=|gamma-1|, |beta-1|, preferred-frame residuals; budget_formula=R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff^2 + epsilon_composite_PPN + epsilon_direct_PPN; current_status=CONDITIONAL_NOT_CLAIM_READY; blocking_inputs=C_PPN, epsilon_eff, epsilon_composite_PPN, R_Gamma_PPN, PPN threshold table; valid_for_claim=false
- `orbital_Newton`: residual_test=delta a/a_Newton or anomalous precession/orbital residual; budget_formula=R_orb <= |R_Gamma_orb| + C_orb epsilon_eff^2 + epsilon_composite_orb; current_status=CONDITIONAL_NOT_CLAIM_READY; blocking_inputs=C_orb, compact-source projection, orbital threshold values, contact absorption; valid_for_claim=false
- `R10_short_range`: residual_test=alpha_psi(lambda) against alpha_bound(lambda); budget_formula=alpha_psi(lambda) <= |R_Gamma_R10| + C_R10(lambda) epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda); current_status=CONDITIONAL_NOT_CLAIM_READY; blocking_inputs=claim-ready alpha_bound curve, C_R10(lambda), contact/source-size routing, two-pi gap/contact bounds; valid_for_claim=false
- `WEP`: residual_test=eta_AB composition dependence; budget_formula=eta_AB <= |R_Gamma_WEP| + C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP + epsilon_direct_WEP; current_status=CONDITIONAL_NOT_CLAIM_READY; blocking_inputs=material response Delta q_AB, direct vertex exclusion, anisotropy/contact bounds; valid_for_claim=false
- `clocks_EM_Poynting`: residual_test=clock shifts, optical/EM propagation, Poynting/stress residual; budget_formula=R_clock <= |R_Gamma_clock| + C_clock epsilon_eff^2 + epsilon_EM_composite_tail + epsilon_direct_EM; current_status=CONDITIONAL_NOT_CLAIM_READY; blocking_inputs=Maxwell stress projection, direct psi-EM exclusion, clock normalization, EM tail bounds; valid_for_claim=false

## Required Input Ledger

- `REQ3328_0_CEH_or_closure`: quantity=measured-G closure declaration or C_EH^ind; needed_for=separating local GR reduction from derivation of G; status=CLOSURE_READY_CEH_MISSING; priority=high; valid_for_claim=false
- `REQ3328_1_smoothing`: quantity=ell_s, epsilon_bg_i, lambda convention; needed_for=T_grad and epsilon_eff; status=MISSING_NUMERIC; priority=high; valid_for_claim=false
- `REQ3328_2_Ci`: quantity=C_PPN, C_R10, C_WEP, C_clock, C_orb; needed_for=arena response coefficients; status=MISSING_NUMERIC_OR_BOUND; priority=high; valid_for_claim=false
- `REQ3328_3_composite`: quantity=ell_c, C_mix, d_eff, C3, delta_bias, rho_P1, dmu_2, m_gap_2pi, contact/boundary/aniso; needed_for=epsilon_composite_i; status=MISSING_NUMERIC_OR_PARENT_BOUND; priority=high; valid_for_claim=false
- `REQ3328_4_Gamma`: quantity=R_Gamma_i or parent local Gamma silence; needed_for=local Gamma/saturation residual; status=MISSING_ARENA_BOUND; priority=medium; valid_for_claim=false
- `REQ3328_5_direct`: quantity=Delta S_direct=0 proof or direct vertex bounds; needed_for=WEP/clock/EM local safety; status=BRANCH_EXCLUSION_READY_MICRO_PROOF_MISSING; priority=medium; valid_for_claim=false
- `REQ3328_6_data`: quantity=PPN, R10 alpha(lambda), WEP, clock, orbital threshold tables; needed_for=arena pass/fail comparisons; status=MISSING_CLAIM_READY_TABLES; priority=medium; valid_for_claim=false

## Claim Status Ledger

- `CLAIM3328_0_measured_G_local_GR`: claim=MTS has a conditional measured-G route to local GR/Newton/Maxwell; status=INTERNAL_CONDITIONAL_SUPPORTED; allowed_wording=conditional local-GR closure theorem, not public pass; forbidden_wording=MTS has fully proved local GR or derived G; valid_for_claim=false
- `CLAIM3328_1_derive_G`: claim=MTS derives Newton's constant; status=NO; allowed_wording=future induced C_EH route; forbidden_wording=G is derived from current gamma/lambda/kappa equations; valid_for_claim=false
- `CLAIM3328_2_Newton_limit`: claim=Newton/Poisson limit is recovered; status=CONDITIONAL; allowed_wording=recovered under measured-G closure and bounded local residuals; forbidden_wording=unconditional Newton pass; valid_for_claim=false
- `CLAIM3328_3_Maxwell_EM`: claim=Maxwell/EM stress is compatible with local branch; status=CONDITIONAL; allowed_wording=EM/Poynting routed through metric T_munu under no direct psi-EM vertices; forbidden_wording=MTS derives/unifies Maxwell; valid_for_claim=false
- `CLAIM3328_4_local_tests`: claim=PPN/R10/WEP/clock/orbital tests pass; status=NO_CLAIM; allowed_wording=budget formulas and required inputs are ready; forbidden_wording=local tests passed; valid_for_claim=false

## Local Branch Scorecard

- `SCORE3328_0_formal_structure`: item=local branch formal structure; grade=strong conditional; reason=measured-G closure, Poisson theorem, matter signature, smoothing tree bound, and composite envelope are assembled; next_action=turn symbolic budget into arena-specific numeric/bounded rows; valid_for_claim=false
- `SCORE3328_1_derivation_depth`: item=derivation depth; grade=mixed; reason=several pieces are derived conditionally, but induced G, microscopic matter descent, C_i numerics, and composite inputs remain open; next_action=prioritize C_i/epsilon_composite numeric envelopes before public claims; valid_for_claim=false
- `SCORE3328_2_empirical_readiness`: item=empirical readiness; grade=not ready; reason=test formulas exist but thresholds/coefficients are not populated; next_action=make an arena-by-arena numeric input matrix; valid_for_claim=false
- `SCORE3328_3_public_safety`: item=public safety; grade=private only; reason=safe as internal discipline; public wording would need strong caveats; next_action=keep in post-checkpoint until at least one local arena budget is populated; valid_for_claim=false

## Next Target

- `3329-Y5-R2FR-local-residual-budget-input-prioritizer-and-minimal-numeric-smoke-under-AX1090.md`: target_script=scripts/Y5_R2FR_3329_local_residual_budget_input_prioritizer_and_minimal_numeric_smoke.py; objective=choose the smallest local arena/numeric route that can stress-test the 3328 residual budget, prioritizing PPN or R10 with conservative symbolic-to-numeric placeholders kept nonclaim; must_include=input priority table; one minimal arena; no-claim smoke numbers; sensitivity to C_i and epsilon_composite; pass/fail conditions; no public claim; fallback_if_failed=keep 3328 as the complete local residual-budget checklist and return to deriving missing coefficients; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- It is a branch-level scorecard, not a public theorem.
- It explicitly rejects claims that `G` is derived or that local tests already pass.
- It gives one complete residual formula that can now be populated arena by arena.
- `formalization-workbench` is not modified.
