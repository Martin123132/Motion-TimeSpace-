# 3742 - Local S-Budget Gate: eta Phi_S^2 and gradK Bound

## Status
- `FULL_S_BUDGET_GATE_FORMALIZED_PHI_AND_GRADK_OPEN`
- The overbroad shorthand `S ≈ K^m` is demoted: the local branch only survives if the full `S_epsilon` budget is small.
- `Phi_S` in the `S` functional is not automatically Newtonian `Phi_N`; the symbol collision is now an explicit gate.

## Symbol Disambiguation
- `Phi_S`: Phi_S := |nabla kappa| or related curvature-tension proxy in S(K,nablaK,Phi) | gate: must not be identified with Newtonian potential without a map
- `Phi_N`: Phi_N appears in weak-field metric and Gamma_kappa=-2 Phi_N/c^2 | gate: distinct from Phi_S unless a parent theorem maps them
- `eta`: eta is present in the S ansatz but no local numeric/source-owned value was found | gate: eta=0 or eta*Phi_S^2 bound is required for local PPN closure
- `ell`: ell appears in ell^2(nablaK)^2 but is not locally normalized in the corpus source | gate: ell/L_K ratio must be bounded
- `K`: K_solar scale supports K^m suppression branch | gate: K term alone cannot certify full S budget

## Budget Bounds
- `epsilon_K` `SOURCE_BACKED_SOLAR_SCALE_PARTIAL_PASS`: epsilon_K <= K_D^m for K_D^m>=0; with K_D≈1e-61 and m>=2 gives <=1e-122 before operator constants | blocker: K_solar and m>=2 source text exist; units/operator constants still open
- `epsilon_grad` `CONDITIONAL_LENGTH_SCALE_BOUND`: if ||nabla K||_D <= K_D/L_K then epsilon_grad <= (ell/L_K)^2*K_D^2/(1+K_D^m) | blocker: requires source-owned ell and local variation length L_K; likely tiny only when ell<<L_K or at least ell/L_K finite
- `epsilon_phi` `UNRESOLVED_DOMINANT_LOCAL_GATE`: epsilon_phi <= |eta|*Phi_S,D^2; if Phi_S=|nabla kappa| and ||nabla kappa||<=kappa_D/L_kappa then <= |eta|*(kappa_D/L_kappa)^2 | blocker: must prove eta=0, Phi_S=0, local projector silence, or numeric bound below PPN tolerance
- `epsilon_boundary` `BOUNDARY_GATE_OPEN`: epsilon_boundary <= B_boundary from domain choice and support projection | blocker: must select local domain/gauge and bound support terms
- `S_epsilon` `ASSEMBLED_BUT_NOT_NUMERIC`: S_epsilon = epsilon_K + epsilon_grad + epsilon_phi + epsilon_boundary | blocker: full local PPN closure is blocked until all four terms satisfy the target tolerance

## Phi_S Zero-or-Bound Routes
- `ZB3742_0_eta_zero` `NOT_PROVED`: eta=0 local theorem -> epsilon_phi=0 | Would close the dangerous morphology term, but no corpus source currently proves eta=0.
- `ZB3742_1_phi_zero` `NOT_PROVED_FOR_LOCAL`: Phi_S=0 symmetry/plateau theorem -> epsilon_phi=0 | FLRW source has Phi=0, but solar/local non-homogeneous branch does not inherit this automatically.
- `ZB3742_2_projector_silence` `OPEN_THEOREM_TARGET`: P_loc Phi_S=0 -> epsilon_phi projected out of local PPN observables | Viable route if the parent projector kills morphology terms in local vacuum without killing galaxy/cosmology behavior.
- `ZB3742_3_numeric_bound` `OPEN_NUMERIC_TARGET`: |eta| Phi_S,D^2 <= epsilon_PPN/(C_beta+C_gamma+C_N) -> epsilon_phi below PPN tolerance | Viable empirical/phenomenological route if eta and Phi_S norms are source-owned.
- `ZB3742_4_modify_S` `CLOSURE_REPAIR_OPTION`: replace S ansatz by local-safe S = K^m + gradK terms only in PPN branch -> epsilon_phi removed by theory design | This is a possible repair but must be explicit; otherwise the old S ansatz remains the blocker.

## PPN Acceptance Gate
- `gamma`: need S_epsilon <= tol_gamma/C_gamma_S | tol_gamma not sourced here; leave symbolic until PPN data gate
- `beta`: need S_epsilon <= tol_beta/C_beta_S | tol_beta not sourced here; leave symbolic until PPN data gate
- `Newton/Poisson`: need S_epsilon <= tol_Newton/C_Newton_S | tol_Newton not sourced here; leave symbolic until local data gate
- `combined local closure`: single acceptance gate for calibrated-GR closure branch | symbolic acceptance gate ready

## Theorem Rows
- `THM3742_0_symbol_split` `SYMBOL_COLLISION_RESOLVED`: The S-functional Phi must be treated as Phi_S, distinct from Newtonian Phi_N, until a parent map is proved. | This blocks a common false local-GR shortcut.
- `THM3742_1_grad_bound` `DERIVED_CONDITIONAL_BOUND`: If ||nabla K||<=K_D/L_K, then the gradK term is bounded by (ell/L_K)^2 K_D^2/(1+K_D^m). | This makes gradK a length-scale gate, not vague doom.
- `THM3742_2_phi_gate` `DOMINANT_OPEN_GATE`: The eta Phi_S^2 term is the dominant unresolved local closure blocker because it is not automatically suppressed by K^m. | The K_solar argument is not enough by itself.
- `THM3742_3_demotion` `OVERBROAD_CLOSURE_DEMOTED`: The statement 'local PPN passes because S≈K^m' is demoted to 'local PPN is conditionally safe if the full S_epsilon budget is below tolerance'. | This is a correction, not a retreat.
- `THM3742_4_claim_gate` `ANTI_OVERCLAIM`: No local-GR/Newton/PPN pass is claimable until eta Phi_S^2, gradK, boundary, and operator constants are closed. | Keeps the route serious.

## Decisions
- `DEC3742_0_progress` `FULL_S_BUDGET_GATE_FORMALIZED` | The local closure branch now has explicit K, gradK, Phi_S, and boundary budget terms.
- `DEC3742_1_demote` `OVERBROAD_KM_LOCAL_PASS_DEMOTED` | The old shorthand S≈K^m is not valid unless gradK and Phi_S terms vanish or are bounded.
- `DEC3742_2_best_route` `BEST_NEXT_ROUTE_PROJECTOR_OR_ETA_ZERO` | The least-circular next leap is to derive P_loc Phi_S=0 or eta=0 in local weak-field/vacuum, rather than fitting eta small.
- `DEC3742_3_fallback` `FALLBACK_MODIFY_S_FUNCTIONAL` | If the Phi_S gate cannot be derived, the local closure branch needs an explicitly local-safe S functional or remains closure-only.

## Next Target
- `3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md`
- Objective: try to prove P_loc Phi_S=0 or eta=0 for the local weak-field/vacuum branch; if not, declare the current S functional local-PPN unsafe without an added projector/modification
