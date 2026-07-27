# 3789 - B_Q First Norm and Patch Convention or Field-Map Fill

## Status

`PATCH_NORM_CONVENTION_DEFINED_CHART_ZERO_CONDITIONAL_OWNER_BLOCKED_RANK_MAP_FORMAL`.

3789 defines the first honest local patch/norm convention for R_A and dR_A, gives a conditional chart/Wilson local zero theorem on defect-free contractible patches, converts rank into a formal distance-to-rank-class residual, and keeps owner as the hard missing parent-field blocker. It is not a local-GR/EM claim.

## Result In Plain Terms

3789 does not pretend to finish EM/local GR. It does something narrower but important: it defines the local patch and positive norm convention that the `R_A` and `dR_A` residuals must use, conditionally zeros pure chart/Wilson residue on a defect-free contractible patch, turns rank into a formal curvature-distance residual, and keeps owner failure as the hard parent-field blocker. That means future rows can be scored without inventing arbitrary coefficients, but the actual component amplitudes are still not claimable.

## Compact Contract

`U_good`: local, defect-free, geodesically convex, `H1(U)=0`, with compact support weight `w_U`.

`||a||_A^2 = int_U w_U |a|_h^2 dV_h / int_U w_U dV_h` for one-forms.

`||f||_F^2 = int_U w_U |f|_h^2 dV_h / int_U w_U dV_h` for two-forms.

`A_ref=max(||A_obs||_A,A_floor)` and `F_ref=max(||F_obs||_F,F_floor)`.

On `U_good`, `R_chart` is pure local gauge and `dR_chart=0`; outside `U_good`, chart/Wilson residue remains live.

`eps_rank_H=dist_F(H_req,R_rank(U))/F_ref`, with `H_req=-q_* F_obs`.

## Patch and Norm Convention
- `PATCH3789_0_U_good_patch` `U_good`: definition: U is an open local test patch inside M minus defect/node support, chosen geodesically convex for g_eff, with H1(U)=0 and fixed compact support weight w_U; mathematical_status: DEFINED_CONDITIONAL_PATCH_CONTRACT; numeric_status: MISSING_ACTUAL_ARENA_DOMAIN; claim_effect: local chart/Wilson residues can be zeroed only inside such a patch
- `PATCH3789_1_positive_norm_metric` `h_eff(u_obs)`: definition: positive local norm metric built from observed frame u_obs, e.g. h_ab=g_eff_ab+2 u_a u_b for signature -+++; use h_eff for amplitude norms instead of indefinite Lorentzian contraction; mathematical_status: DEFINED_NORM_CONVENTION; numeric_status: MISSING_U_OBS_AND_GEFF_COMPONENTS; claim_effect: prevents fake negative/zero field norms from Lorentzian signature
- `PATCH3789_2_A_norm` `||a||_A`: definition: sqrt( int_U w_U |a|^2_h dV_h / int_U w_U dV_h ) for one-forms a; mathematical_status: DEFINED_NORM_CONVENTION; numeric_status: MISSING_FIELD_PROFILE_AND_WEIGHT; claim_effect: sets the response norm used by eps_BQ_descent_A, eps_BQ_chart_A, and eps_qA
- `PATCH3789_3_F_norm` `||f||_F`: definition: sqrt( int_U w_U |f|^2_h dV_h / int_U w_U dV_h ) for two-forms f; equivalently local positive E/B amplitude in u_obs split; mathematical_status: DEFINED_NORM_CONVENTION; numeric_status: MISSING_FIELD_PROFILE_AND_WEIGHT; claim_effect: sets the response norm used by eps_dBQ_A, eps_dchart_A, eps_betaqF, eps_dbetaqA, and eps_rank_H
- `PATCH3789_4_A_ref` `A_ref`: definition: A_ref=max(||A_obs||_A,A_floor); if ||A_obs||_A>0, self-normalization is allowed; otherwise A_floor must be sourced; mathematical_status: DEFINED_REFERENCE_CONVENTION; numeric_status: MISSING_A_OBS_PROFILE_OR_A_FLOOR; claim_effect: blocks division-by-zero and separates proof patches from measurement-floor patches
- `PATCH3789_5_F_ref` `F_ref`: definition: F_ref=max(||F_obs||_F,F_floor); if ||F_obs||_F>0, self-normalization is allowed; otherwise F_floor must be sourced; mathematical_status: DEFINED_REFERENCE_CONVENTION; numeric_status: MISSING_F_OBS_PROFILE_OR_F_FLOOR; claim_effect: blocks division-by-zero and separates proof patches from measurement-floor patches
- `PATCH3789_6_floor_policy` `A_floor,F_floor`: definition: floors may be instrument/noise floors, regularity cutoffs, or arena-declared minimum reference amplitudes; they cannot be fitted after seeing the target bound; mathematical_status: DEFINED_ANTI_FIT_POLICY; numeric_status: MISSING_SOURCE_BACKED_FLOORS; claim_effect: keeps tiny-field/vacuum patches from producing fake finite scores

## Chart/Wilson Local Zero Conditions
- `CHART3789_0_local_zero_theorem`: condition: U is contractible, H1(U)=0, local bundle trivialization exists, and defect/Wilson support is outside U; result: R_chart=d chi is pure local gauge and can be set to zero for the local response calculation; dR_chart=0; component_effect: eps_BQ_chart_A=0 and eps_dchart_A=0 conditionally on U_good; status: CONDITIONAL_LOCAL_THEOREM
- `CHART3789_1_nonlocal_residue`: condition: U has nontrivial cycles, crosses a defect/node, or needs multiple chart overlaps with nonzero Wilson data; result: chart/Wilson residue is physical/topological until its cycles are owned or bounded; component_effect: eps_BQ_chart_A and eps_dchart_A remain live bound rows; status: GLOBAL_OR_DEFECT_BLOCKER
- `CHART3789_2_no_smuggling_rule`: condition: local chart zero is used; result: the zero applies only to chart/Wilson bookkeeping, not to B_Q descent, q_* variation, Z_EM, same-current descent, or rank/owner failures; component_effect: prevents using local trivialization as a fake EM derivation; status: ACTIVE_GUARD

## Owner Field Map Attempt
- `OWNER3789_0_field_map_definition` `Delta B_owner`: definition: Delta B_owner := B_Q - B_owned[Y_Q] on U, with eps_owner_B=||Delta B_owner||_A/A_ref; requirement: a parent-owned field class Y_Q and a non-circular operator B_owned[Y_Q] built without A_obs,F_obs,Maxwell equations, or Lorentz force; current_status: MISSING_OWNED_FIELD_CLASS_AND_OPERATOR; claim_effect: owner absence remains a model-class blocker until this map exists
- `OWNER3789_1_distance_class_fallback` `dist_A(B_Q,Owned_B)`: definition: eps_owner_dist := inf_{B in Owned_B(U)} ||B_Q-B||_A/A_ref; requirement: Owned_B(U) must be specified by the parent action before the infimum is meaningful; current_status: FORMAL_ONLY_NOT_COMPUTABLE; claim_effect: useful future bound shape, but not a present score
- `OWNER3789_2_zero_route` `owner_zero`: definition: if B_Q=B_owned[Y_Q] and Lie_EA Y_Q=0 modulo chart gauge, then eps_owner_B=0 and B_Q descent becomes a theorem target; requirement: parent-signed Y_Q or CP2/Berry multiplet plus q_obs descent; current_status: CONDITIONAL_NOT_SIGNED; claim_effect: shows exact route to closure without treating owner as a fitted coefficient

## Rank Field Map Attempt
- `RANK3789_0_field_distance` `eps_rank_H`: definition: eps_rank_H := dist_F(H_req,R_rank(U))/F_ref, where H_req=-q_* F_obs and R_rank(U) is the allowed curvature class generated by the chosen B_Q branch; requirement: F_obs profile or symbolic target class, q_*, F_ref, and chosen rank class; current_status: FORMAL_FIELD_MAP_DEFINED_NUMERIC_INPUTS_MISSING; claim_effect: rank is no longer just a word; it becomes a curvature-distance residual once inputs exist
- `RANK3789_1_one_pair_gate` `R_rank_one_pair`: definition: one Clebsch pair gives H=dC wedge dD, hence H wedge H=0; any H_req with nonzero H_req wedge H_req cannot be exactly represented by one pair; requirement: evaluate H_req wedge H_req on U or prove it vanishes in the tested sector; current_status: GENERIC_EM_BLOCKS_ONE_PAIR_EXACTNESS; claim_effect: single-pair route is rejected for generic local EM unless the sector is null/simple
- `RANK3789_2_two_pair_gate` `R_rank_two_pair_or_CP2`: definition: two Clebsch pairs or a CP2/Berry-equivalent internal multiplet can represent a generic local closed two-form by Darboux/Clebsch on a good patch; requirement: parent-owned two-pair coordinates or CP2/Berry multiplet, plus chart covariance; current_status: RANK_ROUTE_OK_OWNER_ROUTE_MISSING; claim_effect: rank obstruction can be zero in the two-pair route, but only after owner is supplied
- `RANK3789_3_lower_bound_guard` `wedge_defect_lower_bound`: definition: nonzero H_req wedge H_req is a one-way certificate that one-pair exactness fails; converting it to a numeric lower bound needs the chosen F_norm and a norm-equivalence constant; requirement: norm-specific constant and field profile; current_status: CERTIFICATE_AVAILABLE_NUMERIC_BOUND_MISSING; claim_effect: prevents calling one-pair approximate success without a quantitative residual

## Updated R_A/dR_A Component Ledger
- `COMP3789_0_eps_BQ_descent_A` `eps_BQ_descent_A`: definition: ||q_*^-1 Lie_EA B_Q||_A/A_ref; 3789_update: norm convention defined; component value still requires B_Q vertical descent amplitude or zero theorem; status: LIVE_NUMERIC_MISSING
- `COMP3789_1_eps_BQ_chart_A` `eps_BQ_chart_A`: definition: ||R_chart||_A/A_ref; 3789_update: conditionally zero on U_good with H1(U)=0 and no defect/Wilson support; status: CONDITIONAL_LOCAL_ZERO_OR_LIVE_GLOBAL_RESIDUE
- `COMP3789_2_eps_qA` `eps_qA`: definition: |beta_q,A| ||A_obs||_A/A_ref; 3789_update: norm convention defined; next low-cost zero route is q_* superselection/charge-lattice ownership; status: LIVE_UNTIL_BETA_Q_ZERO_OR_BOUND
- `COMP3789_3_eps_dBQ_A` `eps_dBQ_A`: definition: ||q_*^-1 d(Lie_EA B_Q)||_F/F_ref; 3789_update: norm convention defined; component value still requires differential B_Q descent amplitude; status: LIVE_NUMERIC_MISSING
- `COMP3789_4_eps_dchart_A` `eps_dchart_A`: definition: ||dR_chart||_F/F_ref; 3789_update: conditionally zero on U_good; remains live for global/defect cycles; status: CONDITIONAL_LOCAL_ZERO_OR_LIVE_GLOBAL_RESIDUE
- `COMP3789_5_eps_betaqF` `eps_betaqF`: definition: |beta_q,A| ||F_obs||_F/F_ref; 3789_update: norm convention defined; next low-cost zero route is q_* superselection/charge-lattice ownership; status: LIVE_UNTIL_BETA_Q_ZERO_OR_BOUND
- `COMP3789_6_eps_dbetaqA` `eps_dbetaqA`: definition: ||d beta_q,A wedge A_obs||_F/F_ref; 3789_update: zero if q_* is superselected or beta_q,A is constant on U; otherwise needs field profile; status: LIVE_UNTIL_BETA_Q_CONSTANT_ZERO_OR_BOUND
- `COMP3789_7_eps_rank_H` `eps_rank_H`: definition: dist_F(H_req,R_rank(U))/F_ref; 3789_update: formal field-valued map defined; numeric value requires H_req/F_obs, rank class, and F_ref; status: FORMAL_MAP_DEFINED_NUMERIC_MISSING
- `COMP3789_8_eps_owner_B` `eps_owner_B`: definition: ||B_Q-B_owned[Y_Q]||_A/A_ref or dist_A(B_Q,Owned_B)/A_ref; 3789_update: formal route defined but current corpus lacks Owned_B and B_owned[Y_Q]; status: MODEL_CLASS_BLOCKER_UNTIL_PARENT_OWNER_SUPPLIED

## Claim Gates
- `CG3789_0_sources`: pass: True; claim_allowed: False; details: all cited local source paths resolve
- `CG3789_1_patch_norm_contract`: pass: True; claim_allowed: False; details: U_good, h_eff, A_norm, F_norm, A_ref, F_ref, and floor policy are now defined as a mathematical convention
- `CG3789_2_chart_local_zero`: pass: True; claim_allowed: False; details: chart/Wilson residue is conditionally zero on a contractible defect-free local patch only
- `CG3789_3_owner_field_map`: pass: False; claim_allowed: False; details: owner field map needs parent-owned Y_Q or Owned_B class; current corpus does not supply it
- `CG3789_4_rank_field_map`: pass: True; claim_allowed: False; details: rank residual can be represented as dist_F(H_req,R_rank)/F_ref, but numeric inputs are missing
- `CG3789_5_numeric_score_ready`: pass: False; claim_allowed: False; details: actual arena domains, field profiles, floors, owner map, beta_q, and rank distances are not numeric/source-backed
- `CG3789_6_local_GR_EM_claim`: pass: False; claim_allowed: False; details: no local-GR/EM claim; 3789 defines the scoring convention and one conditional chart zero only

## Decisions
- `DEC3789_0_norm_progress`: decision: The first local norm convention is now defined without relying on indefinite Lorentzian amplitudes.; action: Use U_good, h_eff(u_obs), weighted local L2 norms, and A_ref/F_ref in future RA/dRA rows.
- `DEC3789_1_chart_progress`: decision: Chart/Wilson residues can be conditionally zeroed for a defect-free contractible local patch.; action: Do not use this local zero for global/topological claims or to hide B_Q descent, q_*, Z_EM, owner, or rank failures.
- `DEC3789_2_owner_rank`: decision: Rank can be made field-valued by a distance-to-rank-class map; owner cannot be scored until the owned B_Q class exists.; action: Keep owner as the hard blocker and use the rank distance map only as a formal nonclaim residual until inputs exist.
- `DEC3789_3_next`: decision: The next cheapest real derivation target is q_* superselection because it could zero eps_qA, eps_betaqF, and eps_dbetaqA.; action: Attempt a compact-charge-lattice q_* zero theorem; if it fails, emit beta_q bound rows.

## Next Target
- `3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md`: target_script: scripts/Y5_R2FR_3790_charge_unit_superselection_or_betaq_bound.py; objective: Try to prove Lie_EA q_*=0 and d beta_q,A=0 from compact U(1) charge-lattice/superselection structure; otherwise emit source-ready beta_q bound rows for eps_qA, eps_betaqF, and eps_dbetaqA.

## Validation
- `sources_exist` `PASS`: detail: every cited source path exists
- `csv_outputs_parse` `PASS`: detail: all generated CSV outputs exist and parse
- `doc_written` `PASS`: detail: 3789 markdown document written
- `patch_norm_defined` `PASS`: detail: patch and norm conventions emitted
- `chart_local_zero_conditional` `PASS`: detail: conditional local chart/Wilson zero theorem emitted
- `owner_remains_blocked` `PASS`: detail: owner map remains honestly blocked
- `rank_distance_map` `PASS`: detail: rank field-distance map emitted
- `claim_gate_closed` `PASS`: detail: local GR/EM claim remains closed
- `next_target` `PASS`: detail: 3790 q-star target emitted
- `formalization_clean` `PASS`: detail: no 3789 files written under formalization-workbench
