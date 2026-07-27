# 3821 - Closed-System Stress Virial Cancellation Or Pressure/Binding Bound

## Status

`PASS_NONCLAIM_CLOSED_SYSTEM_STRESS_VIRIAL_MECHANISM_BUILT`

This checkpoint attacks the pressure/binding objection directly. In a closed stationary total source, the integrated spatial stress trace cancels by the stress-virial identity, so the Komar/Tolman active mass reduces to total energy over `c^2`. If the source is open, radiating, nonstationary, or cut by a matter-only domain, the leftover is kept as a finite correction vector.

## Stress Virial Theorem

| theorem_id | status | statement | derivation | zero_condition |
| --- | --- | --- | --- | --- |
| SVT3821_0_total_conservation_input | EXACT_CONDITIONAL_INPUT | Use the total Hilbert stress, not matter-only stress: in a local orthonormal source frame, partial_mu T_total^{mu nu}=0 up to named Ward, boundary, curvature and parent-exchange residuals. | This imports 3817/3776/3792 same-current total-stress ownership. | C_Bianchi_total=0, epsilon_J_Q=0, boundary/domain flux silent |
| SVT3821_1_tensor_virial_identity | EXACT_LOCAL_IDENTITY_WITH_RESIDUALS | For a localized total source, the integrated spatial stress is controlled by the second time derivative of the inertia tensor plus surface and covariant-connection terms. | From partial_mu T_total^{mu j}=0, integrate d/dt int x^i T^{0j}; equivalently d2I^{ij}/dt2=2 int T^{ij} dV plus boundary/covariant terms. | stationary or time-averaged d2I^{ij}/dt2=0 and surface/covariant terms vanish |
| SVT3821_2_trace_cancellation | EXACT_CONDITIONAL_TRACE_ZERO | Taking the trace gives int T_total^{i}{}_{i} dV=0 for a stationary closed total source in the local branch. | Trace SVT3821_1 and impose stationarity, no boundary stress flux, and total-system domain closure. | epsilon_virial=epsilon_surface=epsilon_covariant=epsilon_domain=0 |
| SVT3821_3_pressure_paradox_resolution | MECHANISM_CONSTRUCTED | The isolated 3p/c^2 pressure term is not deleted; it is cancelled or compensated by stabilizing/binding/container/field stresses only when the total system is included. | Sector pressure by itself can be nonzero, but the total spatial stress integral vanishes for the closed stationary composite. | all support classes from the total-system domain are included or bounded |
| SVT3821_4_nonstationary_bound | FINITE_BOUND_FORM | If the source is not exactly stationary, pressure/stress correction is bounded by the virial acceleration, surface flux, covariant-frame and open-domain residuals. | Retain the right-hand side of SVT3821_1 instead of setting it to zero. | not required; finite bound can feed empirical gates |
| SVT3821_5_verdict | DERIVATION_ADVANCE_NOT_FULL_CLAIM | The pressure/binding gap has a real closure mechanism: closed stationary total stress reduces the Tolman source to energy mass; open/nonstationary sources carry finite residuals. | This directly improves 3820's R_stress_virial route. | Newton/local GR still waits on source ledger, Pi_M fixedness, EH/PPN/readout residuals |

## Tolman To Energy-Mass Reduction

| reduction_id | status | formula | meaning | residual_if_unsigned |
| --- | --- | --- | --- | --- |
| TER3821_0_Tolman_density_split | EXACT_CONDITIONAL_SPLIT | M_T = c^-2 int (T00_total + Tii_total) dV + R_GR_boundary | The active mass includes energy density plus spatial stress trace in the local weak stationary convention. | R_Tolman_density |
| TER3821_1_closed_trace_zero | EXACT_CONDITIONAL_ZERO | int Tii_total dV = 0 for stationary closed total source | Pressure/stress terms cancel only after total-system support is included. | R_stress_virial |
| TER3821_2_energy_mass_limit | EXACT_CONDITIONAL_REDUCTION | M_T = c^-2 int T00_total dV + R_boundary + R_nonstationary + R_covariant + R_open_domain | For the closed stationary branch, active source mass equals total energy over c^2. | R_active_mass_total |
| TER3821_3_Newton_source_consequence | CONDITIONAL_NEWTON_SOURCE_SIMPLIFICATION | rho_KT -> rho_energy/c^2 when stress-virial residuals vanish or are below tolerance | 3818's Poisson source can use ordinary source energy density only after this gate, not before. | epsilon_source_total |

## Pressure/Binding Bound Vector

| bound_id | symbol | definition | bound_formula | exit_requirement |
| --- | --- | --- | --- | --- |
| PBV3821_0_virial_acceleration | epsilon_virial_accel | nonstationary inertia-tensor term | abs(0.5*d2I_trace_dt2)/(M_ref*c^2) | zero for stationary or long-time averaged bound source |
| PBV3821_1_surface_stress | epsilon_surface_stress | stress flux through source boundary | abs(surface_int x_i T^{ki} n_k dS)/(M_ref*c^2) | zero if total boundary is closed; otherwise source-backed bound |
| PBV3821_2_covariant_frame | epsilon_covariant_frame | connection/curvature correction to local partial-conservation virial identity | abs(int Gamma*T*x dV)/(M_ref*c^2) | small local-Fermi/weak-field bound or retained GR correction |
| PBV3821_3_open_domain | epsilon_open_domain | missing EM/Poynting/binding/apparatus support outside chosen matter tube | abs(E_tail+stress_tail)/(M_ref*c^2) | zero only for total-system domain; else use 3777 tail classes |
| PBV3821_4_parent_exchange | epsilon_parent_exchange | parent/non-EM exchange current not cancelled inside total stress | abs(int x_i Q_parent^i dV)/(M_ref*c^2) | zero from same-current parent action or bounded epsilon_J_Q |
| PBV3821_5_total | epsilon_pressure_binding_total | total pressure/binding correction after virial theorem | sum_abs(epsilon_virial_accel,epsilon_surface_stress,epsilon_covariant_frame,epsilon_open_domain,epsilon_parent_exchange) | feeds active-mass residual and test ledger |

## Closed Source Classifier

| class_id | source_class | virial_status | required_evidence | result |
| --- | --- | --- | --- | --- |
| CLS3821_0_closed_stationary_lab_body | closed stationary lab source | BEST_CASE_ZERO_ROUTE | mass certificate, rigid/support stress included, no radiative flux, fixed boundary/reference | pressure/stress correction can be theorem-zero or tiny bounded |
| CLS3821_1_bound_orbital_body | planet/star/quasi-static body | QUASI_STATIC_BOUND_ROUTE | hydrostatic/stationary model, surface stresses, binding energy, independent mass model | stress correction may be bounded but orbital GM cannot define mass |
| CLS3821_2_radiating_or_open_EM_system | radiating/open EM or Poynting system | OPEN_DOMAIN_BOUND_ROUTE | Poynting flux, field tail, apparatus/boundary inclusion | pressure/stress cancellation is not automatic; retain flux residual |
| CLS3821_3_galaxy_cosmology | nonlocal galaxy/cosmology source | NOT_A_LOCAL_GR_SOURCE_PROOF | separate empirical modelling and covariance | use as empirical pillar, not proof of local closed-source cancellation |

## Residual Rows

| residual_id | symbol | definition | bound_symbol | current_status |
| --- | --- | --- | --- | --- |
| R3821_0_virial_accel | R_virial_accel | nonstationary virial acceleration residual | epsilon_virial_accel | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |
| R3821_1_surface_stress | R_surface_stress | surface/boundary stress residual | epsilon_surface_stress | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |
| R3821_2_covariant_frame | R_covariant_frame | local-frame/covariant derivative correction | epsilon_covariant_frame | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |
| R3821_3_open_domain | R_open_domain | missing total-system support residual | epsilon_open_domain | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |
| R3821_4_parent_exchange | R_parent_exchange | uncancelled parent exchange residual | epsilon_parent_exchange | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |
| R3821_5_total | R_stress_virial_total | total stress-virial pressure/binding residual | epsilon_pressure_binding_total | ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND |

## Claim Gates

| gate_id | gate_status | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3821_0_sources | PASS_NONCLAIM | false | all source paths and needles present |
| GATE3821_1_virial_identity | PASS_NONCLAIM | false | stress-virial identity derived with residuals |
| GATE3821_2_closed_stationary_zero | PASS_CONDITIONAL_ZERO | false | pressure/stress trace cancels for closed stationary total source |
| GATE3821_3_open_source_bound | PASS_BOUND_SCHEMA | false | open/nonstationary/domain residuals are finite named bounds |
| GATE3821_4_source_ledger | BLOCKED_INPUT_REQUIRED | false | numeric independent source rows still not attached |
| GATE3821_5_Newton_claim | BLOCKED | false | Newton claim still waits on source ledger, Pi_M fixedness and Poisson/PPN gates |
| GATE3821_6_local_GR_claim | BLOCKED | false | local GR claim still waits on source normalization plus local PPN/readout closure |

## Next Target

`3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md`

Target: populate local test-ready source rows using independent evidence status, carry the stress-virial correction vector into R10/WEP/PPN/clock/orbital gates, and keep orbital `GM` as product evidence only.

## Machine Outputs

| status | summary |
| --- | --- |
| PASS_NONCLAIM_CLOSED_SYSTEM_STRESS_VIRIAL_MECHANISM_BUILT | 3821 derives the closed-system stress-virial cancellation route, reduces Tolman active mass to total energy over c^2 conditionally, and emits finite open-source correction bounds. |
