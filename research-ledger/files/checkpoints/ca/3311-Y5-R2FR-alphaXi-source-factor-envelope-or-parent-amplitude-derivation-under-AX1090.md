# 3311 - AlphaXi source-factor envelope or parent amplitude derivation under AX1090

Run UTC: `2026-06-27T19:11:30.174164+00:00`

## Verdict

The remaining WEP multiplier is now explicit.

Define

`A_0 = alpha0_star Xi_0[Earth] = (1/3) Z_0 U_0 Xi_0[Earth]`

and

`A_2 = alpha2_star Xi_2[Earth] = (-4/3) Z_2 U_2 Xi_2[Earth]`.

The WEP scan therefore constrains

`|A_i (s_i dot Delta_q_AB)| <= eta_bound/F(lambda,r)`.

No `A_i` value is promoted here. The important discipline is that `A_i` is not absorbed into `G_cal`; it remains a finite-mode source/readout amplitude that must be derived or bounded.

## Source Register

- `SRC3311_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3310-Y5-R2FR-lambda-scan-WEP-envelope-or-parent-range-derivation-under-AX1090.md` — exists=true; role=3310 lambda envelope handoff
- `SRC3311_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3310_PARENT_RANGE_DERIVATION_AUDIT.csv` — exists=true; role=3310 parent range audit
- `SRC3311_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3310_WEP_KLAMBDA_ENVELOPE.csv` — exists=true; role=3310 F(lambda) envelope
- `SRC3311_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3310_ENVELOPE_SUMMARY.csv` — exists=true; role=3310 sensitivity summary
- `SRC3311_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3310_NEXT_TARGET.csv` — exists=true; role=3310 next target
- `SRC3311_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3310_VALIDATION.csv` — exists=true; role=3310 validation
- `SRC3311_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3308_WEP_LINEAR_CONSTRAINT_MATRIX.csv` — exists=true; role=3308 eta and linear forms
- `SRC3311_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv` — exists=true; role=3303 alpha factor law

## Factor Law

- `AXF3311_0_scalar` `A_0`: A_0 = alpha0_star Xi_0[Earth] = (1/3) Z_0 U_0 Xi_0[Earth].
- `AXF3311_1_spin2` `A_2`: A_2 = alpha2_star Xi_2[Earth] = (-4/3) Z_2 U_2 Xi_2[Earth].
- `AXF3311_2_no_G_absorption` `A_i`: A_i is a finite-mode relative source factor, not a calibrated Newtonian G.

## Parent Alpha/Xi Audit

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\cosmology\jwst\impossible-galaxies.md`: status=NO_ALPHA_XI_PROMOTION; hits=alpha_0; evidence=L22:= \bigl(\alpha_0 + \alpha_1 \log(1+z)\bigr)\,\log(1+z) + \beta z,
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\37-local-switch-off-and-ppn-gate.md`: status=NO_ALPHA_XI_PROMOTION; hits=alpha_2; evidence=L255:|alpha_2,MTS| <= 1e-5 | L261:alpha_1,MTS = alpha_2,MTS = 0 | L521:| L4 vector/preferred frame | `alpha_1`, `alpha_2` | `0` | `<= 1e-4`, `<= 1e-5` |
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\73-support-powers-kperp-lemma.md`: status=NO_ALPHA_XI_PROMOTION; hits=source\s+factor; evidence=L201:But the current parent v0 only states the first source factor:
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\77-sigma-L-source-silence-theorem.md`: status=NO_ALPHA_XI_PROMOTION; hits=source\s+factor; evidence=L196:S_cg has a linear unscreened-source factor;
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\mathematics\riemann-zeta\impossible-galaxies.md`: status=NO_ALPHA_XI_PROMOTION; hits=alpha_0; evidence=L22:= \bigl(\alpha_0 + \alpha_1 \log(1+z)\bigr)\,\log(1+z) + \beta z,

## Envelope Summary

- `LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: bound proxy at F>=0.9 is `2.75248934774e-15` on |A_i(s_i dot Delta_q)|.
- `LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: bound proxy at F>=0.9 is `2.75248934774e-15` on |A_i(s_i dot Delta_q)|.
- `LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: bound proxy at F>=0.9 is `1.80350837937e-13` on |A_i(s_i dot Delta_q)|.
- `LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: bound proxy at F>=0.9 is `1.80350837937e-13` on |A_i(s_i dot Delta_q)|.

## Runner

- `RUN3311_0_parent_alphaXi`: `NO_ALPHA_XI_PROMOTION` — candidate_count=0
- `RUN3311_1_alphaXi_envelope`: `PASS_NONCLAIM` — rows=44
- `RUN3311_2_claim_permission`: `REFUSE_CLAIM_EXACT_MATERIAL_CONFIDENCE_AND_PARENT_FACTORS_MISSING` — A_i is explicit but not parent-derived; eta/material rows remain proxy/partial

## Promotion Gates

- `GATE3311_0_parent_Ai`: passed=false; claim=A_0 and A_2 are derived from parent mode/source data
- `GATE3311_1_Ai_bound`: passed=false; claim=WEP data bounds A_i*s_i combinations claim-ready
- `GATE3311_2_no_G_absorption`: passed=false; claim=finite-mode source factor can be hidden inside calibrated G

## Decision

- `DEC3311_0`: no — no reviewed parent source-factor row has been promoted
- `DEC3311_1`: WEP constraints now bound |A_i(s_i dot Delta_q)| over the lambda scan — alpha/source factor is separated from range factor and material projection

## Next Target

- `3312-Y5-R2FR-exact-WEP-material-confidence-ledger-or-parent-Ai-proof-under-AX1090.md`
- `scripts/Y5_R2FR_3312_exact_WEP_material_confidence_ledger_or_parent_Ai_proof.py`
- Objective: replace proxy material/confidence rows with exact WEP inputs where available, or prove A_i values from parent amplitude/source factors
