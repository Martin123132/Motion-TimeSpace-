# 604 Y5 R10 P_MTS boundary-kernel block or unit-map channel fill

Generated: 2026-06-05T19:17:44.240754+00:00  
Status: `Y5_R10_PMTS_boundary_kernel_block_theorem_written_parent_sector_charge_missing_unit_map_not_filled`  
Claim ceiling: `conditional_PMTS_kernel_block_theorem_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass`  
Next target: `605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md`  
Run root: `runs/20260605-191744-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill`

## Verdict
- The exact block-kernel theorem is now written: if a self-adjoint parent sector charge `Q_sec` has a nondegenerate MTS eigenvalue and `[K_B,Q_sec]=0`, then the MTS spectral projector `P_MTS,D=1_(q_MTS)(Q_sec)` is parent-fixed and ordinary/MTS cross-kernel terms vanish.
- This is the right derivation shape for protecting `b_D` and therefore `A_D=b_D c_D` from ordinary bath pollution.
- The theorem is not promoted: the current corpus does not derive `Q_sec`, its nondegeneracy against ordinary/edge sectors, or the boundary action symmetry that gives `[K_B,Q_sec]=0`.
- This puts real pressure on the next step: derive the parent sector charge, or stop circling the projector lock and demote to compact-shell unit-map scoring.

## Kernel Theorem
For boundary eigenmodes:

```text
Q_sec u_a = q_a u_a
Q_sec u_b = q_b u_b
[K_B,Q_sec]=0
```

then:

```text
q_a <u_a,K_B u_b> = <u_a,Q_sec K_B u_b>
                 = <u_a,K_B Q_sec u_b>
                 = q_b <u_a,K_B u_b>.
```

So if `q_a != q_b`:

```text
<u_a,K_B u_b> = 0.
```

That is the clean ordinary/MTS block split. The missing physics is the parent origin of `Q_sec`.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md | True | immediate 603 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_603_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv | True | A_D=b_D c_D primitive candidate |
| source-intake/mts_residuals/P8_Y5_R10_603_PARENT_OWNERSHIP_GATE.csv | True | P_MTS boundary-kernel blocker |
| 309-MTS-boundary-projector-contract-attempt.md | True | P_MTS projector contract |
| 310-ordinary-MTS-sector-split-attempt.md | True | ordinary/MTS block-kernel superselection lemma |
| 311-sector-label-SD-origin-attempt.md | True | support label S_D and activity operator route |
| 323-S3-sector-label-combined-gate.md | True | S3 singlet cannot replace sector label |
| 324-CD-activity-kernel-commutation-gate.md | True | C_D activity and kernel-commutation gate |
| 328-topological-MTS-support-projector-gate.md | True | P_top and P_MTS support projector route |
| 348-N5-projector-stress-conservation-theorem.md | True | metric-independent/topological projector stress gate |
| 356-parent-action-ward-identity-and-projector-variation.md | True | Ward ledger for projector/boundary/domain forces |
| 582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md | True | boundary charge and momentum-map blocker |
| scripts/Y5_R10_PMTS_boundary_kernel_block_or_unit_map_channel_fill.py | True | this checkpoint generator |

## Sector-Charge Theorem Attempt
| theorem_id | object | mathematical_form | claim_if_true | current_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SCT604_0_boundary_space | boundary data space H_B(D) | H_B(D)=H_ord plus H_MTS plus H_edge with boundary quadratic form <u,K_B v>_D | ordinary bath, MTS memory, and edge/horizon/domain data can be represented before projection | definition_gate | physical decomposition is not a theorem until a parent charge labels the subspaces | false |
| SCT604_1_parent_sector_charge | Q_sec | Q_sec^dagger=Q_sec; Q_sec u=q_ord u; Q_sec v=q_MTS v; Q_sec w=q_edge w with q_MTS distinct | P_MTS is the spectral projector onto the nondegenerate q_MTS eigenspace | not_parent_derived | no current parent action supplies a conserved nondegenerate MTS sector charge | false |
| SCT604_2_projector_from_charge | P_MTS,D | P_MTS,D = 1_{q_MTS}(Q_sec) | P_MTS,D is not a hand filter; it is a spectral projector fixed by Q_sec | conditional_spectral_projector | depends entirely on SCT604_1 and nondegeneracy against edge/ordinary sectors | false |
| SCT604_3_kernel_commutation | boundary kernel K_B | [K_B,Q_sec]=0 | K_B preserves Q_sec eigenspaces, so ordinary/MTS cross terms vanish | not_parent_derived | requires boundary action invariant under the Q_sec superselection symmetry | false |
| SCT604_4_cross_block_zero | K_cross | for q_a != q_b, <u_a,K_B u_b>=0 because q_a<u_a,K_B u_b>=<u_a,Q_sec K_B u_b>=q_b<u_a,K_B u_b> | ordinary coherent local baths cannot drive b_D through the MTS sector | proved_from_Qsec_commutation_premise | premises SCT604_1 and SCT604_3 are not derived | false |
| SCT604_5_stress_and_charge_ledger | projector/boundary stress | delta_g P_MTS=0 if Q_sec is topological/internal and metric-independent; otherwise delta_g P_MTS is retained as residual | no hidden Bianchi/projector-stress deletion | policy_gate_written | actual Q_sec type is missing, so stress fate is unknown | false |

## Boundary Kernel Block Gate
| gate_id | requirement | result_if_satisfied | current_status | failure_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| KBG604_0_block_theorem | Q_sec self-adjoint, q_MTS nondegenerate, and [K_B,Q_sec]=0 | K_boundary is block diagonal between ordinary and MTS sectors | conditional_theorem | ordinary coherent local baths can leak into rho_MTS,D | false |
| KBG604_1_relation_to_A_D | P_MTS,D from Q_sec is used inside b_D and A_D=b_D c_D | A_D activation is protected from ordinary bath pollution | conditional_support | A_D is a closure filter, not a parent primitive | false |
| KBG604_2_S3_insufficient | do not replace Q_sec with S3/coherent singlet alone | ordinary isotropic thermal/EM singlets do not falsely count as MTS | guard_pass | P_singlet leaks ordinary coherent baths | false |
| KBG604_3_Ptop_insufficient | relative/topological projector P_top must be supplemented by P_MTS | edge/horizon/topological classes do not degenerate with MTS top class | guard_pass | edge/top-class leakage survives | false |
| KBG604_4_Bianchi | projector/boundary/domain variations are zero by theorem or retained | block split is compatible with the Ward/Bianchi ledger | open | hidden projector stress or boundary charge can re-enter q_loc | false |
| KBG604_5_verdict | parent action derives Q_sec and [K_B,Q_sec]=0 | P_MTS,D kernel block becomes a parent theorem | fail_current_corpus | selector route remains conditional; unit-map demotion becomes likely | false |

## Leak Counterexample Gate
| leak_id | counterexample | why_it_matters | required_blocker | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LCG604_0_ordinary_isotropic_bath | ordinary isotropic EM/thermal bath is coherent/IR but not MTS | P_coh or S3 singlet alone would retain it | Q_sec with q_ord != q_MTS and P_MTS=1_{q_MTS}(Q_sec) | not_blocked_by_current_parent | false |
| LCG604_1_edge_top_class | edge/horizon/domain topological class has non-exact relative support | P_top alone cannot distinguish it from MTS top class | nondegenerate sector charge with q_edge != q_MTS | not_blocked_by_current_parent | false |
| LCG604_2_generic_boundary_mixing | generic K_B has nonzero <H_ord,K_B H_MTS> | even a defined P_MTS does not block mixing unless K_B commutes with Q_sec | boundary action symmetry giving [K_B,Q_sec]=0 | not_derived | false |
| LCG604_3_metric_projector_stress | metric-dependent spectral/Hodge projector varies with g | projector stress can act as a hidden local source | topological/internal Q_sec or explicit retained stress row | open | false |
| LCG604_4_hard_support_instability | tiny ordinary/MTS mixing makes hard support projector activate | exact superselection is required; approximate separation is a numeric residual problem | exact Q_sec theorem or demote to unit-map/residual scoring | open | false |

## Unit-Map Fork Status
| fork_id | route | status | why | required_next_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| UMF604_0_derivation_status | P_MTS boundary-kernel derivation | conditional_theorem_written_parent_charge_missing | Q_sec would derive both P_MTS and K_cross=0, but Q_sec itself is absent | derive parent sector charge origin or demote | false |
| UMF604_1_unit_map_warning | compact-shell unit map | likely_next_if_Qsec_fails | without Q_sec, further selector work risks circling the same projector closure | choose R10 alpha(lambda), PPN vector, WEP, or clock channel | false |
| UMF604_2_no_score | local-bound evidence | no_claim | proxy 7.432631961576971e-06 remains unconverted and no P_MTS theorem-zero certificate exists | source-backed coefficient/unit map or accepted theorem-zero gate | false |

## Runner Update
| runner_id | previous_status | new_status | reason | still_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RU604_0_PMTS_kernel | P_MTS_boundary_kernel_block_missing | conditional_Qsec_kernel_theorem_written | self-adjoint Q_sec plus [K_B,Q_sec]=0 proves ordinary/MTS cross block zero | parent origin of Q_sec and its nondegenerate MTS eigenvalue | false |
| RU604_1_ND_primitive | A_D_zero_nonzero_candidate_conditionally_derived | blocked_on_Qsec_parent_origin | b_D is protected only if P_MTS,D is parent-derived by Q_sec | Q_sec or explicit residual/unit-map demotion | false |
| RU604_2_q_loc_local_GR | q_loc_R11_boundary_open | still_open | kernel block theorem does not close boundary charge, R11, source-normalization, or full q_loc | local residual rows zeroed or scored | false |
| RU604_3_unit_map | fallback_deferred | queued_if_Qsec_origin_fails | 604 narrows the final derivation lock to a parent sector charge | if Q_sec fails, choose channel and fill physical unit map | false |

## Decision
| decision_id | decision | meaning | claim_status | next_target |
| --- | --- | --- | --- | --- |
| D604_0_kernel_theorem | accept Q_sec commutation as the exact P_MTS kernel theorem target | if Q_sec exists and [K_B,Q_sec]=0, ordinary/MTS boundary mixing is zero by superselection | conditional_not_promoted | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |
| D604_1_missing_parent_charge | do not claim P_MTS is parent-derived | the current corpus has no conserved nondegenerate MTS sector charge | no_claim | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |
| D604_2_unit_map_pressure | put unit-map demotion on deck | if the next step cannot derive Q_sec, the disciplined move is to stop stacking conditional projector clauses and score the closure branch | fallback_queued | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |
| D604_3_promotion | forbid local-GR/PPN/R10 promotion | P_MTS kernel theorem is conditional and does not close q_loc/R11/boundary debts | forbidden | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |

## Route Update
| route_id | allowed_after_604 | forbidden_after_604 | next_action |
| --- | --- | --- | --- |
| RU604_0_allowed | try one focused parent-sector-charge origin step | relabel P_MTS as derived from S3, P_coh, P_top, or ordinary gauge invariance alone | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |
| RU604_1_allowed | use Q_sec commutation theorem as a conditional exact result | use conditional block algebra as local-bound evidence | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |
| RU604_2_allowed | demote to compact-shell unit-map scoring if Q_sec origin fails | continue indefinitely through equivalent projector closures | 605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V604_0_source_paths_exist | pass | missing=0 |
| V604_1_prior_603_clean | pass | prior_rows=8;prior_failures=0;primitive_rows=6;ownership_rows=6 |
| V604_2_Qsec_block_theorem_written | pass | Qsec_missing=True;cross_block_theorem=True |
| V604_3_kernel_not_promoted | pass | parent Q_sec and kernel commutation not derived |
| V604_4_leak_guards_retained | pass | ordinary_leak_guard=True;edge_leak_guard=True |
| V604_5_unit_map_queued_and_local_GR_open | pass | unit_queued=True;local_GR_open=True;proxy=7.432631961576971e-06 |
| V604_6_no_claim_rows | pass | claim_rows=0 |
| V604_7_no_R10_or_local_GR_claim | pass | claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is a clean theorem-shaped result, but it is still a conditional shot. The good news: if `Q_sec` exists, the ordinary/MTS split is not handwaving. The hard news: without `Q_sec`, `P_MTS` is still a smart filter rather than a parent-owned object. Next we either derive that sector charge or we stop burning rounds and build the unit-map scorer.
