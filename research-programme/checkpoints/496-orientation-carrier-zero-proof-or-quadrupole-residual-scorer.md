# 496 PPC4161 - Orientation Carrier Zero Proof Or Quadrupole Residual Scorer

Private checkpoint: `4480`
Marker: `PPC4161_ORIENTATION_CARRIER_ZERO_PROOF_OR_QUADRUPOLE_SCORER_4480`
Decision: `ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_DERIVED_NONCLAIM`
Generated UTC: `2026-07-05T21:16:01+00:00`

## Result

4480 takes the leap that 4479 set up.

The clean zero route is now an actual representation-theory statement:

```text
F_M is a true local SO(3)-scalar profile
=> M^{ij}=int y^i y^j F_M d^3y = (mu2_M/3) h^{ij}
=> Q_M_TF^{ij}=0.
```

So the local isotropic branch is not magic. It is valid if the parent action really has no surviving orientation carrier.

The important catch is also now explicit:

```text
wave vector / Poynting flux / spin axis / tidal tensor / nematic director / boundary normal
```

are exactly the things that can source the tracefree `l=2` carrier. That means the user's Poynting-vector instinct is not a distraction; it is a live fork in the derivation.

If any such carrier survives, the branch is still not handwavy. It becomes:

```text
Q_M_TF^{ij}=epsilon_Q * mu0_abs * ell_sup^2 * A_STF^{ij},
0 <= epsilon_Q <= 1,
R_quad_a = lambda_M*zeta_Q_a*Q_M_TF^{ij}*H_a,ij^TF/(2*N_a).
```

With the compact-support envelope:

```text
|R_quad_a| <= |lambda_M| |zeta_Q_a| mu0_abs ell_sup^2 /(2 |N_a| L_loc^2).
```

That is forward motion: either sign the carrier absence, or score the quadrupole residual honestly.

## Orientation Zero Proof

| proof_id | clause | formal_statement | derivation | zero_result | current_status | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OCZ4480_0_SO3_scalar_profile_theorem | a true local scalar marker profile has no tracefree second moment | If F_M(y) is invariant under the local SO(3) little group of h_ij, then M^{ij}=int y^i y^j F_M d^3y commutes with every rotation and therefore M^{ij}=(mu2_M/3)h^{ij}. | The second moment tensor is a symmetric rank-2 representation. The only SO(3)-invariant symmetric rank-2 tensor is the spatial metric h^{ij}; equivalently the l=2 irreducible part is projected out. Hence Q_M_TF^{ij}=M^{ij}-(mu2_M/3)h^{ij}=0. | Z_orientation=True implies Q_M_TF^{ij}=0 and R_quad=0 on the spatial branch | DERIVED_REPRESENTATION_THEOREM_CONDITIONAL_ON_SO3_SCALAR_PARENT | False | False |
| OCZ4480_1_STF_carrier_inventory | a nonzero tracefree quadrupole needs a rank-2 STF carrier | Q_M_TF^{ij} can be sourced only by an available STF object: n^{<i}n^{j>}, s^{<i}s^{j>}, k^{<i}k^{j>}, E^{ij}_TF, B^{ij}_TF, N^{ij}, boundary-normal b^{<i}b^{j>}, anisotropic support metric, or an equivalent orientation distribution. | The l=2 part cannot be manufactured from scalars alone. Products of one vector/director, spin axis, wave vector, Poynting/flux direction, tidal tensor, nematic tensor, or boundary normal supply the needed SO(3) representation. | if the parent support alphabet contains no such carrier and no anisotropic boundary routing, Q_M_TF^{ij}=0 | CARRIER_ALPHABET_TEST_WRITTEN_PARENT_UNSIGNED | False | False |
| OCZ4480_2_orientation_averaging_theorem | random or gauge orientation kills the STF branch only with a signed average | If orientation variables A are integrated with an isotropic measure dmu(A) independent of local source response, then int A^{ij}_STF dmu(A)=0. | The isotropic group average annihilates every l=2 component. This is a real zero proof only if the parent measure is isotropic before variation and no boundary, material or readout term reselects an axis. | orientation averaging can sign Z_orientation only when the measure and response are parent-owned | AVERAGING_ZERO_THEOREM_CONDITIONAL_PARENT_MEASURE_UNSIGNED | False | False |
| OCZ4480_3_wave_and_Poynting_counterroute | waves, flux and the Poynting vector are live orientation carriers unless excluded | A finite background flux S^i, wave vector k^i, polarization tensor e^{ij}, or EM/gravitational radiation stress can generate S^{<i}S^{j>}, k^{<i}k^{j>} or e^{ij}_TF in the marker profile. | This route directly addresses the possible 'background field / Poynting vector' intuition: it is not automatically wrong. It is exactly an orientation-carrier branch, and therefore either a parent mechanism or a residual scorer is required. | do not set Q_M_TF=0 while wave/flux carriers remain in the parent alphabet | COUNTERROUTE_KEPT_LIVE_FOR_EM_WAVE_BACKGROUND | False | False |
| OCZ4480_4_boundary_normal_counterroute | local boundary or worldtube normals can reintroduce anisotropy | Even if the bulk scalar profile is SO(3)-silent, boundary terms can source Q_M_TF^{ij} through b^{<i}b^{j>} unless the boundary support is fixed, topological, no-flux, or Hamiltonian-routed. | The support-zero branch already separated boundary support. 4480 carries that discipline into the l=2 channel: boundary orientation is a separate carrier, not a harmless surface detail. | bulk isotropy is insufficient without boundary-orientation routing | BOUNDARY_ORIENTATION_FIREWALL_UNSIGNED | False | False |
| OCZ4480_5_verdict | orientation zero theorem exists but is not parent-signed | Z_orientation=True iff the parent marker/support alphabet has no STF carrier, no surviving anisotropic orientation distribution, and no boundary-normal or wave/flux counterroute. | 4480 proves the representation-theory zero route and writes the carrier inventory test. Current MTS has not yet signed the full parent carrier alphabet, so the finite quadrupole scorer remains live. | no local-GR/R10/PPN claim; use quadrupole residual scorer until Z_orientation signs | ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_REQUIRED | False | False |

## Quadrupole Residual Scorer

| scorer_id | quantity | formula | derivation | target_arenas | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QRS4480_0_canonical_STF_amplitude | Q_M_TF^{ij} | Q_M_TF^{ij}=epsilon_Q * mu0_abs * ell_sup^2 * A_STF^{ij}, with \|\|A_STF\|\|=1 and 0<=epsilon_Q<=1 | Any finite tracefree second moment can be written as an amplitude times a unit STF tensor. Compact support gives epsilon_Q<=1 because \|\|Q_M_TF\|\|<=mu2_abs<=ell_sup^2 mu0_abs. | all_l2_local_residuals | DERIVED_CANONICAL_QUADRUPOLE_PARAMETERIZATION | False |
| QRS4480_1_local_projection_bound | R_quad_a | R_quad_a = lambda_M*zeta_Q_a*Q_M_TF^{ij}*H_a,ij^TF/(2*N_a); \|R_quad_a\| <= \|lambda_M\| \|zeta_Q_a\| mu0_abs ell_sup^2 /(2 \|N_a\| L_loc^2) | Normalize the tracefree Hessian response by \|\|H_a^TF\|\|<=1/L_loc^2 and apply the compact-support STF bound. No cancellation across arenas is allowed. | PPN;clock;orbital;R10_shape_guard | DERIVED_COMPONENTWISE_LOCAL_BOUND | False |
| QRS4480_2_PPN_anisotropy_gate | R_PPN_Q | R_PPN_Q = Pi_PPN_Q[R_quad_a] with \|R_PPN_Q\| <= tau_PPN_Q required | A pure l=2 residual can vanish in a spherical monopole average but still enter preferred-location, anisotropic metric, or non-spherical light/clock readouts. The PPN gate must therefore use an l=2 projector, not a scalar gamma average. | PPN_xi;preferred_location;anisotropic_metric | SCORER_CONTRACT_WRITTEN_NEEDS_BOUND_INPUT | False |
| QRS4480_3_Shapiro_LOS_kernel | R_Shapiro_Q | Delta_Q = A_Q*C_Q*Pi_quad_LOS[W], with \|Pi_quad_LOS\|<=1 for positive radial W | Imported from the prior anisotropic Shapiro kernel: spherical orthogonality does not imply line-of-sight invisibility. The safe envelope is the worst-case LOS kernel unless a source geometry is supplied. | Shapiro;light_bending;Cassini_style_anisotropic_smoke | KERNEL_IMPORTED_NONCLAIM_NEEDS_TAU_SHAPIRO_Q | False |
| QRS4480_4_clock_quadrupole_gate | R_clock_Q | R_clock_Q = Pi_clock_Q[R_quad_a] and must satisfy \|R_clock_Q\|<=tau_clock_Q | Clock comparisons read potential/redshift differences along actual baseline geometry, so an l=2 field survives whenever the two clock locations sample different STF projections. | clock_redshift;clock_anisotropy;Lorentz_locality | SCORER_CONTRACT_WRITTEN_NEEDS_CLOCK_GEOMETRY_BOUND | False |
| QRS4480_5_orbital_quadrupole_gate | R_orbital_Q | R_orbital_Q = Pi_orb_Q[R_quad_a] and must satisfy \|R_orbital_Q\|<=tau_orbital_Q | A tracefree local potential shifts precession/nodal/phase observables through the orbit's orientation relative to A_STF. It is scoreable only after a source-domain transfer or direct local source geometry is declared. | orbital_precession;ephemerides;binary_orbits | SCORER_CONTRACT_WRITTEN_NEEDS_ORBITAL_TRANSFER | False |
| QRS4480_6_no_cancellation_envelope | R_Q_abs | R_Q_abs=max(\|R_PPN_Q\|/tau_PPN_Q, \|R_clock_Q\|/tau_clock_Q, \|R_orbital_Q\|/tau_orbital_Q, \|R_Shapiro_Q\|/tau_Shapiro_Q) when numeric bounds exist | The branch passes only if every relevant l=2 observable is below its own bound. A scalar pass cannot hide an anisotropic failure. | claim_gate_guard | NO_CANCELLATION_QUADRUPOLE_ENVELOPE_WRITTEN | False |

## Quadrupole Input Rows

| row_id | quantity | definition | formula_or_test | needed_inputs | current_value | units | target | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QRI4480_0_Z_orientation | Z_orientation | certificate that the parent support alphabet has no l=2 orientation carrier | True iff no vector/director/spin/wave/Poynting/tidal/nematic/boundary-normal carrier survives before variation | parent carrier alphabet; support variables; boundary routing; wave/EM flux treatment | MISSING_PARENT_ORIENTATION_ZERO_CERTIFICATE | boolean_certificate | Q_M_TF=0;R_quad=0 | BLOCKED_SOURCE_READY | False |
| QRI4480_1_carrier_inventory | I_STF | explicit list of possible rank-2 STF carrier sources | I_STF={n_i n_j, s_i s_j, k_i k_j, S_i S_j, E_ij^TF, B_ij^TF, N_ij, b_i b_j, anisotropic_support_metric}_TF intersect S_parent | parent action/support alphabet and all integrated-out/background fields | MISSING_STF_CARRIER_INVENTORY | set | orientation_zero_or_finite_branch | BLOCKED_SOURCE_READY | False |
| QRI4480_2_epsilon_Q | epsilon_Q | dimensionless tracefree quadrupole support fraction | epsilon_Q=\|\|Q_M_TF\|\|/(mu0_abs ell_sup^2), bounded 0<=epsilon_Q<=1 | Q_M_TF norm or carrier amplitude; mu0_abs; ell_sup | MISSING_QUADRUPOLE_FRACTION | dimensionless | finite_quadrupole_scorer | BLOCKED_SOURCE_READY | False |
| QRI4480_3_A_STF | A_STF^{ij} | unit orientation tensor for the finite quadrupole branch | A_STF^{ij}=Q_M_TF^{ij}/\|\|Q_M_TF\|\| when Q_M_TF is nonzero | orientation axis/tensor; norm convention; source frame | MISSING_UNIT_STF_ORIENTATION | dimensionless_tensor | PPN;clock;orbital;Shapiro kernels | BLOCKED_SOURCE_READY | False |
| QRI4480_4_tau_PPN_Q | tau_PPN_Q | empirical bound for anisotropic local metric/PPN l=2 residual | require \|R_PPN_Q\|<=tau_PPN_Q in a declared convention | PPN anisotropy bound source; convention map; projection Pi_PPN_Q | MISSING_PPN_QUADRUPOLE_BOUND | dimensionless | PPN_xi;preferred_location | BLOCKED_SOURCE_READY | False |
| QRI4480_5_tau_clock_Q | tau_clock_Q | empirical bound for clock/redshift anisotropic quadrupole residual | require \|R_clock_Q\|<=tau_clock_Q | clock geometry; redshift convention; projection Pi_clock_Q | MISSING_CLOCK_QUADRUPOLE_BOUND | dimensionless | clock_redshift;clock_anisotropy | BLOCKED_SOURCE_READY | False |
| QRI4480_6_tau_orbital_Q | tau_orbital_Q | empirical orbital/ephemeris bound for source quadrupole residual | require \|R_orbital_Q\|<=tau_orbital_Q | orbital data bound; source-domain transfer; projection Pi_orb_Q | MISSING_ORBITAL_QUADRUPOLE_BOUND | declared_by_arena | orbital_precession;ephemerides | BLOCKED_SOURCE_READY | False |
| QRI4480_7_tau_Shapiro_Q | tau_Shapiro_Q | empirical line-of-sight Shapiro/light-bending anisotropic quadrupole bound | require \|A_Q*C_Q*Pi_quad_LOS\|<=tau_Shapiro_Q | anisotropic Shapiro or light-bending source; LOS geometry; source-domain transfer | MISSING_SHAPIRO_QUADRUPOLE_BOUND | declared_by_arena | Shapiro;light_bending | BLOCKED_SOURCE_READY | False |

## Decision Ledger

| decision_id | finding | consequence | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC4480_0_zero_route | a genuine SO(3)-scalar marker profile has Q_M_TF^{ij}=0 by representation theory | the clean local branch is mathematically real if the parent carrier alphabet is signed | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | False |
| DEC4480_1_counterroute | wave vectors, Poynting/flux directions, spin axes, tidal tensors and boundary normals are exactly the objects that can revive Q_M_TF | MTS should not ignore EM/wave-background intuitions; they become explicit carrier rows | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | False |
| DEC4480_2_scorer_route | if any l=2 carrier survives, the quadrupole branch is scoreable with a compact-support no-cancellation envelope | the next target should source or bound the carrier inventory and empirical l=2 arena tolerances | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | False |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | detail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4480_0_sources | all cited local sources exist and needles are found | True | False | source register validates 4479 handoff plus prior quadrupole/orientation clues | False |
| CG4480_1_orientation_zero_theorem_written | SO(3) scalar marker implies Q_M_TF=0 | True | False | representation theorem is written as a conditional branch | False |
| CG4480_2_orientation_zero_parent_signed | MTS parent signs absence of all l=2 orientation carriers | False | False | carrier alphabet, wave/Poynting route and boundary orientation remain unsigned | False |
| CG4480_3_quadrupole_scorer_written | finite quadrupole branch has scorer formulas | True | False | canonical amplitude, local bound, Shapiro/clock/orbital/PPN contracts and no-cancellation envelope are written | False |
| CG4480_4_bound_inputs_ready | quadrupole scorer has numeric/source-ready arena inputs | False | False | epsilon_Q, A_STF, carrier inventory and empirical l=2 bounds remain missing | False |
| CG4480_5_no_generated_claim_rows | no generated row is promoted to local-GR evidence | True | False | 4480 is a conditional zero theorem plus finite quadrupole scoring contract | False |

## Status

| checkpoint | marker | claim_id | decision | orientation_zero_theorem | wave_Poynting_route | quadrupole_scorer | sharpest_open_clause | public_local_GR_claim | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4480 | PPC4161_ORIENTATION_CARRIER_ZERO_PROOF_OR_QUADRUPOLE_SCORER_4480 | L-322 | ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_DERIVED_NONCLAIM | derived_parent_unsigned | kept_as_explicit_STF_carrier_counterroute | derived_contract_nonclaim | parent_STF_carrier_inventory_and_l2_arena_bounds | False | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | False | 2026-07-05T21:16:01+00:00 |

## Next Target

| next_id | target | objective | derive_first | fallback | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4480_0 | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | Source the parent STF carrier inventory and l=2 empirical bound inputs, or sign Z_orientation from the parent action. | enumerate whether vectors, spin axes, wave/Poynting fluxes, tidal tensors, nematic directors, anisotropic support metrics, or boundary normals survive in the parent marker/support alphabet | fill epsilon_Q, A_STF, tau_PPN_Q, tau_clock_Q, tau_orbital_Q and tau_Shapiro_Q as nonclaim bound rows | using scalar monopole tests to hide an l=2 anisotropic residual | False |

## Source Register

| checkpoint | source_id | source_kind | source_ref | local_path_exists | needle | needle_found | line_number | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4480 | SRC4480_00_next4479 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4479_NEXT_TARGET.csv | True | 4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md | True | 2 | 4479 selected orientation-carrier zero proof or quadrupole scorer. | False |
| 4480 | SRC4480_01_formal495_result | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\495-PPC4161-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md | True | no orientation/nematic/tidal carrier | True | 18 | formal 4479 shape branch requiring orientation-carrier closure. | False |
| 4480 | SRC4480_02_theorem4479_orientation | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4479_LOCAL_SPATIAL_SYMMETRY_THEOREM.csv | True | LSS4479_3_isotropy_no_orientation_carrier | True | 5 | 4479 row that makes isotropy conditional on no orientation carrier. | False |
| 4480 | SRC4480_03_bounds4479_quadrupole | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4479_ANISOTROPY_BOUND_ROWS.csv | True | AB4479_2_quadrupole | True | 4 | 4479 quadrupole residual bound handoff. | False |
| 4480 | SRC4480_04_inputs4479_orientation | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4479_SHAPE_BRANCH_INPUT_ROWS.csv | True | SBI4479_3_orientation_carrier | True | 5 | 4479 missing orientation-carrier certificate. | False |
| 4480 | SRC4480_05_gates4479_parent_unsigned | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4479_CLAIM_GATES.csv | True | CG4479_2_clean_branch_parent_signed | True | 4 | 4479 gate that blocks the clean branch. | False |
| 4480 | SRC4480_06_shapiro3168_kernel | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3168-Y5-R2FR-anisotropic-Shapiro-quadrupole-kernel-or-source-transfer-contract-under-AX1090.md | True | \|Pi_quad_LOS\| <= 1 | True | 67 | prior anisotropic Shapiro line-of-sight quadrupole kernel. | False |
| 4480 | SRC4480_07_metric3182_slip | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md | True | Psi - Phi = 2 Sigma_H phi_ext | True | 78 | prior tracefree Hessian carrier enters weak-field metric readout. | False |
| 4480 | SRC4480_08_boundary867_orientation | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md | True | boundary orientation sign | True | 39 | prior boundary orientation warning. | False |
| 4480 | SRC4480_09_trace161_quadrupole | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\161-trace-quadrupole-source-law-attempt.md | True | quadrupole law: plausible rough clue | True | 178 | prior trace/quadrupole source-law clue, kept nonclaim. | False |
| 4480 | SRC4480_10_gate | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\orientation_carrier_quadrupole_gate.py | True | def orientation_zero_proof_rows | True | 25 | 4480 orientation carrier and quadrupole scorer gate. | False |
| 4480 | SRC4480_11_generator | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_4480_orientation_carrier_zero_proof_or_quadrupole_residual_scorer.py | True | CHECKPOINT = "4480" | True | 30 | 4480 generator script. | False |

## Decision Row

| checkpoint | marker | claim_id | decision | proof_result | fallback_result | claim_status | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4480 | PPC4161_ORIENTATION_CARRIER_ZERO_PROOF_OR_QUADRUPOLE_SCORER_4480 | L-322 | ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_DERIVED_NONCLAIM | SO(3) scalar marker gives Q_M_TF=0 by representation theory, but parent carrier alphabet is unsigned | finite l=2 quadrupole branch now has canonical amplitude, compact-support bound and PPN/clock/orbital/Shapiro scorer contracts | private_nonclaim | 4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md | False | 2026-07-05T21:16:01+00:00 |
