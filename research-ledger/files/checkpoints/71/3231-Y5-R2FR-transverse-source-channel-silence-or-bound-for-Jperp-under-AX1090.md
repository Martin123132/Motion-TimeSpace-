# 3231 - Transverse Source Channel Silence Or Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3231 splits the source that controls the transverse clock-path drift from 3230.

The zero route is exact but demanding:

```text
J_perp^tau = 0,
Phi_perp^tau = 0,
O_perp positive with no kernel
=> Y_perp=0
=> v_perp=0.
```

But `J_perp^tau=0` is not a single statement. The no-cancellation split is:

```text
J_perp^tau
= J_geom
 + J_matter
 + J_EM_trace
 + J_EM_F2
 + J_Poynting_bulk/collar
 + J_memory
 + J_projector.
```

Therefore

```text
||J_perp^tau||_2
<= J_geom_bound
 + J_matter_bound
 + J_EM_trace_bound
 + (1/4)|f_perp_prime(0)| ||F^2||_2
 + J_Poynting_bound
 + J_memory_projector_bound.
```

Boundary/collar flux contributes separately:

```text
|Phi_perp^tau|
<= Phi_geom + Phi_matter + Phi_EM_F2_boundary
 + Phi_Poynting + Phi_memory_projector.
```

This feeds the 3230 amplitude law:

```text
Y_perp <= (J_perp_bound/m_perp_min
          + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2.
```

Key result: Maxwell trace silence is not enough. The two live danger channels are:

```text
J_EM_F2 = (1/4) f_perp_prime(0) F^2,
Phi_Poynting <= C_flux ||S_EM · n||_boundary/collar/worldtube.
```

`F^2=0` can silence one scalar bulk invariant, but it does not silence Poynting/stress/boundary flux.

Current verdict: `JPERP_SOURCE_SPLIT_DERIVED_EMF2_AND_POYNTING_REMAIN_LIVE`.

## Jperp Source Silence Audit

| audit_id | channel | source_formula | zero_condition | finite_bound | status | blocks_exact_zero | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JPA3231_0_total_decomposition | total J_perp | J_perp^tau = J_geom + J_matter + J_EM_trace + J_EM_F2 + J_Poynting_bulk/collar + J_memory + J_projector | all summands are theorem-zero on the same parent transverse branch | \|\|J_perp^tau\|\|_2 <= sum_i \|\|J_i\|\|_2 with absolute no-cancellation | DECOMPOSITION_DERIVED | any live channel | false |
| JPA3231_1_geom | geometric/source curvature | J_geom from transverse variation of the local operator/background geometry | local exterior solves parent Euler equations and P_perp excludes pure gauge/branch reparametrization | J_geom_bound := \|\|J_geom\|\|_2 | BOUND_SYMBOL_STAGED | MISSING_PARENT_EULER_SAME_BRANCH | false |
| JPA3231_2_EM_trace | Maxwell trace | J_EM_trace proportional to T_EM^mu_mu | trace-only coupling to pure Maxwell in 4D; no material/readout/F2/Poynting couplings | J_EM_trace_bound := \|\|c_trace T_EM\|\|_2 | CONDITIONAL_ZERO_NOT_SUFFICIENT | safe only for trace-only parent coupling | false |
| JPA3231_3_EM_F2 | EM kinetic F2 coupling | J_EM_F2 = (1/4) f_perp_prime(0) F_{mu nu}F^{mu nu} | no-extra-F2 theorem, f_perp_prime(0)=0, strict same-branch EM source-root, or F^2 support zero plus no readout reentry | \|\|J_EM_F2\|\|_2 <= (1/4)\|f_perp_prime(0)\| \|\|F^2\|\|_2 | ACTIVE_DANGER_CHANNEL | MISSING_NO_EXTRA_F2_OR_SOURCE_ROOT | false |
| JPA3231_4_Poynting | Poynting/collar/worldtube flux | J_Poynting or Phi_Poynting sourced by S_EM·n, T_EM^{0i}, or boundary/collar flux | flux channel is absent from parent coupling, or exact/proper/orthogonal boundary theorem kills it | J_Poynting_bound + Phi_Poynting_bound from absolute boundary/worldtube flux norm | ACTIVE_BOUNDARY_GUARD | F^2=0 DOES_NOT_KILL_POYNTING | false |
| JPA3231_5_matter_marker | matter/readout/material markers | J_matter = Lie_vperp S_matter plus label/readout/material-constant variations | matter functor, labels, masses, charges, and readout descend through q with no transverse marker | J_matter_bound := \|\|Lie_vperp S_matter\|\|_2 plus readout-marker bounds | UNSIGNED_SOURCE_FUNCTOR | MISSING_NO_MARKER_THEOREM | false |
| JPA3231_6_memory_projector | memory/projector | J_memory + J_projector from transverse variation of memory kernel/projector/domain | projector commutes with transverse split or transverse sector is orthogonal to memory source | J_memory_projector_bound := \|\|J_memory\|\|_2 + \|\|J_projector\|\|_2 | BOUND_SYMBOL_STAGED | MISSING_PROJECTOR_ORTHOGONALITY | false |

## Jperp Finite Bound Formula

| bound_id | quantity | formula | zero_requirement | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| JPB3231_0_total_norm | \|\|J_perp^tau\|\|_2 | \|\|J_perp^tau\|\|_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4)\|f_perp_prime(0)\| \|\|F^2\|\|_2 + J_Poynting_bound + J_memory_projector_bound | each term is zero by theorem on the same R_Q transverse branch | FINITE_SUM_BOUND_DERIVED_SYMBOLIC | false |
| JPB3231_1_exact_zero | J_perp^tau | J_perp^tau=0 if J_geom=J_matter=J_EM_trace=J_EM_F2=J_Poynting=J_memory=J_projector=0 | no-extra-F2/source-root plus Poynting/boundary silence plus no-marker/projector orthogonality | EXACT_ZERO_CONDITION_DERIVED_NOT_SIGNED | false |
| JPB3231_2_Yperp_update | a_perp | a_perp <= \|\|J_perp^tau\|\|_2_bound / m_perp_min | a_perp=0 only if total source norm is theorem-zero | FEEDS_3230_YPERP | false |

## Phi-perp Boundary Audit

| phi_id | quantity | formula | zero_condition | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PHI3231_0_total_boundary | Phi_perp^tau | \|Phi_perp^tau\| <= Phi_geom + Phi_matter + Phi_EM_F2_boundary + Phi_Poynting + Phi_memory_projector | each boundary/corner/worldtube term is exact/proper/orthogonal or absent | BOUND_DECOMPOSITION_DERIVED | false |
| PHI3231_1_Poynting_boundary | Phi_Poynting | Phi_Poynting <= C_flux \|\|S_EM·n\|\|_{boundary/collar/worldtube} | no EM flux through the relevant boundary, or flux term is exact/proper/orthogonal to v_perp | ACTIVE_BOUNDARY_GUARD | false |
| PHI3231_2_exact_zero | Phi_perp^tau=0 | Phi_perp^tau=0 if all boundary/corner/worldtube terms vanish theorem-wise | not established by F^2=0 or trace silence alone | EXACT_ZERO_CONDITION_DERIVED_NOT_SIGNED | false |

## Vperp Feedback To 3230

| feedback_id | feeds | substitution | result | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VFB3231_0_finite_Yperp | VP3230_3_amplitude_bound | a_perp=J_perp_bound/m_perp_min; b_perp=Phi_perp_bound | Y_perp <= (J_perp_bound/m_perp_min + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2 | FORMULA_READY_INPUTS_MISSING | false |
| VFB3231_1_exact_vperp_zero | VP3230_5_zero_case | J_perp_bound=0 and Phi_perp_bound=0 | Y_perp=0 and v_perp=0 if O_perp is positive with no kernel | ZERO_ROUTE_CLEAR_BUT_UNSIGNED | false |
| VFB3231_2_live_danger_channels | 3232 target | EM_F2 and Poynting are the first channels to prove zero or bound | trace silence alone cannot close v_perp; F^2=0 alone cannot close Poynting | NEXT_TARGET_SELECTED | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3231_0_result | JPERP_SOURCE_SPLIT_DERIVED_EMF2_AND_POYNTING_REMAIN_LIVE | the transverse source norm now has an exact no-cancellation bound and an exact zero condition, but EM_F2 and Poynting/boundary flux cannot be killed by Maxwell trace silence or F^2=0 alone | NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM | attack EM_F2 no-extra/source-root and Poynting boundary silence/bounds as the first live channels feeding v_perp | false |
| DEC3231_1_next_target | 3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090 | these are the channels most likely to spoil v_perp=0; closing or bounding them directly improves the local clock/EM coupling gate | PRIVATE_NEXT_TARGET | derive no-extra-F2/source-root conditions for f_perp_prime(0), and a proper/orthogonal/finite Poynting flux boundary clause | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_JPERP_FINITE_BOUND_FORMULA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_VPERP_FEEDBACK_TO_3230.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3231_00_3230_doc | 3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090.md | true | 3230 handoff selecting J_perp source channels | L21:O_perp v_perp = J_perp^tau + boundary/corner/source-worldtube terms, \| L29:a_perp := \|\|J_perp^tau\|\|_2 / m_perp_min, \| L59:J_perp^tau = 0, \| L77:\| VP3230_1_linearized_operator \| v_perp equation \| transverse tangent solves a 3210-type linearized elliptic/coercive problem \| O_perp v_perp = J_perp^tau + Phi_perp^tau boundary terms \| CONDITIONAL_OPERATOR_ROUTE \| pare | false |
| SRC3231_01_3230_split | P8_Y5_R2FR_3230_TRANSVERSE_SOURCE_CHANNEL_SPLIT.csv | true | machine transverse source-channel split | L4:JPERP3230_2_EM_F2,EM kinetic scalar coupling,J_perp^EM_F2 proportional to f_perp'(0) F^2,zero if no-extra-F2 theorem or f_perp'(0)=0; otherwise bound by local field invariant support,ACTIVE_DANGER_CHANNEL,false,2026-06-2 \| L5:JPERP3230_3_Poynting_flux,EM wave/Poynting boundary flux,null radiation can have F^2=0 while T_EM^{0i} and boundary/worldtube flux are nonzero,must be shown orthogonal/proper/boundary-silent or finitely bounded; cannot b \| L7:JPERP3230_5_boundary,Phi_perp^tau,all boundary/corner/source-worldtube flux for transverse tangent energy,zero if exact/proper/orthogonal boundary theorem; otherwise finite source-backed absolute bound,MISSING_BOUNDARY_Z | false |
| SRC3231_02_3230_vperp | P8_Y5_R2FR_3230_VPERP_AMPLITUDE_BOUND.csv | true | machine v_perp amplitude law | L3:VP3230_1_linearized_operator,v_perp equation,transverse tangent solves a 3210-type linearized elliptic/coercive problem,O_perp v_perp = J_perp^tau + Phi_perp^tau boundary terms,CONDITIONAL_OPERATOR_ROUTE,parent-signed O_ \| L5:VP3230_3_amplitude_bound,Y_perp,Y_perp := sqrt(E_perp),"Y_perp <= (a_perp + sqrt(a_perp^2 + 4 b_perp))/2, with a_perp=\|\|J_perp^tau\|\|_2/m_perp_min and b_perp=\|Phi_perp^tau\|",AMPLITUDE_BOUND_DERIVED_CONDITIONALLY,"numeric/ \| L7:VP3230_5_zero_case,v_perp=0,transverse no-hair/tangent collapse,"if J_perp^tau=0, Phi_perp^tau=0, ker(O_perp)=0, and positive coercivity holds, then Y_perp=0 and v_perp=0",EXACT_CONDITIONAL_ZERO_THEOREM,"source silence,  | false |
| SRC3231_03_3210_doc | 3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md | true | source split and Poynting warning | L10:source/boundary leakage -> X amplitude -> deltaX amplitude -> omega_X curl bound. \| L17:= int_A X J_X dV + Phi_boundary \| L22:a_X := \|\|J_X\|\|_2 / m_min \| L45:J_X = 0, Phi_boundary = 0, tangent source = 0, tangent boundary = 0 | false |
| SRC3231_04_3210_source_split | P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv | true | machine source split with EM/Poynting channels | L4:JXS3210_2_EM_F2,gauge kinetic scalar coupling,DeltaS_EM=-(1/4)int sqrt(-g) f_X(X) F_{mu nu}F^{mu nu}; J_X^EM=(1/4)sqrt(-g) f_X'(X) F^2.,no-extra-F2 theorem or f_X'(0)=0 from parent representation/gauge-norm signature,cou \| L5:JXS3210_3_Poynting_flux,EM wave/Poynting boundary flux,"For null radiation F^2=0 can hold while S=(E x B)/mu0 and T_EM^{0i} are nonzero; this is boundary/worldtube flux, not automatically bulk scalar trace source.","pare \| L6:JXS3210_4_matter_marker,ordinary matter/material constants,"J_X^matter=Lie_vX S_matter or qbar_XT; vanishes if matter, constants, masses, EM markers, and readout labels descend through q with Lie_vX theta_A=0.",no-marker | false |
| SRC3231_05_3220_doc | 3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md | true | EM F2 source-root and wave-stress guard | L23:Branch B: stop claiming zero and source finite bounds for lambda_F, F_EM'', Delta m, Z_min, \|\|F_Q^2\|\|, G_mem, readout, and EM stress/Poynting residuals. \| L26:Important wave guard: `F_Q^2=0` for null radiation does **not** mean the Maxwell stress tensor or Poynting vector vanishes. So an EM `F^2` double-zero can silence one scalar bulk coefficient, but it is not by itself a fu \| L28:Current verdict: `EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED_FINITE_DZ_INPUTS_STAGED`. \| L40:\| ROOT3220_6_wave_stress_channel \| EM wave/Poynting channel is not silently ignored \| F_Q^2=0 for null waves does not imply T_EM=0 or Poynting flux=0 \| SEPARATE_CHANNEL_RETAINED \| Hodge-star/readout/current stress descen | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3231_00_inputs_exist | true | inputs=6 |
| VAL3231_01_total_bound | true | J_perp no-cancellation finite sum bound derived |
| VAL3231_02_emf2_live_guard | true | EM_F2 retained as active danger channel |
| VAL3231_03_poynting_live_guard | true | Poynting/boundary flux retained as active guard |
| VAL3231_04_yperp_feedback | true | J/Phi bounds feed Y_perp |
| VAL3231_05_claims_blocked | true | claim_rows_true=0 |
| VAL3231_06_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3231_07_csv_parse | true | P8_Y5_R2FR_3231_INPUTS.csv;P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv;P8_Y5_R2FR_3231_JPERP_FINITE_BOUND_FORMULA.csv;P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv;P8_Y5_R2FR_3231_VPERP_FEEDBACK_TO_3230.csv;P8_Y5_R2FR_3231_DECISION.csv |
| VAL3231_08_next_target | true | 3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
