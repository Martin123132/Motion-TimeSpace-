# 1171 — Y5/R10 natural boundary condition for B_C or first finite bound row

**Current verdict:** the generic natural-boundary route does not close the local branch. A standard variational boundary condition sets the conjugate boundary momentum `Pi_B`, not the boundary primitive integral `int_partialD B_C`. So `B_C=0` cannot be claimed from generic naturalness.

**Main progress:** this checkpoint converts the obstruction into a source-ready finite-bound row: `|int_partialD B_C| <= area(partialD) sup|B_C|` or `||1||_* ||B_C||_*`, plus the weighted-Stokes corner, kernel-derivative, harmonic, and residual terms.

**Important no-go:** the boundary integral cannot be erased by the ordinary gauge shift `B_C -> B_C + d_S Lambda_C` on a closed boundary, because the integrated exact shift vanishes. If the integral is nonzero, it is a real boundary/cohomology coefficient.

**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.

## Source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1171_0_1170_next | source-intake/mts_residuals/P8_Y5_R10_1170_NEXT_TARGET.csv | NEXT1170_0_1171 | handoff to natural boundary condition or finite bound row. | True | True |
| SRC1171_1_1170_summary | source-intake/mts_residuals/P8_Y5_BRR545_1170_VALIDATION.csv | V1170_SUMMARY | 1170 validation summary. | True | True |
| SRC1171_2_1170_split | source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv | BST1170_0_stokes_split | boundary primitive plus top-class split. | True | True |
| SRC1171_3_1170_no_flux | source-intake/mts_residuals/P8_Y5_R10_1170_PHI_BC_RELATION.csv | PBC1170_1_no_flux_condition | sufficient no-flux condition not derived. | True | True |
| SRC1171_4_1170_bound | source-intake/mts_residuals/P8_Y5_R10_1170_PHI_BC_RELATION.csv | PBC1170_2_finite_bound | finite boundary fallback. | True | True |
| SRC1171_5_1170_local_gap | source-intake/mts_residuals/P8_Y5_R10_1170_LOCAL_ZERO_CERTIFICATE.csv | LZC1170_1_boundary_primitive | main local zero boundary gap. | True | True |
| SRC1171_6_1170_stokes_guard | source-intake/mts_residuals/P8_Y5_R10_1170_WEIGHTED_STOKES_C_SECTOR.csv | WSC1170_3_zero_or_bound | strict zero-or-bound acceptance rule. | True | True |
| SRC1171_7_1170_gate | source-intake/mts_residuals/P8_Y5_R10_1170_CLAIM_GATES.csv | G1170_1_local_zero | local zero gate blocked by boundary flux. | True | True |
| SRC1171_8_274_decomp | 274-lifted-C-sector-form-holonomy-route.md | J_C = dB_C + J_C^{top} | lifted-C exact/top decomposition. | True | True |
| SRC1171_9_1020_bound | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_3_residual_bound | source-backed finite bound precedent. | True | True |
| SRC1171_10_1020_guard | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | CG1020_8_guardrail | weighted-Stokes guardrail. | True | True |
| SRC1171_11_207_bianchi | 207-domain-projector-action-and-Bianchi-identity.md | Bianchi closure can be made formal; | Bianchi/Ward conservation guard. | True | True |

## Natural boundary variation attempt

| attempt_id | object | statement | status | derives | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NBC1171_0_generic_variation | B_C exact-sector action | For a generic exact-sector kinetic term with H_C=d_D B_C, variation has the form delta S_B = bulk(delta B_C, d_D^dagger H_C + source) + int_partialD delta B_C wedge Pi_B, where Pi_B is the boundary conjugate momentum. | FORMAL_VARIATION_SHAPE | the natural boundary datum is the conjugate momentum Pi_B, not the boundary value B_C itself. | actual parent C-sector Lagrangian and exact sign/Hodge conventions | False |
| NBC1171_1_neumann_natural_condition | natural boundary condition | The ordinary free-endpoint/natural condition is Pi_B|partialD=0. This can mean no normal H_C flux, but it does not imply int_partialD B_C=0. | NO_LOCAL_ZERO_FROM_GENERIC_NATURAL_BC | generic variational naturalness is weaker than the local zero theorem needs. | special parent term proving B_C itself is pure gauge, exact with closed weight, or zero on the lifted-C residual boundary | False |
| NBC1171_2_dirichlet_condition | Dirichlet/fixed B_C boundary | Fixing pullback(B_C) or setting pullback(B_C)=0 would kill the boundary primitive, but this is an imposed boundary condition unless derived as a physical residual-sector boundary from the parent action. | CLOSURE_NOT_THEOREM | a possible closure condition, not a derivation. | parent reason for residual-sector B_C boundary silence and proof physical Hamiltonian/charge generators survive | False |
| NBC1171_3_gauge_guard | B_C gauge shift | On a closed two-boundary, int_partialD(B_C + d_S Lambda_C)=int_partialD B_C. Therefore the integrated B_C boundary primitive cannot be gauged away by an ordinary exact shift. | GAUGE_SHORTCUT_REJECTED | the boundary integral is the real obstruction, not a removable representative artifact. | separate treatment of large gauge/relative cohomology sectors if introduced later | False |
| NBC1171_4_compact_support_or_infinity | outer boundary route | A falloff/compact-support theorem at infinity could silence the outer boundary of an isolated system, but it does not automatically silence arbitrary local laboratory or solar-system subdomain boundaries. | ASYMPTOTIC_ROUTE_ONLY | asymptotic boundary control is not enough for local PPN/R10 unless the local domain boundary is physically chosen around support with no residual flux. | source-support theorem plus domain-choice rule compatible with PPN/R10 tests | False |
| NBC1171_5_verdict | natural boundary theorem verdict | 1171 does not derive a parent natural-boundary theorem strong enough to set int_partialD B_C=0. The honest route is now a finite B_C boundary-bound source row or a more specific parent boundary action. | THEOREM_NOT_CLOSED_MOVE_TO_BOUND_ROW | a no-go against the cheap natural-boundary shortcut. | parent boundary action or source-backed finite B_C norms | False |

## No-go ledger

| nog_id | claim_tested | result | reason | what_would_fix | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NOG1171_0_neumann_gap | natural BC gives local zero | fail_as_general_theorem | Pi_B=0 controls conjugate momentum/normal derivative, not the integral of B_C on the boundary | parent action where boundary equation directly imposes residual pullback(B_C)=0 or exact closed-weight cancellation | False | False |
| NOG1171_1_dirichlet_gap | set pullback B_C=0 | closure_only | Dirichlet boundary values restrict admissible histories; they are not automatically selected by a local vacuum theorem | derive residual-sector Dirichlet from finite-action/falloff/symmetry without killing physical charges | False | False |
| NOG1171_2_gauge_gap | gauge away boundary integral | fail_on_closed_boundary | closed-boundary integral of an exact gauge shift vanishes, leaving int_partialD B_C unchanged | separate parent theorem that B_C has zero boundary cohomology coefficient | False | False |
| NOG1171_3_bianchi_gap | silent boundary flux without stress ledger | fail_conservation_guard | any source/flux removal must appear in the Ward/Bianchi bookkeeping | stress tensor/current ledger for B_C, Phi_C, Sigma_C, and domain projector | False | False |

## First finite B_C boundary-bound row

| bound_id | arena | quantity | bound_formula | weighted_stokes_extension | units | numeric_value | source_path | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FBC1171_0_first_boundary_bound_row | local_R10_PPN_clock_orbital_generic | Q_C_boundary_exact | |int_partialD B_C| <= area(partialD) * sup_partialD|B_C|, or <= ||1||_* ||B_C||_* in the chosen boundary norm | + C_corner + ||d_S(F_lambda epsilon_C)||_* ||b_C||_* + |harmonic_edge_C| + |residual_edge_C| | MISSING_BOUNDARY_BC_UNITS | MISSING_BC_NORM | MISSING_SOURCE_BACKED_BC_NORM_OR_PARENT_ZERO_THEOREM | STAGED_NONCLAIM_FIRST_BOUND_ROW | False | False |
| FBC1171_1_required_area_norm | local_boundary_geometry | area(partialD) or ||1||_* | finite surface measure for the selected test domain | must use the same surface convention as B_C and weighted-Stokes terms | MISSING_SURFACE_UNITS | MISSING_DOMAIN_GEOMETRY | MISSING_DOMAIN_SPEC | REQUIRED_INPUT_MISSING | False | False |
| FBC1171_2_required_BC_norm | lifted_C_boundary | ||B_C||_* or sup_partialD|B_C| | must be derived from parent C-sector or measured/source-bounded in arena | if B_C=d_S b_C+h_C+r_C, then b_C, h_C, r_C each require norm rows | MISSING_BC_UNITS | MISSING_BC_VALUE | MISSING_PARENT_BC_PROFILE | REQUIRED_INPUT_MISSING | False | False |
| FBC1171_3_required_kernel_derivative | weighted_Stokes_C | ||d_S(F_lambda epsilon_C)||_* | zero theorem or finite derivative norm | multiplies ||b_C||_* in exact-boundary branch | MISSING_WEIGHT_DERIVATIVE_UNITS | MISSING_DSF_EPS_VALUE | MISSING_CLOSED_WEIGHT_CERTIFICATE_OR_BOUND | REQUIRED_INPUT_MISSING | False | False |
| FBC1171_4_acceptance_gate | all_local_arenas | local exact-sector residual | claim only if every term is numeric/source-backed or parent-zero | corner, harmonic, residual, kernel derivative, and primitive norms all included | BLOCKED_UNTIL_ALL_TERMS_DEFINED | NOT_EVALUATED | NO_CLAIM_FROM_1171 | RUNNER_MUST_REFUSE_CLAIM | False | False |

## Form-degree ledger

| degree_id | object | degree | boundary_role | zero_implication | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FDL1171_0_BC | B_C | 2-form on spatial D; top-degree pullback on partialD | integrates over partialD | none by degree alone | parent primitive definition and norm | False |
| FDL1171_1_bC | b_C | 1-form primitive on S if pullback(B_C)=d_S b_C | appears in weighted-Stokes derivative residual | requires corner-free S and closed weight | existence and norm of b_C | False |
| FDL1171_2_weight | F_lambda epsilon_C | weight/representative factor paired with exact-boundary primitive | d_S(F_lambda epsilon_C) multiplies b_C in residual | zero only if closed/constant in the actual weighted identity | degree and closure certificate that does not remove physical generators | False |
| FDL1171_3_Phi_C | Phi_C | 2-form boundary flux in spatial continuity split | exact-sector time-transport flux | must be natural-boundary silent or source-bounded | Phi_C-B_C parent transport law | False |

## Runner dry-run

| run_id | test | status | result | blocked_by | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RUN1171_0_generic_natural_bc | does generic natural BC imply int_partialD B_C=0 | FAILS_AS_GENERAL_THEOREM | natural BC gives Pi_B=0, not B_C boundary integral zero | parent_special_boundary_action;residual_Dirichlet_theorem | False | False |
| RUN1171_1_gauge_shortcut | can exact gauge shift remove int_partialD B_C | REFUSED_GAUGE_INVARIANT_INTEGRAL | closed-boundary integral is unchanged by B_C -> B_C + d_S Lambda_C | boundary_cohomology_coefficient_zero_theorem | False | False |
| RUN1171_2_first_finite_bound_row | can finite row be staged | PASS_SCHEMA_NONCLAIM | first B_C boundary-bound row exists but has MISSING inputs and valid_for_claim=false | B_C_norm;surface_area;dSFeps;corner;harmonic;residual;units | False | False |
| RUN1171_3_local_promotion | local-GR/R10/PPN/WEP/clock/orbital promotion | REFUSED_NO_LOCAL_CLAIM | 1171 narrows the gap to specific boundary-bound inputs but does not pass local tests | finite_bound_inputs_or_parent_boundary_zero | False | False |

## Claim gates

| gate_id | gate | current_status | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1171_0_natural_bc | natural-boundary theorem for B_C | FAILED_AS_GENERIC_THEOREM | generic natural condition sets conjugate boundary momentum, not boundary primitive integral | False | False |
| G1171_1_parent_special_bc | parent special boundary action | BLOCKED | no parent action term currently derives residual pullback(B_C)=0 | False | False |
| G1171_2_finite_bound | finite B_C boundary-bound row | SCHEMA_READY_VALUES_MISSING | row exists but B_C norm, surface geometry, kernel derivative, harmonic/residual, corner, and units are missing | False | False |
| G1171_3_charge_guard | physical-charge preservation | BLOCKED | must show residual boundary silence does not delete physical mass/time/rotation/charge generators | False | False |
| G1171_4_local_promotion | local-GR/R10/PPN/WEP/clock/orbital promotion | BLOCKED_NO_LOCAL_CLAIM | neither parent boundary zero nor finite numeric/source bound is available | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1171_0_no_generic_natural_bc | do_not_claim_boundary_zero_from_generic_naturalness | the variational boundary term does not set B_C itself to zero | look for a special parent boundary action or source finite B_C norm | False |
| D1171_1_bound_row_created | stage_first_finite_BC_bound_row | the theorem route currently fails; a finite bound is the honest fallback | derive/source B_C profile or norm in the simplest local arena | False |
| D1171_2_best_next | target_BC_norm_owner | all local residual scoring now depends on either B_C=0 theorem or an actual B_C norm | try deriving B_C primitive/norm from J_C=dB_C+J_top on a contractible local domain | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1171_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1171_1_variation_shape_written | pass | generic boundary variation identifies conjugate momentum rather than B_C value | False |
| V1171_2_natural_bc_not_overclaimed | pass | generic natural boundary route is refused as local zero proof | False |
| V1171_3_no_go_rows_written | pass | Neumann, Dirichlet, gauge, and Bianchi gaps are explicitly recorded | False |
| V1171_4_first_bound_row_created | pass | first finite B_C boundary-bound row is staged | False |
| V1171_5_missing_inputs_not_claim_valid | pass | rows with MISSING inputs remain invalid for claim | False |
| V1171_6_form_degree_ledger_written | pass | B_C, b_C, F epsilon_C, and Phi_C degree roles are logged | False |
| V1171_7_runner_refuses_claim | pass | runner refuses natural-boundary, gauge, finite-bound, and local-promotion claims | False |
| V1171_8_claim_gates_blocked | pass | all 1171 claim gates remain nonclaim | False |
| V1171_9_no_claim_rows | pass | all generated science rows remain nonclaim | False |
| V1171_10_next_target | pass | 1172 handoff targets B_C primitive/norm owner or finite bound runner | False |
| V1171_11_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1171_12_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1171_SUMMARY | pass | 1171 rejects the generic natural-boundary shortcut, stages the first finite B_C boundary-bound row, and moves the next target to deriving/sourcing B_C primitive norms | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1171_0_1172 | 1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md | derive or source a B_C primitive/norm from the local exact-sector equation, then feed the finite boundary-bound row without claiming a pass | local contractible domain; Hodge/Poincare bound for B_C from J_C; gauge fixing; boundary norm; surface geometry; units; no-claim runner | generic natural-boundary zero; gauge-erasing boundary integral; local claim; c_g zero; invented values; GitHub; formalization edits | False | False |
