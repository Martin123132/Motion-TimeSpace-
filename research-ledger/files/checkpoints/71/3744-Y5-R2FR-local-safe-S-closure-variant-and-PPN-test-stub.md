# 3744 - Local-Safe S Closure Variant and PPN Test Stub

## Status
- `LOCAL_SAFE_S_STUB_BUILT_NONCLAIM_PARENT_LEGITIMACY_REQUIRED`
- This is a forward step: the 3743 repair contract is now an executable local budget gate.
- The raw `S` branch remains demoted; no local GR/Newton/PPN pass is claimed from dry-run arithmetic.

## Closure Variants
- `LS3744_0_raw_S` `LOCAL_PPN_UNSAFE_RETAINS_3743_DEMOTION`: S_eff = epsilon_K + epsilon_grad + epsilon_phi_raw + epsilon_boundary | This is carried only as a blocked baseline.
- `LS3744_1_projected_S` `PREFERRED_REPAIR_CANDIDATE_NONCLAIM`: S_eff = epsilon_K + epsilon_grad + sigma_phi_local*epsilon_phi_raw + epsilon_boundary | This is the cleanest repair because it quarantines morphology locally without deleting it globally.
- `LS3744_2_eta_zero_S` `SECOND_REPAIR_CANDIDATE_NONCLAIM`: S_eff = epsilon_K + epsilon_grad + epsilon_boundary | This is simpler but more fragile because it risks looking like term deletion unless parent-signed.
- `LS3744_3_numeric_bound_S` `EMPIRICAL_REPAIR_CANDIDATE_NONCLAIM`: S_eff = epsilon_K + epsilon_grad + epsilon_phi_raw + epsilon_boundary | This is a useful fallback once real local profiles exist.

## PPN/Newton Stub Rule
- `gamma`: pass arithmetic only if `C_gamma_S*S_eff <= tol_gamma`.
- `beta`: pass arithmetic only if `C_beta_S*S_eff <= tol_beta`.
- `Newton`: pass arithmetic only if `C_Newton_S*S_eff <= tol_Newton`.
- `claim_allowed`: remains false unless the input row is sourced and the relevant projector/eta/numeric branch is parent-owned.

## Dry-Run Results
- `RES3744_0_raw_hazard` `LS3744_0_raw_S`: S_eff=1.000000000000e-03 gamma=1.000000000000e-03 beta=1.000000000000e-03 numeric_pass=False claim_allowed=False | exceeds_tolerance
- `RES3744_1_projected_zero` `LS3744_1_projected_S`: S_eff=2.000000000000e-20 gamma=2.000000000000e-20 beta=2.000000000000e-20 numeric_pass=True claim_allowed=False | none_numeric_only
- `RES3744_2_eta_zero` `LS3744_2_eta_zero_S`: S_eff=2.000000000000e-20 gamma=2.000000000000e-20 beta=2.000000000000e-20 numeric_pass=True claim_allowed=False | none_numeric_only
- `RES3744_3_numeric_bound` `LS3744_3_numeric_bound_S`: S_eff=1.000000000002e-08 gamma=1.000000000002e-08 beta=1.000000000002e-08 numeric_pass=True claim_allowed=False | none_numeric_only

## Decisions
- `DEC3744_0_progress` `RUNNABLE_LOCAL_SAFE_S_GATE_BUILT` | The local branch is now an executable budget gate, not just prose.
- `DEC3744_1_best_route` `PROJECTED_LOCAL_SAFE_S_IS_PREFERRED_REPAIR` | It preserves galaxy/cosmology morphology while letting the local PPN projection be silent if a real parent projector exists.
- `DEC3744_2_eta_zero_fallback` `ETA_ZERO_IS_SECOND_BEST` | It is algebraically clean but needs stronger parent legitimacy because it removes a term outright.
- `DEC3744_3_no_claim` `NO_LOCAL_GR_CLAIM_FROM_DRY_RUN` | Dry-run arithmetic passing is not a theorem and not evidence.
- `DEC3744_4_next` `NEXT_PARENT_LEGITIMACY_GATE` | The next leap is to derive or reject the parent legitimacy of the projected local-safe S closure.

## Claim Gates
- `CG3744_0_sources` passed=True claim_allowed=False | 3741-3743 handoff sources registered: source needles found for budget, tolerance, and repair contract
- `CG3744_1_raw_blocked` passed=True claim_allowed=False | raw S branch remains blocked: raw demo fails because epsilon_phi_raw dominates
- `CG3744_2_projected_arithmetic` passed=True claim_allowed=False | projected closure arithmetic works as a stub: sigma_phi_local=0 kills the local Phi_S term in dry-run arithmetic
- `CG3744_3_eta_zero_arithmetic` passed=True claim_allowed=False | eta-zero closure arithmetic works as a stub: eta-zero branch kills the local Phi_S term in dry-run arithmetic
- `CG3744_4_numeric_bound_arithmetic` passed=True claim_allowed=False | numeric-bound closure arithmetic works as a stub: small supplied epsilon_phi_raw passes the tolerance dry run
- `CG3744_5_no_repair_claim` passed=True claim_allowed=False | repair rows do not claim a pass: dry-run arithmetic is not a sourced theorem or data result
- `CG3744_6_local_claim` passed=False claim_allowed=False | local GR/Newton/PPN pass claim allowed: parent projector/eta-zero/numeric local profile sources remain absent

## Next Target
- `3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md`
- Objective: derive or reject whether the projected local-safe S closure follows from a parent action/quotient projector rather than being an explicit closure patch
