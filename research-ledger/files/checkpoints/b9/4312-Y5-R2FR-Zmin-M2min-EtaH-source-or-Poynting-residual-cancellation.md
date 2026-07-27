# 4312 - Zmin/M2min/EtaH source or Poynting residual cancellation

## Verdict
- Derived the Poynting once-only cancellation condition: same Maxwell-Hodge Hilbert owner implies `c_Poynt_extra=0`.
- Kept physical Poynting/radiation alive as boundary flux or named residual, not as hidden background force.
- Replaced the EM part of `Eta_H` with six named defect channels: `Delta_Hodge_EM`, `delta_w_EM`, `C_XF2`, `C_JQ`, `Delta_rad_Poynting`, and `Delta_internal_exchange`.
- Updated the collar numerator path: `S_U` now has an auditable `R_EM_Poynting` term.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4312_00_4311_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md | True | True | 4311 declared EM/Poynting as an explicit collar residual target. |
| SRC4312_01_4311_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4311_NEXT_TARGET.csv | True | True | 4311 handoff selecting lambda components or Poynting residual cancellation. |
| SRC4312_02_4207_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md | True | True | Poynting is Hilbert EM stress, not a second source, on the safe branch. |
| SRC4312_03_4207_once | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md | True | True | once-only source theorem for extra Poynting coefficient. |
| SRC4312_04_4207_gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4207_RETAINED_GATES.csv | True | True | retained EM/Poynting failure gates. |
| SRC4312_05_4207_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv | True | True | Ward exchange identity and Hilbert owner chain. |
| SRC4312_06_319_visible | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | visible-sector no-direct-m source clause. |
| SRC4312_07_321_source_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | source-pair residual split with EM/rest terms retained. |
| SRC4312_08_4176_noflux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | local no-flux/support-separation collar selector. |
| SRC4312_09_4302_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | Eta_H remains the correction bucket containing EM/Hodge/boundary terms. |
| SRC4312_10_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision forbids unbounded EM side-channel leakage. |
| SRC4312_11_newton_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality gate remains open. |

## EM Cancellation Theorem
| theorem_id | clause | statement | result | status | implication |
| --- | --- | --- | --- | --- | --- |
| EC4312_0_same_hodge | same Maxwell-Hodge/Hilbert owner | S_MH uses the same observed metric/coframe/Hodge star as the local gravitational source functional | EM Hilbert stress is counted once inside T_total | CONDITIONAL_BRANCH_SIGNATURE_FROM_4207 | needed before cancellation can fire |
| EC4312_1_poynting_identity | Poynting identity | S_i = -T_EM(n,e_i) = (E cross B)_i | Poynting is real energy flow, not an extra source field | EXACT_LOCAL_FRAME_IDENTITY_FROM_4207 | use this to forbid double counting, not to erase radiation |
| EC4312_2_once_only | extra Poynting source coefficient | M_trial = M_H[J_H_total] + c_Poynt_extra int_boundary S_Poynting dot n dA | single-owner branch requires c_Poynt_extra=0 | CANCELS_IF_SINGLE_SOURCE_FUNCTIONAL_PARENT_SIGNED | blocks hidden preferred-frame/background-force source |
| EC4312_3_ward_exchange | matter-EM Ward exchange | div T_EM = -FJ and div T_matter = +FJ | Lorentz force is internal exchange when both actions share the same current | CONDITIONAL_WARD_CANCELLATION | unmatched exchange stays as Delta_internal_exchange |
| EC4312_4_boundary_route | radiative flux route | net Poynting flux through the collar is boundary/Hamiltonian flux | static bulk m-source receives no extra term if no-flux selector is signed | CONDITIONAL_NOFLUX_OR_BOUNDARY_ROW | nonzero radiation enters N_boundary, not hidden R_U |
| EC4312_5_zero_theorem | R_EM_Poynting zero branch | same Hodge owner, c_Poynt_extra=0, no X F2, fixed charge/current, Ward exchange, and no net radiative collar flux | R_EM_Poynting=0 | EXACT_ZERO_IF_ALL_CLAUSES_SIGNED | not live until parent signatures or source rows exist |

## Residual Defect Ledger
| defect_id | symbol | failure_condition | bound_contribution | feeds | status | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| RD4312_0_delta_Hodge_EM | Delta_Hodge_EM | observed Hodge/coframe not parent-owned or differs from local metric readout | C_Hodge \|\|Delta_Hodge_EM\|\| \|\|F\|\|^2 | Eta_H and S_U | EXPLICIT_DEFECT_ROW_VALUE_MISSING | derive same-Hodge owner or source constitutive bound |
| RD4312_1_delta_w_EM | delta_w_EM | species/readout EM source weight survives | C_w \|delta_w_EM\| \|\|T_EM\|\| | Eta_H/source normalization | EXPLICIT_DEFECT_ROW_VALUE_MISSING | prove no independent EM weight or source local bound |
| RD4312_2_C_XF2 | C_XF2 | extra MTS X F^2 coupling | \|C_XF2\| \|\|F\|\|^2 | R_EM_Poynting and fifth-force side-channel | EXPLICIT_DEFECT_ROW_VALUE_MISSING | parent-forbid, screen, or empirically bound |
| RD4312_3_C_JQ | C_JQ | hidden EM-current multiplier or charge normalization drift | \|C_JQ\| \|\|J dot A\|\| | source-current and clock/WEP residual | EXPLICIT_DEFECT_ROW_VALUE_MISSING | derive charge normalization or bound drift |
| RD4312_4_Delta_rad_Poynting | Delta_rad_Poynting | net radiative Poynting flux crosses the collar | \|int_boundary S_Poynting dot n dA\| | N_boundary/Hamiltonian flux | EXPLICIT_DEFECT_ROW_VALUE_MISSING | prove no-through-flux selector or route as boundary value |
| RD4312_5_Delta_internal_exchange | Delta_internal_exchange | matter-EM exchange not owned by one action/current | \|\|div T_EM + div T_matter\|\|_dual | source conservation and Eta_H | EXPLICIT_DEFECT_ROW_VALUE_MISSING | derive Ward exchange cancellation |
| RD4312_6_c_Poynt_extra | c_Poynt_extra | standalone Poynting source coefficient | \|c_Poynt_extra\| \|int_boundary S_Poynting dot n dA\| | forbidden double-count channel | EXPLICIT_DEFECT_ROW_VALUE_MISSING | set exactly zero on single-owner branch; otherwise claim blocked |

## Bound Update
| bound_id | symbol | law | role | status |
| --- | --- | --- | --- | --- |
| RB4312_0_R_EM_bound | R_EM_Poynting | R_EM_Poynting <= C_H dH \|\|F\|\|^2 + C_w \|dw\| \|\|T_EM\|\| + \|C_XF2\| \|\|F\|\|^2 + \|C_JQ\| \|\|J dot A\|\| + \|Phi_rad\| + \|Delta_ex\| | explicit bound for EM/Poynting contribution to S_U | BOUND_DERIVED_VALUES_MISSING |
| RB4312_1_safe_branch | R_EM_Poynting_zero | if dH=dw=C_XF2=C_JQ=Phi_rad=Delta_ex=0 and c_Poynt_extra=0 then R_EM_Poynting=0 | exact cancellation branch | CONDITIONAL_ZERO_NOT_LIVE |
| RB4312_2_EtaH_update | Eta_H_EM | Eta_H >= Eta_H_nonEM + C_Eta_EM(dH,dw,C_XF2,C_JQ,Phi_rad,Delta_ex) | moves EM/Hodge defects into the lambda-floor correction ledger | ETA_UPDATE_FORMULA_READY_VALUES_MISSING |
| RB4312_3_SU_update | S_U | S_U <= R_visible + R_transition + R_boundary + R_nonHilbert + R_N + R_EM_Poynting | 4311 residual numerator with EM term made auditable | RESIDUAL_NUMERATOR_UPDATED |
| RB4312_4_no_double_count | c_Poynt_extra | single Hilbert source owner implies c_Poynt_extra=0 | prevents adding Poynting as separate source after T_EM | DERIVED_CANCELLATION_CLAUSE |

## Lambda Status
| status_id | symbol | status | requirement | implication |
| --- | --- | --- | --- | --- |
| LS4312_0_Zmin | Z_min | unchanged | still requires parent kinetic sign/normalization | not affected by EM cancellation except through shared normalization |
| LS4312_1_M2min | M2_min | unchanged | still requires parent potential/Hessian signature | mass-only branch remains possible but unsourced |
| LS4312_2_lambda1 | lambda_1(D_loc) | unchanged | still requires collar domain/zero-mode selector | no EM shortcut to domain spectrum |
| LS4312_3_EtaH | Eta_H | updated | EM/Poynting defects now enter Eta_H as named terms instead of a black box | this is the real gain of 4312 |
| LS4312_4_lambda_star | lambda_* | guarded | lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H remains unscored | positive margin improves if EM defects cancel or are small |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4312_0_current_corpus | current corpus with 4207 owner chain but retained EM defect gates | BOUND_ROUTE_ONLY | Poynting double-count channel is forbidden conditionally, but same-Hodge/current/Ward/no-flux signatures are not all parent-closed | use explicit R_EM_Poynting bound rows |
| RUN4312_1_safe_EM | single Hodge owner, fixed charge/current, Ward exchange, no extra XF2, no radiative collar flux | ALLOW_R_EM_ZERO_CONDITIONAL | EM/Poynting does not contribute an extra collar bulk source | then S_U can drop R_EM_Poynting before lambda scoring |
| RUN4312_2_radiative_flux | net Poynting flux through collar survives | ROUTE_TO_BOUNDARY | radiation is a boundary/Hamiltonian flux, not a static hidden source | feed Phi_rad into N_boundary or an explicit source row |
| RUN4312_3_side_channel | Hodge/current/XF2/Ward defects survive | KEEP_EM_RESIDUAL | defects enter Eta_H and S_U, weakening lambda positivity and local precision | source or derive each defect bound |
| RUN4312_4_local_claim | claim local GR/Newton/R10/PPN after EM split | REJECT | lambda components, non-EM residuals, R_eq, I_commutator and projection gates remain open | continue derivation chain |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4312_0 | Do not add Poynting as a standalone source after T_EM is already included in T_total. | ACTIVE |
| FW4312_1 | Do not erase radiation; nonzero Poynting flux must route to N_boundary/Hamiltonian flux. | ACTIVE |
| FW4312_2 | Do not claim EM cancellation unless same Hodge owner, current normalization and Ward exchange are signed. | ACTIVE |
| FW4312_3 | Do not hide X F^2 or current/charge drift inside Eta_H without a named bound row. | ACTIVE |
| FW4312_4 | Do not score local GR/Newton/R10/PPN from the EM split alone. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4312_0_poynting | POYNTING_IS_REAL_BUT_NOT_SECOND_SOURCE | In the same-Hodge Hilbert branch, Poynting is the EM energy-flux component of T_EM already counted in T_total. | set c_Poynt_extra=0 if the single source functional is parent-signed |
| DEC4312_1_residual | EM_DEFECTS_ARE_NOW_NAMED | Hodge mismatch, source weight, XF2, current normalization, radiative flux and Ward mismatch are the only EM/Poynting residual channels retained here. | source or cancel these rows instead of revisiting vague coupling |
| DEC4312_2_eta | ETAH_BLACK_BOX_SHRINKS | EM/Poynting no longer sits as an undefined correction; it enters Eta_H/S_U through explicit rows. | positive lambda margin can improve if these rows vanish or are bounded small |
| DEC4312_3_claim | NO_LOCAL_GR_CLAIM | This is a source-coupling derivation step, not a completed local-GR/Newton reduction. | keep all arena claims blocked |
| DEC4312_4_next | WARD_CURRENT_NORMALIZATION_NEXT | The least handwavy next target is to close the shared current/charge/Ward exchange row or assign a collar bound value. | 4313-Y5-R2FR-EM-Ward-current-normalization-or-collar-residual-bound-values.md |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4312_0_poynting | Poynting | OWNER_LOCKED_CONDITIONAL | real EM flow, not an extra bulk source on safe branch |
| STAT4312_1_extra_source | c_Poynt_extra | ZERO_IF_SINGLE_OWNER_SIGNED | forbidden double-count channel |
| STAT4312_2_R_EM | R_EM_Poynting | ZERO_OR_BOUND | zero only if all EM defect clauses vanish |
| STAT4312_3_EtaH | Eta_H | MORE_EXPLICIT | EM correction is decomposed into named defect rows |
| STAT4312_4_lambda | lambda_* | STILL_UNSCORED | Z_min/M2_min/lambda_1/Eta_H values still missing |
| STAT4312_5_local | local GR/Newton | BLOCKED | source coupling improved but not complete |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4312_0 | 4313-Y5-R2FR-EM-Ward-current-normalization-or-collar-residual-bound-values.md | Can the shared EM current/charge/Ward exchange be parent-signed, or must its collar residual be bounded numerically? | derive shared current normalization and Ward exchange cancellation from one matter+EM action | fill nonclaim bounds for C_JQ, Delta_internal_exchange and Delta_rad_Poynting |
