# 3559 - Hilbert identity PiM chainmap source-support adoption or bound

## Verdict
3559 takes the branch instead of circling it: the preferred local source branch now adopts `Pi_M^H` as the identity/inclusion on the typed Hilbert mass-current complex `C_H^M(W,e_obs,tau)`. On that fixed complex, the independent operator commutator is exactly zero: `[d,Pi_M^H]J_H^M=0`.

This is not a local-GR claim. The work moved the live problem out of vague projector algebra and into the real remaining places: source support, q-basic worldtube descent, `M_H_ref`, actual vertical basis, extra mass projection, and parent anomaly/side-flux silence.

## Reduced obstruction
Starting from 3558, `d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`.

After preferred-branch adoption, the fixed-complex operator piece is zero, so the honest reduced gate is:

`d(Pi_M^H J_H^M)=0` only if `Pi_M^H dJ_extra=0`, `A_parent=0`, `Delta_support=0`, and exterior side flux is zero.

Here `Delta_support` carries `W_source`, `tau/e_obs`, `H_ref`, source-shape, domain and q-basic descent drift. This is the useful separation.

## What moved
- `Pi_M` is no longer allowed to mean three things at once; the preferred branch uses `Pi_M^H=id/inclusion`.
- Old topological/Hodge/readout `Pi_M` is demoted unless an equivalence theorem or bound branch is supplied.
- The independent projector operator commutator is theorem-zero on the typed Hilbert current complex.
- Source-support drift is still live and cannot be hidden inside the identity operator.
- The next derivation target is now sharply `W_source`/`Y=(M_H_ref,sigma^a)` q-basic descent.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_SOURCE_REGISTER.csv`
- `adoption_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv`
- `clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_ADOPTION_CLAUSE_AUDIT.csv`
- `obstruction_split`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_SOURCE_SUPPORT_OBSTRUCTION_MAP.csv`
- `coefficient_bound_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_COEFFICIENT_BOUND_ROWS.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_Hilbert_identity_PiM_chainmap_source_support_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3559_VALIDATION.csv`

## Adoption theorem rows
- `PIA3559_0_typed_Hilbert_mass_current_complex`: Define C_H^M(W,e_obs,tau) as the typed Hilbert mass-current complex built from the same observed coframe, time generator, and source collar before any orbital/R10/PPN readout.
- `PIA3559_1_identity_chainmap_zero`: On C_H^M, take Pi_M^H as the identity/inclusion of the typed Hilbert mass-current slot. Then [d,Pi_M^H]J_H^M=0 exactly on that fixed complex.
- `PIA3559_2_operator_vs_support_split`: The old symbol [d,Pi_M]J_H must now be split into a zero operator piece [d,Pi_M^H]J_H^M and a live source-support/domain piece Delta_support when W_source, tau, frame, H_ref, or q-basic source coordinates drift.
- `PIA3559_3_qbasic_source_support_zero_route`: If Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and v_X is in ker(Dq), then A_X=dY(v_X)=0, so C_M=C_shape=0 and the source-coordinate part of Delta_support vanishes.
- `PIA3559_4_reduced_closure_obstruction`: After adopting Pi_M^H on C_H^M, the local source closure gate reduces to Pi_M^H dJ_extra=0, A_parent=0, Delta_support=0, and exterior side flux=0; the independent Pi_M operator-stress branch is no longer the preferred obstruction.

## Clause audit
- `CLA3559_0_C_HM_branch`: C_H^M(W,e_obs,tau) typed Hilbert mass-current complex exists before readout -> ADOPTED_PRIVATE_BRANCH_CONTRACT
- `CLA3559_1_PiMH_identity`: Pi_M^H is identity/inclusion on C_H^M -> EXACT_OPERATOR_ZERO_ON_FIXED_COMPLEX
- `CLA3559_2_old_PiM_demoted`: old topological/Hodge/readout Pi_M not used in preferred local source branch -> DEMOTION_LOCK_ACTIVE
- `CLA3559_3_worldtube_support`: W_source=closure(supp J_H[tau]) is parent-owned and fixed before readout -> UNSIGNED_REMAINS_LIVE
- `CLA3559_4_qbasic_MHref`: M_H_ref=H_tau-H_ref descends through q -> UNSIGNED_REMAINS_LIVE
- `CLA3559_5_qbasic_shape`: source shape/support coordinates sigma^a descend through q -> UNSIGNED_REMAINS_LIVE
- `CLA3559_6_actual_vertical_basis`: residual directions satisfy Dq(v_X)=0 for the actual q map -> MISSING_ACTUAL_QMAP_AND_BASIS
- `CLA3559_7_no_readout_laundering`: source mass, support, and projector are not chosen after seeing orbital GM -> GUARD_ACTIVE_NOT_THEOREM
- `CLA3559_8_tau_eobs_lock`: same tau/e_obs branch feeds Hilbert source, H_tau, clocks, orbit and R10 readout -> CONDITIONAL_UNSIGNED

## Obstruction split
- `OBS3559_0_Delta_PiM_operator` `[d,Pi_M^H]J_H^M`: THEOREM_ZERO_ON_FIXED_C_HM (No longer counted as an independent live obstruction on the preferred branch.)
- `OBS3559_1_Delta_support` `D_X W_source; D_X sigma^a`: LIVE_UNSIGNED (Cannot be killed by identity Pi_M; it is the next actual derivation target.)
- `OBS3559_2_C_M` `partial_M A_X^M`: LIVE_UNSIGNED (Killed if source-coordinate quotient descent fires.)
- `OBS3559_3_C_shape` `partial_M A_X^a`: LIVE_UNSIGNED (Killed if worldtube shape descends through q.)
- `OBS3559_4_C_domain_C_frame` `C_domain+C_frame`: LIVE_UNSIGNED (Needs a source-support adoption theorem or bound rows.)
- `OBS3559_5_PiM_extra_mass` `Pi_M^H dJ_extra`: LIVE_UNSIGNED (Survives 3559 and remains one of the true local-GR gates.)
- `OBS3559_6_parent_anomaly` `A_parent`: LIVE_UNSIGNED (Survives 3559 and must not be canceled by source fitting.)

## Coefficient / bound rows
- `CF3559_0_Delta_PiM_operator` `Delta_PiM_operator`: THEOREM_ZERO_ON_PREFERRED_BRANCH
- `CF3559_1_Delta_PiM_old_top` `R_eq_top;B_zero_flux;I_commutator_top`: DEMOTED_TO_BOUND_BRANCH
- `CF3559_2_Delta_support` `Delta_W;C_domain;C_shape`: MISSING_SOURCE_SUPPORT_QBASIC_THEOREM_OR_BOUND
- `CF3559_3_C_M` `C_M;A_X^M;partial_M_A_XM`: MISSING_MHREF_QBASIC_DESCENT_OR_BOUND
- `CF3559_4_C_frame` `C_frame;Delta_tau;Delta_eobs`: MISSING_SAME_FRAME_PARENT_LOCK_OR_BOUND
- `CF3559_5_E_Dq_source` `E_Dq_source;Dq(v_X)`: MISSING_ACTUAL_QMAP_VERTICAL_BASIS
- `CF3559_6_mu_extra_after_PiMH` `Pi_M^H dJ_extra;mu_extra`: MISSING_ZERO_THEOREM_OR_CHANNEL_VECTOR_VALUES

## Decision ledger
- `DEC3559_0`: Adopt Pi_M^H as the preferred private local source branch. This is a real forward move: the independent Pi_M operator commutator is zero on the typed Hilbert current complex, instead of being left as a generic missing target.
- `DEC3559_1`: Move source-support drift out of the Pi_M operator bucket. The remaining problem is no longer 'the projector' in general; it is W_source/tau/e_obs/H_ref/q-basic source-support ownership.
- `DEC3559_2`: Forbid old Pi_M from sneaking back into the preferred branch. Topological/Hodge/readout Pi_M can only return through an explicit equivalence theorem or a bound branch.
- `DEC3559_3`: Next target should attack source support directly. The best next shot is q-basic W_source/M_H_ref descent: prove W_source=closure(supp J_H[tau]) and Y=Ybar(q(Phi)), or produce source-ready support coefficients.

## Next target
- `3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md`
- Objective: try to prove W_source=closure(supp J_H[tau]) and Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) on the same e_obs/tau branch; if not, fill Delta_W, C_domain, C_shape, C_frame and E_Dq_source bound rows
