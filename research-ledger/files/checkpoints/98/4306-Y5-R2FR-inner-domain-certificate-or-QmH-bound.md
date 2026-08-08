# 4306 - inner-domain certificate or QmH bound

## Verdict
- Derived the weak-form boundary identity for `N_inner`.
- Proved exactly when `N_inner=0`: smooth no-excision source domain, signed Dirichlet/source matching, or signed no-flux plus no source-boundary injection.
- Replaced the crude `C_inner |Q_m^H|` row with a sharper trace fallback: `C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||`.
- No local-GR claim fires; the next target is parent ownership of the source domain or real inner flux profile inputs.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4306_00_4305_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4305-Y5-R2FR-source-power-amplitude-or-inner-charge-bound-runner.md | True | True | 4305 handoff: derive domain certificate or Q_m^H bound. |
| SRC4306_01_4305_inner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4305_INNER_CHARGE_DOMAIN_SPLIT.csv | True | True | 4305 inner smooth/excision split and finite bound route. |
| SRC4306_02_4302_operator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | m-lock operator whose integration-by-parts boundary term defines B_inner. |
| SRC4306_03_1538_inner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv | True | True | older N_inner <= C_inner \|Q_m^H\| finite row. |
| SRC4306_04_1529_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv | True | True | boundary/no-flux certificate audit. |
| SRC4306_05_1529_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1529_CERTIFICATE_OR_BOUND_RUNNER.csv | True | True | certificate route blocked unless parent signs domain/boundary/zero-mode clauses. |
| SRC4306_06_192_noflux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | local no-flux/support-separation theorem precedent. |
| SRC4306_07_284_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | True | fixed compact no-flux collar branch for boundary/projector row. |
| SRC4306_08_319_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 inner charge component bound. |

## Boundary Variation Identity
| row_id | formula | basis | implication | status |
| --- | --- | --- | --- | --- |
| BID4306_0_operator | L_m u = -nabla_i(Z_m h^{ij}nabla_j u)+M_m^2 u+Delta_H[u] | 4302 operator form | starting point | OPERATOR_IMPORTED |
| BID4306_1_weak_form | <phi,L_m u>_D = int_D Z_m grad phi.grad u + int_D phi(M_m^2u+Delta_H[u]) - int_partialD phi Z_m n.grad u | integration by parts | boundary term is not optional | DERIVED_WEAK_FORM |
| BID4306_2_inner_functional | B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi] | definition | inner source/excision boundary forcing | DERIVED_BOUNDARY_FUNCTIONAL |
| BID4306_3_dual_norm | N_inner = sup_{\|\|phi\|\|_{H1(D)}<=1} \|B_inner[phi]\| | boundary-dual norm | turns prose inner charge into a scoreable norm | DERIVED_NORM_DEFINITION |
| BID4306_4_trace_bound | N_inner <= C_tr \|\|Z_m n.grad u\|\|_{H^{-1/2}(partialD_in)} + \|\|B_src\|\|_{H^{-1/2}} | trace theorem | finite route when zero certificate fails | DERIVED_TRACE_BOUND |

## Domain Certificate Matrix
| row_id | condition | consequence | status | note |
| --- | --- | --- | --- | --- |
| DOM4306_0_smooth_no_excision | partialD_in = empty set | B_inner=0, N_inner=0 | EXACT_ZERO_IF_PARENT_OWNS_SMOOTH_SOURCE_DOMAIN | Best clean route: local branch treats compact sources as smooth Hilbert matter, not excised point holes. |
| DOM4306_1_Dirichlet | phi\|partialD_in=0 or u fixed by parent source matching | B_inner[phi]=0 | EXACT_ZERO_IF_PARENT_BOUNDARY_VALUE_SIGNED | Cannot choose Dirichlet by hand; source matching must own it. |
| DOM4306_2_Neumann_no_flux | Z_m n.grad u\|partialD_in=0 and source-boundary injection B_src=0 | B_inner=0, N_inner=0 | EXACT_ZERO_IF_NO_FLUX_CERTIFICATE_SIGNED | 1529 says this certificate is not found for the older lambda_phi route. |
| DOM4306_3_Hilbert_no_memory_charge | source action factors through q/Hilbert variables with no independent m-boundary charge | Q_m^H=0 and B_src=0 | EXACT_ZERO_ROUTE_UNSIGNED | Equivalent to proving compact matter carries no extra memory monopole. |
| DOM4306_4_excision_hair | partialD_in nonempty and Z_m n.grad u or B_src survives | N_inner must be bounded, not erased | FINITE_HAIR_ROUTE | This is the honest exterior point/source branch. |

## QmH Trace Bound
| row_id | formula | meaning | status | next_input |
| --- | --- | --- | --- | --- |
| QMH4306_0_flux_profile | g_in := Z_m n.grad u\|partialD_in | inner normal memory flux profile | MISSING_PROFILE | source g_in on the parent source boundary or prove it vanishes |
| QMH4306_1_monopole | Q_m^H := int_partialD_in g_in dSigma | monopole/hair charge | MISSING_VALUE | 1538 C_inner\|Q_m^H\| is only safe if higher modes are absent or separately bounded |
| QMH4306_2_multipole_split | g_in = Q_m^H/Area(partialD_in) + g_perp, int g_perp dSigma=0 | separates monopole from multipole/tidal boundary hair | DERIVED_DECOMPOSITION | prevents hiding multipole boundary flux inside a scalar Q_m^H number |
| QMH4306_3_sharp_bound | N_inner <= C_0 \|Q_m^H\| + C_perp \|\|g_perp\|\|_{H^{-1/2}} + \|\|B_src\|\|_{H^{-1/2}} | sharpened finite bound | DERIVED_BOUND_FORM_INPUTS_MISSING | required inputs: C_0, C_perp, Q_m^H, g_perp norm, B_src norm and source-domain convention |
| QMH4306_4_1538_recovery | N_inner <= C_inner \|Q_m^H\| when g_perp=0 and B_src=0 or absorbed into C_inner | recovers 1538 finite row as a special case | CONDITIONAL_SIMPLIFICATION | do not use the scalar simplification until multipole/source-boundary injection is killed |

## Updated Npair Runner
| runner_id | branch_name | formula | role | status |
| --- | --- | --- | --- | --- |
| RUN4306_0_smooth_selector | smooth no-excision source domain | N_pair <= N_EM + N_rest; if N_EM=N_rest=0 then N_pair=0 | A_src and N_inner are both zero on this branch. | EXACT_ROUTE_CONDITIONAL |
| RUN4306_1_no_flux_excision | excision domain with parent no-flux/source-boundary certificate | N_pair <= N_EM + N_rest | inner boundary exists but contributes zero by certificate. | EXACT_ROUTE_UNSIGNED |
| RUN4306_2_trace_fallback | excision domain with surviving memory flux | N_pair <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| + N_EM + N_rest | scoreable fallback replacing a vague C_inner slot. | BOUND_ROUTE_READY_INPUTS_MISSING |
| RUN4306_3_to_m_lock | m-lock handoff | Delta_m <= (N_pair+N_N)/lambda_m; C4302_DVGAMMA_QUAD uses Delta_m and Delta_Dv_m | same 4302 route after inner-domain reduction. | HANDOFF_READY_NOT_SCORE_READY |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4306_0_gain | INNER_BOUNDARY_LAW_DERIVED | N_inner is now the dual norm of an explicit boundary functional, not a vague charge label. | Use the trace/QmH profile law for all future source-pair scoring. |
| DEC4306_1_zero | ZERO_ROUTE_IS_DOMAIN_OWNERSHIP | N_inner=0 is exact for smooth no-excision source domains, signed Dirichlet, or signed no-flux/source-boundary silence. | Next step must prove which domain the parent owns. |
| DEC4306_2_bound | SCALAR_QMH_NOT_ENOUGH_BY_ITSELF | A scalar Q_m^H bound is safe only after multipole flux g_perp and source-boundary injection B_src are killed or bounded. | Source Q_m^H, g_perp, B_src and trace constants if no zero certificate closes. |
| DEC4306_3_next | SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_NEXT | The shortest path is to parent-own smooth matter/no-excision; fallback is finite inner flux profile fill. | 4307-Y5-R2FR-source-domain-owner-or-inner-flux-profile-fill.md |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4306_0 | Do not use smooth no-excision N_inner=0 for exterior point/excision source models. | ACTIVE |
| FW4306_1 | Do not import old no-flux precedent as a parent certificate; 1529 says the certificate was not found. | ACTIVE |
| FW4306_2 | Do not reduce N_inner to C_inner\|Q_m^H\| unless g_perp and B_src are zero or separately bounded. | ACTIVE |
| FW4306_3 | Do not drop radiative/boundary flux; route it as boundary/Hamiltonian flux or bound it. | ACTIVE |
| FW4306_4 | Do not claim local GR until N_pair, lambda_m, Khat/connection and projection constants are theorem-zero or source-backed. | ACTIVE |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4306_0_Ninner | N_inner | BOUNDARY_LAW_DERIVED | zero requires source-domain ownership; fallback requires flux profile |
| STAT4306_1_QmH | Q_m^H | MONOPOLE_INPUT_MISSING | not enough without multipole/source-boundary guard |
| STAT4306_2_gperp | g_perp | NEW_REQUIRED_INPUT | prevents scalar monopole overclaim |
| STAT4306_3_Bsrc | B_src | NEW_REQUIRED_INPUT | source-boundary injection must be zero or bounded |
| STAT4306_4_Npair | N_pair | REDUCED_NOT_CLOSED | smooth branch promising; excision branch needs profile/certificate |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4306_0 | 4307-Y5-R2FR-source-domain-owner-or-inner-flux-profile-fill.md | Does the parent local source branch own a smooth no-excision Hilbert domain, or must the inner flux profile be filled? | prove compact sources are smooth Hilbert matter on the m-lock domain so partialD_in is empty and N_inner=0 | fill Q_m^H, g_perp, B_src, C_0 and C_perp for the trace-bound fallback |
