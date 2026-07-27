# 3307 - Material source-charge model for DeltaXi WEP bounds under AX1090

Run UTC: `2026-06-27T18:52:35.585358+00:00`

## Verdict

The WEP fallback now has a material-charge model.

For each finite mode,

`Delta_Xi_i[A,B] = s_iB Delta_q_B + s_ip Delta_q_p + s_in Delta_q_n + s_iC Delta_q_C + s_iD Delta_q_D + ...`.

This turns the coupling gap into a concrete object: either derive the source coefficients `s_ik` from the parent projector, or use WEP anchors to bound combinations of them.

The material rows are proxy rows only. They are useful for plumbing and scale checks, not publication claims, because exact alloy/isotope composition, source-body composition, ranges, mode strengths, and confidence conventions remain unresolved.

## Source Register

- `SRC3307_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3306-Y5-R2FR-linearized-public-metric-projector-extraction-or-WEP-data-acquisition-under-AX1090.md` — exists=true; role=3306 projector/WEP handoff
- `SRC3307_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3306_WEP_SOURCE_ANCHORS.csv` — exists=true; role=3306 WEP anchors
- `SRC3307_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3306_WEP_TO_DELTA_XI_MAPPING.csv` — exists=true; role=3306 WEP mapping
- `SRC3307_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3306_DECISION_LEDGER.csv` — exists=true; role=3306 decision
- `SRC3307_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3306_NEXT_TARGET.csv` — exists=true; role=3306 next target
- `SRC3307_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3306_VALIDATION.csv` — exists=true; role=3306 validation

## Charge Basis

- `q_B`: baryon/mass-normalized universal matter charge using `1`.
- `q_p`: proton fraction proxy using `Z/A`.
- `q_n`: neutron fraction proxy using `(A-Z)/A`.
- `q_C`: semi-empirical Coulomb binding proxy using `Z(Z-1)/A^(4/3)`.
- `q_D`: neutron-proton imbalance proxy using `(A-2Z)/A`.

## Material Proxy Charges

- `Be_proxy` Be: q_p=0.443842790883, q_n=0.556157209117, q_C=0.639843090689, q_D=0.112314418233.
- `Ti_proxy` Ti: q_p=0.459606827251, q_n=0.540393172749, q_C=2.65823698503, q_D=0.080786345499.
- `Pt_proxy` Pt: q_p=0.399827766501, q_n=0.600172233499, q_C=5.30831221877, q_D=0.200344466999.

## Pair Charge Contrasts

- `PAIR3307_0_MICROSCOPE_Ti_Pt`: Delta(q_B,q_p,q_n,q_C,q_D)=(0,0.05977906075,-0.05977906075,-2.65007523374,-0.1195581215).
- `PAIR3307_1_EOTWASH_Be_Ti`: Delta(q_B,q_p,q_n,q_C,q_D)=(0,-0.015764036368,0.015764036368,-2.01839389434,0.031528072734).

## DeltaXi Linear Laws

- `DXI3307_0_scalar_linear_charge` `Delta_Xi_0[A,B]`: `Delta_Xi_0[A,B] = s_0B Delta_q_B + s_0p Delta_q_p + s_0n Delta_q_n + s_0C Delta_q_C + s_0D Delta_q_D + higher_terms`
- `DXI3307_1_spin2_linear_charge` `Delta_Xi_2[A,B]`: `Delta_Xi_2[A,B] = s_2B Delta_q_B + s_2p Delta_q_p + s_2n Delta_q_n + s_2C Delta_q_C + s_2D Delta_q_D + higher_terms`
- `DXI3307_2_universal_limit` `Xi_i[A]=1`: `all nonuniversal coefficients s_ik=0, or all material charge contrasts project to zero`

## Nonclaim WEP Bound Rows

- `BND3307_WEP3306_0_MICROSCOPE_Ti_Pt`: `Ti/Pt alloys` eta=-1.5e-15 sigma_proxy=2.74590604355e-15; template `|sum_i alpha_i_star Xi_i[E] (s_i dot Delta_q_AB) range_factor(lambda_i,r)| <= eta_bound`
- `BND3307_WEP3306_1_EOTWASH_Be_Ti`: `Be/Ti` eta=0.3e-13 sigma_proxy=MISSING_COMBINED_UNCERTAINTY; template `|sum_i alpha_i_star Xi_i[E] (s_i dot Delta_q_AB) range_factor(lambda_i,r)| <= eta_bound`

## Runner

- `RUN3307_0_material_basis`: `PASS_NONCLAIM` — Be_proxy;Ti_proxy;Pt_proxy
- `RUN3307_1_pair_deltas`: `PASS_NONCLAIM` — PAIR3307_0_MICROSCOPE_Ti_Pt;PAIR3307_1_EOTWASH_Be_Ti
- `RUN3307_2_bound_rows_safe`: `PASS_NONCLAIM` — BND3307_WEP3306_0_MICROSCOPE_Ti_Pt;BND3307_WEP3306_1_EOTWASH_Be_Ti
- `RUN3307_3_claim_permission`: `REFUSE_CLAIM_SOURCE_COEFFICIENTS_MISSING` — s_ik, alpha_i_star, lambda_i, Xi_i[E], exact materials, and CL convention are missing

## Promotion Gates

- `GATE3307_0_material_charge_claim`: passed=false; claim=proxy material charges are exact experiment material charges
- `GATE3307_1_DeltaXi_bound_claim`: passed=false; claim=WEP anchors bound Delta_Xi_0 and Delta_Xi_2
- `GATE3307_2_source_coupling_closed`: passed=false; claim=finite-mode source coupling is safe for local GR

## Decision

- `DEC3307_0`: yes, nonclaim — Delta_Xi is now represented as source-coefficient vectors dotted into material charge contrasts for Ti/Pt and Be/Ti
- `DEC3307_1`: no — charge rows are proxy-level and source coefficients/ranges are missing

## Next Target

- `3308-Y5-R2FR-source-coefficient-sik-gate-or-WEP-linear-bound-runner-under-AX1090.md`
- `scripts/Y5_R2FR_3308_source_coefficient_sik_gate_or_WEP_linear_bound_runner.py`
- Objective: derive the source-charge coefficients s_ik from the parent projector, or build a linear WEP bound runner that constrains combinations of s_ik using the Ti/Pt and Be/Ti charge contrasts
