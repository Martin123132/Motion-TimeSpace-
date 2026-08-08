# 3310 - Lambda-scan WEP envelope or parent range derivation under AX1090

Run UTC: `2026-06-27T19:07:57.513695+00:00`

## Verdict

This checkpoint tries the parent range route first, then builds the nonclaim lambda envelope.

The parent route is not promoted unless a reviewed parent coefficient/mass row supplies `lambda_0` or `lambda_2` with units and convention.

The scan route uses

`F(lambda,r) = (1+r/lambda) exp(-r/lambda)`

so each WEP constraint becomes

`|alpha_i_star Xi_i[Earth] (s_i dot Delta_q_AB)| <= eta_bound / F(lambda,r)`.

This is range-aware but still nonclaim because `alpha_i_star`, `Xi_i[Earth]`, exact materials, and confidence conventions remain open.

## Source Register

- `SRC3310_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3309-Y5-R2FR-mode-factor-Klambda-and-exact-WEP-inputs-under-AX1090.md` — exists=true; role=3309 K(lambda) handoff
- `SRC3310_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3309_KLAMBDA_DERIVATION.csv` — exists=true; role=3309 K(lambda) derivation
- `SRC3310_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3309_EXACT_WEP_INPUT_LEDGER.csv` — exists=true; role=3309 upgraded WEP inputs
- `SRC3310_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3309_KLAMBDA_CONSTRAINT_UPDATE.csv` — exists=true; role=3309 K(lambda) constraints
- `SRC3310_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3309_WEP_CLAIM_BLOCKERS.csv` — exists=true; role=3309 claim blockers
- `SRC3310_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3309_NEXT_TARGET.csv` — exists=true; role=3309 next target
- `SRC3310_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3309_VALIDATION.csv` — exists=true; role=3309 validation
- `SRC3310_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_PARENT_COEFFICIENT_EXTRACTION_SCAN.csv` — exists=true; role=3302 parent coefficient scan

## Parent Range Audit

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\gravity-as-emergent-mass-geometry-scaling-in-motion-timespace-mts.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L96:g(r) = v(r)^2 / r = GM(r) / r^2.
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L96:g(r) = G M(r) / r^2.
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-gravity-a-geometric-stiffness-memory-description-of-galactic-dynamics.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L426:R^2 = 0.8394. | L436:R^2 ≈ 0.96.
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\relativity\time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L69:ds^2 = - (1 + \frac{2\Phi}{c^2}) c^2 dt^2 + (1 - \frac{2\Phi}{c^2})^{-1} dr^2 + r^2 d\Omega^2,
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\00-theory-map-test-first.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L62:V^2(r) = V_bar^2(r) + (c H0 / 8 pi) L_eff [1 - exp(-(r/L_eff)^q)]
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\01-empirical-test-roadmap.md`: status=NO_PARENT_RANGE_PROMOTION; hits=R\^2; evidence=L34:V_bar^2 = V_gas^2 + Upsilon_disk V_disk^2 + Upsilon_bulge V_bulge^2
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\04-variable-audit.csv`: status=NO_PARENT_RANGE_PROMOTION; hits=\blambda_0\b;Weyl;R\^2; evidence=L10:chi,χ; support field; transport response,galaxies,effective_observable_field,Macroscopic support/transport-response field mapping curvature exchange into galaxy rotation support.,velocity squared in galaxy law: km^2/s^2,u^mu nabla_mu chi + chi/tau_Gamma = Gamma/4; V^2=V_bar^2+... | L31:V_bar,Vbar; V_bar; baryonic velocity,galaxies,observable_construct,Baryonic rotation contribution from gas/disk/bulge components.,km/s; squared version km^2/s^2,V_bar^2=V_gas^2+0.5 V_disk^2+0.7 V_bulge^2,galaxy-work/sparc-analysis/a-transport-response-framework-for-disk-galaxi... | L32:Gamma0_galaxy,Γ0; Gamma_0; cH0/8pi,galaxies,empirical_bridge_constant,Cosmologically normalized source scale in galaxy transport law.,km^2 s^-2 kpc^-1 if using galaxy units,Gamma0=cH0/(8pi); V^2=V_bar^2+Gamma0 L_eff kernel,galaxy-work/sparc-analysis/a-transport-response-framew... | L36:lambda_B,λ_B; baryonic-gradient coupling; suppression strength,galaxies,open_theory_target,ETG/H+ suppression-channel amplitude decomposed into observable lower bound plus excess.,dimensionless if multiplying gradient convolution into velocity squared; confirm,lambda_B=lambda_...
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\05-equation-register.md`: status=NO_PARENT_RANGE_PROMOTION; hits=\blambda_0\b;\bm_0\b;\bm_2\b;Weyl;R\^2; evidence=L196:|b_mem| |delta m|^2/(4 ell_scr^2) <= 1e-5 |4 pi G rho|/c^2 | L325:|box m| ~ M_tr/L_tr^2 | L333:+ |b_mem| M_tr^2/L_tr^3 | L366:a(r) = GM/r^2
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\06-consistency-red-team.md`: status=NO_PARENT_RANGE_PROMOTION; hits=\blambda_0\b;\bm_2\b;Weyl;R\^2; evidence=L133:+ |b_mem| M_tr^2/L_tr^3 | L703:+ 1/2 |F_2| M_tr^2/ell_tr | L705:+ C_K |b_mem| M_tr^2/ell_tr^3 | L1301:G + Lambda_0 g = K_matter + K_MTS
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\123-local-source-power-theorem.md`: status=NO_PARENT_RANGE_PROMOTION; hits=\bm_2\b; evidence=L144:+ 1/2 m_2(Y) D_L^2

## Lambda Sensitivity Summary

- `LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: F>=0.1 at lambda=10000000 m; F>=0.9 at lambda=100000000 m.
- `LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: F>=0.1 at lambda=10000000 m; F>=0.9 at lambda=100000000 m.
- `LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: F>=0.1 at lambda=10000000 m; F>=0.9 at lambda=100000000 m.
- `LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: F>=0.1 at lambda=10000000 m; F>=0.9 at lambda=100000000 m.

## Runner

- `RUN3310_0_parent_range`: `NO_PARENT_RANGE_PROMOTION` — candidate_count=0
- `RUN3310_1_lambda_envelope`: `PASS_NONCLAIM` — rows=44; constraints=4; grid=11
- `RUN3310_2_sensitivity_summary`: `PASS_NONCLAIM` — LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt:10000000;LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt:10000000;LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti:10000000;LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti:10000000
- `RUN3310_3_claim_permission`: `REFUSE_CLAIM_ALPHA_XI_MATERIAL_CONFIDENCE_MISSING` — range envelope is numeric in F(lambda) only; amplitude/source/material/confidence blockers remain

## Promotion Gates

- `GATE3310_0_parent_lambda`: passed=false; claim=lambda_0/lambda_2 are derived from parent coefficients
- `GATE3310_1_lambda_scan_bound`: passed=false; claim=WEP lambda scan bounds s_ik combinations
- `GATE3310_2_local_source_range_gate`: passed=false; claim=local source-coupling range gate is closed

## Decision

- `DEC3310_0`: no — no reviewed parent coefficient/mass row with units has been promoted
- `DEC3310_1`: range-aware F(lambda) envelopes for every MICROSCOPE/Eot-Wash scalar/spin2 constraint — the WEP bound now knows when finite modes are exponentially suppressed or long-range sensitive

## Next Target

- `3311-Y5-R2FR-alphaXi-source-factor-envelope-or-parent-amplitude-derivation-under-AX1090.md`
- `scripts/Y5_R2FR_3311_alphaXi_source_factor_envelope_or_parent_amplitude_derivation.py`
- Objective: derive alpha_i_star and Xi_i[Earth] from parent mode/source data if possible; otherwise keep them as an explicit envelope factor multiplying the lambda-scan WEP constraints
