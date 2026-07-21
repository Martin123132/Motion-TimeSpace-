# 4520 - Rank-Zero Source Current Silence Or Alpha Input Acquisition

Marker: `PPC4161_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520`

Decision: `RANK_ZERO_HILBERT_SOURCE_CURRENT_SILENCE_DERIVED_CONDITIONALLY_BOUNDARY_CDB_READOUT_STILL_LIVE`

## Result

4520 takes the actual derivation route first. 4519 left the rank-zero algebraic branch as

`M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector`.

The new move is to split `J_A` rather than treating it as a foggy missing coefficient:

`J_A = J_A^Hilbert + J_A^EM/Poynting + J_A^retained`.

The conditional theorem is:

`S_src = Sbar_src[q(Phi), Psi, theta]`, `v_A in ker(Dq)`, no explicit vertical action on matter standards, and a stationary no-flux worldtube imply

`J_A^Hilbert = 0`, and Hilbert-owned EM/Poynting flow is not a separate bulk vertical current.

So the rank-zero equation is reduced to

`M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A^src/readout/projector`.

That is forward motion: the ordinary Hilbert/Poynting worry is conditionally neutralized. It is not a local-GR claim because the retained current, boundary/corner, CDB and readout gates still need their own derivations.

## Source Register

| checkpoint | source_id | role | path | exists | needle | needle_found | line | note | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4520 | SRC4520_00_formal4519 | 4519 formal branch split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\535-PPC4161-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md | True | PPC4161_BULK_RANGE_ALPHA_CURVE_INPUT_FILL_OR_RANK_ZERO_CONSTRAINT_4519 | True | 3 | finite/rank-zero classifier handoff | False |
| 4520 | SRC4520_01_post4519 | 4519 post next target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4519-Y5-R2FR-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md | True | NT4519_0 | True | 132 | declares rank-zero source-current target | False |
| 4520 | SRC4520_02_rzr4519 | 4519 rank-zero RHS map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv | True | RZR4519_1_J | True | 3 | source current component in RHS | False |
| 4520 | SRC4520_03_branch4519 | 4519 branch status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4519_BRANCH_STATUS.csv | True | BST4519_1_rank_zero | True | 3 | rank-zero theorem ready but unsigned | False |
| 4520 | SRC4520_04_alpha4519 | 4519 alpha fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4519_ALPHA_LAMBDA_INPUT_CONTRACT.csv | True | AIC4519_2_Qsource | True | 4 | finite-range input fallback | False |
| 4520 | SRC4520_05_formal4515 | 4515 source functor prose | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\531-PPC4161-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md | True | PPC4161_Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR_4515 | True | 3 | source functor descent theorem | False |
| 4520 | SRC4520_06_sft4515 | 4515 source functor theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv | True | SFT4515_4_EM_Poynting_guard | True | 6 | Poynting/Hilbert guard | False |
| 4520 | SRC4520_07_scv4515 | 4515 coupling vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv | True | SCV4515_2_Jmem_EM_Poynting | True | 4 | EM/Poynting flux channel | False |
| 4520 | SRC4520_08_ward | source-current Ward contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv | True | SC4_no_nonHilbert_source_current | True | 6 | non-Hilbert current gate | False |
| 4520 | SRC4520_09_owner | source-owner action contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv | True | A2_no_retained_source_constraint | True | 4 | retained source exclusion | False |
| 4520 | SRC4520_10_hilbert_div | Hilbert divergence identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv | True | DIV2467_4_Killing_clock | True | 6 | stationary Hilbert current route | False |
| 4520 | SRC4520_11_hilbert_verdict | Hilbert promotion verdict | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv | True | PV2467_2_worldtube | True | 4 | worldtube surface independence | False |
| 4520 | SRC4520_12_formal4516 | 4516 stationary source subset | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\532-PPC4161-source-functor-parent-signature-or-first-Y5-coefficient-fill.md | True | PPC4161_SOURCE_FUNCTOR_PARENT_SIGNATURE_OR_FIRST_Y5_COEFFICIENT_FILL_4516 | True | 3 | stationary no-flux source closures | False |
| 4520 | SRC4520_13_formal4517 | 4517 domain source theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\533-PPC4161-domain-bulk-species-source-tail-or-coefficient-fill.md | True | PPC4161_DOMAIN_BULK_SPECIES_SOURCE_TAIL_OR_COEFFICIENT_FILL_4517 | True | 3 | domain/source split | False |
| 4520 | SRC4520_14_rz2213 | 2213 rank-zero theorem attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv | True | RZS2213_2_rank_zero_silence_theorem | True | 4 | older rank-zero silence theorem | False |
| 4520 | SRC4520_15_constraint2264 | 2264 conditional constraint theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2264_CONDITIONAL_CONSTRAINT_THEOREM.csv | True | THM2264_0_constraint_statement | True | 2 | constraint route | False |
| 4520 | SRC4520_16_gates2263 | 2263 constraint algebra gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv | True | CAG2263_5_matter | True | 7 | matter compatibility gate | False |

## Rank-Zero Source Current Silence Theorem

| theorem_id | piece | statement | derivation_status | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RZSC4520_0_definition | rank-zero source current | For an eliminated/rank-zero direction v_A, define J_A^src := D_{v_A} S_src, the vertical derivative of the source sector before readout. | DERIVED_DEFINITION | NONCLAIM | False |
| RZSC4520_1_chain_rule | quotient descent zero | If S_src = Sbar_src[q(Phi),Psi,theta] and Dq[v_A]=0 with no vertical action on Psi or theta, then D_{v_A} Sbar_src = <delta Sbar_src/delta q,Dq[v_A]>=0. | DERIVED_CONDITIONAL | NONCLAIM | False |
| RZSC4520_2_hilbert_matter | ordinary Hilbert matter silence | For q-basic Hilbert matter with a universal coframe/current owner, ordinary matter contributes no independent vertical source current: J_A^Hilbert=0. | DERIVED_CONDITIONAL | NONCLAIM | False |
| RZSC4520_3_poynting | EM/Poynting flow | Poynting flow is a Hilbert stress flux, S^i=-T_EM^i{}_nu tau^nu. In a stationary no-flux worldtube it contributes boundary flux, not a bulk J_A; if the wall flux vanishes and the EM action is q-basic, J_A^EM/Poynting=0. | DERIVED_CONDITIONAL | NONCLAIM | False |
| RZSC4520_4_retained | retained/non-Hilbert exception | Any explicit vertical dependence in constitutive maps, non-Hilbert source standards, memory kernels, material markers, or readout selectors survives as J_A^retained. | DERIVED_SPLIT | NONCLAIM | False |
| RZSC4520_5_rhs_reduction | rank-zero RHS after Hilbert silence | The rank-zero equation reduces to M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A^src/readout/projector once the Hilbert/ordinary/Poynting subcurrent is silent. | DERIVED_CONDITIONAL_REDUCTION | NONCLAIM | False |
| RZSC4520_6_verdict | 4520 theorem verdict | 4520 proves the useful conditional source-current part, not the whole local-GR branch. The remaining live gates are retained current, boundary/corner B_A, CDB tails, readout/projector R_A, and the rank/M lock. | PARTIAL_ADVANCE_NOT_FULL_CLOSURE | NONCLAIM | False |

## Source Current Clause Audit

| clause_id | clause | needed_for | current_status | closes | still_open | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SCA4520_0_vertical | v_A in ker(Dq) | Dq[v_A]=0 chain-rule zero | CONDITIONAL_FROM_RANK_ZERO_ROUTE_NOT_PARENT_CERTIFIED | quotient-visible source variation | rank certificate on physical quotient | False |
| SCA4520_1_matter_descent | S_matter descends through q(Phi) and observed coframe | ordinary matter source silence | CONTRACT_EXISTS_PARENT_SIGNATURE_INCOMPLETE | J_A^Hilbert conditionally | full parent action signature | False |
| SCA4520_2_no_vertical_standards | masses, clocks, rods, material labels and source standards have no explicit v_A dependence | no retained source current | NOT_FULLY_SIGNED | none globally | species/material/readout charges | False |
| SCA4520_3_hilbert_ward | Hilbert current conserved in stationary collar | closed source monopole and no bulk source leak | DERIVED_CONDITIONAL_FROM_2467_4516 | radial/time Hilbert drift subset | parent ell_J and Newton calibration | False |
| SCA4520_4_poynting_no_flux | EM/Poynting is Hilbert-owned and no wall flux crosses the local worldtube | J_A^EM/Poynting=0 | DERIVED_CONDITIONAL_GUARD | Poynting bulk-current worry under no-flux | radiative/constitutive/non-Hilbert EM branch | False |
| SCA4520_5_boundary | boundary/corner/reference source charge vanishes | B_A=0 | LIVE | nothing in 4520 | proper boundary/topological class proof | False |
| SCA4520_6_cdb | connection/domain/boundary derivative tails are zero or constraint-owned | C_A^CDB=0 | LIVE | nothing in 4520 | CDB operator inventory and sign | False |
| SCA4520_7_readout | source-normalization/readout/projector does not reinsert v_A | R_A=0 | LIVE | nothing in 4520 | observed-descent/fixed-readout protocol | False |

## Poynting Hilbert Flow Gate

| gate_id | object | mathematical_role | if_hilbert_owned | if_not_hilbert_owned | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PHF4520_0_identify | Poynting vector | S^i=-T_EM^i{}_nu tau^nu is an energy flux component of the Hilbert stress tensor | belongs to T_EM in the ordinary source current | becomes retained current J_A^retained | False |
| PHF4520_1_worldtube | local no-flux collar | int_{partial W} T_EM^{mu nu} tau_nu n_mu dSigma = 0 | no independent bulk J_A^EM/Poynting | finite flux/current bound required | False |
| PHF4520_2_stationarity | stationary EM field branch | partial_t source monopole = 0 and no radiative escape in local collar | supports J_A^EM/Poynting=0 under quotient descent | route to alpha/source-current acquisition | False |
| PHF4520_3_verdict | Poynting concern | not ignored; it is either Hilbert-owned no-flux or explicitly retained | conditionally silent | live finite residual | False |

## Rank-Zero RHS Closure Map

| rhs_id | component | before_4520 | after_4520 | status | next_gate | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RHS4520_0_J_Hilbert | ordinary Hilbert source current | part of J_A | J_A^Hilbert=0 under q-basic matter, vertical silence, stationary/no-flux collar | CONDITIONALLY_DERIVED_ZERO | parent action signature and rank certificate | False |
| RHS4520_1_J_EM_Poynting | EM/Poynting source flow | possible J_A concern | zero if Hilbert-owned and no worldtube flux; retained otherwise | CONDITIONALLY_DERIVED_ZERO_OR_RETAINED | EM owner/constitutive branch | False |
| RHS4520_2_J_retained | retained non-Hilbert current | live | still live unless parent excludes explicit vertical source dependence | LIVE | source-owner no-retained-current theorem | False |
| RHS4520_3_B | B_A boundary/corner/reference | live | unchanged | LIVE | boundary/corner no source charge | False |
| RHS4520_4_CDB | C_A^CDB derivative tails | live | unchanged | LIVE | CDB topological/constraint-owned inventory | False |
| RHS4520_5_R | R_A source/readout/projector | live | unchanged | LIVE | observed-descent fixed readout | False |
| RHS4520_6_Z | rank-zero solution | M_AB Z^B = J+B+CDB+R | M_AB Z^B = J_retained+B+CDB+R after Hilbert/Poynting silence | PARTIAL_REDUCTION_NOT_CLOSURE | 4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md | False |

## Alpha Input Fallback Acquisition

| fallback_id | source_quantity | required_if | formula_role | required_evidence | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AFA4520_0_Z | Z_X or Z_AB eigenvalue | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | normalizes kinetic operator and alpha denominator | parent action/principal symbol with units | MISSING_PARENT_Z | False |
| AFA4520_1_M | M_X^2 or M_AB eigenvalue | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | sets mu^2 and lambda=sqrt(Z/M^2) | parent Hessian/operator mass on same quotient domain | MISSING_PARENT_M | False |
| AFA4520_2_Qsource | Q_X^S | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | source charge in alpha numerator | same-frame source-normalized charge integral, not inferred from bound | MISSING_SOURCE_CHARGE_ZERO_OR_VALUE | False |
| AFA4520_3_qtest | q_X^T | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | test charge in alpha numerator | test-body response/source charge theorem or value | MISSING_TEST_CHARGE_ZERO_OR_VALUE | False |
| AFA4520_4_calibration | G_N^obs M_S m_T | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | Newton denominator and same-frame calibration | pre-readout Hilbert mass/current calibration | CONDITIONAL_CALIBRATION_NOT_FULLY_SIGNED | False |
| AFA4520_5_bound_curve | alpha_bound(lambda) | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | R10 acceptance bound | full digitized/source-backed curve or official table | FULL_CURVE_MISSING_VISUAL_POINTS_NONCLAIM | False |
| AFA4520_6_interpolation | interpolation rule | rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0 | evaluate bound at predicted lambda | declared log-log or official interpolation over in-domain lambda | PRIVATE_CANDIDATE_ONLY | False |

## Branch Decision

| decision_id | branch | result | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BD4520_0_source_current | rank-zero source-current silence | PARTIAL_ADVANCE | Hilbert ordinary matter and Hilbert-owned Poynting are silent under quotient descent and stationary no-flux; retained current remains live. | try boundary/CDB/readout silence before alpha scoring | False |
| BD4520_1_rank_zero | full rank-zero local silence | NOT_CLOSED | rank certificate, M_AB lock, retained source, boundary, CDB and readout gates remain unsigned | 4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md | False |
| BD4520_2_alpha | finite-range alpha(lambda) | FALLBACK_STAGED | use only if rank-zero route fails or finite rank is parent-selected; no alpha rows are claim-valid | fill Z/M/source/test/bound curve inputs only after branch selection | False |

## Claim Gates

| gate_id | claim | passed | blocker | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG4520_0_Hilbert_source | ordinary Hilbert source current is silent | False | conditional proof lacks full parent signature and rank certificate | False |
| CG4520_1_Poynting | Poynting is harmless | False | true only for Hilbert-owned stationary no-flux branch; radiative/constitutive branch retained | False |
| CG4520_2_rank_zero | rank-zero RHS vanishes | False | J_retained, B_A, CDB, R_A and rank/M lock remain live | False |
| CG4520_3_local_GR | local GR/Newton/PPN pass | False | rank-zero closure and finite-range alpha branch are nonclaim | False |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | next_target | valid_for_claim | claim_allowed | generated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4520 | PPC4161_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520 | L-362 | RANK_ZERO_HILBERT_SOURCE_CURRENT_SILENCE_DERIVED_CONDITIONALLY_BOUNDARY_CDB_READOUT_STILL_LIVE | J_A^Hilbert=0 and J_A^EM/Poynting=0 under q-basic Hilbert ownership and stationary no-flux | rank certificate,M_AB lock,J_retained,B_A,CDB,R_A,finite alpha inputs | NONCLAIM | 4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md | False | False | 2026-07-06T10:13:03.464522+00:00 |

## Next Target

| next_id | target_file | task |
| --- | --- | --- |
| NT4520_0 | 4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md | try to silence boundary/corner, CDB derivative tails and readout/projector reentry in the rank-zero RHS; if any cannot be derived, route to finite alpha input acquisition |

## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4520_00_sources | PASS | all source paths exist and source needles are found |
| VAL4520_01_theorem | PASS | Poynting theorem and RHS reduction rows exist |
| VAL4520_02_clauses | PASS | eight source-current clauses including Poynting no-flux |
| VAL4520_03_rhs | PASS | retained source current remains live, not hidden |
| VAL4520_04_claims_blocked | PASS | all claim gates remain blocked |
| VAL4520_05_csv_parse | PASS | P8_Y5_R2FR_4520_SOURCE_REGISTER.csv:17;P8_Y5_R2FR_4520_RANK_ZERO_SOURCE_CURRENT_SILENCE_THEOREM.csv:7;P8_Y5_R2FR_4520_SOURCE_CURRENT_CLAUSE_AUDIT.csv:8;P8_Y5_R2FR_4520_POYNTING_HILBERT_FLOW_GATE.csv:4;P8_Y5_R2FR_4520_RANK_ZERO_RHS_CLOSURE_MAP.csv:7;P8_Y5_R2FR_4520_ALPHA_INPUT_FALLBACK_ACQUISITION.csv:7;P8_Y5_R2FR_4520_BRANCH_DECISION.csv:3;P8_Y5_R2FR_4520_CLAIM_GATES.csv:4;P8_Y5_R2FR_4520_STATUS.csv:1;P8_Y5_R2FR_4520_NEXT_TARGET.csv:1 |
| VAL4520_06_next_target | PASS | 4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md |
| VAL4520_07_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4520_OVERALL | PASS | 4520 rank-zero source-current silence or alpha input acquisition |
