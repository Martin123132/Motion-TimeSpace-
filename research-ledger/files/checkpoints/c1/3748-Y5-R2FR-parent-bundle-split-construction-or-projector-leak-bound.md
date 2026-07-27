# 3748 - Parent Bundle Split Construction or Projector Leak Bound

## Status
- `BUNDLE_SPLIT_ANSATZ_AND_PROJECTOR_LEAK_BOUND_FORMULAS_READY_VALUES_MISSING`
- A clean `E = E_L direct-sum E_M` construction exists as mathematics, but not yet as a parent-signed MTS object.
- The important progress is the bound path: projector leakage is now tied to off-diagonal connection blocks and the older Fermi-domain drift formula.

## Corpus Evidence
- `EVD3748_0_owner_bundle` `OWNER_BUNDLE_NOT_CLOSED`: requires P_loc owner, action existence, Khat metric response, boundary/source closure | does not sign the parent split
- `EVD3748_1_commutator_identity` `IDENTITY_AND_BOUND_ROUTE_AVAILABLE`: nabla(P_loc K)=P_loc nabla K+(nabla P_loc)K | supports bound route for R_comm
- `EVD3748_2_parallel_condition` `CONDITION_MATCHES_3747`: P^2=P implies derivative leakage off-diagonal; zero requires parallel image/kernel split | supports exact route but not sourced as parent geometry
- `EVD3748_3_fermi_bound` `BOUND_FORMULA_AVAILABLE`: ||nabla P_loc|| <= C_Fermi L_D||Riemann|| + C_Fermi2 L_D^2||nabla Riemann|| | first concrete leakage bound formula
- `EVD3748_4_domain_lift` `FAIL_CURRENT_CLAIM`: Pi_M origin and commutator remain not parent-derived | confirms no hidden pass
- `EVD3748_5_reference_split` `GUARD_ONLY`: bulk/edge split has no-cancellation policy but lacks orthogonality proof | helps prevent cancellation cheating
- `EVD3748_6_line_bundle` `CONDITIONAL_UNSIGNED`: ordinary subaction descent exists as conditional route but remains unsigned | useful for later R_matter_M, not enough for projector zero

## Bundle Split Attempt
- `BSA3748_0_total_bundle` `CONSTRUCTIBLE_AS_ANSATZ`: E = E_L direct-sum E_M | local metric/source response sector plus morphology/memory sector
- `BSA3748_1_projectors` `ALGEBRAICALLY_VALID`: P_L(phi_L,phi_M)=(phi_L,0), P_M(phi_L,phi_M)=(0,phi_M) | canonical projectors for the direct-sum ansatz
- `BSA3748_2_connection_matrix` `DERIVED_TEST_OBJECT`: nabla_E = [[nabla_L, Omega_LM],[Omega_ML,nabla_M]] | off-diagonal connection blocks measure projector leakage
- `BSA3748_3_parallel_condition` `ZERO_ROUTE_CONDITION`: Omega_LM=Omega_ML=0 | connection preserves E_L and E_M, giving nabla P_M=0
- `BSA3748_4_field_dependent_basis` `COUNTERMODEL_ACTIVE`: P_M = U(Phi) P_M0 U(Phi)^-1 | generic marker/transition projector as moving split
- `BSA3748_5_verdict` `ANSATZ_READY_NOT_PROOF`: parent bundle split | mathematically clean ansatz exists, but corpus does not source its parent origin

## Matrix Identities
- `MAT3748_0_projector_matrices`: P_L=[[I,0],[0,0]], P_M=[[0,0],[0,I]] | P_L^2=P_L; P_M^2=P_M; P_L P_M=0
- `MAT3748_1_connection_blocks`: A_E=[[A_LL,A_LM],[A_ML,A_MM]] | off-diagonal blocks are the obstruction
- `MAT3748_2_commutator`: [nabla,P_M]=[A_E,P_M]=[[0,A_LM],[-A_ML,0]] | zero iff A_LM=A_ML=0
- `MAT3748_3_local_action`: [nabla,P_M]P_L deltaPhi = (0,-A_ML deltaPhi_L) | R_comm controlled by ||A_ML||
- `MAT3748_4_moving_basis_delta`: delta P_M=[delta U U^-1,P_M] | ||deltaP_M|| <= 2||deltaU U^-1|| for orthogonal P_M
- `MAT3748_5_moving_basis_comm`: nabla P_M=[(nabla U)U^-1,P_M] | ||nabla P_M|| <= 2||(nabla U)U^-1||

## Projector Leak Bounds
- `LB3748_0_epsilon_comm_matrix` `epsilon_comm_matrix` `BOUND_FORMULA_READY_VALUES_MISSING`: C_pair * ||E_M^nabla||_D * ||A_ML||_D * ||deltaPhi_L||_D
- `LB3748_1_epsilon_deltaP_matrix` `epsilon_deltaP_matrix` `BOUND_FORMULA_READY_VALUES_MISSING`: C_pair * ||E_M||_D * ||Phi_S||_D * ||deltaU U^-1||_D
- `LB3748_2_fermi_projector_drift` `epsilon_comm_Fermi` `SOURCE_BACKED_FORMULA_VALUES_MISSING`: C_pair * ||E_M^nabla||_D * (C_Fermi L_D||Riemann||_D + C_Fermi2 L_D^2||nabla Riemann||_D) * ||deltaPhi_L||_D
- `LB3748_3_transition_projector_drift` `epsilon_comm_transition` `SCHEMA_ONLY_VALUES_MISSING`: C_pair * ||E_M^nabla||_D * ||deltaPhi_L||_D / ell_transition
- `LB3748_4_no_cancellation_total` `epsilon_proj_leak_abs` `BOUND_INTERFACE_READY_VALUES_MISSING`: abs(epsilon_deltaP_matrix)+abs(epsilon_comm_matrix)+abs(epsilon_comm_Fermi)+abs(epsilon_comm_transition)
- `LB3748_5_ppn_gate` `S_eff_3748` `NONCLAIM_UNTIL_ALL_VALUES_SOURCED`: S_eff_3746 + epsilon_proj_leak_abs

## Decisions
- `DEC3748_0_construction` `DIRECT_SUM_ANSATZ_CONSTRUCTED` | A clean mathematical parent split can be written, but it is an ansatz until sourced from MTS parent variables.
- `DEC3748_1_derivation` `PARALLEL_CONNECTION_IS_THE_EXACT_ZERO_CONDITION` | The off-diagonal connection blocks A_LM/A_ML are the precise obstruction to R_comm=0.
- `DEC3748_2_bound_progress` `FERMI_DOMAIN_BOUND_IMPORTED` | The older 1654 bound gives a real formula route for projector drift instead of handwaving.
- `DEC3748_3_current_status` `LOCAL_CLAIM_STILL_BLOCKED` | No numeric/source-owned values for A_ML, L_D, curvature norms, or operator constants exist here.
- `DEC3748_4_next` `FILL_LOCAL_FERMI_DOMAIN_NUMERIC_SCALES` | The next best move is to instantiate L_D, Solar-system curvature scale, and operator-normalization placeholders as nonclaim numeric smoke rows.

## Claim Gates
- `CG3748_0_sources` passed=True claim_allowed=False | 3748 source sweep complete: all registered source paths and needles found
- `CG3748_1_split_ansatz` passed=True claim_allowed=False | direct-sum parent split ansatz written: E=E_L direct-sum E_M and canonical projectors emitted
- `CG3748_2_parallel_condition` passed=True claim_allowed=False | parallel connection zero condition derived: off-diagonal connection blocks are exact obstruction
- `CG3748_3_parent_signed` passed=False claim_allowed=False | split and parallel connection parent-signed: not sourced by current corpus
- `CG3748_4_bound_formula` passed=True claim_allowed=False | epsilon_deltaP/epsilon_comm bound formulas emitted: matrix and Fermi-domain bound formulas written
- `CG3748_5_bound_values` passed=False claim_allowed=False | projector leak numeric/source values filled: A_ML, L_D, curvature norms, and operator constants missing
- `CG3748_6_local_claim` passed=False claim_allowed=False | local GR/Newton/PPN pass claim allowed: zero route unsigned and bound values missing

## Next Target
- `3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md`
- Objective: instantiate nonclaim local Fermi-domain smoke rows for L_D, Solar-system curvature norms, and projector/operator constants to test whether epsilon_comm_Fermi could plausibly sit below PPN/Newton tolerances
