# 4307 - source-domain owner or inner flux profile fill

## Verdict
- Derived the source-domain split behind `N_inner`: smooth Hilbert volume source gives exact `N_inner=0`; exterior/worldtube/excision source keeps a live boundary flux.
- Converted the fallback into a concrete schema: `g_in`, `Q_m^H`, `g_perp`, `B_src`, `C_0`, `C_perp`, and the no-cancellation `N_inner` envelope.
- Updated `N_pair`: smooth branch reduces to `N_EM + N_rest`; exterior branch uses the full flux-profile bound.
- No Newton/local-GR claim fires, because the worldtube-Hilbert equality, `I_commutator`, calibration and `lambda_m` gates are still open.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4307_00_4306_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md | True | True | 4306 handoff: decide source-domain ownership or fill inner flux profile. |
| SRC4307_01_4306_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\322-PPC4161-inner-domain-certificate-or-QmH-bound.md | True | True | 4306 theorem: smooth no-excision domain kills N_inner. |
| SRC4307_02_hilbert_source_measure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md | True | True | ordinary source sectors already written as one Hilbert volume source measure. |
| SRC4307_03_hilbert_source_action | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md | True | True | source action begins as Hilbert matter plus EM/binding sectors. |
| SRC4307_04_worldtube_glue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md | True | True | worldtube support and Hamiltonian source readout are defined as the same source object. |
| SRC4307_05_same_source_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md | True | True | worldtube readout should not be a post-orbit fitted mass. |
| SRC4307_06_selector_quarantine | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\190-PPC4161-parent-action-selector-or-local-branch-quarantine.md | True | True | conditional local parent-action selector includes single Hilbert source ownership. |
| SRC4307_07_boundary_noflux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | boundary/radiative flux is routed rather than erased. |
| SRC4307_08_4211_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4211-Y5-R2FR-Htau-MHsource-parent-charge-owner-or-visible-matter-residual-scorecard.md | True | True | H_tau/M_H source owner contract remains viable but unsigned. |
| SRC4307_09_1714_equality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton chain remains blocked by same-object equality. |
| SRC4307_10_1715_commutator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md | True | True | topological/exterior branch needs chain-map/source-domain ownership. |

## Source-Domain Owner Matrix
| row_id | domain_choice | boundary_status | inner_result | status | note |
| --- | --- | --- | --- | --- | --- |
| DOM4307_0_smooth_Hilbert_volume | D_m contains the compact source as a Hilbert volume source; no source hole is removed. | partialD_in = empty set | N_inner = 0 exactly | SUPPORTED_CONDITIONAL_BRANCH | Best route for local GR: source is matter density on the same observed Hilbert measure, not an excised inner boundary. |
| DOM4307_1_exterior_worldtube_annulus | D_m is the exterior annulus A_ext = D_m \ W_H and W_H is removed from the operator domain. | partialD_in = partial W_H | N_inner <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| | LIVE_FALLBACK_BRANCH | This is the honest orbit/readout branch until the flux profile or no-flux matching is supplied. |
| DOM4307_2_point_particle_excision | source is treated as a point/hole/singularity and matched only by exterior data. | partialD_in nonempty or distributional | no zero theorem; use profile/renormalized boundary data | CLOSURE_ONLY_UNTIL_REGULARIZED | Do not borrow smooth Hilbert volume zero for point-particle closure language. |
| DOM4307_3_parent_no_flux_boundary | parent signs Z_m n.grad u\|partialW=0 and B_src=0 on the worldtube surface. | partialD_in exists but integrand is zero | N_inner = 0 exactly | UNSIGNED_ZERO_BRANCH | Useful if derived, but older no-flux attempts did not already provide this certificate. |
| DOM4307_4_smoothing_limit | a family of smooth Hilbert source densities rho_epsilon converges to an exterior mass readout. | partialD_in empty for every epsilon; limit may create a surface term | zero survives only if trace/defect measure tends to zero | PROMISING_BUT_NEEDS_LIMIT_THEOREM | This is the bridge between engineering intuition and rigorous exterior-source tests. |

## Smooth Hilbert No-Inner-Boundary Theorem
| theorem_id | statement | proof_input | consequence | status |
| --- | --- | --- | --- | --- |
| THM4307_0_domain_identity | If D_m is the smooth Hilbert source volume domain, then partialD_in is empty. | 4306 gives B_inner[phi]=int_partialD_in phi Z_m n.grad u dSigma + B_src[phi]. | No inner surface means the geometric boundary integral is absent. | DERIVED_CONDITIONAL |
| THM4307_1_source_injection_absent | On the smooth Hilbert volume branch, source support is in the volume Euler-Lagrange/Hilbert term, not injected on an artificial inner boundary. | 185 writes ordinary sectors on the same observed metric/coframe and volume measure. | B_src[phi]=0 for artificial inner-boundary injection on that branch. | CONDITIONAL_ON_PARENT_SOURCE_DOMAIN |
| THM4307_2_smooth_zero | smooth Hilbert volume branch: partialD_in=empty and B_src=0. | N_inner=sup \|B_inner[phi]\|. | N_inner=0 exactly. | EXACT_ZERO_IF_BRANCH_SIGNED |
| THM4307_3_exterior_obstruction | If the source is removed and only A_ext is solved, partialW_H is a true boundary. | 4306 trace theorem applies. | N_inner cannot be set to zero without no-flux/matching or a flux profile. | OBSTRUCTION_RETAINED |
| THM4307_4_same_source_warning | Worldtube mass readout can be same-source without killing the exterior inner flux. | 1714/1715 keep R_eq and I_commutator open. | source-to-Newton normalization remains blocked even if N_inner smooth branch is conditionally clean. | NO_LOCAL_GR_CLAIM |

## Exterior/Worldtube Matching Runner
| runner_id | branch_name | inner_input | formula | status | note |
| --- | --- | --- | --- | --- | --- |
| RUN4307_0_smooth_Hilbert_m_lock | smooth Hilbert volume source domain | N_inner=0 | N_pair <= N_EM + N_rest | CONDITIONAL_FAST_ROUTE | Use only if parent signs that the m-lock operator domain includes the smooth source volume. |
| RUN4307_1_smooth_plus_EM_rest_zero | smooth Hilbert source plus Maxwell-Hodge/rest selector zeros | N_inner=N_EM=N_rest=0 | N_pair=0 | EXACT_SOURCE_PAIR_ZERO_IF_ALL_SELECTOR_CLAUSES_SIGNED | This is the serious route toward the local no-hair/local-GR gate, but it is still conditional. |
| RUN4307_2_exterior_worldtube | exterior annulus with source removed | N_inner <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| | N_pair <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| + N_EM + N_rest | PROFILE_ROUTE_READY_INPUTS_MISSING | No more vague Q_m^H: the monopole, multipole and injection terms must be separated. |
| RUN4307_3_parent_no_flux_worldtube | exterior annulus with parent no-flux matching | Z_m n.grad u=0 and B_src=0 on partialW_H | N_pair <= N_EM + N_rest | UNSIGNED_ZERO_ROUTE | Equivalent strength to the smooth branch for N_inner, but needs a real matching theorem. |
| RUN4307_4_to_m_lock_lambda | source-domain-selected N_pair into m-lock | Delta_m <= (N_pair+N_N)/lambda_m | C4302_DVGAMMA_QUAD receives the selected source-domain branch | HANDOFF_READY_NOT_NUMERIC | Next gate is parent-signing the domain choice or filling first flux numbers before scoring lambda_m. |

## Inner Flux Profile Schema
| profile_id | symbol | definition | units | status | next_input |
| --- | --- | --- | --- | --- | --- |
| FLUX4307_0_domain_convention | domain_choice | smooth_volume \| exterior_worldtube \| point_excision \| no_flux_matched | dimensionless selector | MISSING_PARENT_INPUT | must be parent-signed before choosing zero or profile branch |
| FLUX4307_1_inner_surface | partialW_H | worldtube inner boundary geometry if exterior branch is used | area/length convention | MISSING_ARENA_PROJECTION | needed for trace constants and monopole/multipole split |
| FLUX4307_2_normal_flux_profile | g_in = Z_m n.grad u\|partialW_H | normal memory/source flux profile on the inner boundary | same units as Z_m grad u | MISSING_PARENT_INPUT | zero theorem or measured/bounded profile required |
| FLUX4307_3_monopole_charge | Q_m^H = int_partialW_H g_in dSigma | inner monopole memory/source hair | profile units times area | MISSING_VALUE | scalar Q_m^H alone is insufficient unless g_perp and B_src are killed |
| FLUX4307_4_multipole_tail | g_perp = g_in - Q_m^H/Area(partialW_H) | higher-mode/tidal boundary flux | H^{-1/2}(partialW_H) | MISSING_VALUE | prevents scalar monopole overclaim |
| FLUX4307_5_source_boundary_injection | B_src | source injection/improvement term living on partialW_H | H^{-1/2} dual norm | MISSING_PARENT_INPUT | must be zero by smooth volume branch or bounded in exterior branch |
| FLUX4307_6_trace_constants | C_0, C_perp | trace/geometry constants converting flux profile into N_inner | operator-domain constants | MISSING_ARENA_PROJECTION | needed before any numeric R10/PPN/local test can score this branch |
| FLUX4307_7_no_cancellation_sum | N_inner_bound | C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| | same norm as N_inner | FORMULA_READY_VALUES_MISSING | absolute envelope only; no cancellation between channels allowed |

## Npair Source-Domain Update
| update_id | branch_name | formula | reason | status |
| --- | --- | --- | --- | --- |
| NPAIR4307_0_standard_smooth_branch | standard Dq/Hperp source branch plus smooth Hilbert volume source domain | N_pair <= N_EM + N_rest | N_src=0 from 4305 and N_inner=0 from 4307 conditional domain identity | REDUCED_IF_DOMAIN_SIGNED |
| NPAIR4307_1_all_visible_selector | smooth Hilbert volume plus visible Maxwell-Hodge/rest selector | N_pair=0 | requires EM/rest/source-domain clauses all parent-signed | EXACT_ROUTE_CONDITIONAL_NOT_CLAIMED |
| NPAIR4307_2_exterior_profile | exterior worldtube/source-removed branch | N_pair <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| + N_EM + N_rest | the safe fallback if source-domain ownership does not close | BOUND_ROUTE_READY_INPUTS_MISSING |
| NPAIR4307_3_source_to_Newton_guard | any branch trying Newton/local-GR source normalization | retain R_eq + I_commutator + calibration tail unless 1714/1715 gates close | N_inner zero is not the same as worldtube-Hilbert/topological equality | GUARD_ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4307_0_gain | SOURCE_DOMAIN_SPLIT_DERIVED | The inner-boundary problem is no longer a fog bank: smooth Hilbert volume domain gives exact N_inner=0; exterior/worldtube domain keeps a flux profile. | Carry both branches explicitly until the parent signs the domain choice. |
| DEC4307_1_preferred | PREFER_SMOOTH_HILBERT_VOLUME_PARENT_SIGNATURE | It uses the existing Hilbert source-measure descent and avoids inventing artificial point-source boundary hair. | Try to parent-sign the smooth volume domain as the local ordinary-matter source branch. |
| DEC4307_2_fallback | EXTERIOR_FLUX_PROFILE_RETAINED | If tests require exterior worldtube/excision language, the inner boundary must be scored through Q_m^H, g_perp and B_src. | Create sourced/zero-theorem rows for the first worldtube flux profile. |
| DEC4307_3_guard | NEWTON_LOCAL_GR_STILL_BLOCKED | N_inner zero does not close R_eq/I_commutator/source-to-Newton chain or lambda_m numeric scoring. | Keep local-GR claim shut until source-domain, EM/rest, lambda_m, R_eq and I_commutator gates are all closed or bounded. |
| DEC4307_4_next | PARENT_SIGNATURE_OR_FIRST_FLUX_ROW_NEXT | The next useful move is not another audit; it is either sign the smooth Hilbert domain or fill the first concrete flux row. | 4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4307_0 | Do not use smooth Hilbert N_inner=0 inside an exterior/worldtube/excision domain. | ACTIVE |
| FW4307_1 | Do not erase a worldtube boundary by saying the source is Hilbert unless the operator domain actually includes the source volume. | ACTIVE |
| FW4307_2 | Do not reduce exterior flux to a scalar Q_m^H without g_perp and B_src zero/bound rows. | ACTIVE |
| FW4307_3 | Do not hide Poynting or radiative flux in the static bulk source; route it as Hilbert EM stress or boundary flux. | ACTIVE |
| FW4307_4 | Do not claim Newton/local-GR source normalization from N_inner alone; R_eq, I_commutator and calibration remain live. | ACTIVE |
| FW4307_5 | Do not score R10/PPN/clock/orbital rows from the flux schema until numeric values or theorem-zero certificates are sourced. | ACTIVE |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4307_0_source_domain | source-domain choice | SPLIT_DERIVED_PARENT_SIGNATURE_NEEDED | smooth Hilbert branch versus exterior worldtube branch is now explicit |
| STAT4307_1_Ninner_smooth | N_inner smooth branch | EXACT_ZERO_IF_PARENT_SIGNED | partialD_in empty and no artificial B_src |
| STAT4307_2_Ninner_exterior | N_inner exterior branch | FLUX_PROFILE_REQUIRED | Q_m^H, g_perp, B_src, C_0, C_perp needed |
| STAT4307_3_Npair | N_pair | REDUCED_BY_BRANCH_NOT_CLOSED | smooth branch can reduce to N_EM+N_rest; exterior branch has profile envelope |
| STAT4307_4_source_to_Newton | source-to-Newton chain | STILL_BLOCKED | 1714/1715 equality/commutator gates remain open |
| STAT4307_5_next | next target | DERIVATION_OR_FIRST_ROW | 4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4307_0 | 4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md | Can the parent local branch sign the smooth Hilbert volume source domain, or must the first worldtube flux-profile row be sourced? | derive from the parent/source action that ordinary compact matter stays inside the m-lock Hilbert volume domain, so partialD_in is empty | create the first sourced/zero-theorem row for g_in, Q_m^H, g_perp, B_src, C_0 and C_perp on partialW_H |
