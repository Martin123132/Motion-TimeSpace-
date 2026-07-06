# 495 PPC4161 - Profile Symmetry Dimension Branch Or Anisotropic Quadrupole Bound

Private checkpoint: `4479`
Marker: `PPC4161_PROFILE_SYMMETRY_DIMENSION_BRANCH_OR_ANISOTROPIC_QUADRUPOLE_BOUND_4479`
Decision: `SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_TEMPORAL_DIPOLE_QUADRUPOLE_BOUNDS_DERIVED_NONCLAIM`
Generated UTC: `2026-07-05T21:07:21+00:00`

## Result

4479 closes the shape-assumption loophole.

The clean local branch is:

```text
no temporal marker kernel
+ Hamiltonian/local worldtube split
+ positive centred support
+ no orientation/nematic/tidal carrier
=> d_eff=3, D_M^i=0, Q_M_TF^ij=0.
```

Then the moment correction is the spatial one:

```text
C_a^M = lambda_M Q_M*(zeta_a + zeta_grad_a ell_rms^2/(6 L_loc^2))/N_a.
```

But none of those shape clauses are free. If temporal support, non-centering, or anisotropy survives, it becomes an explicit residual:

```text
R_shape_abs = abs(R_time)+abs(R_dip)+abs(R_quad).
```

This keeps the local-GR route honest: isotropy is not smuggled in from scalar notation.

## Local Spatial Symmetry Theorem

| theorem_id | clause | formal_statement | derivation | zero_or_bound_result | current_status | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LSS4479_0_spatial_worldtube_branch | local tests use a spatial profile after Hamiltonian/worldtube split | F_M(t,x) -> F_M^Sigma(x) on Sigma_t for static/adiabatic local tests, with time as the evolution parameter rather than a support coordinate | PPN, R10, clock-redshift and orbital local limits are read from fields on local spatial slices after source charges are defined. If no finite temporal marker kernel is retained, the profile moment expansion is spatial. | d_eff=3 and the gradient coefficient is mu2_M/(6 L_loc^2) | CONDITIONAL_LOCAL_SPATIAL_BRANCH | False | False |
| LSS4479_1_temporal_smearing_counterroute | covariant time-smearing is a finite residual, not a free d_eff choice | F_M(tau,x)=K_M(tau) f_M(x) gives eta0 O + eta1 dt O + 1/2 eta2 dt^2 O + ... | If the marker has temporal support, the expansion includes time derivatives. These feed clock, Lorentz, locality, Gdot and orbital phase residuals, so d_eff=4 cannot be used as harmless covariance dressing. | temporal residuals vanish only if eta1_M=eta2_M=0 or tau_M/T_loc is bounded | TEMPORAL_SMEARING_BOUND_REQUIRED | False | False |
| LSS4479_2_centering_theorem | positive compact profiles can be centred exactly | x_M = (int x f_M)/(int f_M) gives D_M^i=int (x-x_M)^i F_M=0 for positive nonzero mu0_M | The dipole term is a coordinate-centre artefact for positive profiles. Choosing the centroid removes it exactly. Signed profiles require an absolute-centre guard or a finite signed dipole row. | D_M^i=0 on positive centred branch; abs(D_M)<=ell_sup mu0_abs for signed fallback | CENTERING_DERIVED_SIGNED_FALLBACK_LIVE | False | False |
| LSS4479_3_isotropy_no_orientation_carrier | isotropy follows only if no orientation/nematic/tidal marker carrier exists | Q_M_TF^{ij}=0 iff the finite marker support has SO(3) little-group symmetry or the parent action has no orientation carrier that can select a tracefree tensor | A scalar support amplitude does not by itself carry a preferred direction. But an anisotropic body, nematic marker, tidal alignment, spin axis or boundary orientation can generate a tracefree second moment. | Q_M_TF=0 on the no-orientation branch; otherwise a quadrupole residual is mandatory | ISOTROPY_PARENT_UNSIGNED_ORIENTATION_COUNTERROUTE_LIVE | False | False |
| LSS4479_4_quadrupole_bound | tracefree quadrupole has a compact-support bound | mu2_M^{ij}=(mu2_M/3)h^{ij}+Q_M_TF^{ij}; \|\|Q_M_TF\|\| <= mu2_abs <= ell_sup^2 mu0_abs on the spatial branch | The tracefree part cannot exceed the absolute second moment. Compact support bounds the absolute second moment by the support radius squared times total absolute profile weight. | abs(R_quad) <= abs(lambda_M)*abs(zeta_Q)*ell_sup^2*mu0_abs/(2 abs(N_a) L_loc^2) | DERIVED_QUADRUPOLE_BOUND | True | False |
| LSS4479_5_dipole_bound | unremoved dipole has a compact-support bound | D_M^i=int y^i F_M and \|\|D_M\|\| <= ell_sup mu0_abs | If profile centering is unavailable or the signed profile has cancellations, the first moment is still bounded by support radius times absolute profile weight. | abs(R_dip) <= abs(lambda_M)*abs(zeta_dip)*ell_sup*mu0_abs/(abs(N_a) L_loc) | DERIVED_DIPOLE_BOUND | True | False |
| LSS4479_6_verdict | local d_eff=3 plus centering/isotropy is conditional, but finite anisotropy is bound-ready | local clean branch requires no temporal smearing, centroid-valid profile and no orientation carrier; otherwise temporal, dipole and quadrupole residual rows are used | 4479 proves the shape assumptions as conditional branches and derives componentwise fallback bounds. Current MTS has not parent-signed no-time-smearing or no-orientation carrier. | no local-GR/R10 claim; anisotropic residual rows staged | SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_ANISOTROPY_BOUNDS_DERIVED | False | False |

## Anisotropy Bound Rows

| bound_id | quantity | residual_formula | zero_condition | needed_inputs | target_arenas | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AB4479_0_temporal_kernel | tau_M, eta1_M, eta2_M | R_time <= abs(lambda_M)*(abs(zeta_t1)*abs(eta1_M)/T_loc + abs(zeta_t2)*abs(eta2_M)/(2 T_loc^2))/abs(N_a) | no finite temporal marker support, or K_M is instantaneous/even with eta1=eta2=0 at local-test order | temporal kernel; tau_M; local timescale T_loc; clock/Lorentz projection | clock;Lorentz;Gdot;orbital_phase | BLOCKED_SOURCE_READY | False |
| AB4479_1_dipole | D_M^i | R_dip <= abs(lambda_M)*abs(zeta_dip)*ell_sup*mu0_abs/(abs(N_a)*L_loc) | positive profile centred at x_M, or signed-profile dipole source proves D_M^i=0 | centering proof; ell_sup; mu0_abs; zeta_dip; N_a; L_loc | PPN_preferred_location;clock_gradient;orbital_anisotropy | BLOCKED_SOURCE_READY | False |
| AB4479_2_quadrupole | Q_M_TF^{ij} | R_quad <= abs(lambda_M)*abs(zeta_Q)*ell_sup^2*mu0_abs/(2*abs(N_a)*L_loc^2) | SO(3)-isotropic support or no orientation/nematic/tidal carrier in parent action | orientation-carrier zero proof or Q_M_TF bound; ell_sup; mu0_abs; zeta_Q; N_a; L_loc | PPN_xi_alpha;clock_anisotropy;orbital_precession | BLOCKED_SOURCE_READY | False |
| AB4479_3_dimension_branch | d_eff | d_eff=3 gives mu2/(6 L_loc^2); d_eff=4 gives mu2/(8 L_loc^2) plus temporal residual R_time | Hamiltonian local spatial branch with no time-smearing marker | support branch; temporal kernel absence; local-test slicing convention | R10;PPN;clock;orbital | BLOCKED_SOURCE_READY | False |
| AB4479_4_component_envelope | R_shape_abs | R_shape_abs = abs(R_time)+abs(R_dip)+abs(R_quad) | R_time=R_dip=R_quad=0 individually | all temporal, dipole and quadrupole values or separate zero certificates | claim_gate_guard | BLOCKED_SOURCE_READY | False |

## Shape Branch Input Rows

| row_id | quantity | definition | formula_or_test | needed_inputs | current_value | units | target | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SBI4479_0_spatial_branch_certificate | Z_spatial | certificate that local marker support is spatial on Sigma_t and not temporally smeared | Z_spatial=True iff d_eff=3 branch signs and temporal kernel residuals vanish | Hamiltonian/worldtube split; no temporal marker kernel; local-test readout convention | MISSING_SPATIAL_BRANCH_CERTIFICATE | boolean_certificate | d_eff=3;R_time=0 | BLOCKED_SOURCE_READY | False |
| SBI4479_1_tau_M | tau_M | temporal support width if covariant time-smearing survives | tau_M^2=eta2_abs/eta0_abs or declared temporal kernel width | K_M(tau); eta0_abs; eta2_abs; local clock/orbital timescale | MISSING_TEMPORAL_SUPPORT_WIDTH | s | clock;Lorentz;orbital_phase | BLOCKED_SOURCE_READY | False |
| SBI4479_2_centering_certificate | Z_center | certificate that the marker dipole vanishes | Z_center=True iff profile is positive and centred, or signed dipole D_M^i is independently zero | profile sign branch; centroid definition; D_M^i value or proof | MISSING_CENTERING_CERTIFICATE | boolean_certificate | D_M^i=0;R_dip=0 | BLOCKED_SOURCE_READY | False |
| SBI4479_3_orientation_carrier | Z_orientation | certificate that no orientation/nematic/tidal marker carrier exists | Z_orientation=True iff parent action/support has no vector, spin-axis, tidal, boundary-normal or nematic carrier that can source Q_M_TF | parent support alphabet; body/orientation averaging; boundary orientation routing | MISSING_ORIENTATION_CARRIER_ZERO_CERTIFICATE | boolean_certificate | Q_M_TF=0;R_quad=0 | BLOCKED_SOURCE_READY | False |
| SBI4479_4_D_M_bound | D_M_abs | absolute dipole bound | D_M_abs <= ell_sup mu0_abs | ell_sup; mu0_abs; signed-profile guard | MISSING_DIPOLE_BOUND_INPUTS | m_times_profile_units | R_dip | BLOCKED_SOURCE_READY | False |
| SBI4479_5_Q_TF_bound | Q_M_TF_abs | absolute tracefree quadrupole bound | \|\|Q_M_TF\|\| <= mu2_abs <= ell_sup^2 mu0_abs | ell_sup; mu0_abs; tensor norm convention | MISSING_QUADRUPOLE_BOUND_INPUTS | m^2_times_profile_units | R_quad | BLOCKED_SOURCE_READY | False |

## Decision Ledger

| decision_id | finding | consequence | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC4479_0_spatial_branch | d_eff=3 is justified only on the Hamiltonian local spatial branch with no temporal marker kernel | time-smearing is retained as an explicit clock/Lorentz/orbital residual | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | False |
| DEC4479_1_symmetry_branch | centering and isotropy are derived as branch conditions, not assumed | dipole and tracefree quadrupole residuals are bounded if centering/isotropy do not sign | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | False |
| DEC4479_2_next_target | the next sharp target is the orientation-carrier zero proof; if that fails, score the quadrupole residual | attack Z_orientation before trying numeric local scoring | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | False |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | detail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4479_0_sources | all cited local sources exist and needles are found | True | False | source register validates 4478 dimension/symmetry handoff | False |
| CG4479_1_spatial_symmetry_theorem_written | local d_eff/centering/isotropy branch theorem is explicit | True | False | spatial branch, time-smearing counterroute, centering, isotropy and bounds are written | False |
| CG4479_2_clean_branch_parent_signed | MTS parent signs d_eff=3, centering and isotropy | False | False | no-time-smearing and no-orientation carrier remain unsigned | False |
| CG4479_3_anisotropy_bounds_written | temporal, dipole and quadrupole bounds are written | True | False | fallback residual bounds are componentwise and no-cancellation | False |
| CG4479_4_bound_inputs_ready | anisotropy bound inputs are numeric/source ready | False | False | input rows still need spatial branch, temporal width, centering, orientation, dipole and quadrupole values | False |
| CG4479_5_no_generated_claim_rows | no generated row is promoted to public/local-GR evidence | True | False | 4479 is a branch theorem plus anisotropy bound pack | False |

## Status

| checkpoint | marker | claim_id | decision | spatial_symmetry_branch | anisotropy_bounds | sharpest_open_clause | shape_input_status | public_local_GR_claim | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4479 | PPC4161_PROFILE_SYMMETRY_DIMENSION_BRANCH_OR_ANISOTROPIC_QUADRUPOLE_BOUND_4479 | L-321 | SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_TEMPORAL_DIPOLE_QUADRUPOLE_BOUNDS_DERIVED_NONCLAIM | written_parent_unsigned | derived | orientation_carrier_zero_or_quadrupole_residual_scorer | staged_missing_values | False | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | False | 2026-07-05T21:07:21+00:00 |

## Next Target

| next_id | target | objective | derive_first | fallback | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4479_0 | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | Prove no orientation/nematic/tidal carrier can source Q_M_TF, or build the quadrupole residual scorer. | show the parent support alphabet has no vector, spin-axis, tidal, boundary-normal or nematic carrier | score Q_M_TF through R_quad into PPN, clock anisotropy and orbital precession gates | assuming isotropy from scalar notation while an orientation carrier survives | False |

## Source Register

| checkpoint | source_id | source_kind | source_ref | local_path_exists | needle | needle_found | line_number | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4479 | SRC4479_00_next4478 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_NEXT_TARGET.csv | True | 4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md | True | 2 | 4478 selected profile symmetry/dimension branch or anisotropic quadrupole bound. | False |
| 4479 | SRC4479_01_formal494_deff | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\494-PPC4161-marker-profile-support-zero-certificate-or-first-moment-input-row.md | True | The local support branch is conditionally `d_eff=3` | True | 39 | formal 4478 local d_eff branch. | False |
| 4479 | SRC4479_02_formal494_quadrupole | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\494-PPC4161-marker-profile-support-zero-certificate-or-first-moment-input-row.md | True | Q_M_TF^{ij} | True | 39 | formal 4478 anisotropic quadrupole row. | False |
| 4479 | SRC4479_03_support4478_verdict | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_SUPPORT_ZERO_CERTIFICATE.csv | True | SZC4478_5_verdict | True | 7 | 4478 support zero verdict. | False |
| 4479 | SRC4479_04_laws4478_deff | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_LAWS.csv | True | MIL4478_2_support_dimension_branch | True | 4 | 4478 local spatial support dimension law. | False |
| 4479 | SRC4479_05_laws4478_centering | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_LAWS.csv | True | MIL4478_4_centering_choice | True | 6 | 4478 centering/dipole law. | False |
| 4479 | SRC4479_06_laws4478_quadrupole | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_LAWS.csv | True | MIL4478_5_isotropy_or_quadrupole | True | 7 | 4478 isotropy/quadrupole law. | False |
| 4479 | SRC4479_07_inputs4478_deff | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_ROWS.csv | True | FMI4478_2_d_eff | True | 4 | 4478 d_eff input row. | False |
| 4479 | SRC4479_08_inputs4478_dipole | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_ROWS.csv | True | FMI4478_5_dipole_or_centering | True | 7 | 4478 dipole input row. | False |
| 4479 | SRC4479_09_inputs4478_quad | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_ROWS.csv | True | FMI4478_6_quadrupole_TF | True | 8 | 4478 quadrupole input row. | False |
| 4479 | SRC4479_10_gates4478_support | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4478_CLAIM_GATES.csv | True | CG4478_2_support_zero_parent_signed | True | 4 | 4478 gate blocking support-zero overclaim. | False |
| 4479 | SRC4479_11_gate | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\profile_symmetry_dimension_gate.py | True | def local_spatial_symmetry_rows | True | 25 | 4479 profile symmetry/dimension gate. | False |
| 4479 | SRC4479_12_generator | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_4479_profile_symmetry_dimension_branch_or_anisotropic_quadrupole_bound.py | True | CHECKPOINT = "4479" | True | 30 | 4479 generator script. | False |

## Decision Row

| checkpoint | marker | claim_id | decision | proof_result | fallback_result | claim_status | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4479 | PPC4161_PROFILE_SYMMETRY_DIMENSION_BRANCH_OR_ANISOTROPIC_QUADRUPOLE_BOUND_4479 | L-321 | SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_TEMPORAL_DIPOLE_QUADRUPOLE_BOUNDS_DERIVED_NONCLAIM | conditional d_eff=3, centering and isotropy branch written but not parent-signed | temporal-smearing, dipole and tracefree quadrupole residual bounds derived and staged | private_nonclaim | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | False | 2026-07-05T21:07:21+00:00 |
