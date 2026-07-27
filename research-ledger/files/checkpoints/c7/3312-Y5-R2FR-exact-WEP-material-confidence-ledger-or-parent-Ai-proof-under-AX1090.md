# 3312 - Exact WEP material-confidence ledger or parent Ai proof under AX1090

Run UTC: `2026-06-27T19:17:49.263176+00:00`

## Verdict

This checkpoint upgrades the WEP input side without making a claim.

MICROSCOPE is moved from crude element proxies toward source-backed material categories: `PtRh10` versus `TA6V` (`Ti-Al-V`). Eot-Wash keeps `Be/Ti` and adds the staged `B/mu` anchor.

Confidence handling is now explicit:

- MICROSCOPE combines stat/syst in quadrature as a proxy, then records a 1.96-sigma proxy.
- Eot-Wash records the abstract eta uncertainty as a proxy, with missing full covariance/systematic treatment called out.

No local-GR/source-coupling claim is promoted because `A_i`, exact isotope/alloy assay, full confidence/covariance treatment, and parent source factors remain open.

## Source Register

- `SRC3312_0` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3311-Y5-R2FR-alphaXi-source-factor-envelope-or-parent-amplitude-derivation-under-AX1090.md` — role=3311 alphaXi handoff
- `SRC3312_1` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv` — role=3311 factor law
- `SRC3312_2` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_ALPHA_XI_WEP_ENVELOPE.csv` — role=3311 alphaXi envelope
- `SRC3312_3` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_ALPHA_XI_ENVELOPE_SUMMARY.csv` — role=3311 summary
- `SRC3312_4` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_NEXT_TARGET.csv` — role=3311 next target
- `SRC3312_5` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3311_VALIDATION.csv` — role=3311 validation
- `SRC3312_6` (external_primary): `https://arxiv.org/abs/2209.15487` — role=MICROSCOPE eta and uncertainty source
- `SRC3312_7` (external_primary): `https://www.esa.int/Science_Exploration/Space_Science/Microscope` — role=MICROSCOPE material category source
- `SRC3312_8` (external_primary): `https://arxiv.org/abs/0712.0607` — role=Eot-Wash Be/Ti eta, acceleration, and B/mu source

## Parent Ai Audit

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\cosmology\activation-cosmology\a-unified-geometric-framework-for-cosmology-and-thermodynamics.md`: status=NO_PARENT_Ai_PROMOTION; evidence=L47:where $a(z) = a_0 + a_1 \ln(1+z)$ is a slowly varying function (with $a_0, a_1$ constants) and $B$ is another constant. This functional form means that the contribution of curvature stiffness increases with $z$ (through the $\ln(1+z)$ dependence) but not as steeply as a raw po... | L52:H(z) \;=\; H_0\, \frac{\,1 + \big(a_0 + a_1\,\ln(1+z)\big)\,\ln(1+z) + B\,z\,}{\,1 + r\,z\,}\,. \tag{3} | L54:Here $H_0$ is the present-day Hubble constant, and the parameters $a_0$, $a_1$, $B$, and $r$ characterize the departures from $\Lambda$CDM. The form (3) can be understood as follows: the numerator $1 + (a_0 + a_1 \ln(1+z))\ln(1+z) + Bz$ represents $1 + \Lambda_{\kappa}(z)$, i.... | L64:Table 1: MBT-5 model parameters with their interpretations in the MTS framework and best-fit values. (Parameters $a_0$ and $B$ from Eq. 3 are also fitted but represent secondary shape parameters: $a_0$ sets the present value of the stiffness term $\Lambda_{\kappa}(0)$ while $B...
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\04-variable-audit.csv`: status=NO_PARENT_Ai_PROMOTION; evidence=L107:local_ppn_tensor_ansatz_run_20260527_135230,runs/local_ppn_tensor_ansatz_20260527-135230,infrastructure,complete_open_tensor_ansatz,First generated run folder for the local PPN tensor ansatz gate.,run artifact,summary.csv row_count=10; pass_exact_zero_reference=1; open_ppn_met...
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\27-time-clock-limit-derivation.md`: status=NO_PARENT_Ai_PROMOTION; evidence=L100:(d tau_1 / dt) / (d tau_2 / dt)
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\62-local-ppn-tensor-ansatz-first-results.md`: status=NO_PARENT_Ai_PROMOTION; evidence=L34:runs/local_ppn_tensor_ansatz_20260527-135230/ | L40:runs/local_ppn_tensor_ansatz_20260527-135230/summary.csv | L41:runs/local_ppn_tensor_ansatz_20260527-135230/status.json | L42:runs/local_ppn_tensor_ansatz_20260527-135230/log.txt
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\transition_closure_first_true_micro_test.py`: status=NO_PARENT_Ai_PROMOTION; evidence=L22:"local_ppn_tensor_ansatz": "runs/local_ppn_tensor_ansatz_20260527-135230/status.json",

## Material Ledger

- `MICROSCOPE_PtRh10`: PtRh10 alloy components `Pt:0.9;Rh:0.1`; status=source-backed mass-fraction category; isotopic assay still not extracted
- `MICROSCOPE_TA6V`: TA6V / Ti-Al-V alloy components `Ti:0.9;Al:0.06;V:0.04`; status=source-backed mass-fraction category; exact alloy/isotope assay still not extracted
- `EOTWASH_Be`: Be components `Be:1.0`; status=source-backed test-body element; purity/isotope details not fully extracted
- `EOTWASH_Ti`: Ti components `Ti:1.0`; status=source-backed test-body element; purity/isotope details not fully extracted

## Confidence Ledger

- `CONF3312_0_MICROSCOPE`: eta=-1.5e-15, sigma_proxy=2.74590604355e-15, 95_proxy=5.38197584536e-15.
- `CONF3312_1_EOTWASH`: eta=0.3e-13, sigma_proxy=1.8e-13, 95_proxy=3.528e-13.

## Upgraded Pair Deltas

- `PAIR3312_0_MICROSCOPE_PtRh10_TA6V`: Delta(q_B,q_p,q_n,q_C,q_D)=(0,-0.057040341775,0.057040341775,2.57282130507,0.114080683551), Delta_B/mu=MISSING_FOR_PAIR.
- `PAIR3312_1_EOTWASH_Be_Ti`: Delta(q_B,q_p,q_n,q_C,q_D)=(0,-0.015764036368,0.015764036368,-2.01839389434,0.031528072734), Delta_B/mu=-0.002397.

## Runner

- `RUN3312_0_parent_Ai`: `NO_PARENT_Ai_PROMOTION` — candidate_count=0
- `RUN3312_1_material_upgrade`: `PASS_NONCLAIM` — MICROSCOPE_PtRh10;MICROSCOPE_TA6V;EOTWASH_Be;EOTWASH_Ti
- `RUN3312_2_confidence_upgrade`: `PASS_NONCLAIM` — CONF3312_0_MICROSCOPE;CONF3312_1_EOTWASH
- `RUN3312_3_claim_permission`: `REFUSE_CLAIM_PARENT_Ai_AND_FULL_ASSAY_COVARIANCE_MISSING` — A_i remains parent-unproven; exact isotope/alloy assay and full covariance are not applied

## Promotion Gates

- `GATE3312_0_parent_Ai`: passed=false; claim=A_i values are parent-proven
- `GATE3312_1_exact_materials`: passed=false; claim=WEP material charges are exact experimental charges
- `GATE3312_2_confidence`: passed=false; claim=eta bounds are final confidence-ready rows

## Decision

- `DEC3312_0`: no — no reviewed parent amplitude/source-factor derivation is promoted
- `DEC3312_1`: yes — MICROSCOPE material rows are upgraded to PtRh10 vs TA6V categories and confidence rows are explicit; Eot-Wash Be/Ti B/mu anchor is staged

## Next Target

- `3313-Y5-R2FR-upgraded-WEP-matrix-with-material-confidence-rows-under-AX1090.md`
- `scripts/Y5_R2FR_3313_upgraded_WEP_matrix_with_material_confidence_rows.py`
- Objective: rebuild the WEP linear matrix using upgraded material deltas and confidence rows, while keeping A_i/lambda/source factors explicit and nonclaim
