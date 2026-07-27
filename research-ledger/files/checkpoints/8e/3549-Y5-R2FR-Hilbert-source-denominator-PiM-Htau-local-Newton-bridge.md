# 3549 — Hilbert source denominator PiM/Htau local Newton bridge

## Verdict

- **The source denominator bridge is now locked into one exact square:** `R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.
- **No Newton/Poisson/local-GR claim is allowed yet.** The conditional zero route is clean, but the mass-flat source connection, Htau integrability, worldtube selector, reference lock, same-frame branch and denominator units are not parent-signed.
- **The best next move is not another broad audit:** attack `C_M` and `C_shape` by deriving the mass-flat source-branch connection for `Pi_M`.
- **PPN remains separate:** even a future first-order Newton bridge cannot be promoted to full local GR until second-order beta/gamma/operator residuals close.

## Identity Lock

| identity_id | object | mathematical_form | meaning | current_status |
| --- | --- | --- | --- | --- |
| ID3549_0_MHref | Hilbert source denominator | M_H_ref := H_tau[S_outer] - H_ref | source mass denominator must be finite, positive, same-frame and defined before orbital GM readout | CONDITIONAL_DEFINITION_NOT_CLAIMED |
| ID3549_1_ellJ | source-current normalization drift | z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units | source coupling is no longer vague; its denominator drift has named obstruction terms | EXACT_DECOMPOSITION_NONCLAIM |
| ID3549_2_PiM_Htau_square | algebraic denominator heart | R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units | the hardest denominator terms reduce to a mass-connection/integrability/reference/domain/frame/units square | EXACT_COMPONENT_DECOMPOSITION_NONCLAIM |
| ID3549_3_Newton_target | Newton/Poisson bridge | nabla^2 Phi = 4*pi*G_eff*rho_H and surface_integral grad Phi.dS = 4*pi*G_eff*M_H_ref | becomes claimable only after EH operator, source denominator, closed flux, Gauss calibration and readout residuals close | TARGET_WRITTEN_NOT_PROMOTED |

## Zero Clauses

| component | zero_clause | mathematical_condition | effect | current_status | missing_owner |
| --- | --- | --- | --- | --- | --- |
| C_M | mass-flat source connection | partial_M A_X^M = 0 | residual direction X does not reparameterize source mass | NEW_PARENT_CONNECTION_REQUIRED | A_X source-branch geometry from q(Phi) |
| C_shape | mass/shape orthogonality | partial_M A_X^a = 0 or shape directions are Pi_M-orthogonal | source shape/domain leakage cannot masquerade as mass denominator drift | SOURCE_SHAPE_CONNECTION_UNSIGNED | parent source metric or shape-support orthogonality theorem |
| C_curl | integrable observed-time Hamiltonian | curl(delta H_tau)=0 up to exact/proper boundary terms | H_tau is a real charge rather than path-dependent bookkeeping | HTAU_INTEGRABILITY_CURL_OPEN | parent theta/omega owner, tau/surface lock and boundary exactness |
| C_domain | fixed parent worldtube/support selector | W_source = closure(supp J_H[tau]) and linked surfaces fixed before readout | Pi_M does not move source support after seeing data | DOMAIN_SUPPORT_NOT_PARENT_SIGNED | same-frame J_H, tau lock, compact support and no readout mask |
| C_ref | source-blind reference subtraction | D_X H_ref=0 and [D_X,Pi_M]H_ref=0 | reference subtraction cannot launder source mass normalization | REFERENCE_SELECTOR_UNSIGNED | Sigma_ref/H_ref selector from boundary/topology/stationarity/asymptotic coframe data |
| C_frame | same observed frame/tau/surface/readout branch | tau, e_obs, surfaces and readout frame are fixed together before readout | clock/frame normalization cannot change the denominator commutator | PARALLEL_RFRAME_FACTOR | same-frame source variation, not merely same-frame matter motion |
| C_units | parent-owned denominator units | M_H_ref units, G_ref and source-current normalization are declared before measured GM | unit/source normalization cannot be absorbed into orbital GM | ELLJ_UNITS_NONCLAIM | positive M_H_ref, no-orbital-import certificate and source-current unit lock |

## Bound Interfaces

| bound_id | component | observable_arena | candidate_bound | prediction_status | numeric_bound_ready |
| --- | --- | --- | --- | --- | --- |
| B3549_0_C_M_time | C_M | Gdot/time drift | 4.0e-14 yr^-1 anchor from 3514 template only | MISSING_MASS_CONNECTION_VALUE | False |
| B3549_1_C_shape_profile | C_shape | PPN source profile / R10 source support | MISSING_SHAPE_PROJECTION_BOUND | MISSING_SOURCE_SHAPE_CONNECTION_VALUE | False |
| B3549_2_C_curl_integrability | C_curl | Gdot / Newton source / clocks / PPN | MISSING_CURL_BOUND | MISSING_THETA_OMEGA_OWNER | False |
| B3549_3_C_domain_support | C_domain | R10 / Newton source / PPN source profile | MISSING_DOMAIN_SUPPORT_BOUND | MISSING_WORLDTUBE_SELECTOR | False |
| B3549_4_C_ref_reference | C_ref | Gdot / R10 denominator / local boundary terms | MISSING_REFERENCE_DERIVATIVE_BOUND | MISSING_HREF_SELECTOR | False |
| B3549_5_C_frame | C_frame | clock / PPN / orbital GM | MISSING_FRAME_SPLIT_BOUND | MISSING_SOURCE_FRAME_THEOREM | False |
| B3549_6_C_units | C_units | Gdot / Newton G / action normalization | MISSING_SOURCE_UNIT_BOUND | MISSING_DENOMINATOR_UNIT_LOCK | False |

## Newton Bridge Rungs

| rung_id | required_identity | math_form | blocked_by | current_status | claim_effect |
| --- | --- | --- | --- | --- | --- |
| NBR3549_0_candidate_charge | observed-time Hamiltonian charge exists and is integrable | H_xi = B_xi on shell; delta H_tau is path independent | C_curl; C_ref; C_frame | CONDITIONAL_NOT_PARENT_DERIVED | no source charge candidate can be promoted |
| NBR3549_1_charge_equals_Hilbert | Hamiltonian charge equals projected Hilbert mass current | B_xi/G_eff = M_eff[Pi_M J_H] | C_M; C_shape; C_domain; C_ref | NOT_PARENT_DERIVED | geometric charge is not yet Newton source mass |
| NBR3549_2_closed_flux | projected Hilbert mass flux is closed in compact exterior | d(Pi_M J_H)=0 and partial_t,r M_eff=0 outside support | C_domain; C_frame; C_units; R_Ward | NOT_PARENT_DERIVED | time drift/radial hair remain live |
| NBR3549_3_Poisson_source | EH weak-field 00 equation sources the same rho_H | nabla^2 Phi = 4*pi*G_eff*rho_H | R11 operator/source residuals plus source denominator rows | EXACT_CONDITIONAL_NOT_CLAIMED | no Newton/Poisson pass yet |
| NBR3549_4_Gauss_orbital_readout | Poisson source integrates to measured orbital monopole | surface_integral grad Phi.dS = 4*pi*G_eff*M_H_ref and a_r=-G_eff*M_H_ref/r^2 | closed flux, radial hair, range/source/frame residuals | NOT_PARENT_DERIVED | orbital GM remains empirical readout, not definition of source charge |
| NBR3549_5_second_order_GR | first-order source calibration survives PPN beta/gamma order | gamma-1=0 and delta_beta_source=0 after measured-GM normalization | R11 operator vector and nonlinear source stability | DEFERRED_AFTER_FIRST_ORDER | even a future Newton bridge is not full local GR until PPN closes |

## Decisions

| decision_id | question | decision | basis | consequence |
| --- | --- | --- | --- | --- |
| DEC3549_0_zero_status | Did 3549 prove R_PiM+R_Htau=0? | NO | the conditional theorem is clear, but C_M/C_shape/C_curl/C_domain/C_ref/C_frame/C_units are not parent-owned zeros | no Newton/Poisson/local-GR claim |
| DEC3549_1_forward_value | What did 3549 actually add? | DENOMINATOR_BRIDGE_LOCKED | the exact residual square and Newton bridge rungs are now aligned in one gate | next work can attack C_M/C_shape first rather than circling all source coupling at once |
| DEC3549_2_next_route | Which component is best next? | MASS_FLAT_SOURCE_CONNECTION | 3514 explicitly says derive mass-flat source connection before numeric scoring; C_M/C_shape are the cleanest algebraic blockers | 3550 should target A_X source-branch geometry and Pi_M chainmap mass/shape orthogonality |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3549_0_sources_exist | True | PASS | all cited 3549 source paths exist |
| VAL3549_1_generated_csvs_parse | True | PASS | 9 generated CSV files parse with DictReader |
| VAL3549_2_all_components_covered | True | PASS | C_M, C_shape, C_curl, C_domain, C_ref, C_frame and C_units are all present |
| VAL3549_3_bound_rows_nonclaim | True | PASS | all denominator bound interface rows remain nonclaim |
| VAL3549_4_newton_rungs_nonclaim | True | PASS | Newton/Poisson/PPN rungs remain no-promotion rows |
| VAL3549_5_formalization_workbench_untouched | True | PASS | 3549 generated outputs only inside post-checkpoint-work |

## Next target

Move to `3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md`: derive `partial_M A_X^M=0` and `partial_M A_X^a=0` from parent source-branch geometry, or turn `C_M`/`C_shape` into explicit finite nonclaim rows.

Generated UTC: 2026-06-29T11:17:44.725594+00:00