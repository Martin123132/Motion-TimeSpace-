# 3338 - PPN projector/patch geometry source contract under AX1090

Run UTC: `2026-06-28T01:57:00.112266+00:00`

## Verdict

3338 turns the PPN patch problem into a concrete contract rather than another missing-input list.

The gamma readout branch is now explicit:

`P_gamma[h,U] := delta^{ij} h_ij/(6 U) - 1`

on a weak-field isotropic PPN patch with the Newtonian potential `U` already fixed by measured local `G_N M`.

Freezing `U=U0` on an interior patch makes the gamma readout a constant-coefficient Fourier multiplier, so the 3337 commutator-zero theorem can apply.

If `U` is not frozen, the variation scale is not mysterious:

`L_var := U/|grad U|`

and for an exterior solar monopole `U=G_N M/(c^2 r)`, this reduces to:

`L_var = r`

so a Cassini-like near-Sun path uses the impact parameter as the conservative local variation scale.

Using the 3336/3337 private steering budget gives `delta_comm_allowed = 6.900e-03` and `B_comp = 6.900e-06`.

That converts the geometry into two real inequalities:

`ell_s/L_var <= (delta_comm_allowed - boundary_tail - epsilon_gauge_res)/C_comm`

`ell_c/L_PPN <= (B_comp/C_contact)^(1/p_contact)`

This does not claim local GR/PPN success, but it tells us exactly what physical lengths and coupling signatures must be derived next.

## Source Register

- `SRC3338_0_3337_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3337-Y5-R2FR-PPN-commutator-contact-zero-or-bound-theorem-under-AX1090.md` exists=true parse_ok=true role=3337 handoff for commutator/contact theorem
- `SRC3338_1_3337_commutator`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3337_COMMUTATOR_THEOREM.csv` exists=true parse_ok=true role=delta_comm exact-zero and bound theorem
- `SRC3338_2_3337_contact`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3337_CONTACT_THEOREM.csv` exists=true parse_ok=true role=contact zero-or-scale theorem
- `SRC3338_3_3337_requirements`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3337_REQUIRED_INPUTS.csv` exists=true parse_ok=true role=projector, patch, boundary, contact, and spectral missing inputs
- `SRC3338_4_3336_thresholds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3336_PPN_THRESHOLD_CANDIDATES.csv` exists=true parse_ok=true role=Cassini gamma candidate steering threshold
- `SRC3338_5_3336_web_sources`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3336_WEB_SOURCE_REGISTER.csv` exists=true parse_ok=true role=Cassini and Will PPN source references already recorded
- `SRC3338_6_3331_cmetric`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3331_CMETRIC_BOUND.csv` exists=true parse_ok=true role=PPN gauge/projector slot and C_metric factorization
- `SRC3338_7_3332_composite`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv` exists=true parse_ok=true role=PPN composite budget template

## PPN Projector Contract

- `PPROJ3338_0_gamma_trace_readout`: slot=PPN gamma; local_projector=P_gamma[h,U] := delta^{ij} h_ij/(6 U) - 1; derivation=In isotropic PPN gauge, g_ij = delta_ij(1+2 gamma U)+O(U^2), so h_ij=g_ij-delta_ij and delta^{ij}h_ij=6 gamma U; subtracting 1 scores gamma-1 against GR.; conditions=weak-field isotropic PPN gauge; calibrated Newtonian potential U=G_N M/(c^2 r); source GM mode is fixed before residual scoring; fourier_symbol=on a frozen interior patch U=U0, P_gamma has constant symbol delta^{ij}/(6 U0) on the spatial-trace component; commutator_status=FOURIER_MULTIPLIER_BRANCH_IF_U_FROZEN; valid_for_claim=false
- `PPROJ3338_1_beta_temporal_readout`: slot=PPN beta; local_projector=P_beta[h00,U] := (2 U - h00)/(2 U^2) - 1; derivation=With g_00=-1+2U-2 beta U^2+O(U^3), h00=g_00+1, so beta=(2U-h00)/(2U^2); subtracting 1 scores beta-1.; conditions=same source U and gauge convention as gamma; higher-order terms must be separated from MTS residuals; fourier_symbol=constant local coefficient if U is frozen to U0; otherwise coefficient varies on L_var=U/|grad U|; commutator_status=SECONDARY_SLOT_NOT_CASSINI_PRIMARY; valid_for_claim=false
- `PPROJ3338_2_gm_absorption_guard`: slot=Newtonian source calibration; local_projector=project out pure GM/source-normalization shifts before PPN residual scoring; derivation=Measured G_N and the source mass define U. A residual that only rescales U is Newtonian calibration, not a gamma/beta anomaly.; conditions=MTS residual is evaluated after the Newtonian slot is fixed; no hidden re-fit inside the PPN projector; fourier_symbol=removes the source normalization mode from the residual vector; commutator_status=REQUIRED_FOR_NO_DOUBLE_COUNTING; valid_for_claim=false
- `PPROJ3338_3_exact_commutator_route`: slot=projector/smoothing compatibility; local_projector=P_PPN(k) S_ell(k)=S_ell(k) P_PPN(k) after local freezing and gauge fixing; derivation=The 3337 theorem applies if the readout map is a constant-coefficient projector on the patch and S_ell is scalar/isotropic in the PPN band.; conditions=interior patch; frozen U0; constant tetrad/frame; scalar smoothing kernel; no boundary leakage; fourier_symbol=matrix P_PPN(k) times scalar s_ell(k); commutator_status=DELTA_COMM_ZERO_CONDITION; valid_for_claim=false

## Patch Geometry Derivation

- `PGEOM3338_0_variation_length_general`: quantity=L_var; formula=L_var := U/|grad U| for the PPN readout coefficient 1/U; derivation=The gamma projector coefficient is proportional to 1/U, so |grad ln(1/U)|=|grad U|/U; the inverse logarithmic gradient is the commutator variation scale.; source_status=DERIVED_FROM_PROJECTOR_CONTRACT; valid_for_claim=false
- `PGEOM3338_1_monopole_reduction`: quantity=solar-system monopole L_var; formula=if U=G_N M/(c^2 r), then L_var=r; derivation=|grad U|=U/r for a monopole exterior, hence U/|grad U|=r; along a ray the minimum scale is the impact parameter b.; source_status=NEEDS_CASSINI_GEOMETRY_SOURCE_FOR_b; valid_for_claim=false
- `PGEOM3338_2_boundary_tail`: quantity=boundary leakage; formula=epsilon_boundary_comm <= C_boundary exp[-d_boundary^2/(2 ell_s^2)]; derivation=A Gaussian or similarly localized smoothing kernel loses mass across a patch boundary only through its tail outside the interior support.; source_status=KERNEL_CONVENTION_NEEDED; valid_for_claim=false
- `PGEOM3338_3_commutator_requirement`: quantity=smoothing-to-variation ratio; formula=ell_s/L_var <= (delta_comm_allowed - boundary_tail - epsilon_gauge_res)/C_comm; derivation=Insert the 3337 bound delta_comm <= C_comm ell_s/L_var + boundary_tail + epsilon_gauge_res into the 3336 Cassini-gamma composite allocation.; source_status=NUMERIC_STEERING_FROM_3336_3337; valid_for_claim=false
- `PGEOM3338_4_contact_scale_requirement`: quantity=contact correlation ratio; formula=ell_c/L_PPN <= (B_comp/C_contact)^(1/p_contact); derivation=Rearrange epsilon_contact <= C_contact(ell_c/L_PPN)^p_contact and require it below the 3336 composite budget B_comp.; source_status=NUMERIC_STEERING_FROM_3337; valid_for_claim=false

## Patch Scale Solver

- `SOLVE3338_comm_C1_clean`: kind=commutator_patch; C_comm=1.000000e+00; boundary_tail=0.000000e+00; epsilon_gauge_res=0.000000e+00; allowed_ratio=6.900000e-03; allowed_ell_s_if_Lvar_Rsun_m=4.800330e+06; allowed_ell_s_if_Lvar_AU_m=1.032225e+09; budget=6.900000e-03; passes_possible=true; source_note=R_sun/AU columns are nonclaim steering constants; source official constants before claim; comment=generic clean interior patch; valid_for_claim=false
- `SOLVE3338_comm_C2_clean`: kind=commutator_patch; C_comm=2.000000e+00; boundary_tail=0.000000e+00; epsilon_gauge_res=0.000000e+00; allowed_ratio=3.450000e-03; allowed_ell_s_if_Lvar_Rsun_m=2.400165e+06; allowed_ell_s_if_Lvar_AU_m=5.161127e+08; budget=6.900000e-03; passes_possible=true; source_note=R_sun/AU columns are nonclaim steering constants; source official constants before claim; comment=moderate projector variation constant; valid_for_claim=false
- `SOLVE3338_comm_C2_boundary`: kind=commutator_patch; C_comm=2.000000e+00; boundary_tail=9.000000e-04; epsilon_gauge_res=0.000000e+00; allowed_ratio=3.000000e-03; allowed_ell_s_if_Lvar_Rsun_m=2.087100e+06; allowed_ell_s_if_Lvar_AU_m=4.487936e+08; budget=6.900000e-03; passes_possible=true; source_note=R_sun/AU columns are nonclaim steering constants; source official constants before claim; comment=uses 3337 ceiling-edge boundary allocation; valid_for_claim=false
- `SOLVE3338_comm_C2_gauge`: kind=commutator_patch; C_comm=2.000000e+00; boundary_tail=9.000000e-04; epsilon_gauge_res=1.000000e-03; allowed_ratio=2.500000e-03; allowed_ell_s_if_Lvar_Rsun_m=1.739250e+06; allowed_ell_s_if_Lvar_AU_m=3.739947e+08; budget=6.900000e-03; passes_possible=true; source_note=R_sun/AU columns are nonclaim steering constants; source official constants before claim; comment=boundary plus residual gauge leakage; valid_for_claim=false
- `SOLVE3338_comm_fail_boundary`: kind=commutator_patch; C_comm=2.000000e+00; boundary_tail=7.000000e-03; epsilon_gauge_res=0.000000e+00; allowed_ratio=0.000000e+00; allowed_ell_s_if_Lvar_Rsun_m=0.000000e+00; allowed_ell_s_if_Lvar_AU_m=0.000000e+00; budget=6.900000e-03; passes_possible=false; source_note=R_sun/AU columns are nonclaim steering constants; source official constants before claim; comment=boundary already exceeds composite allocation; valid_for_claim=false
- `SOLVE3338_contact_p2`: kind=contact_scale; C_contact=1.000000e+00; p_contact=2; allowed_ratio=2.626785e-03; allowed_ell_c_if_Lppn_Rsun_m=1.827454e+06; allowed_ell_c_if_Lppn_AU_m=3.929615e+08; budget=6.900000e-06; passes_possible=true; source_note=claim requires parent-owned ell_c and C_contact, not these steering scales; comment=contact scale-separation ceiling from 3337 theorem; valid_for_claim=false
- `SOLVE3338_contact_p4`: kind=contact_scale; C_contact=1.000000e+00; p_contact=4; allowed_ratio=5.125217e-02; allowed_ell_c_if_Lppn_Rsun_m=3.565614e+07; allowed_ell_c_if_Lppn_AU_m=7.667216e+09; budget=6.900000e-06; passes_possible=true; source_note=claim requires parent-owned ell_c and C_contact, not these steering scales; comment=contact scale-separation ceiling from 3337 theorem; valid_for_claim=false

## Contact Universality Contract

- `CUNI3338_0_absorbable_metric_contact`: condition=contact tensor is universal and proportional to the same metric/Newtonian source tensor used to define measured G_N; result=epsilon_contact_PPN=0 after source calibration; failure_mode=none if no species, spin, orientation, or nonmetric residue survives; needed_source=parent coupling/current tensor decomposition; valid_for_claim=false
- `CUNI3338_1_derivative_contact`: condition=zeroth contact is absorbed but derivative finite-size residue remains analytic and isotropic; result=epsilon_contact_PPN <= C_contact(ell_c/L_PPN)^p_contact with p>=2, or p>=4 if second-order term is also forbidden/absorbed; failure_mode=large ell_c/L_PPN or unsourced C_contact leaves explicit floor; needed_source=ell_c, C_contact, p_contact from parent branch or empirical upper bound; valid_for_claim=false
- `CUNI3338_2_nonuniversal_contact`: condition=contact carries composition-dependent, nonmetric, spin, orientation, or clock-channel structure; result=cannot be absorbed into local G_N; becomes a WEP/clock/PPN residual source; failure_mode=local-GR branch blocked unless externally bounded below relevant experiment limits; needed_source=WEP/clock/orbital projection of the nonuniversal tensor; valid_for_claim=false

## Source Acquisition Rows

- `ACQ3338_0_Will_PPN_metric_convention`: quantity=PPN metric convention for gamma and beta readouts; current_status=SOURCE_REFERENCE_RECORDED_IN_3336_WEB_REGISTER; required_action=quote/check exact sign and normalization convention against Will LRR before public use; claim_blocker=gamma/beta projector not source-owned in final notation; valid_for_claim=false
- `ACQ3338_1_Cassini_geometry`: quantity=Cassini solar-conjunction impact parameter b and observable mapping to gamma; current_status=THRESHOLD_RECORDED_BUT_GEOMETRY_NOT_EXTRACTED; required_action=extract b/range geometry from Cassini source or use a conservative b>=R_sun bound with source; claim_blocker=L_var numerical floor not source-owned; valid_for_claim=false
- `ACQ3338_2_official_length_constants`: quantity=R_sun, AU, and any solar-system patch scale constants; current_status=NONCLAIM_STEERING_VALUES_USED_IN_SOLVER; required_action=record official IAU/CODATA source rows before promoting any numeric scale; claim_blocker=length scale source provenance incomplete; valid_for_claim=false
- `ACQ3338_3_MTS_smoothing_length`: quantity=ell_s used by the local PPN branch; current_status=PARENT_BRANCH_MISSING; required_action=derive ell_s from parent action/coarse-graining or define it as a bounded regulator with physical source; claim_blocker=cannot evaluate ell_s/L_var; valid_for_claim=false
- `ACQ3338_4_MTS_contact_length`: quantity=ell_c, C_contact, and p_contact; current_status=PARENT_BRANCH_MISSING; required_action=derive from contact/current tensor or fit-independent parent correlation scale; claim_blocker=cannot evaluate contact floor; valid_for_claim=false
- `ACQ3338_5_contact_tensor_universality`: quantity=whether contact/source coupling is universal metric or nonuniversal; current_status=PARENT_SIGNATURE_NEEDED; required_action=decompose source coupling into metric trace, traceless, species, spin, and clock components; claim_blocker=absorption into measured G_N not proven; valid_for_claim=false
- `ACQ3338_6_spectral_tail_after_composite_cleanup`: quantity=two-particle spectral gap/tail in PPN band; current_status=STILL_MISSING_FROM_3337; required_action=bound epsilon_2p or prove gap/band suppression after patch geometry is fixed; claim_blocker=remaining composite floor not closed; valid_for_claim=false

## Promotion Gates

- `GATE3338_0_gamma_projector_defined`: claim=PPN gamma projector/readout is explicitly defined; passed=true; reason=gamma readout P_gamma[h,U]=delta^{ij}h_ij/(6U)-1 is derived from isotropic PPN form; valid_for_claim=false
- `GATE3338_1_Lvar_derived`: claim=PPN readout variation scale is derived; passed=true; reason=L_var=U/|grad U| and monopole exterior gives L_var=r, with impact parameter b as local minimum; valid_for_claim=false
- `GATE3338_2_scale_solver_present`: claim=commutator/contact ceilings have explicit allowed ratios; passed=true; reason=solver rows convert 3336/3337 budgets into ell_s/L_var and ell_c/L_PPN ceilings; valid_for_claim=false
- `GATE3338_3_numeric_claim_ready`: claim=PPN patch geometry is numerically source-owned; passed=false; reason=Cassini geometry, official constants, ell_s, ell_c, C_contact, and contact tensor signature remain unpromoted; valid_for_claim=false
- `GATE3338_4_local_GR_claim`: claim=MTS local-GR/PPN branch is claim-ready; passed=false; reason=3338 defines the projector and derives scale requirements, but does not supply parent smoothing/contact/spectral inputs; valid_for_claim=false

## Decision Ledger

- `DEC3338_0`: question=Did 3338 move beyond a missing-input ledger?; answer=yes; reason=it derives the gamma projector, shows L_var=U/|grad U|, reduces solar monopole variation to L_var=r, and solves allowed scale ratios; next_action=derive parent ell_s/ell_c/contact universality or source them from the MTS parent branch; valid_for_claim=false
- `DEC3338_1`: question=Is the commutator scary after the patch derivation?; answer=conditionally not; reason=if ell_s is microscopic or even modestly smaller than the solar-system variation scale, ell_s/L_var can sit below the 3337 ceiling; if ell_s is astronomical, it fails; next_action=stop treating ell_s as vague; derive its physical value or bound; valid_for_claim=false
- `DEC3338_2`: question=What is the new real bottleneck?; answer=parent source coupling and correlation scales; reason=the PPN projector geometry is now mostly a contract; the missing physics is whether the MTS contact/coupling is universal metric and what ell_s/ell_c are; next_action=build 3339 parent coupling decomposition into metric trace, traceless, spin/species, and clock channels; valid_for_claim=false

## Next Target

- `3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md`: target_script=scripts/Y5_R2FR_3339_parent_source_coupling_decomposition.py; objective=decompose the MTS source/contact coupling into universal metric trace, traceless metric, species/spin, clock, and boundary channels; derive whether measured-G absorption is legitimate; must_include=contact tensor signature; ell_s and ell_c ownership; WEP/clock risk routing; no local-GR claim unless nonmetric residues vanish or are source-bounded; fallback_if_failed=retain explicit source-coupling floor and move to empirical local bound acquisition; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- It derives the PPN gamma readout and patch scale law, but it does not supply parent-owned `ell_s`, `ell_c`, or contact tensor signatures.
- The `R_sun` and `AU` numerical columns are steering scales only until official source rows are attached.
- `formalization-workbench` is not modified.
