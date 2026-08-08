# 3213 - Hidden/Visible Product Sequester Or EM Coefficient Provenance Pack under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, R10 pass, WEP pass, clock pass, `b_alpha=0` claim, product-sequester claim, or public-facing result.

## Result

3213 gives the honest theorem/countertheorem fork.

The clean theorem route:

```text
C_parent -> C_vis x C_hid
S_vis = S_vis[q(Phi), theta_rep]
Hom(C_hid, Coeff(O_vis)) = Const or absent
boundary/readout/radiative maps preserve the split
=> hidden X cannot generate f_X F^2, C_Hodge, C_Poynting, mass, or clock coefficients.
```

The countertheorem:

```text
If a nonconstant hidden invariant scalar I survives,
then c(I)=c0+epsilon I is a visible coefficient map.
So c(I)F^2, c(I)T_EM, or c(I)n_iT_EM^(0i)
is legal unless product/sequester, exact shift, or typed-out target action forbids it.
```

Current verdict: product/sequester is the right theorem, but it is not parent-signed; the scalar-invariant countertheorem is active. Therefore EM coefficients must stay as finite provenance rows unless the surviving invariant generators are killed.

## Product Sequester Test

| test_id | claim_piece | formal_condition | derivation_result | current_status | blocks_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SEQ3213_0_product_domain | visible-hidden product domain | C_parent -> C_vis x C_hid, with visible objects pulled back from q and representation labels; hidden variables have no target action on visible coefficient modules. | if parent-signed, hidden representative motion cannot generate f_X F2, Hodge coefficient drift, matter masses, or readout constants | conditional_not_parent_signed | parent split and target-action exclusion are not derived from primitives | false |
| SEQ3213_1_visible_action_pullback | visible action ignores hidden coordinates except through q | S_vis = S_EM[A_Q,q,T_Q,theta_rep]+S_matter[Psi,e_obs(q),theta_rep]+S_readout[q,theta_rep] | Dq[v_X]=0 then gives delta_X S_vis=0, including b_alpha=0 and C_Hodge=0 at tree level | exact_conditional_theorem | actual parent visible action and all readout maps are not signed to have this form | false |
| SEQ3213_2_boundary_functor | boundary/Poynting sequester | S_boundary and source-worldtube terms depend only on q-visible stress flux or are exact/proper/orthogonal to hidden X | would make Phi_Poynting zero or independent of X on the local branch | new_required_clause_not_signed | product functor must cover boundary/worldtube flux, not just bulk F2 | false |
| SEQ3213_3_radiative_readout | EFT/readout closure | renormalized S_eff and clock/spectroscopy/readout maps remain in the product image | tree-level no-extra-F2 would survive to observable alpha products | unsigned | loop/readout re-entry can recreate b_alpha or clock coefficients | false |
| SEQ3213_4_total | product sequester theorem promotes EM source silence | SEQ3213_0 through SEQ3213_3 all parent-signed on the same branch | J_EM=0 and Phi_Poynting=0 for the hidden X source channel | fail_current_claim | same-branch product/readout/boundary theorem is not available | false |

## Invariant Scalar Countertheorem

| counter_id | assumption | construction | operator | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CTR3213_0_scalar_invariant | there exists nonconstant hidden invariant scalar I with Lie_vX I nonzero | c(I)=c0+epsilon I is a natural scalar coefficient | c(I) F^2, c(I) F*F, c(I) T_EM/stress, or c(I) boundary flux weight | hidden-visible coefficient morphism exists; b_alpha/Hodge/Poynting cannot be theorem-zero | countertheorem_active_unless_invariant_algebra_trivial_or_typed_out | false |
| CTR3213_1_covariance_limit | only diffeomorphism covariance and visible U(1) gauge invariance are imposed | f(I)F^2 is a scalar gauge-invariant density | hidden-scalar gauge kinetic counterterm | ordinary symmetries do not forbid the EM source channel | no_zero_from_covariance_or_gauge_invariance | false |
| CTR3213_2_shift_limit | only parity or weak shift evidence is available | even functions such as I^2 F^2 or radiative/readout terms survive unless exact shift/product closure is signed | even/radiative coefficient maps | linear coefficient may die while quadratic/readout source remains | shift_route_requires_exact_parent_symmetry_and_closure | false |
| CTR3213_3_boundary_limit | bulk visible action is sequestered but boundary/source-worldtube action is not | hidden-dependent boundary weight multiplies EM energy flux | C_Poynting(I) n_i T_EM^{0i} | Poynting source re-enters through Phi_boundary even if bulk F2 is banned | boundary_functor_must_be_part_of_theorem | false |

## EM Coefficient Provenance Pack

| row_id | coefficient | definition | zero_route | finite_route_inputs | feeds | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROV3213_0_balpha | b_alpha | vertical derivative of EM gauge kinetic/readout coefficient; partial_X ln Z_A or equivalent | product/sequester plus fixed T_Q/gauge norm plus no radiative/readout re-entry | numeric/source-backed b_alpha or bounded prior width; X normalization; source path; units | FEB3212_0_balpha;J_F2_bound;clock/WEP/R10 alpha rows | MISSING_ZERO_THEOREM_OR_NUMERIC_PROVENANCE | false |
| PROV3213_1_C_Hodge | C_Hodge | partial_X g_obs or partial_X star_obs coefficient in EM stress/Hodge channel | observed Hodge star factors through q and Dq[v_X]=0 | C_Hodge bound;EM stress norm;surface/support;source path;units | FEB3212_3_Hodge;J_Hodge_bound;PPN/clock/EM stress rows | MISSING_HODGE_DESCENT_OR_FINITE_BOUND | false |
| PROV3213_2_C_Poynting | C_Poynting | hidden/X derivative of boundary or worldtube coupling to EM energy flux | boundary functor is exact/proper/orthogonal or depends only on q-visible flux | C_Poynting;flux integral;surface/worldtube rule;orientation;source path;units | FEB3212_4_Poynting;Phi_boundary;3210 b_X | MISSING_BOUNDARY_SEQUESTER_OR_FLUX_BOUND | false |
| PROV3213_3_theta_dual | Theta_A_prime | hidden/X derivative of dual/topological EM coefficient multiplying F*F | dual coefficient is topological/discrete/quotient-owned or exact constant | Theta_A_prime bound;FstarF norm;topological sector rule | FEB3212_2_dual;J_dual_bound | MISSING_DUAL_CHANNEL_POLICY | false |
| PROV3213_4_total | EM_source_envelope | absolute sum of b_alpha, C_Hodge, C_Poynting, dual, and radiative/readout EM source contributions | all component zero routes pass on one parent branch | all component coefficients and field/support norms with no MISSING markers | J_EM_bound_abs;J_X_norm;X amplitude;omega_X bound | NOT_COMPUTED_COMPONENTS_MISSING | false |

## Decision

`PRODUCT_SEQUESTER_THEOREM_CONDITIONAL_COUNTERTHEOREM_ACTIVE_PROVENANCE_PACK_STAGED`.

Claim status: `NO_SEQUESTER_CLAIM_NO_B_ALPHA_ZERO_NO_JEM_ZERO`.

Best next route: attack the surviving invariant generators directly; if any generator survives, keep EM coefficients as finite provenance rows.

Next target:

```text
3214-Y5-R2FR-invariant-generator-kill-list-for-EM-coupling-or-promote-provenance-inputs-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_PRODUCT_SEQUESTER_THEOREM_TEST.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_INVARIANT_SCALAR_COUNTERTHEOREM.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_EM_COEFFICIENT_PROVENANCE_PACK.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3213_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3213_00_inputs_exist | true | inputs=10 |
| VAL3213_01_sequester_theorem | true | same-branch product/readout/boundary theorem gate written |
| VAL3213_02_countertheorem | true | I -> c0+epsilon I creates visible coefficient morphism |
| VAL3213_03_boundary_counterexample | true | bulk sequester alone is insufficient |
| VAL3213_04_provenance_pack | true | b_alpha;C_Hodge;C_Poynting;dual;total |
| VAL3213_05_claims_blocked | true | claim_rows_true=0 |
| VAL3213_06_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3213_07_csv_parse | true | P8_Y5_R2FR_3213_INPUTS.csv;P8_Y5_R2FR_3213_PRODUCT_SEQUESTER_THEOREM_TEST.csv;P8_Y5_R2FR_3213_INVARIANT_SCALAR_COUNTERTHEOREM.csv;P8_Y5_R2FR_3213_EM_COEFFICIENT_PROVENANCE_PACK.csv;P8_Y5_R2FR_3213_DECISION.csv |

All generated rows remain `valid_for_claim=false`.
