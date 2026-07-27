# 3340 - Parent Hilbert source clause or finite residual vector under AX1090

Run UTC: `2026-06-28T02:10:28.516855+00:00`

## Verdict

3340 takes the coupling fork one step further.

The exact parent clause we need is now written as:

`S_parent = S_geom[Phi] + S_matter[g_obs(q(Phi)), Psi_A, theta_A] + S_EM[g_obs(q(Phi)), A_Q, lambda_0] + S_boundary`

with all ordinary source tensors defined by Hilbert/Noether variation before calibration.

If that clause is parent-signed, then:

`J^{mu nu} = kappa_* T_total^{mu nu} + DeltaJ_silent^{mu nu}`

and source-only species weights, hidden EM/Hodge/current maps, tensor-ratio drift, and post-readout source selectors are forbidden.

The current corpus does **not** sign that parent clause yet. The best evidence rows are exact conditional theorems and contracts, not parent-owned derivations.

So the honest branch is:

`R_source_local <= A_k|delta_kappa_common| + A_WEP eta_species + A_T xi_tensor + A_C chi_spin_clock + A_EM epsilon_EM + epsilon_contact + epsilon_boundary + epsilon_bianchi`

with private steering allocation `B_source = 6.900e-06` until arena-specific thresholds are filled.

No local-GR/PPN/Maxwell claim is made.

## Source Register

- `SRC3340_0_3339_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md` exists=true parse_ok=true role=3339 coupling decomposition handoff
- `SRC3340_1_3339_requirements`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3339_PARENT_SIGNATURE_REQUIREMENTS.csv` exists=true parse_ok=true role=parent signature requirements
- `SRC3340_2_3339_residuals`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3339_RESIDUAL_CHANNEL_VECTOR.csv` exists=true parse_ok=true role=residual channel vector
- `SRC3340_3_3293_signature`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv` exists=true parse_ok=true role=Hilbert-source signature theorem attempt
- `SRC3340_4_3292_spurion`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv` exists=true parse_ok=true role=source-only spurion split
- `SRC3340_5_3303_evidence`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_HILBERT_SOURCE_EVIDENCE_SCORE.csv` exists=true parse_ok=true role=Hilbert source evidence score
- `SRC3340_6_same_coframe`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv` exists=true parse_ok=true role=same observed coframe clause
- `SRC3340_7_coframe_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv` exists=true parse_ok=true role=coframe coupling parent contract
- `SRC3340_8_1937_hilbert`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv` exists=true parse_ok=true role=older Hilbert source theorem target
- `SRC3340_9_3127_em_measure`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv` exists=true parse_ok=true role=EM Hilbert stress and Poynting guard
- `SRC3340_10_2577_worldtube`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv` exists=true parse_ok=true role=worldtube Hilbert selector coupling theorem

## Parent Hilbert Source Clause

- `HSC3340_0_parent_action_form`: required_clause=ordinary matter and EM enter the local branch only through one descended observed geometry; mathematical_form=S_parent = S_geom[Phi] + S_matter[g_obs(q(Phi)), Psi_A, theta_A] + S_EM[g_obs(q(Phi)), A_Q, lambda_0] + S_boundary; derives=all ordinary local source tensors are variational derivatives of the same descended action; forbids=post-variation source selectors, hidden source metric, species gravitational charge, and separate EM stress owner; current_status=CANDIDATE_PARENT_CLAUSE_NOT_SIGNED; valid_for_claim=false
- `HSC3340_1_variation_target`: required_clause=source current is defined before calibration by Hilbert variation against g_obs/e_obs; mathematical_form=T_total^{mu nu}:=(-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_{mu nu}; J_Q^mu:=(1/sqrt(-g_obs)) delta S_matter/delta A_Q_mu; derives=J^{mu nu}=kappa_* T_total^{mu nu} before readout; forbids=T_source=sum_A kappa_A T_A introduced after variation; current_status=EXACT_CONDITIONAL_FROM_3293_AND_1937_NOT_PARENT_SIGNED; valid_for_claim=false
- `HSC3340_2_common_kappa`: required_clause=one universal common kappa_* multiplies total Hilbert stress in the local field equation; mathematical_form=E_obs^{mu nu}=kappa_* T_total^{mu nu}+E_boundary^{mu nu}+E_contact^{mu nu}; derives=measured G_N calibrates kappa_* without creating WEP/PPN residuals; forbids=species, tensor, clock, or EM-relative kappa_A channels; current_status=CALIBRATION_ALLOWED_BUT_PARENT_NORMALIZATION_NOT_DERIVED; valid_for_claim=false
- `HSC3340_3_no_spurion_weights`: required_clause=theta_A may contain physical masses/charges/representation constants but no hidden source-only w_A; mathematical_form=partial_hidden theta_A=0 for source-only labels; any allowed theta_A appears in matter dynamics, stress, current, and readout together; derives=species/source residual eta_A vanishes by object-language exclusion; forbids=w_A(I_hidden) or kappa_A(I_hidden) that affects gravity but not matter/readout; current_status=CONDITIONAL_EXCLUSION_FROM_3292_3293_NOT_PARENT_SIGNED; valid_for_claim=false
- `HSC3340_4_public_Maxwell_Hodge`: required_clause=Maxwell/Hodge sector uses the same g_obs and constant hidden-independent lambda_0; mathematical_form=S_EM=-(lambda_0/4) integral sqrt(-g_obs) F_{mu nu}F^{mu nu}; Lie_v lambda_0=0; derives=T_EM and Poynting/radiation stress are part of the same Hilbert source; forbids=lambda(y)F^2, hidden Hodge maps, floating current normalization, and static/radiative double counting; current_status=CONDITIONAL_EM_MEASURE_ROUTE_NOT_PARENT_SIGNED; valid_for_claim=false
- `HSC3340_5_kernel_boundary_owner`: required_clause=contact and boundary terms are either Hilbert-ultralocal, exact zero-flux improvements, or finite bounded residuals; mathematical_form=Delta J^{mu nu}=nabla_lambda B^{lambda mu nu}+C_contact(ell_c/L)^p R^{mu nu}_contact; derives=ell_c=0 for ultralocal Hilbert coupling, otherwise p=2/p=4 finite contact route; forbids=unsourced contact floors, boundary mass drift, and source-worldtube chosen after readout; current_status=ROUTE_DEFINED_NOT_PARENT_OR_NUMERIC_SIGNED; valid_for_claim=false
- `HSC3340_6_bianchi_balance`: required_clause=residual source obeys conservation or is accompanied by a signed compensating field equation; mathematical_form=nabla_mu(E_obs^{mu nu}-kappa_*T_total^{mu nu}-Delta J^{mu nu})=0; derives=no unbalanced fifth-force/nonconservation channel enters the GR comparison; forbids=using a source residual that violates Bianchi constraints as if it were GR; current_status=STANDARD_CONDITIONAL_NOT_PARENT_SIGNED_FOR_ALL_RESIDUALS; valid_for_claim=false

## Parent Clause Evidence Score

- `EV3340_0_parent_action_form`: clause_id=HSC3340_0_parent_action_form; best_evidence=P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv; P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv; evidence_status=CONDITIONAL_CLAUSE_WRITTEN_NOT_DERIVED; passes_parent_signature=false; reason=same coframe/matter functor clauses exist but explicitly mark parent derivation open; valid_for_claim=false
- `EV3340_1_variation_target`: clause_id=HSC3340_1_variation_target; best_evidence=P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv; P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv; evidence_status=EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED; passes_parent_signature=false; reason=Hilbert-source signature excludes source-only selectors if owned, but current corpus says ownership is not derived; valid_for_claim=false
- `EV3340_2_common_kappa`: clause_id=HSC3340_2_common_kappa; best_evidence=P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv; P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv; evidence_status=CALIBRATION_ALLOWED_NOT_PREDICTIVE; passes_parent_signature=false; reason=common kappa can be calibrated as G_N, but no parent normalization principle fixes or signs it; valid_for_claim=false
- `EV3340_3_no_spurion_weights`: clause_id=HSC3340_3_no_spurion_weights; best_evidence=P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv; evidence_status=COUNTERMODEL_FILTER_DEFINED; passes_parent_signature=false; reason=forbidden source-only spurion and hidden spurion return are identified, not eliminated by parent syntax; valid_for_claim=false
- `EV3340_4_public_Maxwell_Hodge`: clause_id=HSC3340_4_public_Maxwell_Hodge; best_evidence=P8_Y5_R2FR_3117_EM_COUPLING_OWNER_ALPHA_PRIORITY.csv; P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv; evidence_status=CONDITIONAL_EM_STRESS_ROUTE_WITH_FLUX_GUARD; passes_parent_signature=false; reason=public Hodge/Maxwell route and Poynting guard exist, but hidden F2/Hodge/current closure is not signed; valid_for_claim=false
- `EV3340_5_kernel_boundary_owner`: clause_id=HSC3340_5_kernel_boundary_owner; best_evidence=P8_Y5_R2FR_3339_KERNEL_CONTACT_SCALE_OWNER.csv; P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv; evidence_status=OWNER_ROUTE_DEFINED_NOT_SIGNED; passes_parent_signature=false; reason=ultralocal/finite-kernel and worldtube routes are defined, but parent kernel moments and zero-flux boundary clauses are not signed; valid_for_claim=false
- `EV3340_6_bianchi_balance`: clause_id=HSC3340_6_bianchi_balance; best_evidence=P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv; 10-observer-map-symplectic-contract.md; evidence_status=WARD_IDENTITY_CONDITIONAL_NOT_FULL_SOURCE_MEASURE; passes_parent_signature=false; reason=standard same-action Ward/Bianchi route exists, but not all residual channels have signed compensators; valid_for_claim=false

## Hilbert Source Theorem Or Fail

- `HST3340_0_sufficient_parent_clause`: statement=If HSC3340_0 through HSC3340_6 are parent-signed, then the local ordinary source is J^{mu nu}=kappa_*T_total^{mu nu}+DeltaJ_silent^{mu nu}.; proof=Variation of one descended S_matter+S_EM against g_obs gives Hilbert T_total. A single kappa_* is common-mode calibrated by G_N. No post-variation source selector exists, so species/tensor/EM relative source coefficients vanish. Diffeomorphism invariance gives the same-frame Ward identity. Boundary/contact terms are silent or scale-bounded by their owner clauses.; result=DeltaJ_noncommon=0 and only silent boundary plus bounded derivative contact remain; current_status=EXACT_CONDITIONAL_THEOREM; valid_for_claim=false
- `HST3340_1_current_corpus_verdict`: statement=The current corpus does not yet parent-sign HSC3340_0 through HSC3340_6.; proof=Every evidence-score row is conditional, not parent-signed; several explicitly mark parent signature missing.; result=do not claim local-GR/PPN/Maxwell source-coupling closure; current_status=PARENT_HILBERT_CLAUSE_NOT_SIGNED_CURRENT_CORPUS; valid_for_claim=false
- `HST3340_2_finite_residual_fallback`: statement=If any HSC3340 clause remains unsigned, retain a finite residual vector R_source instead of closure-zero.; proof=3339 decomposes DeltaJ into common, tensor, species, spin/clock, EM/Hodge, contact, and boundary channels. Each channel has a zero route and an empirical/theorem-bound route.; result=R_source_local <= absolute sum of sourced residual-channel components; current_status=FALLBACK_VECTOR_REQUIRED; valid_for_claim=false

## Finite Residual Vector Schema

- `FRV3340_0_delta_kappa_common`: symbol=delta_kappa_common; definition=vertical/local drift of the universal common coupling after measured-G calibration; zero_condition=D ln kappa_*=0 on the local comparison branch; bound_formula=epsilon_kappa <= |D ln kappa_*|; observable_links=Gdot; orbital GM drift; clock/source calibration; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_1_eta_species`: symbol=eta_species; definition=species/source-only relative gravitational weight after common-mode removal; zero_condition=no source-only w_A/kappa_A in parent object language; bound_formula=epsilon_WEP <= max_{A,B}|eta_A-eta_B|; observable_links=WEP; composition clocks; source-composition tests; R10 materials; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_2_xi_tensor`: symbol=xi_tensor; definition=non-Hilbert tensor-ratio/traceless source coupling; zero_condition=same Hilbert tensor ratio for T00, Tij, pressure, stress, and EM stress; bound_formula=epsilon_tensor <= ||P_PPN G_PPN P_TL DeltaJ||/||kappa_*T00||; observable_links=PPN gamma; PPN beta; orbital stress; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_3_chi_spin_clock`: symbol=chi_spin_clock; definition=spin, torsion, clock, or preferred-frame source coupling outside public coframe; zero_condition=no independent spin/torsion/clock channel outside g_obs/e_obs; bound_formula=epsilon_clock <= ||P_clock DeltaJ||/||kappa_*T||; observable_links=clocks; spin tests; preferred-frame PPN; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_4_epsilon_EM`: symbol=epsilon_EM; definition=hidden EM/Hodge/current/Poynting stress coupling residual; zero_condition=public Hodge Maxwell action, fixed current lattice, and no hidden F2 coefficient; bound_formula=epsilon_EM <= |b_alpha| + |delta_J| + |delta_star| + ||P_EM DeltaT_EM||/||T_EM|| + |Phi_Poynting_unclosed|; observable_links=Maxwell limit; EM stress; Poynting flux; alpha drift; light propagation; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_5_epsilon_contact`: symbol=epsilon_contact; definition=finite-width/contact source-coupling floor; zero_condition=ultralocal Hilbert coupling or absorbed universal contact; bound_formula=epsilon_contact <= C_contact(ell_c/L_PPN)^p_contact; observable_links=PPN contact floor; R10/local force; WEP material contact; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_6_epsilon_boundary`: symbol=epsilon_boundary; definition=worldtube/boundary/improvement current projection; zero_condition=fixed Hilbert source worldtube and zero exterior flux/readout of improvement term; bound_formula=epsilon_boundary <= ||P_exterior nabla_lambda B^{lambda mu nu}||/||kappa_*T||; observable_links=source GM; orbital systems; PPN boundary leakage; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false
- `FRV3340_7_epsilon_bianchi`: symbol=epsilon_bianchi; definition=unbalanced divergence/nonconservation of residual source; zero_condition=nabla_mu DeltaJ^{mu nu}=0 or signed compensating field equation; bound_formula=epsilon_bianchi <= ||nabla_mu DeltaJ^{mu nu}||/(||kappa_*T||/L_PPN); observable_links=fifth force; nonconservation; clocks; orbits; status=SOURCE_NEEDED_OR_ZERO_THEOREM; valid_for_claim=false

## Source Coupling Budget Interface

- `BUD3340_0_absolute_source_vector`: formula=R_source_local <= A_k|delta_kappa_common| + A_WEP eta_species + A_T xi_tensor + A_C chi_spin_clock + A_EM epsilon_EM + epsilon_contact + epsilon_boundary + epsilon_bianchi; budget_value=6.900000e-06; budget_origin=private steering allocation F_SOURCE=0.30 of Cassini-gamma candidate 2.3e-5; acceptance_rule=no local-GR source-coupling claim unless every term is theorem-zero or source-backed and the absolute sum is below the arena threshold; valid_for_claim=false
- `BUD3340_1_theorem_zero_switch`: formula=R_source_local=0 iff all HSC3340 clauses are parent-signed and boundary/contact residuals are zero or suballocated; budget_value=0 for theorem-zero branch; budget_origin=parent Hilbert source clause; acceptance_rule=closure language is forbidden unless parent_signature=true for every clause; valid_for_claim=false
- `BUD3340_2_empirical_fallback`: formula=R_source_local scored component-by-component against WEP, clock, PPN, EM, orbital, and R10 arenas; budget_value=arena-specific; budget_origin=finite residual vector fallback; acceptance_rule=if theorem-zero fails, move to source acquisition rather than claiming local-GR derivation; valid_for_claim=false

## Clause Promotion Requirements

- `REQ3340_0_parent_action_equation`: requirement=explicit parent action or Lagrangian line containing S_matter[g_obs(q(Phi)),Psi,theta] and S_EM[g_obs(q(Phi)),A,lambda0]; current_status=MISSING_EXPLICIT_PARENT_LINE; exit_if_missing=finite residual vector branch remains active; valid_for_claim=false
- `REQ3340_1_parent_signature_vector`: requirement=parent_signature=true for HSC3340_0..HSC3340_6 with source paths and equation refs; current_status=ALL_EVIDENCE_ROWS_CONDITIONAL_NOT_PARENT_SIGNED; exit_if_missing=do not claim DeltaJ=0; valid_for_claim=false
- `REQ3340_2_residual_numeric_or_zero`: requirement=each FRV3340 residual component is theorem-zero or has finite source-backed value, units, response factor, and no-cancellation guard; current_status=SCHEMA_WRITTEN_VALUES_MISSING; exit_if_missing=do not claim empirical local pass; valid_for_claim=false
- `REQ3340_3_EM_flux_split`: requirement=static EM stress, Poynting flux, and radiative boundary terms are separated before source mass scoring; current_status=3127_GUARD_EXISTS_NOT_FILLED_FOR_REAL_SOURCES; exit_if_missing=no EM stress/local-GR source claim; valid_for_claim=false

## Promotion Gates

- `GATE3340_0_parent_clause_written`: claim=minimal parent Hilbert source clause is written exactly; passed=true; reason=HSC3340 rows specify action form, variation target, common kappa, no-spurion rule, Maxwell/Hodge, boundary/contact, and Bianchi balance; valid_for_claim=false
- `GATE3340_1_evidence_scored`: claim=current corpus evidence for the parent clause has been scored; passed=true; reason=each HSC3340 clause is mapped to best available source rows and parent-signature status; valid_for_claim=false
- `GATE3340_2_parent_signature_closed`: claim=parent action signs the Hilbert source clause; passed=false; reason=fails because every current evidence row is conditional/not parent-signed; valid_for_claim=false
- `GATE3340_3_finite_residual_vector_ready`: claim=finite residual vector schema is ready for source acquisition; passed=true; reason=FRV3340 components cover common drift, species, tensor, spin/clock, EM, contact, boundary, and Bianchi channels; valid_for_claim=false
- `GATE3340_4_local_GR_claim`: claim=MTS local-GR/PPN/Maxwell source-coupling branch is claim-ready; passed=false; reason=parent signature is not closed and residual components are not yet finite source-backed values; valid_for_claim=false

## Decision Ledger

- `DEC3340_0`: question=Did 3340 find a signed parent Hilbert source clause?; answer=not in the current corpus; reason=the best rows are exact conditional theorems and contracts, but explicitly say parent signature remains missing; next_action=either supply/construct the explicit parent action line or fill the finite residual vector components; valid_for_claim=false
- `DEC3340_1`: question=Did 3340 move the work forward anyway?; answer=yes; reason=the parent clause is now exact and the fallback residual vector is componentized instead of vague; next_action=attack the highest-leverage component first: no-spurion/common-kappa/EM-Hodge parent signature or numeric eta_species bound; valid_for_claim=false
- `DEC3340_2`: question=What is the best next strike?; answer=build a strict source-coupling residual runner; reason=if the parent action clause cannot be signed immediately, the fastest empirical discipline is to make FRV3340 rows source-fillable and refuse placeholders; next_action=3341 should implement first residual-vector source row runner with theorem-zero switches and absolute-sum budget; valid_for_claim=false

## Next Target

- `3341-Y5-R2FR-source-coupling-residual-vector-runner-under-AX1090.md`: target_script=scripts/Y5_R2FR_3341_source_coupling_residual_vector_runner.py; objective=turn FRV3340 into a strict source-fill runner: accept theorem-zero only with parent-signed clauses, otherwise require finite numeric sourced residual rows with units and no-cancellation absolute-sum budget; must_include=eta_species, xi_tensor, epsilon_EM, epsilon_contact, epsilon_boundary, epsilon_bianchi, response factors, arena thresholds, no placeholder pass, no local-GR claim; fallback_if_failed=select one component, preferably eta_species or epsilon_EM, for dedicated source acquisition/derivation; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- It does not pretend the parent Hilbert clause is signed; it converts the unsigned branch into a strict residual-vector interface.
- It keeps `G_N` and `alpha` as allowed common calibrations unless relative hidden couplings survive.
- `formalization-workbench` is not modified.
