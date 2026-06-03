# 401 - Parent Matter Selector Theorem Attempt

Private parent-action/WEP-selector checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 400 made the pressure point sharp: direct coframe slip and WEP/source charge need suppressions near `2.8e-15`, while flux channels are even harder. The cleanest route is not to tune them; it is to derive that local matter cannot see nonmetric selector variables.

This checkpoint attempts that derivation.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_matter_selector_theorem_attempt.py` |
| Run directory | `runs/20260602-042500-parent-matter-selector-theorem-attempt` |
| Status | `parent_matter_selector_theorem_attempt_written_selector_blind_axiom_sufficient_counterexample_blocks_derivation_from_existing_premises_R0_remains_closure_no_local_GR_pass` |
| Claim ceiling | `parent_matter_selector_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass` |
| Next target | `402-EH-source-normalization-parent-pair.md` |

## 3. Result In One Line

The theorem exists only conditionally:

```text
S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]
partial_Z e|e = 0
partial_Z theta_A = 0
=> delta S_matter/delta Z_I|e = 0
```

But the existing MTS parent action has not yet derived why matter must be selector-blind. So `R0` does not move to `derived_zero`.

## 4. Selector Principle Audit

| principle | result | verdict |
| --- | --- | --- |
| diffeomorphism covariance only | not_zero_generically | reject_as_identity_derivation |
| weak equivalence / one geometry | common_mode_pullback_remains | conditional_common_geometry_only |
| species-blind geometry functor | Delta_F_AB_zero_but_Pi_I_matter_may_remain | conditional_WEP_source_help_not_identity |
| field redefinition e_prime=ehat | not_a_parent_selection | reject_as_proof |
| selector-blind matter symmetry | zero_by_chain_rule | sufficient_conditional_theorem |
| source-normalized constant conformal factor | zero_for_selector_derivatives_but_frame_debts_remain | conditional_identity_up_to_units |

## 5. The Counterexample

The killer counterexample to weak premises is:

```text
ehat = exp(F(C_D)) e
```

This is covariant. It can be universal. It can be species-blind. But if `F'(C_D) != 0`, then:

```text
delta S_matter/delta C_D ~ T_hat F'(C_D)
```

So WEP/covariance/common geometry do not force identity coframe. They only tell us what extra selector principle we need.

## 6. Row Transition Decision

| row | new_state | reason |
| --- | --- | --- |
| R0_identity_coframe_direct | closure_zero | the axiom is not yet derived from existing MTS parent variation; counterexample exp(F(C_D))e remains legal under weaker premises |
| R1_WEP_source_charge | contingent_budget | source/bulk/boundary/domain species charges are not forbidden by an existing parent theorem |
| R2_clock_redshift | budget_only | clock/source normalization remains a separate theorem obligation |

## 7. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| candidate_selector_principles_audited | pass | 6 selector principles tested |
| counterexample_to_weak_premises_written | pass | universal ehat=exp(F(C_D))e blocks derivation from covariance/WEP/species-blindness alone |
| selector_blind_axiom_sufficient | conditional_pass | chain-rule proof gives delta S_matter/delta Z_I|e=0 if matter is selector-blind |
| selector_blind_axiom_parent_derived | fail | no existing MTS parent variation yet forbids universal class metric or selector spurions |
| R0_promoted_to_derived_zero | fail | R0 remains closure_zero; promotion needs parent-derived selector-blind symmetry |
| R1_R2_separate_debts_retained | pass | source-charge and clock constants are not closed by R0 identity alone |
| local_GR_or_WEP_promoted | fail | conditional theorem attempt only |
| claim_ceiling_enforced | pass | parent_matter_selector_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass |

## 8. Decision

The parent matter-selector theorem has a clean conditional form: if nonmetric MTS selectors are gauge/representative variables forbidden from the matter action and from matter constants, then delta S_matter/delta Z_I|e=0 by the chain rule and the direct coframe/WEP pullback row would be derived-zero. The existing corpus does not yet derive that selector-blind matter symmetry. A universal class metric ehat=exp(F(C_D))e is a counterexample to weaker premises: it is covariant, universal, and species-blind, yet still gives a common-mode matter pullback when F prime is nonzero. Therefore R0 remains closure_zero, not derived_zero.

Practical read: this is not a defeat. It is the correct Grossmann move: we found the exact missing principle. Either MTS derives selector-blind matter from its primitive motion/time/space structure, or identity coframe remains an explicit local closure used to test the rest of the GR stack.

## 9. Next Target

`402-EH-source-normalization-parent-pair.md`

Now test whether the dynamics in the same matter frame can become EH plus source-normalized measured `GM`, instead of leaving `gamma`, `beta`, and source-normalization as inserted budgets.
