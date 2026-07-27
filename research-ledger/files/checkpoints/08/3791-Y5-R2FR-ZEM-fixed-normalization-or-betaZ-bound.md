# 3791 - Z_EM Fixed Normalization or beta_Z Bound

## Status

`ZEM_ZERO_CONDITIONAL_UNIQUE_F2_NOT_DERIVED_BETAZ_LAMBDA_RETAINED`.

3791 isolates the exact Z_EM theorem: beta_Z,A vanishes only if q_* is superselected, the parent generator norm/Maxwell subblock is fixed, and independent F^2 operators are forbidden. Current corpus does not ban F^2, so beta_Z,A and lambda_A remain nonclaim finite residuals. Alpha_EM is still not derived.

## Result In Plain Terms

3791 takes the dangerous Maxwell-normalization step and refuses the easy lie. `Z_EM` can be fixed only if the parent branch supplies a nonrescalable generator norm, a unique Maxwell kinetic subblock, no independent `F^2` slot, and no readout/current re-entry. The current corpus does not have that: ordinary covariance and U(1) gauge invariance allow `F^2`, and prior checkpoints already kept this as a counterexample. So `beta_Z,A`, `lambda_A`, hidden `f(Xhat)F^2`, and alpha-readout leakage stay live finite residuals.

## Compact Result

`beta_Z,A := Lie_EA ln Z_EM`.

Conditional zero: `beta_Z,A=0` if `q_*` is fixed, parent `C_P/N_Q` are fixed, no independent `F^2` operator exists, and readout/current normalization descends.

Current-corpus verdict: ordinary symmetries allow `lambda_A F^2` and `f(Xhat)F^2`, so `beta_Z,A` is not claim-zero.

Alpha guard: even abstract `Z_EM` silence does not prove observed `alpha_EM` unless Hodge/coframe, `hbar*c`, spectroscopy, and current normalization descend too.

## Z_EM Fixed-Normalization Theorem
- `ZFT3791_0_definition` `Z_EM vertical coefficient`: mathematical_form: beta_Z,A := Lie_EA ln Z_EM, with Z_EM=Z_Pi/q_*^2 or Z_EM=C_P N_Q/q_*^2 plus retained counterterms if allowed.; derivation_status: DEFINITION_FROM_3784_3790; missing_for_current_claim: parent-owned Z_Pi/C_P/N_Q and no independent F^2 coefficient; if_unsigned: retain beta_Z,A and lambda_A rows
- `ZFT3791_1_conditional_zero` `beta_Z,A=0`: mathematical_form: If q_* is superselected, C_P is quotient-owned/superselected, N_Q is fixed by a nonrescalable parent generator norm, and no independent lambda_A F^2 or f(Xhat)F^2 operator exists, then Lie_EA Z_EM=0.; derivation_status: EXACT_CONDITIONAL_THEOREM; missing_for_current_claim: fixed parent generator norm; unique Maxwell subblock; operator-domain exhaustion; readout/current owner; if_unsigned: Z_EM remains a finite coefficient branch
- `ZFT3791_2_lambda_counterterm` `independent Maxwell kinetic coefficient`: mathematical_form: If DeltaS=-lambda_A/4 int sqrt(-g_eff) F_obs^2 is legal, then Z_EM=Z_parent+lambda_A and beta_Z,A receives Lie_EA ln(Z_parent+lambda_A).; derivation_status: COUNTEREXAMPLE_GUARD; missing_for_current_claim: no-independent-F2 proof; if_unsigned: lambda_A and beta_Z,A must be bounded, not set to zero
- `ZFT3791_3_alpha_readout` `alpha_EM ownership`: mathematical_form: Even beta_Z,A=0 is not a full alpha_EM theorem unless observed Hodge/coframe, hbar*c, current normalization, and spectroscopy/readout also descend through q_obs.; derivation_status: OVERCLAIM_GUARD; missing_for_current_claim: readout descent and same-current/source ownership; if_unsigned: retain b_alpha/readout/current residuals

## Current Corpus Z_EM Signature Audit
- `ZA3791_0_3784_ZEM`: source_signal: 3784 names Z_EM=Z_Pi/q_*^2=C_Q N_Q and keeps Z_EM zero condition unsigned; current_result: ZEM_OWNER_UNSIGNED; impact: cannot promote beta_Z,A=0 in strict current-corpus mode
- `ZA3791_1_3790_qstar`: source_signal: 3790 conditionally zeroes q_* drift but explicitly says this does not derive Z_EM/alpha; current_result: QSTAR_HELPFUL_BUT_INSUFFICIENT; impact: q_* branch removes denominator drift only; numerator normalization remains live
- `ZA3791_2_1056_norm`: source_signal: 1056 says compact U(1) fixes charge labels but not continuous Maxwell kinetic coefficient; current_result: COMPACTNESS_NOT_ENOUGH; impact: requires fixed generator norm plus unique F2 inheritance
- `ZA3791_3_1057_unique_F2`: source_signal: 1057 states exact no-independent-F2 theorem but current corpus fails because gauge/diffeomorphism allow F2; current_result: UNIQUE_F2_NOT_DERIVED; impact: lambda_A/f(Xhat)F2 counterterms remain legal
- `ZA3791_4_1049_operator`: source_signal: 1049 operator classification says ordinary symmetries do not forbid f_X F2; stronger product/sequester rule is unsigned; current_result: OPERATOR_DOMAIN_EXHAUSTION_MISSING; impact: cannot remove beta_Z/lambda by ordinary covariance or gauge invariance
- `ZA3791_5_verdict`: source_signal: sources jointly support theorem shape and jointly block current promotion; current_result: CONDITIONAL_THEOREM_PLUS_RETAINED_BOUND_BRANCH; impact: emit zero branch only as parent-extension theorem; retain bound rows for current corpus

## Operator-Basis Counterexample Guard
- `CTG3791_0_covariant_F2` `lambda_A F_obs^2`: ordinary_symmetry_status: ALLOWED_BY_DIFF_AND_U1; effect: adds an independent contribution to Z_EM and can carry vertical drift; repair_needed: parent operator-domain exhaustion or unique curvature-norm inheritance
- `CTG3791_1_hidden_scalar_F2` `f(Xhat) F_obs^2`: ordinary_symmetry_status: ALLOWED_IF_XHAT_IS_VISIBLE_SCALAR_OR_COEFFICIENT_MARKER; effect: direct beta_Z,A/b_alpha leakage and WEP/clock/R10 pressure; repair_needed: hidden-visible product/sequester theorem plus radiative closure
- `CTG3791_2_generator_rescale` `T_Q -> s T_Q, A_Q -> A_Q/s, current labels compensate`: ordinary_symmetry_status: CONVENTIONAL_UNLESS_PARENT_NORM_FIXED; effect: N_Q and current normalization are not physical until parent norm/current owner is fixed; repair_needed: nonrescalable parent generator norm and same-current owner
- `CTG3791_3_readout_leak` `Hodge/coframe/hbar*c/spectroscopy readout drift`: ordinary_symmetry_status: SEPARATE_FROM_ABSTRACT_ZEM; effect: alpha_EM can drift even if abstract Z_EM is fixed; repair_needed: q_obs-owned observed readout and clock/source descent

## beta_Z/lambda Zero or Bound Components
- `BZ3791_0_beta_ZA` `beta_Z,A`: definition: Lie_EA ln Z_EM; zero_if: q_* superselected, parent C_P/N_Q fixed, no independent F^2 operator, and readout/current normalization does not reintroduce vertical drift; conditional_value: 0; fallback_value: MISSING_BETA_ZA_OR_PARENT_ZERO_THEOREM; feeds: delta_A S_EM;epsilon_alpha_source;WEP;clock;Gdot;PPN; status: CONDITIONAL_ZERO_CURRENTLY_UNSIGNED
- `BZ3791_1_lambda_A` `lambda_A`: definition: coefficient of independent observed/pullback Maxwell kinetic operator outside parent curvature norm; zero_if: operator-domain exhaustion forbids lambda_A F_obs^2 including effective/radiative re-entry; conditional_value: 0; fallback_value: MISSING_LAMBDA_A_PRIOR_OR_OPERATOR_BAN; feeds: delta_A S_EM;alpha_EM;clock;WEP;R10; status: LEGAL_UNLESS_PARENT_DOMAIN_EXCLUDES
- `BZ3791_2_fX_F2` `b_Z_hidden`: definition: vertical derivative of hidden scalar gauge kinetic function f(Xhat)F_obs^2; zero_if: hidden-visible product/sequester theorem forbids Xhat-dependent visible kinetic coefficients; conditional_value: 0; fallback_value: MISSING_FX_F2_PRIOR_OR_SEQUESTER_THEOREM; feeds: beta_Z,A;b_alpha;WEP;clock;R10; status: LEGAL_UNLESS_PRODUCT_FUNCTOR_SIGNED
- `BZ3791_3_b_alpha_readout` `b_alpha_readout`: definition: residual vertical derivative of observed dimensionless alpha readout after abstract Z_EM is fixed; zero_if: observed coframe/Hodge/hbar*c/spectroscopy readout descends through q_obs; conditional_value: 0; fallback_value: MISSING_ALPHA_READOUT_DESCENT_OR_BOUND; feeds: clock;atomic_spectra;WEP_source_alpha; status: SEPARATE_READOUT_GATE

## EM Action and Alpha Update
- `EAU3791_0_current_action_leak` `finite_current_corpus`: formula: delta_A S_EM contains beta_Z,A F^2, dR_A, J_Q dot R_A, and lambda_A contributions; conditions: Z_EM owner and no-independent-F2 are unsigned; status: RETAINED_BOUND_FORM
- `EAU3791_1_ZEM_zero_branch` `ZEM_fixed_parent_extension`: formula: beta_Z,A=0 removes the universal Maxwell-normalization leak from delta_A S_EM; conditions: q_* superselected, C_P/N_Q fixed, no independent F^2, no readout/current re-entry; status: CONDITIONAL_SIMPLIFICATION
- `EAU3791_2_lambda_block` `operator_domain_unsigned`: formula: Z_EM=Z_parent+lambda_A or Z_parent+f(Xhat), so beta_Z,A is not zero by compactness/topology alone; conditions: independent F^2 slot remains legal; status: CURRENT_CORPUS_BLOCKER
- `EAU3791_3_alpha_status` `alpha_readout`: formula: alpha_EM silence requires Z_EM silence plus observed readout descent; Z_EM theorem alone is not enough; conditions: Hodge/coframe/hbar*c/spectroscopy/current normalization separate; status: ALPHA_REMAINS_NONCLAIM

## Claim Gates
- `CG3791_0_sources`: pass: True; claim_allowed: False; details: all cited source paths resolve
- `CG3791_1_ZEM_theorem_shape`: pass: True; claim_allowed: False; details: exact conditional Z_EM fixed-normalization theorem emitted
- `CG3791_2_current_ZEM_signed`: pass: False; claim_allowed: False; details: current corpus lacks fixed generator norm, unique F2 operator-domain exhaustion, and readout/current owner
- `CG3791_3_independent_F2_banned`: pass: False; claim_allowed: False; details: ordinary covariance and U1 gauge invariance allow F2; stronger parent domain theorem is unsigned
- `CG3791_4_betaZ_bound_rows`: pass: True; claim_allowed: False; details: beta_Z/lambda_A/fX/readout bound rows emitted as nonclaim fallbacks
- `CG3791_5_alpha_claim`: pass: False; claim_allowed: False; details: alpha_EM ownership is not derived from Z_EM theorem alone
- `CG3791_6_local_GR_EM_claim`: pass: False; claim_allowed: False; details: no local-GR/EM claim; Maxwell normalization remains finite unless upstream operator-domain gates close

## Decisions
- `DEC3791_0_theorem_shape`: decision: Z_EM can be theorem-zero only under fixed parent normalization plus no independent F2.; action: Keep the exact conditional theorem, but do not promote it in strict current-corpus mode.
- `DEC3791_1_current_failure`: decision: The current corpus cannot ban lambda_A F^2 or f(Xhat)F^2 using ordinary symmetry.; action: Retain beta_Z,A, lambda_A, and hidden scalar F2 rows as finite residuals.
- `DEC3791_2_alpha_honesty`: decision: Even a Z_EM zero theorem would not by itself derive observed alpha_EM.; action: Keep readout/current/Hodge/spectroscopy descent as separate gates.
- `DEC3791_3_next`: decision: The next concrete route is same-current owner or operator-domain exhaustion; same-current is closer to local GR/Newton source coupling.; action: Try the same-source charged-current/Ward/Hilbert-stress owner before returning to the harder B_Q owner.

## Next Target
- `3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md`: target_script: scripts/Y5_R2FR_3792_same_current_Ward_Hilbert_stress_owner_or_epsilonJ_bound.py; objective: Try to prove J_Q, charged matter, EM stress, and binding stress descend from the same q_obs total source action so epsilon_J_Q=0 and EM Hilbert stress can enter Pi_M_total; if it fails, emit source-ready epsilon_J_Q/source-current bound rows.

## Validation
- `sources_exist` `PASS`: detail: every cited source path exists
- `csv_outputs_parse` `PASS`: detail: all generated CSV outputs exist and parse
- `doc_written` `PASS`: detail: 3791 markdown document written
- `zem_theorem` `PASS`: detail: conditional Z_EM theorem emitted
- `f2_counterterm_guard` `PASS`: detail: independent F2 counterterm guard emitted
- `current_failure_retained` `PASS`: detail: current no-independent-F2 failure retained
- `betaz_rows` `PASS`: detail: beta_Z/lambda/readout rows emitted
- `alpha_claim_closed` `PASS`: detail: alpha claim remains closed
- `next_target` `PASS`: detail: 3792 same-current target emitted
- `formalization_clean` `PASS`: detail: no 3791 files written under formalization-workbench
