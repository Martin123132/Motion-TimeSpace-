# 3820 - Komar/Tolman Active Mass And Independent Source Ledger

## Status

`PASS_NONCLAIM_KOMAR_TOLMAN_ACTIVE_MASS_AND_SOURCE_LEDGER_BUILT`

This checkpoint advances the local Newton/GR source problem one notch: `M_H_ref` is treated as a stationary active Hamiltonian/Komar/Tolman charge with explicit correction terms, not as `mu_fit/G_ref`. It remains nonclaim because pressure, binding, field, boundary and independent-source rows still need proof or bounds.

## Komar/Tolman Active-Mass Derivation

| derivation_id | status | statement | formula | requires | failure_mode |
| --- | --- | --- | --- | --- | --- |
| KT3820_0_stationary_charge_owner | EXACT_CONDITIONAL_GEOMETRIC_CHARGE | If the observed local branch has a fixed stationary time generator tau and a fixed reference, the active source mass is the Hamiltonian/Noether charge of tau, not an orbital fit parameter. | M_H_ref(W)=c^-2*(H_tau[W,S]-H_ref) | single observed frame, fixed tau, fixed H_ref, fixed W_src and S_link | selector/readout circularity |
| KT3820_1_Komar_surface_to_EH_volume | EXACT_CONDITIONAL_EH_IDENTITY | On an EH branch with stationary tau, the surface charge equals the Tolman/Komar volume integral of total Hilbert stress plus boundary/reference residuals. | M_K=(2/c^2)*int_Sigma (T_ab-0.5*T*g_ab)n^a tau^b dSigma + R_boundary | EH normal form, Bianchi/Ward total stress, stationary tau, controlled boundary | R_EH_owner or R_worldtube_boundary survives |
| KT3820_2_perfect_fluid_active_density | EXACT_CONDITIONAL_MATTER_LIMIT | For a static perfect-fluid sector in the same frame, the active density entering the Tolman mass has pressure weight, schematically rho_active=rho_energy+3p/c^2 before closed-system stress cancellations. | rho_KT = rho_energy + 3*p/c^2 + rho_anisotropic_stress + rho_binding_boundary | matter model, pressure/stress tensor, total-system domain | pressure/binding terms are dropped without proof |
| KT3820_3_closed_system_warning | NO_PRESSURE_ONLY_CLAIM | The pressure term cannot be read as an isolated extra source unless container, binding, field and boundary stresses are included; otherwise the source mass is not a closed-system charge. | M_closed = int(rho_energy + stress_trace/c^2 + binding_boundary_terms)dV | total Hilbert source domain, not sector-only matter labels | Tolman pressure paradox / missing stabilizing stresses |
| KT3820_4_slow_weak_Newton_limit | EXACT_CONDITIONAL_SLOW_LIMIT | For cold, weakly bound, slowly moving closed sources, the active charge reduces to ordinary rest-plus-internal energy over c^2 up to explicit retained corrections. | M_H_ref = M_rest + E_internal/c^2 + E_binding/c^2 + E_field/c^2 + Delta_stress/c^2 + R_boundary + R_nonEH | small v^2/c^2, p/(rho c^2), binding/(Mc^2), field tails, nonEH residuals | Newton mass limit not numerically bounded |
| KT3820_5_Poisson_source_replacement | DERIVED_CONDITIONAL_SOURCE_REFINEMENT | The Poisson source symbol from 3818 is refined to the selected active density; using bare density is allowed only after the correction vector is zeroed or bounded. | nabla^2 Phi = 4*pi*G_ref*(rho_KT + delta_rho_source) | 3818 EH-to-Poisson bridge plus KT3820 source charge | R_active_density and R_pressure_binding remain |
| KT3820_6_verdict | VIABLE_NOT_CLAIMED | The source-mass route is no longer only a placeholder: it has a concrete Komar/Tolman active-charge derivation path, but closure waits on stress/binding cancellation or source-backed bounds. | M_H_ref = M_KT + R_active_density + R_pressure_binding + R_boundary + R_nonEH | 3821 stress-virial or finite-bound pass | no Newton/local-GR claim |

## Pressure And Binding Correction Law

| correction_id | symbol | definition | bound_formula | exit_requirement |
| --- | --- | --- | --- | --- |
| COR3820_0_pressure_trace | epsilon_pressure | pressure/stress-trace correction to active mass | int(3p/c^2 + anisotropic_trace/c^2)dV / M_ref | derive closed-system cancellation or bound p/(rho c^2) |
| COR3820_1_kinetic_internal | epsilon_kin_int | kinetic and internal energy correction | (E_kin+E_internal)/(M_ref*c^2) | source-backed thermodynamic or virial bound |
| COR3820_2_binding | epsilon_binding | binding/stabilizing stress correction | E_binding/(M_ref*c^2) plus stabilizer stress trace | closed total-system stress ledger |
| COR3820_3_field_energy | epsilon_field | EM/Poynting/field energy admitted to total Hilbert source | E_field/(M_ref*c^2) plus tail flux | same-current EM/source domain gate |
| COR3820_4_boundary_reference | epsilon_boundary_ref | boundary, exact improvement, and H_ref subtraction residual | Delta B_tau/(M_ref*c^2) | fixed reference and surface class |
| COR3820_5_nonEH_operator | epsilon_nonEH | non-EH metric operator/source correction | ||DeltaE_res|| source-equivalent norm | EH owner theorem-zero or numeric operator bound |
| COR3820_6_source_total | epsilon_source_total | total active-source correction vector | sum_abs(epsilon_pressure,epsilon_kin_int,epsilon_binding,epsilon_field,epsilon_boundary_ref,epsilon_nonEH) | all correction terms zeroed or bounded in one shared ledger |

## Independent Source Ledger Template

| ledger_id | arena | allowed_source_evidence | forbidden_evidence | source_status |
| --- | --- | --- | --- | --- |
| LED3820_0_lab_source_mass | R10_WEP_lab | weighed source masses, composition/density-volume, calibration certificate, geometry files, uncertainty | force-law fit converted into mass using assumed G | TEMPLATE_ONLY_NO_NUMERIC_SOURCE_ATTACHED |
| LED3820_1_clock_source_body | clock_redshift_Gdot_local | geodetic/geophysical mass model with uncertainty and independent clock potential model | same clock/gravity residual used to define source mass | TEMPLATE_ONLY_NO_NUMERIC_SOURCE_ATTACHED |
| LED3820_2_solar_system_body | orbital_PPN | independent mass model where available, density/radius/composition priors, external G_ref policy | ephemeris mu=GM as the mass denominator for the same Newton claim | PRODUCT_ONLY_UNTIL_INDEPENDENT_MASS_LEDGER_EXISTS |
| LED3820_3_galaxy_baryons | SPARC_ETG_galaxy | photometry, gas mass, stellar M/L priors, distance/inclination uncertainty | rotation curve residual used to set the same baryonic source mass without prior | EMPIRICAL_PILLAR_BUT_NOT_LOCAL_GR_PROOF |
| LED3820_4_EM_field_stress | EM_stress_Poynting | same-current Hilbert stress plus Poynting/domain flux ledger | matter-only labels when field energy has exterior support | CONDITIONAL_FROM_3792_3817_STYLE_GATES |
| LED3820_5_cosmology_density | FLRW_CMB_BAO_SN | density parameters with stated priors and covariance; separate background fit branch | late-time expansion residual used to define the same source density being tested | SEPARATE_ROBUSTNESS_BRANCH_REQUIRED |

## GM Split Test Contract

| split_id | status | formula | test_use | claim_guard |
| --- | --- | --- | --- | --- |
| GST3820_0_product_law | EXACT_TEST_ACCOUNTING | delta_ln_mu = delta_ln_G_ref + delta_ln_M_H_ref + delta_readout + delta_range + delta_PPN + delta_boundary | orbital data constrain the product side unless M_H_ref is independently fixed | no Newton source-normalization claim from product-only data |
| GST3820_1_independent_mass_gate | REQUIRED_FOR_CLAIM | M_H_ref = M_source_independent*(1+epsilon_source_total) | independent source ledger feeds Poisson/Gauss before orbital residual evaluation | valid_for_claim=false until numeric source rows and correction bounds exist |
| GST3820_2_cross_arena_guard | NO_PER_ARENA_TUNING | same epsilon_source_total vector must feed R10, WEP, PPN, clocks, orbital and EM stress | lets MTS win by coherent field-theory accounting, not by refitting each arena | one shared residual vector or no claim |
| GST3820_3_observable_allowed | SAFE_ORBITAL_USAGE | mu_fit/mu_pred - 1 constrains delta_readout+delta_range+delta_PPN+delta_boundary after source ledger | orbital data remain useful but cannot define their own denominator | mark orbital rows product_evidence unless source ledger is independent |

## Finite Residual Rows

| residual_id | symbol | definition | bound_formula | current_status |
| --- | --- | --- | --- | --- |
| R3820_0_Komar_owner | R_Komar_owner | failure of tau-Hamiltonian/Komar charge ownership | |M_H_ref-M_K|/M_ref | MISSING_STATIONARY_TAU_OR_HAMILTONIAN_CHARGE |
| R3820_1_Tolman_density | R_Tolman_density | active-density difference from naive T00/c^2 density | ||rho_KT-rho_T00||/rho_ref | PRESSURE_STRESS_TRACE_NOT_ZEROED |
| R3820_2_stress_virial | R_stress_virial | closed-system stress/binding cancellation residual | |int stress_trace + binding/stabilizer terms|/(M_ref*c^2) | CLOSED_SYSTEM_STRESS_LEDGER_MISSING |
| R3820_3_source_ledger | R_source_ledger | lack of independent non-orbital source mass evidence | Boolean or sigma_M/M_ref | NO_NUMERIC_INDEPENDENT_SOURCE_ROWS |
| R3820_4_mu_split | R_mu_split | unresolved split between G_ref, M_H_ref and observed mu | |delta_ln_mu-delta_ln_G_ref-delta_ln_M_H_ref| | ORBITAL_PRODUCT_ONLY |
| R3820_5_total | R_active_mass_total | total active-mass source-normalization residual | R_Komar_owner+R_Tolman_density+R_stress_virial+R_source_ledger+R_mu_split | NEWTON_LOCAL_GR_SOURCE_NORMALIZATION_BLOCKED |

## Claim Gates

| gate_id | gate_status | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3820_0_sources | PASS_NONCLAIM | false | all source paths and needles present |
| GATE3820_1_Komar_Tolman_derivation | PASS_NONCLAIM | false | active mass route derived conditionally from stationary EH/Hilbert stress |
| GATE3820_2_pressure_binding | BLOCKED_BOUND_REQUIRED | false | pressure, binding, field and boundary terms retained rather than dropped |
| GATE3820_3_independent_source_ledger | BLOCKED_INPUT_REQUIRED | false | ledger schema exists but no numeric independent source rows are attached |
| GATE3820_4_GM_smuggling | PASS_GUARD | false | orbital GM remains product evidence, not source mass evidence |
| GATE3820_5_Newton_claim | BLOCKED | false | Newton claim waits on stress cancellation/bounds and source ledger |
| GATE3820_6_local_GR_claim | BLOCKED | false | local GR claim waits on source normalization plus PPN/readout closure |

## Next Target

`3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md`

Target: prove the closed-system stress/virial cancellation that reduces Komar/Tolman active mass to ordinary source energy over `c^2`, or keep pressure/binding/field/boundary corrections finite and source-ready.

## Machine Outputs

| status | summary |
| --- | --- |
| PASS_NONCLAIM_KOMAR_TOLMAN_ACTIVE_MASS_AND_SOURCE_LEDGER_BUILT | 3820 derives the conditional Komar/Tolman active-mass route, installs pressure/binding correction laws, creates an independent source ledger template, and selects 3821 stress-virial cancellation or finite bound. |
