# 3733 - H^X and Hodge Variation: Zero or Bound

## Status
- `HX_CHI_ZERO_CONDITIONAL_FINITE_BOUND_SCHEMA_READY`
- `H^X=partial_X g_matter` has a clean chain-rule zero theorem if the matter metric descends through `q` and the vertical direction is in `ker(Dq)`.
- `partial_X chi` has a clean Hodge/constitutive zero theorem if `H^X=0`, EM constants descend through `q`, and no hidden constitutive/background-flow slot remains.
- Neither zero theorem is parent-signed in the current corpus, so the finite no-cancellation bound route stays active.

## H^X Zero Audit
- `HXZ3733_0_definition` `DEFINITION_SHARP`: H^X_{mu nu}:=partial_X g^matter_{mu nu}|branch = Lie_vX g^matter_{mu nu} | missing: none at definition level
- `HXZ3733_1_chain_rule_zero` `CONDITIONAL_THEOREM_VALID`: If g_matter(Phi)=g_pub(q(Phi)) and Dq[v_X]=0, then H^X=Dg_pub[Dq[v_X]]=0. | missing: parent-signed q-kernel and matter-frame factorization
- `HXZ3733_2_shadow_counterbranch` `FINITE_BRANCH_REQUIRED_IF_NOT_EXCLUDED`: If g_matter=A_g(X)^2 g_pub+B_g(X)U_mu U_nu, then H^X=2 c_g g_pub + b_dis U_mu U_nu + extra terms. | missing: c_g,b_dis,extra-frame coefficient rows or no-shadow theorem
- `HXZ3733_3_spm_closure` `CLOSURE_ONLY_NONCLAIM`: Under explicit SPM closure, independent A_g and B_g slots are excluded, so H^X=0 inside that closure branch only. | missing: parent proof if promoted beyond closure
- `HXZ3733_4_verdict` `ZERO_NOT_PARENT_SIGNED`: H^X=0 is not claimable in the current parent corpus; the zero theorem is conditional and the finite branch must be retained. | missing: SPM/no-shadow parent action or finite H^X bound pack

## Hodge/chi Zero Audit
- `CHIZ3733_0_definition` `DEFINITION_SHARP`: partial_X chi^{mu nu rho sigma}:=Lie_vX chi^{mu nu rho sigma} | missing: none at definition level
- `CHIZ3733_1_metric_hodge_chain` `DERIVED_CHAIN_RULE`: If chi=chi_vac[g_matter,theta_EM] then partial_X chi=(delta chi/delta g_matter)[H^X]+(partial chi/partial theta_EM)partial_X theta_EM. | missing: H^X, theta_EM quotient ownership, and vacuum/material constitutive law
- `CHIZ3733_2_vacuum_zero` `CONDITIONAL_THEOREM_VALID`: If H^X=0, theta_EM=theta_EM(q), and there is no hidden medium/background constitutive slot, then partial_X chi=0. | missing: H^X zero, no-marker EM constants, and no hidden constitutive medium
- `CHIZ3733_3_hidden_medium_counterbranch` `FINITE_BRANCH_REQUIRED_IF_NOT_EXCLUDED`: If chi=chi_vac[g]+chi_hidden(X,flow,material), then partial_X chi can be nonzero even when H^X=0. | missing: partial_X chi_hidden or parent Hodge/constitutive rule
- `CHIZ3733_4_verdict` `ZERO_NOT_PARENT_SIGNED`: partial_X chi=0 is not claimable in the current parent corpus; retain a finite constitutive/Hodge coefficient. | missing: parent Hodge rule or finite partial_X chi bound pack

## Finite Bound Rows
- `FIN3733_0_HX_norm` `Hbar_X`: ||H^X||_A <= 2|c_g| C_g,A + |b_dis| C_dis,A + ||H_extra||_A | links: Newton_PPN;clock;EM_Poynting;source_coupling
- `FIN3733_1_trace_source` `J_geom_bound`: ||J_geom||_A <= 1/2 ||T||_A ||H^X||_A | links: Newton_PPN;R10;clock;orbital
- `FIN3733_2_chi_metric_part` `Chibar_metric`: ||partial_X chi_metric||_A <= C_chi_g,A ||H^X||_A | links: EM_Poynting;Maxwell_stress;wave
- `FIN3733_3_chi_marker_part` `Chibar_marker`: ||partial_X chi_marker||_A <= C_chi_theta,A |b_alpha| + sum_I C_chi_I,A |b_I| | links: EM_Poynting;charge;fine_structure;clock
- `FIN3733_4_chi_hidden_part` `Chibar_hidden`: ||partial_X chi_hidden||_A <= C_flow,A |b_flow| + ||tail_chi||_A | links: EM_Poynting;background_flow
- `FIN3733_5_total_abs_guard` `HX_chi_total_abs`: total <= Hbar_X + Chibar_metric + Chibar_marker + Chibar_hidden + retained_tails, with no cancellation between unknowns | links: all local arenas

## Arena Feeds
- `FEED3733_0_Newton_PPN` `Newton_PPN_bridge`: sigma_NP <= C_trace Hbar_X ||T|| + C_dis|b_dis|||T_UU|| + |Delta_GM| + |boundary_NP| + |tail_NP| | missing: Hbar_X,c_g,b_dis,T,T_UU,Delta_GM,boundary_NP,tail_NP
- `FEED3733_1_EM_Poynting` `EM_Poynting_bridge`: sigma_EM <= C_chi Chibar_total ||F^2|| + C_frame Hbar_X ||T_EM|| + C_J||delta_X J_EM|| + |b_alpha C_alpha| + |tail_EM| | missing: Chibar_total,Hbar_X,F^2,T_EM,delta_X_J_EM,b_alpha,tail_EM
- `FEED3733_2_clock` `clock_redshift`: sigma_clock <= C_clock_frame Hbar_X + C_clock_alpha Chibar_marker + marker tails | missing: Hbar_X,Chibar_marker,clock sensitivities
- `FEED3733_3_R10_source` `R10_short_range`: beta_source/test products retain Hbar_X through c_g and tails; do not linearize source-test exchange by accident | missing: c_g,tau_R10,K_X,Qbar_XH,tail envelope

## Theorem Rows
- `THM3733_0_HX_chain_rule` `CONDITIONAL_THEOREM`: g_matter=g_pub(q(Phi)) and Dq[v_X]=0 imply H^X=0. | This is the exact no-shadow matter metric theorem target.
- `THM3733_1_HX_finite_branch` `FINITE_BOUND_CONTRACT`: If a Weyl/disformal matter frame is retained, H^X=2 c_g g+b_dis U U+H_extra and must be bounded componentwise. | This is the finite route for local GR/Newton if zero cannot be derived.
- `THM3733_2_chi_chain_rule` `DERIVED_CHAIN_RULE`: chi=chi[g_matter,theta_EM,hidden] gives partial_X chi=(delta chi/delta g)[H^X]+(partial chi/partial theta)partial_X theta + partial_X chi_hidden. | This is the exact Hodge/constitutive route for Maxwell/EM stress.
- `THM3733_3_chi_zero_conditions` `CONDITIONAL_THEOREM`: H^X=0, quotient-owned EM constants, and no hidden constitutive slot imply partial_X chi=0. | This is the clean Maxwell/Poynting zero theorem target.
- `THM3733_4_no_cancellation` `ANTI_OVERCLAIM`: Unknown H^X, marker, hidden-Hodge, and tail terms obey a no cancellation rule: combine them by absolute envelope, not signed cancellation. | Keeps the bound route honest across Newton/PPN/EM.

## Decisions
- `DEC3733_0_zero_attempt` `ZERO_ROUTE_IS_CLEAN_BUT_NOT_PARENT_SIGNED` | H^X and partial_X chi both have exact chain-rule zero theorems, but current corpus lacks the parent signatures.
- `DEC3733_1_bound_route` `FINITE_BOUND_ROUTE_IS_NOW_COMPONENTIZED` | The finite route is no longer vague: Hbar_X, J_geom_bound, Chibar_metric, Chibar_marker, and Chibar_hidden are separate no-cancellation inputs.
- `DEC3733_2_EM_status` `EM_POYNTING_ROUTE_SURVIVES_AS_HODGE_VARIATION` | Poynting/background-flow intuition is preserved as partial_X chi_hidden or a parent Hodge rule, not used as a claim.
- `DEC3733_3_next` `NEXT_BUILD_HX_CHI_TO_3732_INTERFACE` | The next useful move is to make Hbar_X/Chibar_total rows mechanically feed the 3732 Newton/PPN and EM response entries.

## Next Target
- `3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md`
- Objective: connect `Hbar_X` and `Chibar_total` to the 3732 Newton/PPN and EM/Poynting response entries so future numeric or theorem-zero rows can drive 3729.
