# 3232 - EMF2 and Poynting Transverse Source Zero Or Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, Maxwell-stress claim, or public-facing result.

## Result

3232 attacks the two live electromagnetic channels from 3231.

The transverse scalar EM kinetic source is:

```text
J_EM_F2 = (1/4) f_perp_prime(0) F_mu_nu F^mu_nu.
```

Therefore:

```text
||J_EM_F2||_2 <= (1/4) |f_perp_prime(0)| ||F^2||_2.
```

It is zero only if one of these is actually parent-signed:

```text
f_perp_prime(0)=0
```

from no-extra-F2/operator-domain exclusion, same-branch strict EM source-root, or a support-specific `F^2=0` result with no readout reentry.

The Poynting/boundary channel is separate:

```text
Phi_Poynting <= C_flux ||S_EM . n||_B.
```

and

```text
F^2=0 does not imply S_EM=0 or T_EM^mu_nu=0.
```

So the refined transverse source/boundary update is:

```text
||J_perp^tau||_2
<= J_other_bound + (1/4) C_F2_perp ||F^2||_2 + J_Poynting_bound,

|Phi_perp^tau|
<= Phi_other_bound + Phi_EM_F2_boundary + C_flux ||S_EM . n||_B.
```

where `C_F2_perp:=|f_perp_prime(0)|`.

This feeds directly back into:

```text
Y_perp <= (J_perp_bound/m_perp_min
          + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2.
```

Current verdict: `EMF2_AND_POYNTING_ZERO_OR_BOUND_FORMULAS_DERIVED_NO_CHANNEL_CLOSED`.

## EMF2 Zero Or Bound Audit

| audit_id | channel | formula | zero_route | finite_route | status | claim_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EF3232_0_definition | transverse EM_F2 source | J_EM_F2 = (1/4) f_perp_prime(0) F_{mu nu}F^{mu nu} | f_perp_prime(0)=0 or F^2 support vanishes in the scored region | \|\|J_EM_F2\|\|_2 <= (1/4)\|f_perp_prime(0)\| \|\|F^2\|\|_2 | EXACT_FORMULA_STAGED | f_perp_prime(0) and \|\|F^2\|\| support not source-backed | false |
| EF3232_1_no_extra_F2 | operator-domain exclusion | no independent f_perp(X_perp)F_Q^2 term in the parent visible operator domain | absence of the operator gives f_perp_prime(0)=0 | if absent cannot be proven, retain C_F2_perp:=\|f_perp_prime(0)\| | ZERO_ROUTE_NOT_PARENT_SIGNED | operator-domain exhaustion/no-hidden-visible theorem missing | false |
| EF3232_2_strict_source_root | same-branch EM source-root | f_perp=lambda_F F_EM(X_perp), F_EM(0)=F_EM_prime(0)=0 | strict double-zero kills f_perp_prime(0) | off-root source <= (1/4)\|lambda_F F_EM_second\| \|X_perp\| \|\|F^2\|\|_2 + higher order | CONDITIONAL_THEOREM_NOT_EM_ATTACHED | 3231 transverse branch not proven to be the same EM source-root branch | false |
| EF3232_3_readout_reentry | observed alpha/readout | alpha_eff can reintroduce transverse dependence after bare F2 silence | effective/readout functor preserves no-extra-F2 or strict source-root rule | add J_readout_F2_bound to the transverse source norm | REQUIRED_GUARD_UNSIGNED | readout/radiative closure missing | false |
| EF3232_4_null_F2_support | null-wave scalar invariant | F^2=0 for ideal null radiation can make J_EM_F2 vanish in that support | scored region contains only such null F2 support and no readout/boundary reentry | retain \|\|F^2\|\|_2 for non-null/static/material/Coulomb fields | SUPPORT_SPECIFIC_NOT_GENERAL | does not address Poynting/stress/boundary flux | false |

## Poynting Flux Zero Or Bound Audit

| audit_id | channel | formula | zero_route | finite_route | status | claim_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PY3232_0_definition | Poynting/collar/worldtube flux | Phi_Poynting <= C_flux \|\|S_EM . n\|\|_B, equivalently a stress flux norm built from T_EM^{mu nu} n_mu | no EM flux through boundary/collar/worldtube, or flux form is exact/proper/orthogonal to v_perp | Phi_Poynting_bound := C_flux \|\|S_EM . n\|\|_B | EXACT_BOUND_TEMPLATE | C_flux, boundary norm, and flux support not source-backed | false |
| PY3232_1_F2_nonimplication | F2 versus stress | F^2=0 does not imply T_EM^{mu nu}=0 or S_EM=0 | must separately prove stress/flux silence | retain Poynting/stress norm even when scalar F2 channel is zero | SEPARATE_CHANNEL_GUARD | blocks replacing Poynting by F2 | false |
| PY3232_2_proper_boundary | proper/exact boundary flux | integral_B i_vperp dB_EM or exact/proper corner term vanishes on closed compatible boundary | flux contribution is exact/proper/orthogonal and no corner/worldtube leakage remains | corner/worldtube remainder norm B_corner_flux | CONDITIONAL_ZERO_ROUTE | boundary/collar class and corner exclusions not parent-signed | false |
| PY3232_3_no_flux_support | support silence | S_EM . n = 0 on the selected boundary/collar/worldtube | boundary chosen or derived so physical flux through it is zero | if flux is nonzero, bound by measured/sourced field flux support | SUPPORT_ROUTE_NOT_SOURCE_SIGNED | cannot choose boundary after the fact; must be parent/test-domain owned | false |

## Jperp Phi Bound Update

| update_id | target | formula | definitions | zero_condition | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| UP3232_0_Jperp_update | \|\|J_perp^tau\|\|_2 | \|\|J_perp^tau\|\|_2 <= J_other_bound + (1/4)C_F2_perp \|\|F^2\|\|_2 + J_Poynting_bound | C_F2_perp:=\|f_perp_prime(0)\|; J_other_bound collects geom/matter/trace/memory/projector channels | J_other_bound=0, C_F2_perp\|\|F^2\|\|_2=0, and J_Poynting_bound=0 | REFINED_BOUND_FOR_3231 | false |
| UP3232_1_Phi_update | \|Phi_perp^tau\| | \|Phi_perp^tau\| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux \|\|S_EM . n\|\|_B | Phi_other_bound collects non-EM boundary/corner/worldtube terms | all boundary terms exact/proper/orthogonal/absent and EM flux support zero | REFINED_BOUND_FOR_3231 | false |
| UP3232_2_Yperp_update | Y_perp | Y_perp <= (J_perp_bound/m_perp_min + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2 | J_perp_bound and Phi_perp_bound include the 3232 EM_F2/Poynting terms | Y_perp=0 if both refined source and boundary bounds are zero with coercivity/no kernel | FEEDS_3230_AND_3229 | false |

## Claim Gates

| gate_id | gate | required_evidence | current_status | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G3232_0_EMF2_zero | kill transverse EM_F2 channel | no-extra-F2 operator-domain theorem OR same-branch strict EM source-root OR support-specific F2=0 with readout closure | NOT_PARENT_SIGNED | use (1/4)C_F2_perp\|\|F^2\|\|_2 in J_perp_bound | false |
| G3232_1_Poynting_zero | kill Poynting/boundary channel | no flux through owned boundary/collar/worldtube OR exact/proper/orthogonal flux theorem | NOT_PARENT_SIGNED | use C_flux\|\|S_EM.n\|\|_B in Phi_perp_bound/J_Poynting_bound | false |
| G3232_2_no_trace_shortcut | prevent false closure | do not use Maxwell trace silence or F2=0 to erase Poynting/stress | ACTIVE_GUARD | separate scalar invariant and stress/flux norms | false |
| G3232_3_vperp_zero_feedback | v_perp=0 promotion | EM_F2 zero, Poynting zero, plus other J_perp/Phi channels zero and O_perp coercive/no-kernel | NOT_CLAIM_READY | finite Y_perp bound | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3232_0_result | EMF2_AND_POYNTING_ZERO_OR_BOUND_FORMULAS_DERIVED_NO_CHANNEL_CLOSED | the exact EM_F2 zero routes and Poynting zero routes are now explicit, but current sources do not parent-sign no-extra-F2/source-root/readout closure or Poynting boundary silence | NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_NO_MAXWELL_STRESS_CLAIM | try to close EM_F2 first via no-extra-F2/source-root/readout owner; keep Poynting as separate finite stress/flux channel unless boundary silence is signed | false |
| DEC3232_1_next_target | 3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090 | EM_F2 is the cleaner algebraic channel; if f_perp_prime(0) is killed, the remaining live channel is Poynting/boundary flux and other non-EM sources | PRIVATE_NEXT_TARGET | derive whether transverse f_perp_prime(0)=0 follows from Q_ONLY/no-hidden-visible operator domain, strict source-root, or readout closure | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_EMF2_ZERO_OR_BOUND_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_CLAIM_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3232_00_3231_doc | 3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md | true | 3231 handoff selecting EM_F2 and Poynting | L26:+ J_EM_F2 \| L49:+ Phi_Poynting + Phi_memory_projector. \| L62:J_EM_F2 = (1/4) f_perp_prime(0) F^2, \| L63:Phi_Poynting <= C_flux \|\|S_EM · n\|\|_boundary/collar/worldtube. | false |
| SRC3232_01_3231_source_audit | P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv | true | machine J_perp source audit | L5:JPA3231_3_EM_F2,EM kinetic F2 coupling,J_EM_F2 = (1/4) f_perp_prime(0) F_{mu nu}F^{mu nu},"no-extra-F2 theorem, f_perp_prime(0)=0, strict same-branch EM source-root, or F^2 support zero plus no readout reentry",\|\|J_EM_F2 \| L6:JPA3231_4_Poynting,Poynting/collar/worldtube flux,"J_Poynting or Phi_Poynting sourced by S_EM·n, T_EM^{0i}, or boundary/collar flux","flux channel is absent from parent coupling, or exact/proper/orthogonal boundary theor | false |
| SRC3232_02_3231_phi | P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv | true | machine Phi_perp/Poynting boundary audit | L2:PHI3231_0_total_boundary,Phi_perp^tau,\|Phi_perp^tau\| <= Phi_geom + Phi_matter + Phi_EM_F2_boundary + Phi_Poynting + Phi_memory_projector,each boundary/corner/worldtube term is exact/proper/orthogonal or absent,BOUND_DECO \| L3:PHI3231_1_Poynting_boundary,Phi_Poynting,Phi_Poynting <= C_flux \|\|S_EM·n\|\|_{boundary/collar/worldtube},"no EM flux through the relevant boundary, or flux term is exact/proper/orthogonal to v_perp",ACTIVE_BOUNDARY_GUARD,f | false |
| SRC3232_03_3220_doc | 3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md | true | EM F2 source-root and Poynting stress guard | L12:S_EM = -1/4 int [Z_0 + lambda_F F_EM(m)] F_Q^2 \| L13:F_EM(m_*) = 0 \| L14:F_EM'(m_*) = 0 \| L17:The answer from the current corpus is **no, not yet**. The algebra is solid: if the parent action owns that exact `F_EM` coefficient, then `partial_m Z_A\|m_* = 0` and the linear `b_alpha_m` source dies. But the available | false |
| SRC3232_04_3220_transfer | P8_Y5_R2FR_3220_GENERIC_DZ_TO_EM_F2_TRANSFER_AUDIT.csv | true | machine generic double-zero transfer warning | L2:TR3220_0_conditional_transfer_theorem,generic double-zero can transfer to any coefficient only after ownership,"If a coefficient C_i(m)=C_i0+lambda_i F_i(m) and F_i(m_*)=F_i'(m_*)=0, then partial_m C_i\|m_*=0.",EXACT_COND \| L5:TR3220_3_null_wave_not_F2_proof,F2 source-root is not full EM stress silence,"For radiation, F_Q^2 can vanish while the Maxwell stress tensor and Poynting vector do not; therefore F2-coupling silence must be paired with  | false |
| SRC3232_05_3220_finite | P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv | true | machine finite EM F2/Poynting requirements | L6:FIN3220_4_FQ2_norm,\|\|F_Q^2\|\|_op_or_support,worst-case local support/operator norm for the EM invariant entering the Hessian correction,field-strength squared norm,eta_EM >= (1/4)\|lambda_F F_EM''\| \|\|F_Q^2\|\|,MISSING_ARENA_ \| L9:FIN3220_7_Poynting_stress_bound,EM wave/current stress residual,bound or theorem for Maxwell stress/Poynting channel not controlled by F_Q^2 alone,stress-energy/current flux units,full Maxwell/EM stress descent rather th | false |
| SRC3232_06_3218_doc | 3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md | true | EM F2 vertex owner and readout countermodels | L10:S_EM = -1/4 int Z_A(m,q,readout) F_Q^2 \| L12:b_alpha_m := partial_m ln Z_A \| m_* \| L13:= (partial_m Z_A \| m_*) / Z_A(m_*). \| L19:Z_A = | false |
| SRC3232_07_3219_doc | 3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md | true | strict double-zero EM F2 theorem and Hessian guard | L1:# 3219 - EM F2 Strict Double-Zero Source Root Or b_alpha_m Finite Bound under AX1090 \| L26:So strict double-zero kills the linear source, but it can still shift the memory Hessian/range. The branch is only safe if: \| L29:G_eff >= G_mem - eta_EM > 0. \| L34:## EM F2 Strict Double-Zero Law | false |
| SRC3232_08_3210_source_split | P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv | true | source split with EM trace/F2/Poynting separation | L4:JXS3210_2_EM_F2,gauge kinetic scalar coupling,DeltaS_EM=-(1/4)int sqrt(-g) f_X(X) F_{mu nu}F^{mu nu}; J_X^EM=(1/4)sqrt(-g) f_X'(X) F^2.,no-extra-F2 theorem or f_X'(0)=0 from parent representation/gauge-norm signature,cou \| L5:JXS3210_3_Poynting_flux,EM wave/Poynting boundary flux,"For null radiation F^2=0 can hold while S=(E x B)/mu0 and T_EM^{0i} are nonzero; this is boundary/worldtube flux, not automatically bulk scalar trace source.","pare | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3232_00_inputs_exist | true | inputs=9 |
| VAL3232_01_emf2_bound_formula | true | EM_F2 zero routes and finite bound staged |
| VAL3232_02_poynting_guard | true | F2 nonimplication guard retained |
| VAL3232_03_yperp_feedback | true | bounds feed J/Phi/Y_perp chain |
| VAL3232_04_claims_blocked | true | claim_rows_true=0 |
| VAL3232_05_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3232_06_csv_parse | true | P8_Y5_R2FR_3232_INPUTS.csv;P8_Y5_R2FR_3232_EMF2_ZERO_OR_BOUND_AUDIT.csv;P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv;P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv;P8_Y5_R2FR_3232_CLAIM_GATES.csv;P8_Y5_R2FR_3232_DECISION.csv |
| VAL3232_07_next_target | true | 3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
