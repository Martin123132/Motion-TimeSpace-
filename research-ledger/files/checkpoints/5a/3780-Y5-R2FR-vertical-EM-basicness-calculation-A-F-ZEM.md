# 3780 - Vertical EM Basicness Calculation for A, F, and Z_EM

## Status

`VERTICAL_EM_BASICNESS_DERIVED_AS_PULLBACK_CONNECTION_CONDITION_NOT_PARENT_SIGNED`.

A/F basicness closes if A_obs=Abar(q_obs)+dLambda and local cohomology/Wilson residues are silent; Z_EM closes if q_obs-owned or superselected. Parent construction is still required.

## Result In Plain Terms

The calculation does not merely say EM is missing. It proves the exact shape of the missing or closing term. For a q_obs-vertical direction `E_A`, split `Lie_EA A_obs=d lambda_A+R_A`. Then `Lie_EA F_obs=dR_A`. So the EM route closes locally if `R_A` is zero/exact and `Z_EM` is q_obs-owned or superselected. If not, `R_A`, `dR_A`, Wilson residues, and `beta_Z,A=Lie_EA ln Z_EM` are the physical residuals that must be bounded.

## Vertical Derivation
- `VED3780_0_vertical_setup` `EXACT_DEFINITION`: Let E_A be a basis vector in ker(Dq_obs). For any observed EM potential A_obs(Phi), define delta_A A_obs := Lie_EA A_obs. Meaning: This is the exact fibre direction whose physical invisibility must be proved.
- `VED3780_1_A_split` `EXACT_LOCAL_DECOMPOSITION_WITH_TOPOLOGY_CAVEAT`: Decompose delta_A A_obs = d lambda_A + R_A, where lambda_A is the best gauge representative and R_A is the gauge-orthogonal residue. Meaning: R_A is the honest non-gauge obstruction; setting it to zero by naming it gauge would be cheating.
- `VED3780_2_F_variation` `EXACT_DERIVATION`: Since F_obs=dA_obs, delta_A F_obs = d(delta_A A_obs)=dR_A because d^2 lambda_A=0. Meaning: The local EM readout test is now concrete: prove dR_A=0 or bound ||dR_A||.
- `VED3780_3_local_exactness` `CONDITIONAL_LOCAL_PLATEAU_FOR_EM_READOUT`: On a contractible local patch, dR_A=0 implies R_A=d sigma_A, so delta_A A_obs=d(lambda_A+sigma_A) and delta_A F_obs=0. Meaning: Local GR only needs this on the local domain, but global Wilson residues must be declared if H^1(U) is nontrivial.
- `VED3780_4_pullback_connection_route` `EXACT_SUFFICIENT_ZERO_PROOF`: If A_obs=Abar(q_obs(Phi))+d Lambda(Phi), then delta_A A_obs=d(Lie_EA Lambda) and delta_A F_obs=0 for every E_A in ker(Dq_obs). Meaning: This is the constructive route: make EM a q_obs-bundle connection, not an extra hidden representative field.
- `VED3780_5_ZEM_split` `EXACT_COEFFICIENT_EXTRACTION`: Write ln Z_EM(Phi)=ln Zbar_EM(q_obs(Phi))+z_perp(Phi). Then beta_Z,A:=Lie_EA ln Z_EM=Lie_EA z_perp. Meaning: Z_EM is the coupling throat: q_obs-owned or superselected gives beta_Z,A=0; otherwise WEP/clocks/Gdot/PPN feel it.
- `VED3780_6_EM_action_leak` `EXACT_ACTION_VARIATION_SCHEMA`: For S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab, the vertical bulk leak is proportional to beta_Z,A F^2 plus the Maxwell-current pairing with R_A, up to boundary terms. Meaning: A pure-gauge A variation and beta_Z,A=0 make the EM action vertically silent; R_A or beta_Z,A are physical residuals.
- `VED3780_7_verdict` `DERIVED_NOT_PARENT_SIGNED`: The calculation closes the local EM readout only under the pullback-connection/cohomology/Z_EM-superselection clauses; the present parent corpus has not signed those clauses. Meaning: 3780 is real progress but not a claim: the next step must construct the q_obs U(1) connection from MTS flow/phase data or keep R_A and beta_Z,A as bounded residues.

## A Variation Decomposition
- `AVD3780_0_qobs_owned_part` `PASS_CONDITIONAL_ON_Abar_EXISTENCE`: delta_A Abar(q_obs)=D Abar[Dq_obs(E_A)]=0. Consequence: no physical EM leakage from the quotient-owned part
- `AVD3780_1_gauge_part` `PASS_IF_PARENT_U1_GAUGE_SIGNED`: delta_A dLambda=d(delta_A Lambda). Consequence: pure gauge, harmless for F and Hilbert stress
- `AVD3780_2_residue_part` `LIVE_RESIDUAL`: R_A := delta_A A_obs - d lambda_A. Consequence: physical non-gauge vertical EM potential residue
- `AVD3780_3_exact_zero_condition` `UNSIGNED`: R_A=0, or R_A=d sigma_A on the local patch. Consequence: closes A basicness and forces F vertical silence
- `AVD3780_4_wilson_obstruction` `UNSIGNED_TOPOLOGY_BOUND`: W_A(C)=int_C R_A. Consequence: flat but non-exact A residue can affect phases even when dR_A=0

## F Obstruction
- `FOD3780_0_exact_curvature_identity` `EXACT`: delta_A F_obs=dR_A. Residual: `epsilon_F_vertical=||dR_A||/||F_obs||`. Meaning: The entire F-basicness problem is dR_A.
- `FOD3780_1_local_closed_residue` `UNSIGNED`: dR_A=0. Residual: `must prove or bound`. Meaning: Locally sufficient for F vertical silence; A is pure gauge if H^1(U)=0.
- `FOD3780_2_harmonic_cycle_residue` `UNSIGNED_GLOBAL_OR_MESOSCOPIC_CAVEAT`: R_A=R_A^harm with dR_A=0 but int_C R_A != 0. Residual: `epsilon_Wilson=max_C |int_C R_A|/Phi0`. Meaning: F is silent but charged phases/Wilson loops can still see hidden fibre data.
- `FOD3780_3_source_pairing` `UNSIGNED_CURRENT_DESCENT_CAVEAT`: int sqrt(-g_eff) (nabla_a(Z_EM F^{ab})-J^b) R_{A,b}. Residual: `epsilon_JR`. Meaning: A non-gauge residue couples to Maxwell-current failure unless same-source Ward descent is signed.

## Z_EM and Action Leak
- `ZAD3780_0_ZEM_pullback` `UNSIGNED_ZERO_ROUTE`: Z_EM=Zbar_EM(q_obs) or Z_EM is superselected. Consequence: closes universal EM normalization leakage
- `ZAD3780_1_ZEM_perp` `EXACT_RESIDUAL_COEFFICIENT`: ln Z_EM=ln Zbar_EM(q_obs)+z_perp. Consequence: feeds WEP, clocks, Gdot, PPN, and material response
- `ZAD3780_2_action_variation` `EXACT_VERTICAL_ACTION_LEAK_FORM`: delta_A S_EM=-(1/4) int sqrt(-g_eff) beta_Z,A F^2 - (1/2) int sqrt(-g_eff) Z_EM F^{ab}(dR_A)_{ab} + boundary. Consequence: shows why beta_Z,A and dR_A are not bookkeeping; they move action and stress
- `ZAD3780_3_integrated_by_parts` `EXACT_CURRENT_PAIRING_SCHEMA`: delta_A S_EM=-(1/4) int sqrt(-g_eff) beta_Z,A F^2 + int sqrt(-g_eff) R_{A,b}(nabla_a(Z_EM F^{ab})-J^b) + boundary/source-exchange. Consequence: if Ward descent holds and R_A is gauge/exact, only beta_Z,A remains
- `ZAD3780_4_stress_variation` `EXACT_STRESS_LEAK_SCHEMA`: delta_A T_EM^{ab}=beta_Z,A zeta^A T_EM^{ab}+Z_EM[F^{a}{}_c(dR_A)^{bc}+F^{b}{}_c(dR_A)^{ac}-(1/2)g_eff^{ab}F_cd(dR_A)^{cd}]. Consequence: maps directly into local-GR source residuals

## Local Cohomology Guard
- `LCC3780_0_patch_contractible` local_use=`False`: H^1(U)=0 for the local patch used by the local-GR expansion. Status: `NOT_DOCUMENTED_IN_PARENT_CORPUS`. Consequence: needed to turn dR_A=0 into R_A=d sigma_A
- `LCC3780_1_boundary_wilson_silence` local_use=`False`: all relevant Wilson cycles either absent, fixed as boundary data, or q_obs-owned. Status: `NOT_DOCUMENTED_IN_PARENT_CORPUS`. Consequence: needed to prevent flat A residues from becoming phase observables
- `LCC3780_2_charge_sector_superselection` local_use=`False`: charge labels and EM phase normalization are q_obs-owned or superselected. Status: `NOT_DOCUMENTED_IN_PARENT_CORPUS`. Consequence: needed to keep Z_EM/charge normalization from becoming composition dependence
- `LCC3780_3_local_result_safe` local_use=`True`: for simply-connected weak-field laboratory/solar-system patches, the local proof can ignore global Wilson sectors if the boundary data are fixed. Status: `CONDITIONAL_LOCAL_SIMPLIFICATION`. Consequence: lets local PPN/Newton work proceed while global/topological EM remains a separate bound row

## Residual Bound Vector
- `EVB3780_0_A_perp` `epsilon_A_perp`: inf_lambda ||Lie_EA A_obs-dlambda_A||/||A_obs|| = ||R_A||/||A_obs|| <= `MISSING_PARENT_A_RESIDUE` `dimensionless_or_field_norm`. Arena: gauge/current conservation
- `EVB3780_1_F_vertical` `epsilon_F_vertical`: ||dR_A||/||F_obs|| <= `MISSING_PARENT_DRA_NORM` `dimensionless`. Arena: EM stress; Newton GM; PPN
- `EVB3780_2_Wilson` `epsilon_Wilson`: max_C |int_C R_A|/Phi0 <= `MISSING_WILSON_OR_H1_CERTIFICATE` `dimensionless`. Arena: charged phase; quantum/EM sectors
- `EVB3780_3_ZEM` `epsilon_ZEM`: |beta_Z,A zeta^A| <= `MISSING_ZEM_SUPERSELECTION_OR_BETA_ZERO` `dimensionless`. Arena: WEP; clocks; Gdot; PPN
- `EVB3780_4_SEM` `epsilon_SEM_vertical`: |delta_A S_EM|/|S_EM| <= `MISSING_VERTICAL_ACTION_SILENCE` `dimensionless`. Arena: same-source Hilbert stress
- `EVB3780_5_WEP` `eta_EM_AB`: C_Z epsilon_ZEM + C_F epsilon_F_vertical + C_A epsilon_A_perp + C_mat epsilon_EM_material <= `2.8e-15` `dimensionless`. Arena: WEP
- `EVB3780_6_gamma` `delta_gamma_EM`: C_g epsilon_EM_shadow_metric + C_q Delta_q_EM + C_F epsilon_F_vertical <= `2.3e-05` `dimensionless`. Arena: PPN gamma
- `EVB3780_7_beta` `delta_beta_EM`: C_beta_Z epsilon_ZEM + C_beta_F epsilon_F_vertical + C_beta_mat epsilon_EM_material <= `7.8e-05` `dimensionless`. Arena: PPN beta
- `EVB3780_8_Gdot` `dln_Geff_dt_EM`: |d_t ln Z_EM| + |d_t epsilon_F_vertical| + source-exchange rate <= `9.6e-15` `yr^-1`. Arena: Gdot

## Claim Gates
- `CG3780_0_sources` pass=`True` claim_allowed=`False`: all cited 3778/3779/qobs source paths exist. Details: source register checked
- `CG3780_1_derivation` pass=`True` claim_allowed=`False`: vertical A/F/ZEM derivation emitted. Details: A split, F=dR_A, Z coefficient, and action leak emitted
- `CG3780_2_pullback_route` pass=`True` claim_allowed=`False`: constructive pullback-connection zero route emitted. Details: A=Abar(q_obs)+dLambda suffices
- `CG3780_3_A_residue` pass=`False` claim_allowed=`False`: A non-gauge residue zeroed. Details: R_A remains parent-unsigned
- `CG3780_4_F_residue` pass=`False` claim_allowed=`False`: F vertical residue zeroed. Details: dR_A remains parent-unsigned
- `CG3780_5_ZEM` pass=`False` claim_allowed=`False`: Z_EM beta coefficient zeroed. Details: beta_Z,A remains parent-unsigned
- `CG3780_6_EM_local_GR_claim` pass=`False` claim_allowed=`False`: EM local-GR descent claim allowed. Details: blocked until R_A, dR_A, Wilson, beta_Z,A, current, and metric clauses are signed or bounded

## Decisions
- `DEC3780_0`: The EM problem has been reduced to a connection-descent problem. Action: Try to construct A_obs as a U(1) connection over q_obs, with hidden-fibre changes acting only as gauge transformations.
- `DEC3780_1`: The real obstruction is R_A, not the word coupling. Action: Either prove R_A is exact/zero on local patches or carry epsilon_A_perp, epsilon_F_vertical, and epsilon_Wilson into WEP/PPN/source bounds.
- `DEC3780_2`: Z_EM is the normalization throat. Action: Do not claim universal EM unless beta_Z,A=0, Z_EM is superselected, or a sourced bound beats WEP/clock/Gdot limits.
- `DEC3780_3`: Poynting/wave energy is not an enemy of the route. Action: If EM descends as the same q_obs Maxwell sector, Poynting is internal total Hilbert stress; otherwise it remains Q_EM_Poynting or a flux residual.
- `DEC3780_4`: Next route should be constructive, not another blocker inventory. Action: Attempt the principal-bundle/flow-phase construction of the EM connection from MTS variables.

## Next Target
- `3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md`: Try to construct A_obs as a q_obs U(1) connection generated by MTS flow/phase data; prove vertical changes are pure gauge and Z_EM is superselected, or emit RA/betaZ bounds.

## Validation
- `sources_exist` `PASS`: every cited source path exists
- `csv_outputs_parse` `PASS`: all generated CSV outputs exist and parse
- `doc_written` `PASS`: 3780 markdown document written
- `a_split` `PASS`: A variation split emitted
- `f_derivation` `PASS`: F=dR_A obstruction emitted
- `zem_beta` `PASS`: beta_Z,A coefficient emitted
- `action_leak` `PASS`: vertical EM action leak emitted
- `cohomology_guard` `PASS`: Wilson/cohomology guard emitted
- `nonclaim_bounds` `PASS`: missing parent rows remain nonclaim
- `claim_gate_closed` `PASS`: EM/local-GR claim gate remains closed
- `next_target` `PASS`: 3781 constructive EM connection target emitted
- `formalization_clean` `PASS`: no 3780 files written under formalization-workbench
