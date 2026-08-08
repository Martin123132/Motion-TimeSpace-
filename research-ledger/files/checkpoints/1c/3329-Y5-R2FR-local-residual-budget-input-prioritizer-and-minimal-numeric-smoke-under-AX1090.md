# 3329 - Local residual budget input prioritizer and minimal numeric smoke under AX1090

Run UTC: `2026-06-27T20:49:43.473313+00:00`

## Verdict

3329 runs the first numeric smoke on the local residual budget, using `PPN_local_GR` because it is the smallest clean dimensionless arena.

This is **not evidence** and not a PPN pass. The threshold is an illustrative placeholder:

`B_PPN_smoke = 1.0e-05`.

The smoke equation is

`R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN`.

The scenario grid gives 3 pass-like and 3 fail-like nonclaim rows. The useful result is qualitative: if residual floors are zero/tiny, even large `C_PPN` can be tolerable when `epsilon_eff` is small; if `epsilon_composite_PPN`, `R_Gamma_PPN`, or direct vertices have floors near the smoke threshold, the branch fails regardless of the tree term.

So the next mathematical target is not broad wandering. It is `C_PPN` plus the three local floors: `epsilon_eff_PPN`, `epsilon_composite_PPN`, and `R_Gamma_PPN`.

## Source Register

- `SRC3329_0_3328_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3328-Y5-R2FR-local-GR-residual-budget-and-promotion-map-under-AX1090.md` exists=true parse_ok=true role=local residual budget and next target
- `SRC3329_1_3328_budget`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv` exists=true parse_ok=true role=master residual formulas
- `SRC3329_2_3328_arena`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3328_ARENA_PROMOTION_MAP.csv` exists=true parse_ok=true role=arena formulas and blocking inputs
- `SRC3329_3_3328_inputs`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3328_REQUIRED_INPUT_LEDGER.csv` exists=true parse_ok=true role=required input ledger
- `SRC3329_4_3328_claims`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3328_CLAIM_STATUS_LEDGER.csv` exists=true parse_ok=true role=no-public-claim constraints
- `SRC3329_5_3327_envelope`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv` exists=true parse_ok=true role=epsilon_composite envelope
- `SRC3329_6_3327_inputs`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3327_REQUIRED_NUMERIC_INPUTS.csv` exists=true parse_ok=true role=composite numeric inputs

## Arena Selection

- `PPN_local_GR`: selected_for_3329=true; reason=smallest dimensionless smoke route; no range-dependent bound curve or material-composition model required for algebra stress-test; main_formula=R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff^2 + epsilon_composite_PPN + epsilon_direct_PPN; claim_status=NONCLAIM_SMOKE_ONLY; valid_for_claim=false
- `R10_short_range`: selected_for_3329=false; reason=needs claim-ready alpha_bound(lambda), contact/source-size routing, and C_R10(lambda); main_formula=alpha_psi(lambda) <= |R_Gamma_R10| + C_R10 epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda); claim_status=DEFER_UNTIL_BOUND_CURVE_AND_CONTACT_RULE; valid_for_claim=false
- `WEP`: selected_for_3329=false; reason=needs material response Delta q_AB and direct-vertex exclusion or material-tail bounds; main_formula=eta_AB <= |R_Gamma_WEP| + C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP + epsilon_direct_WEP; claim_status=DEFER; valid_for_claim=false
- `clocks_EM_Poynting`: selected_for_3329=false; reason=needs clock normalization and EM/Poynting projection; useful after PPN budget behavior is understood; main_formula=R_clock <= |R_Gamma_clock| + C_clock epsilon_eff^2 + epsilon_EM_tail + epsilon_direct_EM; claim_status=DEFER; valid_for_claim=false
- `orbital_Newton`: selected_for_3329=false; reason=needs orbital threshold table and compact-source projection; good follow-up after PPN response coefficient; main_formula=R_orb <= |R_Gamma_orb| + C_orb epsilon_eff^2 + epsilon_composite_orb; claim_status=DEFER; valid_for_claim=false

## Smoke Priors

- `PRI3329_0_threshold`: quantity=B_PPN_smoke; value=1.000e-05; meaning=illustrative dimensionless PPN residual ceiling for smoke algebra only; source_status=PLACEHOLDER_NOT_EMPIRICAL_CLAIM; valid_for_claim=false
- `PRI3329_1_G_closure`: quantity=epsilon_G_closure; value=0; meaning=measured-G closure is declared for smoke; no derivation of G implied; source_status=CLOSURE_ASSUMPTION; valid_for_claim=false
- `PRI3329_2_direct_vertex`: quantity=epsilon_direct; value=0 unless scenario explicitly turns it on; meaning=clean local branch excludes direct psi-matter/EM vertices; source_status=BRANCH_SIGNATURE; valid_for_claim=false
- `PRI3329_3_ppn_response`: quantity=C_PPN; value=1 to 1e8 grid; meaning=response coefficient sensitivity sweep; source_status=PLACEHOLDER_NONCLAIM; valid_for_claim=false
- `PRI3329_4_residual_floors`: quantity=R_Gamma_PPN and epsilon_composite_PPN; value=0 to 1e-4 scenario grid; meaning=tests whether floor terms dominate before epsilon_eff matters; source_status=PLACEHOLDER_NONCLAIM; valid_for_claim=false

## PPN Numeric Smoke

- `SMOKE3329_0_optimistic_clean`: C_PPN=1.000000e+00; epsilon_eff=1.000000e-10; tree_C_epsilon2=1.000000e-20; epsilon_composite=1.000000e-18; R_Gamma=0.000000e+00; epsilon_direct=0.000000e+00; R_total=1.010000e-18; B_PPN_smoke=1.000000e-05; smoke_pass=true; dominant_term=epsilon_composite; interpretation=nonclaim pass-like smoke; valid_for_claim=false
- `SMOKE3329_1_large_C_tiny_leak`: C_PPN=1.000000e+06; epsilon_eff=1.000000e-06; tree_C_epsilon2=1.000000e-06; epsilon_composite=1.000000e-12; R_Gamma=0.000000e+00; epsilon_direct=0.000000e+00; R_total=1.000001e-06; B_PPN_smoke=1.000000e-05; smoke_pass=true; dominant_term=tree_C_epsilon2; interpretation=nonclaim pass-like smoke; valid_for_claim=false
- `SMOKE3329_2_large_C_danger`: C_PPN=1.000000e+06; epsilon_eff=1.000000e-05; tree_C_epsilon2=1.000000e-04; epsilon_composite=1.000000e-12; R_Gamma=0.000000e+00; epsilon_direct=0.000000e+00; R_total=1.000000e-04; B_PPN_smoke=1.000000e-05; smoke_pass=false; dominant_term=tree_C_epsilon2; interpretation=nonclaim fail-like smoke; valid_for_claim=false
- `SMOKE3329_3_composite_floor_fail`: C_PPN=1.000000e+00; epsilon_eff=1.000000e-08; tree_C_epsilon2=1.000000e-16; epsilon_composite=1.000000e-04; R_Gamma=0.000000e+00; epsilon_direct=0.000000e+00; R_total=1.000000e-04; B_PPN_smoke=1.000000e-05; smoke_pass=false; dominant_term=epsilon_composite; interpretation=nonclaim fail-like smoke; valid_for_claim=false
- `SMOKE3329_4_Gamma_floor_fail`: C_PPN=1.000000e+00; epsilon_eff=1.000000e-08; tree_C_epsilon2=1.000000e-16; epsilon_composite=1.000000e-12; R_Gamma=1.000000e-04; epsilon_direct=0.000000e+00; R_total=1.000000e-04; B_PPN_smoke=1.000000e-05; smoke_pass=false; dominant_term=R_Gamma; interpretation=nonclaim fail-like smoke; valid_for_claim=false
- `SMOKE3329_5_direct_vertex_warning`: C_PPN=1.000000e+02; epsilon_eff=1.000000e-07; tree_C_epsilon2=1.000000e-12; epsilon_composite=1.000000e-10; R_Gamma=0.000000e+00; epsilon_direct=1.000000e-06; R_total=1.000101e-06; B_PPN_smoke=1.000000e-05; smoke_pass=true; dominant_term=epsilon_direct; interpretation=nonclaim pass-like smoke; valid_for_claim=false

## PPN Sensitivity Table

- `SENS3329_C1e+00_F0e+00`: C_PPN=1.000000e+00; fixed_floor=0.000000e+00; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-03; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+00_F1e-12`: C_PPN=1.000000e+00; fixed_floor=1.000000e-12; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-03; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+00_F1e-08`: C_PPN=1.000000e+00; fixed_floor=1.000000e-08; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.160696e-03; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+00_F1e-06`: C_PPN=1.000000e+00; fixed_floor=1.000000e-06; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.000000e-03; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+00_F1e-05`: C_PPN=1.000000e+00; fixed_floor=1.000000e-05; B_PPN_smoke=1.000000e-05; epsilon_eff_max=; status=NO_ROOM_FOR_TREE_TERM; valid_for_claim=false
- `SENS3329_C1e+02_F0e+00`: C_PPN=1.000000e+02; fixed_floor=0.000000e+00; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-04; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+02_F1e-12`: C_PPN=1.000000e+02; fixed_floor=1.000000e-12; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-04; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+02_F1e-08`: C_PPN=1.000000e+02; fixed_floor=1.000000e-08; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.160696e-04; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+02_F1e-06`: C_PPN=1.000000e+02; fixed_floor=1.000000e-06; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.000000e-04; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+02_F1e-05`: C_PPN=1.000000e+02; fixed_floor=1.000000e-05; B_PPN_smoke=1.000000e-05; epsilon_eff_max=; status=NO_ROOM_FOR_TREE_TERM; valid_for_claim=false
- `SENS3329_C1e+04_F0e+00`: C_PPN=1.000000e+04; fixed_floor=0.000000e+00; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-05; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+04_F1e-12`: C_PPN=1.000000e+04; fixed_floor=1.000000e-12; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-05; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+04_F1e-08`: C_PPN=1.000000e+04; fixed_floor=1.000000e-08; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.160696e-05; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+04_F1e-06`: C_PPN=1.000000e+04; fixed_floor=1.000000e-06; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.000000e-05; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+04_F1e-05`: C_PPN=1.000000e+04; fixed_floor=1.000000e-05; B_PPN_smoke=1.000000e-05; epsilon_eff_max=; status=NO_ROOM_FOR_TREE_TERM; valid_for_claim=false
- `SENS3329_C1e+06_F0e+00`: C_PPN=1.000000e+06; fixed_floor=0.000000e+00; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-06; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+06_F1e-12`: C_PPN=1.000000e+06; fixed_floor=1.000000e-12; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-06; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+06_F1e-08`: C_PPN=1.000000e+06; fixed_floor=1.000000e-08; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.160696e-06; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+06_F1e-06`: C_PPN=1.000000e+06; fixed_floor=1.000000e-06; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.000000e-06; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+06_F1e-05`: C_PPN=1.000000e+06; fixed_floor=1.000000e-05; B_PPN_smoke=1.000000e-05; epsilon_eff_max=; status=NO_ROOM_FOR_TREE_TERM; valid_for_claim=false
- `SENS3329_C1e+08_F0e+00`: C_PPN=1.000000e+08; fixed_floor=0.000000e+00; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-07; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+08_F1e-12`: C_PPN=1.000000e+08; fixed_floor=1.000000e-12; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.162278e-07; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+08_F1e-08`: C_PPN=1.000000e+08; fixed_floor=1.000000e-08; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.160696e-07; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+08_F1e-06`: C_PPN=1.000000e+08; fixed_floor=1.000000e-06; B_PPN_smoke=1.000000e-05; epsilon_eff_max=3.000000e-07; status=SMOKE_THRESHOLD_FORMULA; valid_for_claim=false
- `SENS3329_C1e+08_F1e-05`: C_PPN=1.000000e+08; fixed_floor=1.000000e-05; B_PPN_smoke=1.000000e-05; epsilon_eff_max=; status=NO_ROOM_FOR_TREE_TERM; valid_for_claim=false

## Input Priority

- `1`: input=C_PPN response coefficient; why_first=tree term scales as C_PPN epsilon_eff^2; without C_PPN every epsilon_eff result is floating; next_action=derive/bound PPN projection coefficient from C_i operator formula; valid_for_claim=false
- `2`: input=epsilon_eff_PPN; why_first=even large C_PPN is harmless if epsilon_eff is tiny; this controls the main tree channel; next_action=turn ell_s/epsilon_bg/boundary/aniso into a local PPN bound; valid_for_claim=false
- `3`: input=epsilon_composite_PPN floor; why_first=composite floor can fail the smoke even when tree leakage is tiny; next_action=instantiate 3327 composite envelope for PPN; valid_for_claim=false
- `4`: input=R_Gamma_PPN floor; why_first=any unsuppressed local Gamma/saturation residual dominates immediately; next_action=derive local Gamma silence or a conservative PPN bound; valid_for_claim=false
- `5`: input=claim-ready PPN threshold table; why_first=needed before converting smoke into a test, but algebra can be stress-tested first; next_action=source real PPN bounds only after coefficient side is less foggy; valid_for_claim=false

## Decision Ledger

- `DEC3329_0`: question=Which arena should be smoked first?; answer=PPN_local_GR; reason=it uses the master local residual budget with dimensionless coefficients and avoids R10 range/contact data for the first stress-test; next_action=derive C_PPN and epsilon_eff_PPN before using real PPN data; valid_for_claim=false
- `DEC3329_1`: question=What did the smoke reveal?; answer=floors matter as much as tree leakage; reason=large C_PPN can be tolerated if epsilon_eff is sufficiently small, but composite/Gamma/direct floors can fail immediately; next_action=prioritize C_PPN, epsilon_eff, then composite/Gamma floors; valid_for_claim=false
- `DEC3329_2`: question=Can any smoke pass be used as evidence?; answer=no; reason=threshold and coefficients are placeholders; every row is valid_for_claim=false; next_action=use this only as a coefficient prioritizer; valid_for_claim=false

## Next Target

- `3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md`: target_script=scripts/Y5_R2FR_3330_PPN_response_coefficient_and_local_floor_bound.py; objective=derive or bound C_PPN and the local PPN floor terms R_Gamma_PPN, epsilon_eff_PPN, and epsilon_composite_PPN so the 3329 smoke budget can stop using placeholders; must_include=C_i to C_PPN projection; epsilon_eff_PPN from smoothing/boundary/aniso; composite PPN envelope; Gamma local silence or floor; no real PPN claim yet; fallback_if_failed=keep PPN as symbolic sensitivity and move to R10 data-bound acquisition only after C_i behavior is clearer; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- All thresholds and coefficients are smoke placeholders.
- Pass-like rows are not evidence; fail-like rows are diagnostic only.
- The purpose is input prioritization for the local residual budget.
- `formalization-workbench` is not modified.
