# 3234 - Poynting Boundary Flux Silence Or Finite Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, PPN pass, EM-lock claim, Maxwell-stress claim, or public-facing result.

## Result

3234 turns the Poynting objection into a concrete local residual component instead of letting it float as a vague danger channel.

The flux functional is:

```text
Phi_Poynting[v_perp]
:= int_B w_perp T_EM(u,n) dSigma
 ~= int_B w_perp (S_EM dot n) dSigma.
```

By the dual norm bound:

```text
|Phi_Poynting[v_perp]|
<= ||w_perp||_{B*} ||S_EM dot n||_B + B_corner_flux
:= C_flux ||S_EM dot n||_B + B_corner_flux.
```

If the same channel is represented as collar/worldtube bulk leakage:

```text
J_Poynting_bound <= C_coll ||T_EM(u,n)||_collar.
```

Exact zero is allowed only by one of four owned routes:

```text
S_EM dot n = 0 on the owned support,
or the flux form is exact/proper with no corner leakage,
or the transverse test direction is orthogonal to the flux functional,
or Maxwell stress/current/Hodge descent proves no transverse source.
```

The important guard is retained:

```text
F^2=0 does not imply S_EM dot n=0 or T_EM(u,n)=0.
```

So null-wave scalar-invariant silence cannot be used to erase Poynting/boundary stress.

Current verdict: `POYNTING_FLUX_FUNCTIONAL_AND_FINITE_BOUND_DERIVED_NO_ZERO_CLAIM`.

## Poynting Flux Functional

| functional_id | object | formula | meaning | zero_condition | finite_bound | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PF3234_0_functional | Poynting boundary/collar/worldtube flux functional | Phi_Poynting[v_perp] := int_B w_perp T_EM(u,n) dSigma ~= int_B w_perp (S_EM dot n) dSigma | transverse variation tests the EM stress/energy flux through the owned boundary, collar, or worldtube | T_EM(u,n)=0 or S_EM dot n=0 on the selected owned support, or w_perp is orthogonal to the flux source | \|Phi_Poynting[v_perp]\| <= \|\|w_perp\|\|_{B*} \|\|S_EM dot n\|\|_B + B_corner_flux | FUNCTIONAL_DERIVED_AS_DUAL_PAIRING | false |
| PF3234_1_stress_form | stress tensor equivalent | S_EM dot n = T_EM(u,n) after choosing observed frame u and boundary normal n | keeps the channel covariant; Poynting is the frame expression of the Maxwell stress flux | observed frame/boundary normal and stress tensor descent make T_EM(u,n) vanish | C_flux := \|\|w_perp\|\|_{B*}; flux_norm := \|\|T_EM(u,n)\|\|_B | COVARIANT_REWRITE_READY | false |
| PF3234_2_collar_bulk | collar leakage source | J_Poynting_bound <= C_coll \|\|T_EM(u,n)\|\|_collar | if flux is represented as a collar/worldtube source rather than a pure boundary term, it still enters only through a finite stress norm | collar support is flux-free or the flux form is exact/proper with no corner remainder | C_coll \|\|T_EM(u,n)\|\|_collar | FINITE_COLLAR_BOUND_TEMPLATE | false |
| PF3234_3_F2_guard | F2 shortcut guard | F_mu_nu F^mu_nu=0 does not imply T_EM(u,n)=0 or S_EM dot n=0 | null radiation can have vanishing scalar invariant and nonzero energy flux | none; must separately prove stress/flux silence | retain C_flux \|\|S_EM dot n\|\|_B even if \|\|F^2\|\|_2=0 | NO_F2_SHORTCUT_ACTIVE | false |

## Boundary Silence Audit

| route_id | route | theorem | required_parent_signature | current_status | residual_if_unsigned | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PZ3234_0_no_flux_support | support silence | If S_EM dot n=0 on the parent-owned boundary/collar/worldtube, then Phi_Poynting=0 on that support. | owned boundary B/collar/worldtube; observed u,n; support proof; no hidden corner leakage | NOT_PARENT_SIGNED | C_flux \|\|S_EM dot n\|\|_B | false |
| PZ3234_1_exact_proper_flux | exact/proper boundary | If the transverse flux contribution is an exact/proper boundary form on a closed compatible boundary, its integral vanishes up to corners. | flux potential; compatible closed boundary; orientation; corner/worldtube exclusion | CORNER_AND_BOUNDARY_CLASS_UNSIGNED | B_corner_flux + B_worldtube_leak | false |
| PZ3234_2_orthogonality | transverse test-function orthogonality | If w_perp lies in the annihilator of the EM flux functional, then Phi_Poynting[v_perp]=0. | definition of allowed v_perp space; boundary dual norm; projector theorem P_perp^* flux=0 | PROJECTOR_ORTHOGONALITY_UNSIGNED | \|\|P_perp^* T_EM(u,n)\|\|_B | false |
| PZ3234_3_parent_stress_descent | EM stress descends only to Maxwell/metric sector | If the parent action proves Maxwell stress/Hodge/current descent is quotient-invariant and has no transverse scalar representative coefficient, Poynting cannot source v_perp. | quotient-invariant Hodge star; Maxwell current/stress descent; no representative Weyl/disformal coefficient | DESCENT_NOT_FULLY_SIGNED | C_stress_leak \|\|T_EM\|\|_B | false |
| PZ3234_4_total | total Poynting zero | Poynting channel closes only if no-flux support, exact/proper cancellation, orthogonality, or parent stress descent closes on the same branch. | one complete route plus owned common norm and boundary class | FAIL_CURRENT_CLAIM | Phi_Poynting_bound and J_Poynting_bound remain in the local residual vector | false |
| PZ3234_5_no_F2_shortcut | reject scalar-invariant shortcut | F^2=0 may erase the EM_F2 scalar source on null support but does not erase Poynting, T_EM, or boundary flux. | separate stress/flux proof | ACTIVE_GUARD | C_flux \|\|S_EM dot n\|\|_B remains even with \|\|F^2\|\|_2=0 | false |

## Finite Flux Bound

| bound_id | quantity | formula | required_inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PB3234_0_boundary_flux | Phi_Poynting_bound | Phi_Poynting_bound := C_flux \|\|S_EM dot n\|\|_B + B_corner_flux | C_flux; boundary/collar/worldtube B; observed u,n; flux norm; corner/worldtube remainder; units | FINITE_BOUND_FORMULA_READY_INPUTS_MISSING | false |
| PB3234_1_collar_source | J_Poynting_bound | J_Poynting_bound := C_coll \|\|T_EM(u,n)\|\|_collar | C_coll; collar support; stress-flux norm; projector norm; units | FINITE_BOUND_FORMULA_READY_INPUTS_MISSING | false |
| PB3234_2_total_phi | Phi_perp_bound update | \|Phi_perp^tau\| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux \|\|S_EM dot n\|\|_B + B_corner_flux | Phi_other_bound; Phi_EM_F2_boundary; C_flux; flux norm; corner flux | FEEDS_LOCAL_RESIDUAL_VECTOR | false |
| PB3234_3_total_jperp | J_perp_bound update | \|\|J_perp^tau\|\|_2 <= J_other_bound + (1/4) C_F2_perp \|\|F^2\|\|_2 + C_coll \|\|T_EM(u,n)\|\|_collar | J_other_bound; C_F2_perp; F2 norm; C_coll; collar stress flux norm | FEEDS_TRANSVERSE_AMPLITUDE_LAW | false |

## Jperp/Phi Update

| update_id | target | formula | claim_effect | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| UP3234_0_residual_vector | local residual vector | R_local includes R_EM_F2 + R_Poynting + R_other; R_Poynting is bounded by PB3234_0/PB3234_1 | keeps EM flux as a finite residual rather than erasing it by trace/F2 silence | RESIDUAL_COMPONENT_EXPLICIT | false |
| UP3234_1_Yperp_feedback | transverse amplitude law | Y_perp <= (a_perp + sqrt(a_perp^2+4 b_perp))/2 with a_perp=J_perp_bound/m_perp_min and b_perp=Phi_perp_bound | local PPN branch cannot claim v_perp=0 unless both EM_F2 and Poynting terms vanish or are bounded below tolerance | FEEDS_3230_CHAIN | false |
| UP3234_2_flux_gate | future source rows | required row: {B_id,u,n,C_flux,\|\|S_EM dot n\|\|_B,B_corner_flux,units,source_path,valid_for_claim} | turns Poynting into a sourceable coefficient instead of a vague objection | SOURCE_ROW_CONTRACT_READY | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3234_0_result | POYNTING_FLUX_FUNCTIONAL_AND_FINITE_BOUND_DERIVED_NO_ZERO_CLAIM | Poynting is now a dual boundary/collar flux functional with exact zero routes and finite bounds, but no route is parent-signed on an owned boundary class | NO_LOCAL_GR_NO_MAXWELL_STRESS_NO_CLOCK_NO_PPN_NO_R10_CLAIM | keep Phi_Poynting/J_Poynting in the local residual vector unless a source-backed flux row or parent stress-descent theorem is supplied | false |
| DEC3234_1_next_target | 3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090 | after EM_F2 and Poynting are explicit, the remaining live J_perp channels are ordinary matter/marker/readout, memory/projector, and geometry; matter-source functor is the next lowest-scrutiny gate | PRIVATE_NEXT_TARGET | derive whether ordinary matter/source markers descend only through the observed coframe/metric sector or produce a finite transverse source coefficient | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_BOUNDARY_SILENCE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_JPERP_PHI_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3234_00_3233_doc | 3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090.md | true | 3233 handoff selecting Poynting flux channel | L77:\| ZCF3233_4_total_zero \| C_F2_perp=0 promotion \| C_F2_perp=0 only if Q_ONLY/fixed norm, no-extra-F2 or strict source-root, and readout closure all close on the same transverse branch. \| ZCF3233_0 or ZCF3233_2, plus ZCF32 \| L100:\| DEC3233_0_result \| CF2PERP_OWNER_GATE_DERIVED_COUNTERMODELS_RETAINED_NO_ZERO_CLAIM \| C_F2_perp decomposes into fixed-norm, independent visible, hidden/source-root, and readout terms; exact zero has clear sufficient cla \| L101:\| DEC3233_1_next_target \| 3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090 \| EM_F2 zero is now reduced to a parent owner gate; Poynting remains an independent stress/flux channel that F2 algebra c \| L117:\| SRC3233_00_3232_doc \| 3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090.md \| true \| 3232 handoff selecting C_F2_perp owner \| L12:J_EM_F2 = (1/4) f_perp_prime(0) F_mu_nu F^mu_nu. \\\| L18:\\\|\\\|J_E | false |
| SRC3234_01_3232_doc | 3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090.md | true | 3232 exact Poynting/stress nonimplication guard | L27:from no-extra-F2/operator-domain exclusion, same-branch strict EM source-root, or a support-specific `F^2=0` result with no readout reentry. \| L32:Phi_Poynting <= C_flux \|\|S_EM . n\|\|_B. \| L38:F^2=0 does not imply S_EM=0 or T_EM^mu_nu=0. \| L48:<= Phi_other_bound + Phi_EM_F2_boundary + C_flux \|\|S_EM . n\|\|_B. | false |
| SRC3234_02_3232_poynting | P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv | true | machine Poynting zero-or-bound audit | L2:PY3232_0_definition,Poynting/collar/worldtube flux,"Phi_Poynting <= C_flux \|\|S_EM . n\|\|_B, equivalently a stress flux norm built from T_EM^{mu nu} n_mu","no EM flux through boundary/collar/worldtube, or flux form is exac \| L3:PY3232_1_F2_nonimplication,F2 versus stress,F^2=0 does not imply T_EM^{mu nu}=0 or S_EM=0,must separately prove stress/flux silence,retain Poynting/stress norm even when scalar F2 channel is zero,SEPARATE_CHANNEL_GUARD,b \| L4:PY3232_2_proper_boundary,proper/exact boundary flux,integral_B i_vperp dB_EM or exact/proper corner term vanishes on closed compatible boundary,flux contribution is exact/proper/orthogonal and no corner/worldtube leakage | false |
| SRC3234_03_3232_update | P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv | true | machine J_perp/Phi update carrying Poynting term | L2:UP3232_0_Jperp_update,\|\|J_perp^tau\|\|_2,\|\|J_perp^tau\|\|_2 <= J_other_bound + (1/4)C_F2_perp \|\|F^2\|\|_2 + J_Poynting_bound,C_F2_perp:=\|f_perp_prime(0)\|; J_other_bound collects geom/matter/trace/memory/projector channels,"J_o \| L3:UP3232_1_Phi_update,\|Phi_perp^tau\|,\|Phi_perp^tau\| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux \|\|S_EM . n\|\|_B,Phi_other_bound collects non-EM boundary/corner/worldtube terms,all boundary terms exact/proper/orthogonal \| L4:UP3232_2_Yperp_update,Y_perp,Y_perp <= (J_perp_bound/m_perp_min + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2,J_perp_bound and Phi_perp_bound include the 3232 EM_F2/Poynting terms,Y_perp=0 if both refined sou | false |
| SRC3234_04_3231_source | P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv | true | machine transverse source split with Poynting | L6:JPA3231_4_Poynting,Poynting/collar/worldtube flux,"J_Poynting or Phi_Poynting sourced by S_EM·n, T_EM^{0i}, or boundary/collar flux","flux channel is absent from parent coupling, or exact/proper/orthogonal boundary theor | false |
| SRC3234_05_3231_phi | P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv | true | machine Phi_perp boundary audit | L2:PHI3231_0_total_boundary,Phi_perp^tau,\|Phi_perp^tau\| <= Phi_geom + Phi_matter + Phi_EM_F2_boundary + Phi_Poynting + Phi_memory_projector,each boundary/corner/worldtube term is exact/proper/orthogonal or absent,BOUND_DECO \| L3:PHI3231_1_Poynting_boundary,Phi_Poynting,Phi_Poynting <= C_flux \|\|S_EM·n\|\|_{boundary/collar/worldtube},"no EM flux through the relevant boundary, or flux term is exact/proper/orthogonal to v_perp",ACTIVE_BOUNDARY_GUARD,f | false |
| SRC3234_06_3220_finite | P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv | true | finite EM stress/Poynting requirement | L9:FIN3220_7_Poynting_stress_bound,EM wave/current stress residual,bound or theorem for Maxwell stress/Poynting channel not controlled by F_Q^2 alone,stress-energy/current flux units,full Maxwell/EM stress descent rather th | false |
| SRC3234_07_3210_split | P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv | true | source-channel split separating F2 and Poynting | L3:JXS3210_1_EM_trace,Maxwell trace coupling,"If J_X^EM is proportional only to T_EM, then T^mu_mu[Maxwell]=0 in four dimensions, so pure Maxwell radiation is trace-silent.","parent action couples X only to trace and not to \| L5:JXS3210_3_Poynting_flux,EM wave/Poynting boundary flux,"For null radiation F^2=0 can hold while S=(E x B)/mu0 and T_EM^{0i} are nonzero; this is boundary/worldtube flux, not automatically bulk scalar trace source.","pare | false |
| SRC3234_08_2600_boundary | 2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md | true | boundary/action ownership precedent for flux accounting | L3:**Status:** private nonclaim derivation checkpoint. The exact source-current response to a moving observed time generator is retained, but the coefficient owner and boundary-clock action clause are not yet parent-signed. \| L5:**Main result:** 2600 gives one real step forward and one hard stop. The real step is the exact law `Delta_JH_delta_tau <= C_Tobs_tau \|\|delta tau_obs\|\|_B`, inherited from the 1729 linear map `L_Tobs^A[delta tau]=star_A(T \| L10:\| SRC2600_00_2599_handoff_doc \| D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\2599-Y5-R2FR-boundary-clock-normalized-tau-o \| L29:\| TON2600_2_common_codomain \| codomain current norm \| \|\|star_A(T_obs(delta tau,.))\|\|_{J_A} \| NOT_PARENT_OWNED \| MISSING_A_EXT;MISSING_VOLUME_FORM;MISSING_HODGE_FACTOR;MISSING_CURRENT_NORM;MISSING_UNITS \| false \| false \|  | false |
| SRC3234_09_3136_clock_owner | 3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md | true | observed coframe/descent precedent for owned boundary time | L10:ordinary clock matter descends to the observed coframe \| L41:\| `e_obs=Obs_e(q(Phi))`, `Dq(v)=0` \| representative/internal variations do not change the observed coframe \| \| L42:\| `S_matter=S_matter[e_obs,psi_A,theta_A]` \| clock matter sees the observed coframe \| \| L59:same tau for clock/source/charge/orbit/boundary. | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3234_00_inputs_exist | true | inputs=10 |
| VAL3234_01_functional | true | Poynting dual flux functional present |
| VAL3234_02_f2_guard | true | F2 shortcut explicitly blocked |
| VAL3234_03_total_zero_route | true | total zero route specified but not activated |
| VAL3234_04_finite_bound | true | Phi/J finite flux bounds present |
| VAL3234_05_residual_update | true | local residual vector update present |
| VAL3234_06_claims_blocked | true | claim_rows_true=0 |
| VAL3234_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3234_08_csv_parse | true | P8_Y5_R2FR_3234_INPUTS.csv;P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv;P8_Y5_R2FR_3234_BOUNDARY_SILENCE_AUDIT.csv;P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv;P8_Y5_R2FR_3234_JPERP_PHI_UPDATE.csv;P8_Y5_R2FR_3234_DECISION.csv |
| VAL3234_09_next_target | true | 3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
