# 471 - Boundary Scalar Action Owner Or Domain `alpha3` No-Leak

Private local-GR/Newton/PPN source-normalization checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, measured-GM derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `470` found a conditional kill route for the boundary contribution to `alpha3`:

```text
homogeneous scalar stationary boundary
  -> no vector/preferred-frame flux
  -> W_boundary_alpha3 = 0.
```

This checkpoint asks the hard follow-up:

```text
Does the current parent corpus force that boundary class?
```

Short answer:

```text
No.
```

But the failure is useful: it distinguishes a legitimate local closure branch from a parent-derived local-GR theorem.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_scalar_action_owner_or_domain_alpha3_no_leak.py` |
| Run directory | `runs\20260602-233000-boundary-scalar-action-owner-or-domain-alpha3-no-leak` |
| Status | `boundary_scalar_action_owner_attempt_written_conditional_homogeneous_scalar_contract_not_parent_derived_boundary_alpha3_closure_only_no_local_GR_pass` |
| Claim ceiling | `boundary_scalar_action_contract_or_closure_only_no_boundary_channel_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass` |
| Next target | `472-domain-projector-alpha3-no-leak-or-R11-link.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 229-second-order-beta-or-boundary-scalar-owner.md | True | sufficient scalar-boundary symmetry lemma and warning that parent scalar action remains missing |
| 309-MTS-boundary-projector-contract-attempt.md | True | projector/boundary contract requiring parent-owned scalar/coherent sector and Ward-safe stress accounting |
| 324-CD-activity-kernel-commutation-gate.md | True | conditional route K_boundary=f(A_D) and [K_boundary,A_D]=0, with parent origin not derived |
| 352-boundary-nohair-and-PPN-residual-vector-gate.md | True | boundary residual decomposition showing vector, shear, and flux hazards |
| 353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md | True | boundary no-hair A1-A7 contract and A3-A7 parent gaps |
| 356-parent-action-ward-identity-and-projector-variation.md | True | parent action Ward ledger exposes boundary force channel but does not kill it |
| 470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md | True | conditional boundary alpha3 zero lemma and premise ownership gaps |
| source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv | True | machine-readable premise ownership gaps from checkpoint 470 |
| source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv | True | partial boundary coefficient artifact with alpha3 conditional zero only |

## 4. Key Refinement

The safe condition is not merely:

```text
boundary is scalar.
```

The safe condition is:

```text
boundary is homogeneous scalar monopole,
stationary,
marker-free,
fully varied,
and normal-flux closed.
```

Reason:

```text
an angularly varying scalar can still generate trace-free Hessian/shear terms.
```

So the parent action must do more than remove explicit vector fields. It must also remove angular scalar gradients and boundary marker labels in the compact local branch.

## 5. Owner Attempt

| route_id | candidate_parent_statement | derivation_test | result | owned_by_current_corpus | gap | effect_on_boundary_alpha3 |
| --- | --- | --- | --- | --- | --- | --- |
| O0_representation_zero | local compact boundary carries only the l=0 scalar singlet of the active MTS sector | SO(3) tangent little-group: scalar homogeneous monopole cannot project onto vector/preferred-frame alpha3 channel | mathematical_pass_if_premise | no | parent action has not proved only the scalar singlet is available | conditional_zero_only |
| O1_homogeneous_scalar_action | S_boundary = integral sqrt(abs(gamma)) F(Q_B, trK, R_boundary_topological, scalar_memory) with all scalars homogeneous on the collar | variation gives tau_AB proportional to gamma_AB; tangential Hessian trace-free pieces vanish because D_A scalar = 0 | conditional_pass | no | 229 gives sufficient form but does not derive F or homogeneity from parent dynamics | W_boundary_alpha3_zero_if_owned |
| O2_scalar_not_enough_warning | arbitrary scalar boundary functional is safe | check nonlinear F(R_boundary, phi) terms with angularly varying scalars | fail_as_general_statement | not_applicable | D_A D_B F_R and D_A phi D_B phi can contain trace-free parts | requires homogeneous scalar monopole, not just scalar words |
| O3_kernel_commutation | K_boundary = f(A_D) and C_D/P_MTS are parent-owned, so [K_boundary,A_D]=0 and no ordinary/vector sector mixes into boundary | 324 shows K=f(A_D) commutes and blocks cross-sector leakage if parent-owned | conditional_pass | no | 324 explicitly says parent C_D and kernel commutation are not derived | would help kill marker/vector leakage if derived |
| O4_no_marker_fields | boundary state has no material marker, tangent vector, spin direction, domain velocity, or preferred frame | absence of vector representations removes B_0i and alpha3 source | needed_but_not_derived | no | no parent exclusion theorem for marker/vector boundary data | blocks promotion |
| O5_Ward_flux_closure | boundary normal momentum flux is zero, not merely Ward-owned | n_mu B_boundary^{mu i}=0 or exact cancellation before data | conditional_identity_only | no | 356/429 expose boundary force channel but do not prove absence | blocks promotion |
| O6_constant_monopole | remaining boundary trace is conserved constant measured-GM monopole with no time/radial/frame derivative | partial_t epsilon_boundary = partial_r epsilon_boundary = partial_frame epsilon_boundary = 0 | conditional_safe_for_alpha3 | no | R4 beta and R9 Gdot boundary rows remain unscored | not enough to pass full boundary channel |
| O7_parent_owner_verdict | current corpus parent-derives scalar homogeneous marker-free flux-closed boundary action | all O0-O6 owner gaps closed without new axiom | fail | no | closure-only unless a new parent action clause supplies O0-O6 | conditional_closure_not_scorecard_pass |

Verdict:

```text
The scalar-boundary route is mathematically coherent.
The current parent corpus does not force it.
```

## 6. Repair Ledger

| repair_id | missing_premise | minimum_parent_clause | would_close | current_status | next_test |
| --- | --- | --- | --- | --- | --- |
| R0_parent_scalar_boundary_action | derive the boundary action uses only homogeneous scalar shell/class data | S_boundary depends on Q_B, trK, Euler/topological curvature term, and scalar memory constants only | P0 scalar-only boundary data and homogeneous scalar warning | missing | write explicit parent action clause or demote to closure assumption |
| R1_no_marker_exclusion | exclude tangent vector, spin marker, active-domain velocity, and preferred-frame labels | boundary Hilbert space has only scalar singlet representation in stationary compact local branch | P1 no material boundary marker | missing | prove representation selection from parent symmetry or add retained vector coefficient |
| R2_full_boundary_variation | vary boundary metric and boundary fields without dropping stress | delta S_boundary produces a stress ledger with trace, shear, vector, normal flux components explicitly zero or retained | P2 full metric variation | structural_policy_only | derive stress components for candidate S_boundary |
| R3_stationary_collar_equations | derive isolated compact stationary collar conditions | local vacuum branch has no boundary time flow, radial leakage, or angular scalar gradients | P3 stationary compact collar | branch_assumption | state branch domain and derive Euler/stationarity equations |
| R4_flux_zero | Ward-owned boundary force is actually zero in local compact branch | n_mu B_boundary^{mu i}=0 follows from boundary Euler equations or topological exactness | P4 Ward flux closure | identity_not_absence | derive normal momentum no-flux or keep alpha3 coefficient product |
| R5_constant_monopole_derivative_silence | remaining scalar boundary monopole is constant universal calibration | partial_t,r,frame epsilon_boundary = 0 and source/species/range independence | P5 constant monopole calibration for alpha3-adjacent rows | missing_for_full_channel | score R4_beta/R9_Gdot/R8_xi boundary rows after alpha3 |

The exact parent contract needed for a real promotion is:

```text
S_boundary = integral_boundary sqrt(abs(gamma)) F(Q_B, trK, chi_Euler, scalar_memory_constants)
```

with:

```text
D_A Q_B = D_A scalar_memory = 0,
no tangent vector/tensor boundary representation,
n_mu B_boundary^(mu i) = 0,
and partial_t,r,frame epsilon_boundary = 0.
```

Without those clauses, the boundary `alpha3` row is closure-only.

## 7. Closure Status

| item | status | proof_or_input | valid_for_scorecard | blocks | next_action |
| --- | --- | --- | --- | --- | --- |
| boundary_alpha3 | conditional_closure_only | homogeneous scalar stationary boundary with no marker fields and zero normal flux gives W_boundary_alpha3=0 | false | PPN_alpha3_pass;mu_extra_zero;local_GR | parent-own O0-O6 or supply numeric W_boundary_alpha3 epsilon_boundary_flux |
| boundary_channel_total | not_closed | alpha3 conditional route exists but beta/xi/Gdot boundary coefficients remain missing | false | boundary_monopole_shift_channel_pass | after alpha3, score derivative/shear/monopole rows or prove constant universal monopole |
| domain_alpha3 | unaddressed_tied_pressure_row | domain_projector_mass remains tied at alpha3=4e-20 | false | combined_alpha3;local_GR | 472-domain-projector-alpha3-no-leak-or-R11-link.md |
| local_GR | not_promoted | boundary scalar action owner fails and domain row remains open | false | goal_completion | continue local residual derivations and empirical gates |

This is the honest status:

```text
boundary alpha3 can be killed by an explicit local closure assumption,
but it is not killed by a parent theorem yet.
```

## 8. Decision

| decision_id | status | meaning | next_action |
| --- | --- | --- | --- |
| D0_owner_attempt | fail_as_parent_theorem | the scalar-boundary route is mathematically coherent but not forced by the current parent corpus | do not promote boundary alpha3 |
| D1_closure_option | allowed_if_labelled | one may define an internal local closure branch with homogeneous scalar stationary boundary data | label it closure-only unless O0-O6 are parent-derived |
| D2_scorecard_status | not_scoreable | no parent theorem and no numeric W_boundary_alpha3 epsilon_boundary_flux product | keep score_ready_rows at zero |
| D3_domain_priority | move_to_domain_row | boundary alpha3 has a conditional route; tied domain alpha3 still has no no-leak attempt at this specificity | 472-domain-projector-alpha3-no-leak-or-R11-link.md |
| D4_claim_ceiling | enforced | no mu_extra zero, PPN, Newton, or local-GR pass | continue derivation gates |

Plain-English status:

```text
We did not smuggle the plateau axiom back in.
We found the exact boundary plateau contract and marked it as closure-only until the parent action earns it.
```

Boxing-score version:

```text
This round was not a knockout. It was footwork: we now know which punch is real and which one is still shadowboxing.
```

## 9. Claim Ceiling

Allowed:

```text
The boundary alpha3 row has a clean conditional closure: homogeneous scalar stationary boundary data imply zero preferred-frame flux.
```

Allowed:

```text
The parent action must derive homogeneous scalar boundary data, no marker fields, full variation, Ward no-flux, and constant monopole calibration before alpha3 can pass.
```

Forbidden:

```text
MTS parent-derives boundary alpha3 = 0.
```

Forbidden:

```text
MTS passes PPN alpha3, mu_extra zero, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `472-domain-projector-alpha3-no-leak-or-R11-link.md` | domain/projector row is tied at the same 4e-20 lock and has not received the specific no-leak attempt |
| 2 | `473-boundary-scalar-action-parent-clause-draft.md` | only if we want to propose a new parent action clause rather than mark boundary as closure-only |
| 3 | `474-alpha3-bound-product-evaluator.md` | only useful after either theorem premises or numeric coefficient products exist |
