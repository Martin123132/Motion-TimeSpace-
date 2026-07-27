# 3255 - EM Gram row input pack or static Coulomb stress envelope under AX1090

Generated: `2026-06-27T05:14:23.754413+00:00`

Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material binding, or public source-coupling success.

## Summary
- `3255` fills the first symbolic diagonal Gram formula for the EM/Coulomb source component.
- Arena choice: a static observed Coulomb shell `A_ext(R_in,R_out)` with `R_in>0` and `R_out>R_in`.
- For `E(r)=Q_eff/(4*pi*epsilon0*r^2)` and `B=0`, the energy density is `u_EM=Q_eff^2/(32*pi^2*epsilon0*r^4)`.
- The shell energy is `U_EM=Q_eff^2/(8*pi*epsilon0)*(1/R_in-1/R_out)`.
- The diagonal Gram self-entry is now symbolic: `G_J[EM,EM]_shell=C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5)`.
- This is not a real material claim yet: `Q_eff`, cutoffs, unit lock, tau/e_obs, and screening/internal binding projection are still required.

## Arena Norm Unit Pack

| arena_id | choice | formal_definition | why_this_choice | required_inputs | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ARENA3255_0_static_coulomb_shell | A_ext shell around source worldtube | A_ext(R_in,R_out) := {x on a static observed slice : R_in <= r_eobs(x,W_source) <= R_out} | removes the Coulomb singularity with R_in>0 and keeps finite support with R_out<infty | W_source;observed static slice;r_eobs;R_in;R_out;orientation;regular shell | SYMBOLIC_ARENA_CONTRACT_READY | false |
| ARENA3255_1_current_norm | L2 energy-current norm | G_J[EM,EM] := integral_Aext u_EM(r)^2 dV_eobs for tau=unit static observer and J_EM=tau-energy-current | matches the 3253 Gram/eigenvalue requirement while giving an analytic Coulomb shell integral | tau unit normalization;dV_eobs;J norm convention;frame correction if not locally inertial | NORM_CONVENTION_SELECTED_FOR_ENVELOPE_NONCLAIM | false |
| ARENA3255_2_unit_system | SI shell formula with natural-unit translation deferred | E(r)=Q_eff/(4*pi*epsilon0*r^2), B=0, u_EM=epsilon0 E^2/2 | keeps dimensions visible and prevents hidden alpha/epsilon0 unit drift | epsilon0 or declared natural-unit replacement;kappa_EM;Q_eff units | SI_SYMBOLIC_FORMULA_SELECTED_NONCLAIM | false |
| ARENA3255_3_scope_guard | envelope not material model | Q_eff is an effective unscreened or component charge envelope; neutral materials require internal Coulomb/binding source maps, not a net-charge shortcut | keeps the formula useful without pretending bulk neutral matter has a simple external Coulomb field | screening/neutralization map or material EM binding fraction before any real body score | GUARDRAIL_ACTIVE | false |

## Static Coulomb Stress Envelope

| derivation_id | quantity | formula | derivation | required_inputs | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CSE3255_0_field_profile | static Coulomb E-field | E(r)=Q_eff/(4*pi*epsilon0*r^2), B(r)=0, R_in<=r<=R_out | spherical static Coulomb envelope on the observed shell; not a claim that real neutral material has this unscreened field | Q_eff;epsilon0;R_in;R_out;static observed frame | false |
| CSE3255_1_energy_density | u_EM(r) | u_EM(r)=epsilon0 E^2/2 = Q_eff^2/(32*pi^2*epsilon0*r^4) | standard Maxwell energy density for B=0 | same unit convention as CSE3255_0 | false |
| CSE3255_2_L1_energy_shell | \|\|J_EM\|\|_L1 shell envelope | U_EM_shell = integral u_EM dV = Q_eff^2/(8*pi*epsilon0)*(1/R_in - 1/R_out) | integrate u_EM(r)*4*pi*r^2 dr over [R_in,R_out] | Q_eff;epsilon0;R_in>0;R_out>R_in | false |
| CSE3255_3_L2_energy_current_shell | G_J[EM,EM] shell envelope | G_J[EM,EM]_shell = integral u_EM^2 dV = Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5) | integrate [Q_eff^2/(32*pi^2*epsilon0*r^4)]^2 * 4*pi*r^2 dr | same current norm;Q_eff;epsilon0;R_in>0;R_out>R_in | false |
| CSE3255_4_L2_norm | \|\|J_EM\|\|_L2 shell envelope | \|\|J_EM\|\|_L2 <= C_frame * \|Q_eff\|^2/(sqrt(1280)*pi^(3/2)*epsilon0)*sqrt(R_in^-5 - R_out^-5) | square root of CSE3255_3 with a frame/normalization safety factor C_frame | C_frame from tau/e_obs/current norm;do not set C_frame=1 unless local inertial/unit tau is sourced | false |
| CSE3255_5_poynting_zero_not_stress_zero | Poynting readout | S_EM=(1/mu0)E x B = 0 for B=0, but u_EM and G_J[EM,EM]_shell are nonzero for Q_eff != 0 | static electrostatic branch separates flux silence from stress-current silence | none beyond CSE3255_0; guardrail row | false |

## GJ EM EM Input Requirements

| input_id | input | definition | needed_for | current_value | source_requirement | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| IN3255_0_Q_eff | Q_eff | effective charge or EM binding/source envelope feeding the Coulomb shell | CSE3255_0 through CSE3255_4 | MISSING_Q_EFF_OR_MATERIAL_BINDING_MAP | source profile, material EM binding model, or explicit neutralization/screening map | false |
| IN3255_1_R_in | R_in | inner cutoff radius of static Coulomb shell | finite U_EM_shell and finite G_J[EM,EM] | MISSING_R_IN_POSITIVE | source worldtube radius, material cutoff, or q-basic collar inner radius | false |
| IN3255_2_R_out | R_out | outer cutoff radius of static Coulomb shell | finite arena support and score comparability | MISSING_R_OUT_GT_R_IN | arena/collar outer radius or decay/truncation rule | false |
| IN3255_3_epsilon0_or_unit_lock | epsilon0/kappa_EM/unit convention | unit and Maxwell normalization used by the observed EM stress | dimensionally meaningful CSE3255 formulas | MISSING_UNIT_LOCK | parent EM owner theorem or explicit SI/natural-unit scoring convention | false |
| IN3255_4_tau_eobs | tau and e_obs frame | unit static observer and observed coframe defining J_EM and dV | C_frame and current norm | MISSING_TAU_EOBS_ARENA_LOCK | same-frame package from 3250 signed or specified as finite arena convention | false |
| IN3255_5_screening_neutrality | screening/neutralization/material map | map from real material EM binding to the idealized Q_eff shell envelope | applying the envelope to WEP/local matter rather than a toy charged shell | MISSING_SCREENING_OR_BINDING_SOURCE | material composition/binding model or no-claim toy-envelope label | false |

## GJ EM EM Symbolic Update

| update_id | target | previous_value | new_symbolic_value | new_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| GJU3255_0_symbolic_self_entry | G_J[EM,EM] | MISSING_GJ_EM_EM_NUMERIC_VALUE | G_J[EM,EM]_shell = C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5) | SYMBOLIC_STATIC_COULOMB_ENVELOPE_READY_NONCLAIM | not numeric; not valid for real neutral material without input pack | false |
| GJU3255_1_CTw_diagonal_feed | C_Tw diagonal upper bound | C_Tw_upper^2 receives + \|\|J_EM\|\|_J^2 | C_Tw_upper^2 receives + C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5) | FIRST_COMPONENT_DIAGONAL_FORMULA_FILLED | still requires all other component rows or exact Gram eigenvalue matrix for C_Tw | false |
| GJU3255_2_cross_entries_still_open | G_J[EM,d] | MISSING_GJ_EM_D_CROSS_VALUES | unchanged; need component stress overlap or orthogonality theorem | CROSS_TERMS_REMAIN_REQUIRED | prevents pretending diagonal shell alone is full C_Tw | false |

## Poynting Zero Stress Nonzero Guard

| guard_id | statement | allowed_inference | forbidden_inference | valid_for_claim |
| --- | --- | --- | --- | --- |
| PZG3255_0_static_flux_zero | For the static Coulomb envelope B=0, S_EM=(1/mu0)E x B=0 and normal Poynting flux vanishes. | boundary Poynting flux component can be zero in this idealized static branch | do not infer T_EM=0, u_EM=0, J_EM=0, or G_J[EM,EM]=0 | false |
| PZG3255_1_static_stress_nonzero | For Q_eff != 0 and finite R_in<R_out, u_EM(r)=Q_eff^2/(32*pi^2*epsilon0*r^4)>0 and G_J[EM,EM]_shell>0. | static Coulomb stress can contribute to source/current Gram rows | do not erase EM/Coulomb source coupling by citing quiet/static Poynting alone | false |
| PZG3255_2_neutral_material_warning | For neutral matter, Q_eff may be zero externally while internal Coulomb/binding stress remains material-model dependent. | external shell formula is an envelope/toy source until mapped to material binding | do not use Q_eff=0 external neutrality as proof that EM binding stress vanishes | false |

## Claim Gates

| claim_gate_id | claim | gate_pass | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3255_0_static_envelope_derived | static Coulomb shell envelope formulas are derived | true | CSE3255 rows integrate standard Maxwell energy density over R_in<=r<=R_out | false |
| CG3255_1_GJ_symbolic | G_J[EM,EM] has a symbolic shell formula | true | GJU3255_0 supplies the symbolic diagonal self-entry | false |
| CG3255_2_GJ_numeric | G_J[EM,EM] is numeric/source-backed | false | Q_eff, R_in, R_out, unit lock, tau/e_obs, and screening/material map are missing | false |
| CG3255_3_real_material | static shell formula is a real material EM binding model | false | neutrality/screening/internal binding map has not been supplied | false |
| CG3255_4_local_GR_Newton_Maxwell | local GR/Newton/Maxwell source branch is derived or bounded enough to claim | false | only one symbolic diagonal component is filled; numeric matrix/cross terms/source coupling theorem remain open | false |

## Decisions

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3255_0_progress | Promote G_J[EM,EM] from missing to symbolic Coulomb-shell envelope | this is an actual calculable formula with cutoff dependence, not another target ledger | supply Q_eff/R_in/R_out/unit/tau/e_obs or derive the material binding map | false |
| DEC3255_1_no_overclaim | Keep the shell formula nonclaim | real neutral matter needs screening/internal Coulomb binding, and C_Tw still needs cross terms or an orthogonality theorem | build a material EM binding projection or choose a toy charged-shell smoke input explicitly | false |
| DEC3255_2_best_next | Attack material binding projection before trying numeric C_Tw | without mapping EM binding in neutral matter, Q_eff is just a toy shell parameter | derive/source f_EM,A and convert Coulomb shell envelope into component stress-current rows for real material classes | false |

## Next Target

| next_id | selection | next_checkpoint | next_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3255_0_3256 | selected_primary | 3256-Y5-R2FR-material-EM-binding-projection-or-toy-charged-shell-smoke-input-under-AX1090.md | scripts/Y5_R2FR_3256_material_EM_binding_projection_or_toy_charged_shell_smoke_input.py | Either derive/source the material EM binding projection f_EM,A for neutral matter, or create an explicitly labelled toy charged-shell input row for the symbolic G_J[EM,EM] envelope. | Do not treat external neutrality or zero Poynting flux as zero EM stress; do not claim local GR/Newton/Maxwell pass. | false |

## Source Register

| source_id | source_path | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3255_3254_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3254-Y5-R2FR-first-component-current-Gram-row-or-parent-signature-clause-lock-under-AX1090.md | true | true | 3254 selects static Coulomb/EM envelope as next target | L8:- `3254` takes the `3253` Gram/eigenvalue fallback and fills the first real component slot: EM/Coulomb binding. \| L10:- The first Gram entries are explicit: `G_J[EM,EM]=<J_EM,J_EM>_J` and `G_J[EM,d]=<J_EM,J_d>_J`. \| L13:- Guardrail: Poynting flux silence or `F^2=0` cannot be used to erase EM/Coulomb stress; static Coulomb energy can remain as source stress. \| L19:\| EMD3254_0_component_selection \| DCW1231_4_EM_Coulomb_binding \| Select the EM/Coulomb binding residual component delta_w_EM as the first finite C_Tw component-current target. \| links source coupling, Maxwell stress, Poynting flux, alpha/EM | false |
| SRC3255_3254_gram | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3254_EM_COMPONENT_CURRENT_GRAM_ROW.csv | true | true | EM Gram self/cross row contract | L2:GJ3254_EM_EM_SELF,DCW1231_4_EM_Coulomb_binding,EM/Coulomb binding contribution,delta_w_EM,"J_EM[tau] := star_eobs(T_EM_obs(tau,.))","G_J[EM,EM] = <J_EM,J_EM>_J","integral_Aext w_J g_J^{-1}(j_EM,j_EM) dmu_eobs",unit_system;kappa_EM;A_ext;w_J | false |
| SRC3255_3254_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3254_EM_CURRENT_NORM_BOUND_ROWS.csv | true | true | EM norm bounds and static Coulomb guard | L2:EMB3254_0_L1_energy_current_bound,\|\|J_EM[tau]\|\|_L1(A_ext),\|\|J_EM\|\|_L1 <= C_star C_tau kappa_EM^-1 (\|\|E\|\|_L2(A_ext)^2 + \|\|B\|\|_L2(A_ext)^2),Maxwell stress is quadratic in F; contract with bounded tau and integrate the energy-density envelope, \| L5:EMB3254_3_static_coulomb_warning,EM/Coulomb binding current,"quiet electrostatic fields can have S_EM dot n=0 while T_EM(tau,.) and Coulomb binding energy are nonzero",Poynting flux silence is not the same as EM stress-current silence,"do n | false |
| SRC3255_3116_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md | true | true | public Hodge/Maxwell stress route | L122:## Hilbert Stress Derivation \| L150:## Poynting Vector Readout | false |
| SRC3255_3116_lock_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3116_PUBLIC_HODGE_MAXWELL_STRESS_LOCK.csv | true | true | Maxwell action to Hilbert stress and Poynting readout rows | L3:"EMH3116_1","Maxwell_action_to_Hilbert_stress","derived_conditional_nonclaim","false","S_EM=-1/4 int sqrt(-g_pub) Z_EM F^2 gives T_EM=Z_EM(F^mu_a F^nu_a - 1/4 g^munu F^2) when Z_EM and Hodge are public-owned.","local_GR;source_coupling;orbi \| L4:"EMH3116_2","Poynting_readout","derived_conditional_nonclaim","false","S_pub^mu=-h^mu_a T_EM^{ab}u_b; Poynting is the spatial energy flux component of public EM Hilbert stress, not a second gravitational source.","EM;source_coupling;radiati | false |
| SRC3255_3142_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3142-Y5-R2FR-em-poynting-qbasic-sector-under-AX1090.md | true | true | q-basic Maxwell/Poynting conditional sector | L6:EM/Poynting q-basic sector theorem: \| L17:=> Hilbert EM stress tensor | false |
| SRC3255_3200_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090.md | true | true | quiet static Poynting zero versus stress nonzero distinction | L19:- `PZT3200_01`: `electrostatic_bound_field` - Poynting flux can vanish while T_EM^{ij} and energy density remain nonzero Caveat: composition/EM self-energy still belongs in WEP/PPN source-coupling bounds \| L30:This does **not** zero full EM stress-energy. Electrostatic self-energy and Maxwell spatial stress remain separate source-coupling/WEP concerns. | false |
| SRC3255_3234_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md | true | true | Poynting functional and no-F2 shortcut guard | L12:Phi_Poynting[v_perp] \| L20:\|Phi_Poynting[v_perp]\| \| L43:F^2=0 does not imply S_EM dot n=0 or T_EM(u,n)=0. \| L54:\| PF3234_0_functional \| Poynting boundary/collar/worldtube flux functional \| Phi_Poynting[v_perp] := int_B w_perp T_EM(u,n) dSigma ~= int_B w_perp (S_EM dot n) dSigma \| transverse variation tests the EM stress/energy flux through the owned  | false |
| SRC3255_3246_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md | true | true | Poynting regime classifier | L43:\| REG3246_1_electrostatic \| electrostatic_bound_field \| S_EM dot n=0 can hold while EM stress/energy remains nonzero \| Poynting component may be zero; EM source-coupling still lives elsewhere \| do not confuse Poynting silence with Maxwell/E \| L94:\| SRC3246_3234_functional \| D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL | false |
| SRC3255_3250_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3250_EM_STRESS_PROJECTION_AND_FLUX_NORM_IDENTITY.csv | true | true | Maxwell stress projection and flux norm identities | L2:EMF3250_0_projection,Maxwell stress flux through source-worldtube collar,"T_EM(u,n)=S_EM dot n in an observed orthonormal frame with u timelike unit, n spatial unit, and g_obs(u,n)=0",use this as the frame-owned meaning of the Poynting term \| L3:EMF3250_1_boundary_L1_bound,normal Poynting flux norm,"S_EM dot n=(1/mu0)(E x B) dot n in SI units, or S_EM dot n=(E x B) dot n in natural units",\|\|S_EM dot n\|\|_L1(B) <= mu0^-1 \|\|E_T\|\|_L2(B)\|\|B_T\|\|_L2(B),"unit convention, E/B field norms on | false |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3255_0_sources_exist_parse_hit | true | every cited source exists, parses, and has evidence hits | True |
| VAL3255_1_output_csvs_parse | true | all 3255 output CSVs parse before validation write | True |
| VAL3255_2_arena_shell | true | static Coulomb shell arena is declared | True |
| VAL3255_3_coulomb_integrals | true | L1 and L2 Coulomb shell integrals are present | L1=True L2=True |
| VAL3255_4_symbolic_gj_update | true | G_J[EM,EM] symbolic update exists | True |
| VAL3255_5_input_pack_missing | true | input pack includes Q_eff/R_in/R_out and keeps missing markers | missing=True cutoffs=True |
| VAL3255_6_poynting_guard | true | Poynting zero does not erase EM stress guard is present | zero_guard=True positive=True |
| VAL3255_7_nonclaim_claims_blocked | true | all rows nonclaim and local-GR/Newton/Maxwell gate blocked | nonclaim=True claims=True |
| VAL3255_8_output_scope | true | all generated files stay in post-checkpoint-work | True |
| VAL3255_9_formalization_untouched | true | no 3255 files are written under formalization-workbench | file_count=0 |
| VAL3255_10_next_target | true | 3256 next target is selected | True |
| VAL3255_OVERALL | true | 3255 validation overall | all required validation rows passed |

## Working Verdict
`3255` is a genuine calculation step. `G_J[EM,EM]` is no longer just a missing entry: it has a symbolic Coulomb-shell envelope with explicit cutoff dependence. The next risk is physical interpretation, not algebra: a real neutral material needs an EM binding/screening projection before this can be used as evidence.
