# 3645 Y5 R2FR effective JX source current owner or profile smoke schema

**Status:** 3645 derives the effective source-current identity, splits J_X^eff into matter, hidden/domain, projector, shell, boundary, and topology channels, and converts the profile amplitude problem into source-current zero/bound rows.

**Claim ceiling:** no local-GR/Newton, R10, PPN, clock, orbital, no-hair, or profile-amplitude pass is claimed from this checkpoint.

## Main result

The coupling problem is now an exact variation problem. With the 1025 local operator convention,

`J_X^eff := -(1/sqrt(h)) delta(S_matter+S_hidden+S_domain+S_projector+S_shell)/delta X_N`.

Therefore a local-vacuum/GR route needs theorem-zero rows for the source components, not a plateau axiom. The cleanest branch is matter quotient descent: if `S_matter=Sbar[q(Phi),Psi,theta]`, `v_X in ker(Dq)`, and constants/readouts are X-blind, then `J_X^matter=0` and the beta leg vanishes.

## Derived source split
- `JXD3645_0_operator_convention`: CONDITIONAL_VARIATION_IDENTITY — O_X X_N = J_X^eff with O_X=-nabla_i(D_X nabla^i)+M_X^2 after boundary terms are fixed.
- `JXD3645_1_effective_current_definition`: EXACT_DEFINITION_AFTER_SIGN_CONVENTION — J_X^eff=J_X^matter+J_X^hidden_domain+J_X^projector+J_X^shell, while boundary and topology enter A_bdy/A_top unless represented as distributions.
- `JXD3645_2_matter_metric_variation`: DERIVED_CONDITIONALLY_FROM_STANDARD_VARIATION — Point-particle limit agrees with 1036: J_X^matter contains sum_i beta_i m_i delta^3(x-x_i), beta_i=partial_Xhat ln m_i^eff.
- `JXD3645_3_quotient_zero_gate`: THEOREM_ROUTE_EXACT_PREMISES_UNSIGNED — Under all descent/no-marker/no-shadow clauses, J_X^matter=0, beta_s=beta_t=0, and the matter part of A_src vanishes.
- `JXD3645_4_hidden_domain_current`: SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED — This component is zero only if the parent sector is X-blind, double-zero, or orthogonal to the local projection.
- `JXD3645_5_projector_current`: SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED — Projector current is zero only after Pi_M/P_loc/readout are parent-owned and fixed before calibration.
- `JXD3645_6_boundary_shell_current`: SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED — No plateau/local-vacuum claim can ignore boundary flux or shell mismatch.
- `JXD3645_7_green_amplitude_map`: AMPLITUDE_BOUND_DERIVED_CONDITIONALLY — |A_X| <= |A_src[J_matter]|+|A_src[J_hidden_domain]|+|A_proj|+|A_shell|+|A_bdy|+|A_top| with no tuned cancellation credit.
- `JXD3645_8_verdict`: CONTRACT_READY_NUMERIC_RUN_REFUSED — No local-GR, R10, PPN, clock, orbital, or profile-amplitude pass is claimed here.

## Component owner audit
- `JXC3645_0_matter_quotient`: `J_X^matter` — MISSING_MATTER_DESCENT_OR_BETA_BOUND
- `JXC3645_1_hidden_domain`: `J_X^hidden_domain` — MISSING_HIDDEN_DOMAIN_CURRENT_OWNER
- `JXC3645_2_projector`: `J_X^projector` — MISSING_PROJECTOR_CURRENT_OWNER
- `JXC3645_3_shell`: `J_X^shell` — MISSING_SHELL_CURRENT_OWNER
- `JXC3645_4_boundary`: `boundary_flux_X` — MISSING_BOUNDARY_FLUX_OWNER
- `JXC3645_5_topology`: `A_top;Q_X` — MISSING_TOPOLOGY_OWNER
- `JXC3645_6_operator`: `D_X;M_X^2;ell_X` — MISSING_OPERATOR_RANGE_OWNER
- `JXC3645_7_normalization`: `Xhat;beta_i;qbar_XT` — MISSING_SOURCE_NORMALIZATION_OWNER

## Smoke-runner refusal schema
- `run_id`: REQUIRED — private profile-source smoke run id
- `D_X;M_X2;ell_X`: REQUIRED_MISSING_VALUES — same-branch operator/range values or theorem-zero branch
- `J_matter_theorem_zero;J_matter_L1_bound;beta_source;beta_test`: REQUIRED_MISSING_VALUES — matter descent proof or sourced beta/current bounds
- `J_hidden_domain_theorem_zero;J_hidden_domain_L1_bound`: REQUIRED_MISSING_VALUES — hidden/domain source zero or bound
- `J_projector_theorem_zero;J_projector_L1_bound`: REQUIRED_MISSING_VALUES — projector/readout source zero or bound
- `J_shell_theorem_zero;J_shell_L1_bound;support_radius`: REQUIRED_MISSING_VALUES — transition shell zero or finite-support bound
- `boundary_flux_zero;boundary_flux_bound;topology_zero;Q_X_bound`: REQUIRED_MISSING_VALUES — boundary/topology zero or bound rows
- `source_paths`: REQUIRED_FOR_ANY_NUMERIC_RUN — source path for every nonzero value and every theorem-zero certificate
- `no_cancellation_credit`: REQUIRED_TRUE — must be true: components combine by absolute envelope, not tuned cancellation

## Green amplitude map
- `GMAP3645_0_matter`: `A_src_matter` — <= C_G(D_X,ell_X) ||J_matter||_1 (MISSING_MATTER_SOURCE_ROW)
- `GMAP3645_1_hidden_domain`: `A_src_hidden_domain` — <= C_G(D_X,ell_X) ||J_hidden_domain||_1 (MISSING_HIDDEN_DOMAIN_SOURCE_ROW)
- `GMAP3645_2_projector`: `A_proj` — <= C_G(D_X,ell_X) ||J_projector||_1 (MISSING_PROJECTOR_SOURCE_ROW)
- `GMAP3645_3_shell`: `A_shell` — <= C_G(D_X,ell_X) ||J_shell||_1 (MISSING_SHELL_SOURCE_ROW)
- `GMAP3645_4_boundary`: `A_bdy` — <= boundary_flux_bound mapped by G_ell (MISSING_BOUNDARY_FLUX_ROW)
- `GMAP3645_5_topology`: `A_top;Q_X` — <= Q_X_bound or zero (MISSING_TOPOLOGY_ROW)
- `GMAP3645_6_total_guard`: `A_X_abs` — no cancellation credit (TOTAL_GUARD_NONCLAIM)

## Decisions
- `DEC3645_0_identity_derived`: SOURCE_CURRENT_IDENTITY_DERIVED_CONDITIONALLY — J_X^eff is now defined by parent variation rather than treated as a vague missing coupling.
- `DEC3645_1_cleanest_route`: MATTER_DESCENT_ROUTE_PRIORITIZED — The lowest-scrutiny route is proving matter quotient descent/no-marker silence, because it gives J_X^matter=0 instead of fitted small beta.
- `DEC3645_2_numeric_refusal`: NUMERIC_PROFILE_RUN_REFUSED — No profile smoke run is allowed until every source component has theorem-zero or a numeric sourced bound.
- `DEC3645_3_next`: MATTER_COUPLING_DESCENT_OR_BETA_ROW_NEXT — Next target is the matter-coupling descent theorem or the first explicit beta/source row.

## Next target

`3646-Y5-R2FR-matter-coupling-descent-or-first-beta-source-row.md` via `scripts/Y5_R2FR_3646_matter_coupling_descent_or_first_beta_source_row.py`.

## Sources
- `next_3644`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3644_NEXT_TARGET.csv` exists=True needle_found=True
- `owner_3644`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3644_PROFILE_SOURCE_OWNER_AUDIT.csv` exists=True needle_found=True
- `amp_3644`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3644_AMPLITUDE_PRIOR_ROWS.csv` exists=True needle_found=True
- `schema_3644`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3644_PROFILE_RUNNER_SCHEMA.csv` exists=True needle_found=True
- `second_variation_1025`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv` exists=True needle_found=True
- `scalar_inputs_1024`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md` exists=True needle_found=True
- `beta_split_1036`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv` exists=True needle_found=True
- `parent_x_audit_1036`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv` exists=True needle_found=True
- `current_contract_1009`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md` exists=True needle_found=True
- `profile_3643`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3643_XN_AMPLITUDE_RANGE_PROFILE_ROWS.csv` exists=True needle_found=True
