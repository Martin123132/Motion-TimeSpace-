# 3985 — Source-Charge Ownership Subfactor Closure Or Newtonian GM Bound Runner

Timestamp: `2026-07-01T17:28:00+00:00`

## Result

This checkpoint did not circle the same missing coupling. It split the source-coupling blocker and closed the safest branch-specific pieces.

Closed for the controlled stationary EH/no-extra-hair monopole readout:

- `epsilon_tau_generator_mismatch=0`
- `epsilon_flux_EH_annulus=0`
- `epsilon_boundary_reference_shift=0` for the same-reference comparator
- `epsilon_Gauss_shape_error=0`, meaning the inverse-square Newtonian shape follows from the one-charge EH slow limit

## Reduced Residual

The 3984 residual

`epsilon_closed_source_failure`

is reduced, for this controlled branch, to

`epsilon_closed_source_failure_3985 <= |delta_M_source_Hilbert|/|M_ref| + epsilon_PiM_projector_ownership + epsilon_extra_mass_channel + epsilon_GM_amplitude_calibration + epsilon_PPN_source_stability`.

The important move is that Newtonian *shape* is now derived from the geometry, while Newtonian *amplitude* remains a source-coupling problem:

`epsilon_GM_amplitude_calibration = |mu - G_ref M_source|/|G_ref M_ref|`.

This is the correct discipline: GR itself does not derive the measured numerical value of `G`; what a local-GR recovery branch must prove is that the coupling is universal and that the same dressed source charge owns `mu`.

## Nonclaim Guard

Local GR/Newton/PPN is still not claimed. The live blockers are:

- parent `Pi_M/Hilbert` equality;
- source amplitude `mu=G_ref M_source`;
- extra monopole mass/source channels;
- PPN source stability.

## Runner

`P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_SMOKE_RESULTS.csv` now computes the reduced source residual when numeric parent rows exist and blocks when they do not.

## Source Register

- `SRC3985_00_3984_next`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_NEXT_TARGET.csv` needle `NEXT3984_0` found=True
- `SRC3985_01_3984_certificate_tau`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv` needle `CWO3984_0_same_tau` found=True
- `SRC3985_02_3984_certificate_flux`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv` needle `CWO3984_3_flux_closure` found=True
- `SRC3985_03_3984_certificate_gauss`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv` needle `CWO3984_6_gauss_calibration` found=True
- `SRC3985_04_3984_residual_master`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_SOURCE_CHARGE_RESIDUAL_ROWS.csv` needle `SCR3984_0_master` found=True
- `SRC3985_05_3984_projector`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_PROJECTOR_RESULTS.csv` needle `REAL3984_0_controlled_EH_monopole_l2m0_source_residualized` found=True
- `SRC3985_06_3984_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3984_WORLDTUBE_OWNERSHIP_THEOREM_ATTEMPT.csv` needle `CWO3984_0_EH_reference_derivation` found=True
- `SRC3985_07_3969_unique`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv` needle `UQ3969_1_conditional_uniqueness_theorem` found=True
- `SRC3985_08_3969_square`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv` needle `UQ3969_2_square_law_corollary` found=True
- `SRC3985_09_worldtube_EH`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv` needle `T510_0_EH_reference_glue` found=True
- `SRC3985_10_worldtube_source`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv` needle `T510_1_worldtube_source_measure` found=True
- `SRC3985_11_worldtube_transfer`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv` needle `T510_2_MTS_transfer_condition` found=True
- `SRC3985_12_worldtube_newton`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv` needle `T510_3_Newton_PPN_readout` found=True
- `SRC3985_13_tau_clause`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv` needle `SM509_0_observed_generator` found=True
- `SRC3985_14_flux_clause`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv` needle `SM509_3_flux_closure` found=True
- `SRC3985_15_gauss_clause`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv` needle `SM509_6_Gauss_orbital_calibration` found=True
- `SRC3985_16_ppn_clause`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv` needle `SM509_7_second_order_PPN_stability` found=True
- `SRC3985_17_flux_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv` needle `T509_1_flux_closure` found=True
- `SRC3985_18_no_extra_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv` needle `T509_2_no_extra_mass_channel` found=True
- `SRC3985_19_HC1_tau`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` needle `HC1_observed_time_generator` found=True
- `SRC3985_20_HC2_boundary`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` needle `HC2_differentiable_integrable_Hxi` found=True
- `SRC3985_21_HC4_charge`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` needle `HC4_charge_equals_PiM_Hilbert_mass` found=True
- `SRC3985_22_HC8_gauss`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` needle `HC8_Poisson_Gauss_orbital_calibration` found=True
- `SRC3985_23_TC500_hilbert`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv` needle `TC500_3_Hilbert_equality` found=True
- `SRC3985_24_TC500_cal`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv` needle `TC500_7_calibration` found=True

## Next Target

`3986-Y5-R2FR-parent-PiM-Hilbert-equality-or-GM-source-amplitude-bound.md`

Either prove parent `Pi_M J_H` equals the EH/Hamiltonian mass charge, or build the first real source-backed `GM` amplitude bound row.
