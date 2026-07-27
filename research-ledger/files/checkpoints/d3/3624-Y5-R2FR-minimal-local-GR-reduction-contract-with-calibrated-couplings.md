# 3624 Y5 R2FR minimal local-GR reduction contract with calibrated couplings

**Status:** 3624 consolidates the local-GR/Newton/Maxwell reduction route: calibrated G_eff and alpha_eff are allowed, but every extra MTS residual is now explicit and must be theorem-zeroed or bounded before any local-GR claim.

**Claim ceiling:** this checkpoint does not claim local GR, Newtonian mechanics, Maxwell source ownership, PPN pass, WEP pass, R10/R11 pass, or numerical prediction of `G`/`alpha`.

## Core move

3624 makes the least-smuggled local route explicit:

1. Use calibrated low-energy constants `G_eff`, `alpha_eff`, `Lambda_eff`, and `c` where standard theory also uses measured constants.
2. Derive the **form** of the local equations: Einstein-Hilbert metric equation, Newton/Poisson weak field, Maxwell Hilbert stress, and Poynting source-flow identity.
3. Put every non-GR/MTS contribution into an explicit residual vector.
4. Demand theorem-zero or source-backed bound rows for every residual before any claim.

This is not retreat; it is the cleaner boxing stance. We stop throwing haymakers at constants and make the judges score the actual residuals.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3623_NEXT_TARGET.csv | True | True | 3623 selected calibrated-coupling local-GR contract. |
| gr_constant_3623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3623_GR_G_CONSTANT_ANALOGY.csv | True | True | GR/Newton constant analogy: measured constants are acceptable at reduction stage. |
| coupling_no_go_3623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3623_COUPLING_SCALING_NO_GO.csv | True | True | EM coupling ratio/no-go source. |
| wem_phi_3623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv | True | True | Poynting and EM Hilbert stress split. |
| motion_load_02 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\02-motion-load-local-GR-reduction.md | True | True | early motion-load local-GR conditional status. |
| observer_contract_10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\10-observer-map-symplectic-contract.md | True | True | older no-smuggling PPN/conservation completion requirements. |
| min_parent_action_511 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv | True | True | minimum parent local-GR action blocks. |
| min_parent_residual_511 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv | True | True | prior local-GR residual vector. |
| einstein_lhs_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv | True | True | Einstein left-hand residual decomposition. |
| newton_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv | True | True | Newton/Poisson weak-field conditional bridge. |
| operator_pack_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv | True | True | operator residual pack and nonclaim lock. |
| eh_envelope_2579 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv | True | True | absolute local-GR residual envelope. |
| ppn_interface_2636 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv | True | True | PPN component interface map. |
| gk_stress_2469 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv | True | True | GK stress and local metric equation gate. |
| maxwell_poynting_3463 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv | True | True | Maxwell action, Hilbert stress, Poynting ledger. |

## Minimal local-GR contract

| contract_id | contract_piece | formula | required_proof_or_bound | current_status |
| --- | --- | --- | --- | --- |
| LGC3624_0_domain | observed local fields | Domain_local={g_obs,e_obs,A_Q,psi_matter,Phi_MTS}; readout fixed before tests | parent observer/coframe map and no shadow-frame/readout morphism | CONTRACT_ONLY |
| LGC3624_1_action_normal_form | EH plus calibrated constants | S_local=(2*kappa_eff)^-1 int sqrt(-g)(R-2Lambda_eff)+S_matter+S_EM+S_extra+S_boundary | derive EH dominance and show S_extra/S_boundary contribute only explicit zero-or-bound residuals | CONDITIONAL_NOT_PARENT_SIGNED |
| LGC3624_2_metric_equation | local field equation | G_mn+Lambda_eff g_mn = kappa_eff(T_matter_mn+T_EM_mn)+DeltaE_MTS_mn | DeltaE_MTS_mn=0 by theorem or |projection(DeltaE)| below local tests with no-cancellation guard | EXPLICIT_RESIDUAL_CONTRACT_WRITTEN |
| LGC3624_3_newton_limit | Newton/Poisson limit | nabla^2 Phi = 4*pi*G_eff*rho_H + delta_Newton_MTS; a=-grad Phi | delta_Newton_MTS=0/bounded; rho_H equals measured source charge before orbital fitting | CONDITIONAL_TEMPLATE_NOT_CLAIMED |
| LGC3624_4_ppn_completion | PPN/local GR completion | Delta_PPN_abs=|gamma-1|+|beta-1|+|alpha_i|+|zeta_i|+|xi|+readout/source terms | each PPN component theorem-zeroed or source-bounded independently; no cancellation-only pass | PPN_VECTOR_CONTRACT_WRITTEN |
| LGC3624_5_bianchi_conservation | Bianchi/conservation compatibility | nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=0 with nabla_m(T_matter+T_EM+DeltaT_MTS)^{mn}=0 | parent Noether identity or explicit residual-conservation closure | NEXT_DERIVATION_TARGET |
| LGC3624_6_maxwell_stress | Maxwell/EM stress coupling | T_EM^{mn}=-(2/sqrt(-g))delta S_EM/delta g_mn; T_EM^{0i}=S_Poynting^i/c^2 | observed Hodge/coframe descent, same current owner, w_EM=0/bound, Phi_EM boundary branch | CONDITIONAL_STRUCTURE_WRITTEN |

## Calibrated constants ledger

| constant_id | constant | allowed_status | formula | still_required |
| --- | --- | --- | --- | --- |
| CC3624_0_G_eff | G_eff or kappa_eff | CALIBRATED_CONSTANT_ALLOWED | kappa_eff=8*pi*G_eff/c^4; c=1 convention gives kappa_eff=8*pi*G_eff | prove constancy/local drift bound and same source mass rho_H/M_H_ref |
| CC3624_1_alpha_eff | alpha_eff | CALIBRATED_CONSTANT_ALLOWED | alpha_eff=Q_*^2/(4*pi*Z_Q) | prove no drift/source residual or provide clock/WEP/EM bounds |
| CC3624_2_Lambda_eff | Lambda_eff | LOCAL_BACKGROUND_PARAMETER | G_mn+Lambda_eff g_mn; local compact tests take Lambda_eff*r^2 << tolerance | do not let Lambda/memory branch fake local source residuals |
| CC3624_3_c_units | c | UNIT_AND_CAUSAL_CONVERSION_CONSTANT | ds^2=-c^2 dt^2+dx^2 locally; often set c=1 | if MTS modifies time-flow interpretation, preserve tested null cone and clock observables |

## Explicit MTS residual vector

| residual_id | symbol | contract | observable_links | current_status |
| --- | --- | --- | --- | --- |
| RV3624_0_DeltaE | DeltaE_MTS_mn | must vanish by EH dominance/Lovelock/locality theorem or project below PPN/R10/orbital bounds | PPN;R10;orbital;clocks;growth | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_1_source_weight | DeltaT_source; w_EM; kappa_J; delta_ellJ | same Noether/Hilbert source owner or source-backed WEP/Newton/clock bound | WEP;Newton_GM;R10;PPN;clocks | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_2_coupling_drift | delta_kappa; b_alpha; lambda_F2 | calibration allowed, but local drift and independent F2/source coefficients must be zeroed or bounded | Gdot;alpha_dot;clock spectroscopy;WEP | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_3_q_loc | q_loc^nu | derive Ward/local vacuum zero or map to PPN/R10/clock/orbital components | PPN preferred-frame;R10;clocks;orbital | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_4_GK_stress | T_GK_mn; T_tau/P_mn | positive/no-hair/stealth theorem or metric Green-function bound | PPN gamma,beta;orbital;R10 | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_5_PiM_boundary | delta_PiM; Phi_EM_boundary; Q_boundary | fixed-before-readout Pi_M and no-flux/reference theorem or source-backed boundary flux row | Newton_GM;R10;R11;orbital energy | LIVE_ZERO_OR_BOUND_REQUIRED |
| RV3624_6_PPN_total | Delta_PPN_abs | no cancellation-only pass; every component independently theorem-zeroed or bounded | all local GR/PPN tests | SCHEMA_READY_VALUES_MISSING |

## Newton / PPN completion gates

| gate_id | gate | required_result | current_status | blocks_claim_if_missing |
| --- | --- | --- | --- | --- |
| NPG3624_0_EH_dominance | Einstein left-hand form | E_LHS -> G_mn + Lambda g_mn + explicit DeltaE_MTS_mn | CONDITIONAL_NOT_PARENT_PROOF | True |
| NPG3624_1_Poisson | Newton/Poisson equation | nabla^2 Phi=4*pi*G_eff*rho_H with delta_Newton_MTS=0/bounded | CONDITIONAL_TEMPLATE_NOT_PARENT_DERIVED | True |
| NPG3624_2_Gauss_worldtube | inverse-square/source mass | closed source worldtube gives Phi=-G_eff*M_H/r with M_H fixed before orbital fitting | SOURCE_WORLDTUBE_GLUE_OPEN | True |
| NPG3624_3_gamma | PPN gamma | gamma-1=0 or bounded after reciprocal/readout residuals | CONDITIONAL_GAMMA_NOT_ENOUGH | True |
| NPG3624_4_beta | PPN beta/nonlinear completion | beta-1=0 or bounded from second-order field/readout map | OPEN | True |
| NPG3624_5_bianchi | Bianchi/conservation | residual tensor and source exchange satisfy parent Noether identity | NEXT_TARGET | True |

## Maxwell / Hilbert stress gates

| gate_id | gate | required_result | current_status |
| --- | --- | --- | --- |
| MHG3624_0_action | observed Maxwell action | S_EM uses same g_obs/e_obs/Hodge as the local gravitational variation | STANDARD_CONDITIONAL_ACTION_FORM |
| MHG3624_1_hilbert_stress | EM Hilbert stress | T_EM_mn is the variational stress entering the same source slot as matter | EXACT_FROM_ACTION_CONDITIONAL |
| MHG3624_2_poynting | Poynting/source-flow identity | T_EM^{0i}=S_Poynting^i/c^2 in the local inertial frame | EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY |
| MHG3624_3_exchange | matter/EM stress exchange | nabla_m T_EM^{mn}=-F^{nl}J_l and total matter+EM+MTS stress is conserved | CONDITIONAL_ON_CURRENT_OWNER |
| MHG3624_4_w_phi | EM source-weight/boundary residual | w_EM=0/bounded and Phi_EM_boundary stationary-zero or radiative-flux-accounted | CONDITIONAL_NOT_PARENT_SIGNED |

## Claim gates

| claim_gate_id | claim | gate_status | reason |
| --- | --- | --- | --- |
| CG3624_0_calibrated_constants | using calibrated G_eff and alpha_eff is allowed | PASS_AS_STRATEGY_NOT_PUBLIC_CLAIM | GR itself measures G; the real test is equation form plus residual suppression. |
| CG3624_1_local_GR | MTS derives local GR | FAIL_CURRENT_CLAIM | DeltaE_MTS, source/readout, beta, Bianchi, boundary and PPN residuals are not all zeroed or bounded. |
| CG3624_2_Newton | MTS derives Newtonian mechanics | FAIL_CURRENT_CLAIM | Poisson/Gauss/source-mass closure remains conditional. |
| CG3624_3_Maxwell_source | MTS fully derives Maxwell/EM stress coupling | FAIL_CURRENT_CLAIM_BUT_CONTRACT_SHARP | Poynting/Hilbert identities are exact once the observed Maxwell action is admitted, but parent Hodge/current/source ownership is not signed. |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3625-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md | scripts/Y5_R2FR_3625_Bianchi_residual_closure_or_first_PPN_envelope_runner.py | derive the parent Noether/Bianchi closure for the explicit residual vector, or build the first executable PPN/Newton residual envelope with nonclaim source rows | either nabla_m[DeltaE_MTS-kappa DeltaT_MTS] closes from parent symmetry, or each residual component is mapped to a no-cancellation PPN/Newton bound interface |
