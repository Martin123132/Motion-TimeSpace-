# 2394 — Vertical Sector Variation Ledger Or Qv Piece Leak Rows

## Result

2394 takes the formal 2393 object

`J_v := Theta_parent(v_epsilon) - mu_v = dQ_v + C_v`

and splits it into the sector-level contract

`J_v = sum_s J_v^s = sum_s(Theta_s(v)-mu_s[v]) = d(sum_s Q_v^s) + sum_s C_v^s + leak_v`.

This is a derivation advance, not a claim advance.  The useful result is that the missing `Q_v` is no longer one
foggy object.  It has six named doors:

1. EH/local geometry kernel split.
2. Matter/source descent.
3. Extra residual field charge.
4. Projector/readout commutator charge.
5. Boundary/reference improvement charge.
6. Coupling/coframe/shadow-frame charge.

The only safe route to local GR/Newton is: every door must either close by quotient descent/basicness/constraint,
or become a sourced bound row.  One open door keeps `epsilon_kernel_charge` alive.

## Derived Sector Identity

Assume only a sector-summed parent action:

`L_parent = L_EH + L_matter + L_extra + L_projector + dB_ref + L_coupling`.

Then, by linearity of the variation and Noether current construction,

`Theta_parent(v) = Theta_EH(v) + Theta_matter(v) + Theta_extra(v) + Theta_projector(v) + delta_v B_ref + Theta_coupling(v)`,

`mu_v = mu_EH + mu_matter + mu_extra + mu_projector + mu_boundary + mu_coupling`,

and therefore

`Q_v = Q_v^EH + Q_v^matter + Q_v^extra + Q_v^projector + Q_v^boundary + Q_v^coupling`

only after each sector current has actually been derived as `J_v^s=dQ_v^s+C_v^s+leak_s`.

Current MTS has not yet done this.  So the ledger below refuses the total charge claim and turns each unclosed
piece into an explicit leak row.

## Source Register

| source_id | path | needed_for | needles | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC2394_2393_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md | selected 2394 target and vertical Noether contract | NEXT2393_0_selected|VQC2393_4_Qv|epsilon_theta_piece_missing|epsilon_Qv_piece_missing | false |
| SRC2394_2393_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2393_VERTICAL_QV_CERTIFICATE.csv | missing Qv and Theta certificate rows | VQC2393_1_Theta_parent|VQC2393_4_Qv|MISSING_VERTICAL_QV | false |
| SRC2394_2393_leaks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv | theta/Qv/Bv/integrability leak names | epsilon_theta_piece_missing|epsilon_Qv_piece_missing|epsilon_Bv_ambiguity|epsilon_Hv_integrability | false |
| SRC2394_1008_piece_ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv | prior tau charge sector split | QTA1008_0_L_parent|QTA1008_1_theta_total|QTA1008_5_Q_extra|QTA1008_6_Q_projector | false |
| SRC2394_1008_parent_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv | parent variation blockers | PVA1008_0_parent_action|PVA1008_1_theta_MTS|PVA1008_6_verdict | false |
| SRC2394_1771_sector_variation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv | retained local sectors and silence tests | SAV1771_0_higher_derivative|SAV1771_1_projector|SAV1771_2_boundary|SAV1771_6_verdict | false |
| SRC2394_771_owner_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv | Noether current owner requirements | TQ771_0_parent_variation|TQ771_1_Noether_current|TQ771_5_matter_coupling|TQ771_6_owner_verdict | false |
| SRC2394_2389_matter_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv | matter/source current descent blockers | OCC2389_2_Lm_density|OCC2389_4_matter_lift|OCC2389_7_MHref | false |
| SRC2394_2390_same_frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv | same-frame and support/projector descent blockers | SFC2390_1_Obs_e|SFC2390_2_same_readout|SFC2390_5_projector_support | false |
| SRC2394_2391_q_obse | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv | quotient, basic coframe, and presymplectic-null blockers | QOC2391_2_presymplectic_null|QOC2391_3_basic_coframe|QOC2391_6_matter_readout_descent | false |

## Sector Variation Ledger

| sector_id | sector | vertical_variation_piece | conditional_derivation | current_status | theta_piece_status | Qv_piece_status | source_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SVL2394_0_EH_local_geometry | Einstein-Hilbert / observed local geometry | Theta_EH(e_obs; Lie_v e_obs) and mu_EH[v] | If e_obs=Obs_e(q(Phi)) and Dq(v)=0, then Lie_v e_obs=0; the EH vertical contribution to J_v and Q_v is zero in the quotient kernel. If v includes a true observed diffeomorphism, the usual EH charge is only a reference piece, not an MTS kernel proof. | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | MISSING_BASIC_COFRAME_TO_KILL_THETA_EH | MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT | QOC2391_2_presymplectic_null;QOC2391_3_basic_coframe;SFC2390_1_Obs_e | false |
| SVL2394_1_matter_source | ordinary matter / Hilbert source / worldtube | Theta_matter(v_m) - mu_m[v] plus possible source current constraints C_v^matter | If S_matter=Sbar_matter[q(Phi),psi,theta] and the matter lift fixes representation data along ker(Dq), then delta_v S_matter=0 and the matter/source piece is constraint-only with no independent vertical charge. | CONDITIONAL_DESCENT_NOT_PARENT_SIGNED | MISSING_MATTER_THETA_DESCENT | MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT | OCC2389_2_Lm_density;OCC2389_4_matter_lift;OCC2389_7_MHref;TQ771_5_matter_coupling | false |
| SVL2394_2_extra_residual | motion/time/domain/memory/range residual sector | Theta_extra(v_X) - mu_extra[v] = dQ_v^extra + C_v^extra + leak_extra | Any retained MTS residual field must either be quotient-basic, algebraic/constraint-only, or have its own Noether charge extracted. Otherwise the kernel can carry physical charge and local-GR reduction is not derived. | RETAINED_SECTOR_NOT_VARIED | MISSING_THETA_EXTRA | MISSING_QV_EXTRA | QTA1008_5_Q_extra;SAV1771_4_memory_coframe;TQ771_1_Noether_current | false |
| SVL2394_3_projector_readout | projector / Pi_M / source-measure / readout support | Theta_projector(v_Pi,v_J,v_W)-mu_projector[v] plus [d,Pi_M] and delta Pi_M source terms | A projector/readout sector is silent only if Pi_M, support W, and readout surfaces descend through q/e_obs before scoring and commute with the relevant exterior derivative/current operation. | EXACT_OBSTRUCTION_KNOWN_NOT_SILENCED | MISSING_THETA_PROJECTOR | MISSING_QV_PROJECTOR_OR_COMMUTATOR_BOUND | QTA1008_6_Q_projector;SAV1771_1_projector;SFC2390_5_projector_support | false |
| SVL2394_4_boundary_reference | boundary / reference / improvement | delta_v B_ref, Q_v^boundary, and improvement ambiguity in delta H_v[S] | Boundary/reference data are harmless only if fixed before readout, derivative-silent under v, and unable to absorb the residual normalization. Otherwise Q_v can be shifted by an improvement. | REFERENCE_SHAPE_KNOWN_NOT_PARENT_FIXED | MISSING_BOUNDARY_THETA_AND_BV | MISSING_QV_BOUNDARY_AND_ZERO_FLUX | QTA1008_4_Q_boundary;SAV1771_2_boundary;VQC2393_5_Bv_boundary | false |
| SVL2394_5_coupling_coframe | nonminimal coupling / coframe / preferred-frame | Theta_coupling(v)-mu_coupling[v] and any Weyl/disformal/species/source-prefactor charge | The coupling sector is zero only if all constants, charge normalizations, coframes, connections, and species frames descend from the same q/Obs_e data with no direct residual slot. | COUPLING_ZERO_NOT_SIGNED | MISSING_THETA_COUPLING | MISSING_QV_COUPLING_OR_NO_SLOT_PROOF | SAV1771_3_nonminimal;SAV1771_4_memory_coframe;SFC2390_4_no_shadow_frame;QOC2391_6_matter_readout_descent | false |
| SVL2394_6_total | total parent vertical charge | J_v=sum_s(Theta_s(v)-mu_s[v]) = d(sum_s Q_v^s)+sum_s C_v^s+leak_v | Q_v is extracted only if every sector piece is derived, zeroed by descent, or bounded with a sourced coefficient. One unowned sector keeps epsilon_kernel_charge alive. | TOTAL_QV_NOT_EXTRACTED | epsilon_theta_piece_missing_nonzero | epsilon_Qv_piece_missing_nonzero | VNC2393_5_verdict;VQC2393_4_Qv;QTA1008_8_Q_total | false |

## Sector Closure Contract

| row_id | contract | required_clause | current_result | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SCC2394_0_additive_variation | parent action sector sum | L_parent=sum_s L_s + dB_ref with every retained L_s named before variation | sector labels exist, but no single adopted L_parent sums them | blocks total Theta_parent ownership | false |
| SCC2394_1_vertical_action | v action on every sector | v_epsilon acts on e_obs, matter, residual fields, projector/support, coupling constants/frames, and boundary/reference data | v action is formal and not sector-signed | blocks mu_v and sector current extraction | false |
| SCC2394_2_sector_current | sector Noether current | J_v^s=Theta_s(v)-mu_s[v]=dQ_v^s+C_v^s+leak_s for each sector | only the formal equation is available | Q_v remains a symbol, not a derived charge | false |
| SCC2394_3_zero_or_bound | zero/bound every leak | each leak_s is zero by descent/basicness/constraint, or becomes a sourced numeric bound row | no sector has a full zero certificate | local GR/Newton and PPN pass remain blocked | false |

## Qv Piece Leak Rows

| quantity_id | definition | units | source_sector | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| epsilon_Qv_EH_kernel_split | possible EH/reference charge contamination if vertical v is not separated from observed diffeomorphism | dimensionless after M_H_ref normalization | SVL2394_0_EH_local_geometry | MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT | false |
| epsilon_Qv_matter_source | unowned matter/source constraint or charge contribution to vertical Hamiltonian | dimensionless after M_H_ref normalization | SVL2394_1_matter_source | MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT | false |
| epsilon_Qv_extra | retained motion/time/domain/memory/range Noether charge contribution | dimensionless after M_H_ref normalization | SVL2394_2_extra_residual | MISSING_QV_EXTRA | false |
| epsilon_Qv_projector | Pi_M/support/readout commutator or projector charge contribution | dimensionless after M_H_ref normalization | SVL2394_3_projector_readout | MISSING_QV_PROJECTOR_OR_COMMUTATOR_BOUND | false |
| epsilon_Qv_boundary | boundary/reference/improvement shift in vertical charge | dimensionless after M_H_ref normalization | SVL2394_4_boundary_reference | MISSING_QV_BOUNDARY_AND_ZERO_FLUX | false |
| epsilon_Qv_coupling | nonminimal coupling/coframe/shadow-frame vertical charge contribution | dimensionless after M_H_ref normalization | SVL2394_5_coupling_coframe | MISSING_QV_COUPLING_OR_NO_SLOT_PROOF | false |
| epsilon_Qv_total | sum of all unclosed sector Q_v pieces | dimensionless after M_H_ref normalization | SVL2394_6_total | TOTAL_QV_NOT_EXTRACTED | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2394_0_accept_additive_sector_contract | accept sector-additive vertical current decomposition | If the parent action is a sector sum, the Noether current and charge must split by the same sectors plus boundary improvements. | future derivations must close or bound each sector, not only the EH-looking piece | CONDITIONAL_CONTRACT_ACCEPTED | false |
| DEC2394_1_no_sector_zero_claim | do not claim any sector zero yet | each candidate zero depends on missing q/Obs_e, matter lift, projector, coupling, boundary, or v-action clauses | epsilon_theta_piece_missing and epsilon_Qv_piece_missing stay alive | ALL_SECTOR_ZEROS_UNSIGNED | false |
| DEC2394_2_next | attack EH/local-geometry kernel split first | it is the least exotic sector and can establish whether pure vertical v is truly different from observed diffeomorphism; if this fails, the whole local-GR route becomes much harder | 2395 should derive the EH/reference contribution for vertical v, or produce the EH contamination source row | SELECT_2395_EH_KERNEL_SPLIT | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2394_0_Qv_extracted | vertical Q_v extracted | BLOCKED | not extracted until all sector pieces are derived or killed | false |
| CG2394_1_kernel_null | vertical kernel presymplectic-null | BLOCKED | not proven while any sector charge leak remains | false |
| CG2394_2_matter_invisible | matter/source invisibility under vertical v | BLOCKED | not proven without L_m density, lift, and no-direct-slot grammar | false |
| CG2394_3_projector_silent | projector/readout silent | BLOCKED | not proven without Pi_M/support descent and commutator control | false |
| CG2394_4_GR_Newton | local GR/Newton reduction | BLOCKED | no local GR/Newton claim from 2394 | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2394_0_claim_sector_zero | all vertical sector contributions vanish | false | zero clauses are conditional and parent inputs remain missing | SVL2394_0_EH_local_geometry;SVL2394_1_matter_source;SVL2394_2_extra_residual;SVL2394_3_projector_readout;SVL2394_4_boundary_reference;SVL2394_5_coupling_coframe | false |
| REF2394_1_claim_Qv_piece_sum | Q_v=sum_s Q_v^s has been extracted | false | sector Q_v pieces are named but not calculated from a parent action | SCC2394_0_additive_variation;SCC2394_1_vertical_action;SCC2394_2_sector_current | false |
| REF2394_2_claim_GR_Newton | local GR/Newton follows from the sector ledger | false | the ledger is a derivation map, not the completed derivation | CG2394_0_Qv_extracted;CG2394_1_kernel_null;CG2394_4_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2394_0_selected | 2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | prove pure vertical v gives Lie_v e_obs=0 and no EH Q_v contamination, while observed diffeomorphism charge remains only the GR reference | create epsilon_Qv_EH_kernel_split bound/source row and keep local-GR gate blocked | false |
| NEXT2394_1_parallel | 2395b-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md | prove vertical v leaves matter/source representation data invisible through q/Obs_e | retain epsilon_Qv_matter_source and epsilon_hidden_source_slot | false |
| NEXT2394_2_later | 2395c-Y5-R2FR-projector-commutator-and-boundary-improvement-cleanup.md | prove Pi_M/support descent and fixed boundary improvement | retain projector and boundary Q_v leak rows | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2394_00_sources_exist | PASS | all required source paths exist | false |
| VAL2394_01_needles_found | PASS | all source needles found | false |
| VAL2394_02_all_major_sectors_present | PASS | EH, matter, extra, projector, boundary, coupling, and total sector rows present | false |
| VAL2394_03_contract_has_current_split | PASS | sector current split contract present | false |
| VAL2394_04_leak_rows_nonready | PASS | all Qv piece leak rows remain nonclaim/nonready | false |
| VAL2394_05_global_claims_blocked | PASS | Qv, kernel-null, matter invisibility, projector silence, and GR/Newton gates blocked | false |
| VAL2394_06_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2394_07_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2394_08_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2394_09_next_selected | PASS | EH/local-geometry kernel split selected next | false |
| VAL2394_OVERALL | PASS | 2394 splits the formal vertical Qv problem into EH, matter, extra, projector, boundary, and coupling sectors, keeps every unsigned sector nonclaim, and selects EH kernel split next | false |

## Practical Status

This is a better shape than before.  We are no longer saying "derive `Q_v`" as if that is one black box.  The problem
has split into named pieces.  The least-scrutiny next move is the EH/local-geometry kernel split, because if pure
vertical directions truly leave `e_obs` fixed, then the EH sector can plausibly be removed from the kernel problem
without importing a fitted GR charge.  If that fails, the local branch keeps a concrete EH contamination row instead
of smuggling a plateau or gauge axiom.
