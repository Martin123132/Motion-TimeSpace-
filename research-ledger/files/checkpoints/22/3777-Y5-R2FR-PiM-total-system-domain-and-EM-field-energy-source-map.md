# 3777 - Pi_M Total-System Domain And EM Field-Energy Source Map

## Status

`PIM_TOTAL_CONDITIONAL_PROJECTOR_AND_EM_FIELD_SOURCE_MAP_DERIVED_NOT_PARENT_SIGNED`.

3777 constructs the conditional Pi_M_total projector and total-system domain map. It defines total mass as the observed-time projection of total Hilbert stress over matter, EM field support, binding, apparatus, interaction, and source/theta support, with explicit no-double-counting against mu_extra. It separates EM cases into neutral tail, net charge tail, stationary Poynting, radiative flux, and material response. Current MTS still cannot claim measured-GM closure because EM parent descent, tail/flux certificates, theta/source normalization, and total boundary flux are unsigned.

## Result In Plain Terms

3777 turns `Pi_M_total` from a phrase into a conditional construction. The total source is the observed-time projection of total Hilbert stress over a total-system domain. Matter-only mass is not enough when EM fields, Poynting momentum, binding, apparatus, or source-normalization support are part of the physical system. Anything included in `M_H,total` is removed from `mu_extra`; anything not included stays as a bound row.

## Pi_M Total Projector Construction
- `PIM3777_0_observed_time_charge` `SETUP_REQUIRED`: Choose the same observed time generator xi/tau_obs used by the Hamiltonian/Gauss charge and slow-orbit readout. Meaning: If the mass projector uses a different time, M_H,total can differ from the orbital monopole by a frame/readout residual.
- `PIM3777_1_total_current` `EXACT_CONDITIONAL_TOTAL_CURRENT_DEFINITION`: Define J_M,total^a[xi] := -(T_total^{a}{}_{b} xi^b)/c^2 for the descended total Hilbert stress T_total=T_matter+T_EM+T_binding+T_apparatus+T_int. Meaning: This is the total active mass-energy current. EM/Poynting is included through T_EM, not by adding a separate fifth-force charge.
- `PIM3777_2_projector_definition` `EXACT_CONDITIONAL_PROJECTOR_DEFINITION`: Pi_M_total maps a q_obs source history to M_H,total[W,Sigma,xi] = int_{Sigma cap D_total(W)} n_a J_M,total^a[xi] dSigma plus declared finite tail terms that are not cut by D_total. Meaning: The projector is a bookkeeping map from total stress to monopole source charge; it is not an empirical fit of GM.
- `PIM3777_3_domain_closure` `EXACT_TOTAL_SYSTEM_DOMAIN_RULE`: D_total must include matter support, descended EM field support assigned to the source, binding/interaction support, apparatus/readout support, and source/theta normalization support up to a boundary where total flux is zero or bounded. Meaning: This prevents matter-only cuts from manufacturing Q_EM_Poynting or Q_source_theta.
- `PIM3777_4_no_double_counting` `EXACT_NO_DOUBLE_COUNTING_RULE`: Any stress included in M_H,total must be removed from mu_extra; any stress not included must stay in a named Q_i row with a bound. Meaning: The same field energy cannot be both source mass and extra monopole.
- `PIM3777_5_conservation_condition` `EXACT_CONDITIONAL_CLOSED_TOTAL_FLUX_THEOREM`: If xi is stationary/Killing in the local exterior, total source descent holds, parent exchange is silent, and the total-domain side flux vanishes, then d(Pi_M_total J_M,total)=0 outside the chosen total source. Meaning: This is the bridge from source projector to Hamiltonian/Gauss equality.
- `PIM3777_6_measured_GM_condition` `EXACT_CONDITIONAL_MEASURED_GM_PROMOTION`: If PIM3777_1 through PIM3777_5 are parent-signed and the 3773 Hamiltonian/Gauss charge equality uses Pi_M_total, then mu_obs=G_eff M_H,total up to the remaining non-total-source Q_i channels. Meaning: This is the constructive measured-GM route after rejecting matter-only mass.

## Total-System Domain Rules
- `TSD3777_0_matter_core` `matter core` action=`included`: material rest mass, kinetic energy, pressure/internal stress, and matter charge current support Status: `MISSING_PARENT_SIGNED_QOBS_MATTER_SOURCE_DOMAIN`.
- `TSD3777_1_EM_near_field` `EM near field` action=`included_if_descended`: Coulomb/magnetic/dipole near-field energy and stress assigned to the same source system Status: `MISSING_EM_DESCENT_AND_NEAR_FIELD_DOMAIN`.
- `TSD3777_2_EM_tail` `EM exterior tail` action=`include_or_bound`: long-range field energy outside the practical source surface; neutral multipole tails may be bounded by E_tail(R)/M_H c^2, net-charge tails require explicit treatment Status: `MISSING_EM_TAIL_CLASS_AND_BOUND`.
- `TSD3777_3_Poynting_flux` `Poynting flux/momentum` action=`include_and_check_flux`: stationary circulating field momentum belongs to T_EM; radiative or nonstationary flux through the boundary must be zero or bounded Status: `MISSING_POYNTING_BOUNDARY_FLUX_CERTIFICATE`.
- `TSD3777_4_binding_interaction` `binding and interaction stress` action=`included_if_descended`: EM/nuclear/material binding and interaction stress that changes inertial and active mass Status: `MISSING_BINDING_INTERACTION_SOURCE_DESCENT`.
- `TSD3777_5_apparatus_readout` `apparatus/readout support` action=`include_or_exclude_with_readout_bound`: readout devices, clock support, and calibration stress only when they are part of the measured source system Status: `MISSING_APPARATUS_DOMAIN_DECLARATION`.
- `TSD3777_6_theta_source_norm` `source/theta normalization support` action=`included_if_superselected_or_qobs_owned`: constant/material-marker source normalization that fixes active/passive/inertial mass equality Status: `MISSING_THETA_SOURCE_NORMALIZATION_DESCENT`.
- `TSD3777_7_boundary_surface` `total-domain boundary` action=`zero_or_bound_flux`: boundary selected so n_a T_total^{ab} xi_b has no unowned side flux, or the flux is a named residual Status: `MISSING_TOTAL_DOMAIN_WALL_FLUX_CERTIFICATE`.

## EM Field-Energy Source Map
- `ESM3777_0_descended_Maxwell` `descended Maxwell field` -> `M_H,total`: T_EM^{ab}=Z_EM(F^{a c}F^b_c - 1/4 g_eff^{ab}F^2) Condition: requires MTS parent descent to same q_obs Maxwell Hilbert stress. Status: `MISSING_MTS_EM_MAXWELL_DESCENT`.
- `ESM3777_1_neutral_bound_source` `neutral bound source` -> `M_H,total plus tail bound`: near-field EM/binding energy plus multipole tail Condition: tail energy must be included up to boundary or bounded by E_tail(R)/M_H c^2. Status: `MISSING_NEUTRAL_EM_TAIL_BOUND`.
- `ESM3777_2_net_charge_source` `net charged source` -> `explicit field-domain problem`: Coulomb 1/r field with field energy outside every finite material radius Condition: not safe as compact local source unless total field energy/renormalization and boundary convention are signed. Status: `MISSING_NET_CHARGE_FIELD_ENERGY_RENORMALIZATION_OR_BOUND`.
- `ESM3777_3_magnetic_stationary` `stationary magnetic/source current` -> `M_H,total if same action and no net boundary flux`: magnetic field energy and possible circulating Poynting momentum Condition: T_EM^{0i} is included; net Poynting flux through boundary must vanish or be bounded. Status: `MISSING_STATIONARY_POYNTING_FLUX_CERTIFICATE`.
- `ESM3777_4_radiative_EM` `radiative EM field` -> `not closed source mass without flux term`: outgoing/incoming radiation crossing source boundary Condition: radiation flux is a time-dependent source exchange term, not a static Newton GM mass. Status: `MISSING_RADIATIVE_FLUX_BOUND`.
- `ESM3777_5_material_response` `material response/binding markers` -> `M_H,total if theta/source markers descend`: polarization, magnetization, nuclear/EM binding fractions, and material coefficients Condition: otherwise composition-dependent WEP/clock/Newton residual. Status: `MISSING_MATERIAL_RESPONSE_THETA_DESCENT`.

## Closure Attempt
- `PCA3777_0_projector_defined` pass=`True`: Pi_M_total has a precise conditional definition. Evidence: PIM3777_2 emitted. Consequence: construction route exists.
- `PCA3777_1_domain_rules_defined` pass=`True`: total-system domain rules cover matter, EM, tail, Poynting, binding, apparatus, theta, and boundary. Evidence: TSD3777_0 through TSD3777_7 emitted. Consequence: source support map is explicit.
- `PCA3777_2_no_double_counting` pass=`True`: included stress is removed from mu_extra and excluded stress remains Q_i. Evidence: PIM3777_4 emitted. Consequence: bookkeeping trap is closed at formula level.
- `PCA3777_3_EM_parent_descent` pass=`False`: MTS parent signs low-energy EM descends to universal Maxwell Hilbert stress. Evidence: 3760 EMT3760_4 still unsigned. Consequence: Pi_M_total cannot yet claim EM inclusion.
- `PCA3777_4_EM_tail_bound` pass=`False`: EM exterior tail class and energy bound are supplied. Evidence: ESM3777_1/2/3/4 remain missing tail/flux certificates. Consequence: Q_EM_Poynting remains live.
- `PCA3777_5_theta_domain` pass=`False`: source/theta normalization support descends or is superselected. Evidence: 3771 CMT3771_2 remains parent-unsigned. Consequence: Q_source_theta remains live.
- `PCA3777_6_boundary_flux` pass=`False`: total-domain boundary has zero or bounded side flux. Evidence: TSD3777_7 remains missing wall-flux certificate. Consequence: domain-wall residual remains live.
- `PCA3777_7_verdict` pass=`False`: current branch closes Pi_M_total for measured GM. Evidence: projector/domain construction exists but EM descent, tail bounds, theta silence, and boundary flux are unsigned. Consequence: do not claim Newton/local-GR closure.

## Field/Domain Bound Vector
- `FDB3777_0_EM_tail` `epsilon_EM_tail`: E_EM_tail(R)/(M_H,total c^2) <= `MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND` `dimensionless`. Feeds: Newton GM; radial hair; WEP.
- `FDB3777_1_Poynting_flux` `epsilon_Poynting_flux`: |int_boundary S_EM dot dA dt|/(M_H,total c^2) <= `MISSING_POYNTING_FLUX_BOUND` `dimensionless_or_rate`. Feeds: Gdot; source conservation; radiation.
- `FDB3777_2_total_domain_wall` `epsilon_total_domain_wall`: |int_wall n_a T_total^{ab} xi_b|/M_H,total <= `MISSING_TOTAL_DOMAIN_WALL_FLUX_BOUND` `dimensionless`. Feeds: Hamiltonian/Gauss; radial hair.
- `FDB3777_3_theta_source_norm` `epsilon_theta_source_norm`: |delta M_source_norm|/M_H,total <= `MISSING_THETA_SOURCE_NORMALIZATION_DESCENT_OR_BOUND` `dimensionless`. Feeds: Newton GM; WEP; clock.
- `FDB3777_4_WEP_domain` `eta_domain_AB`: C_EM epsilon_EM_tail + C_theta epsilon_theta_source_norm + C_mat epsilon_material_response <= `2.8e-15` `dimensionless`. Feeds: WEP.
- `FDB3777_5_gamma_domain` `delta_gamma_domain`: C_gamma_EM epsilon_EM_tail + C_gamma_domain epsilon_total_domain_wall <= `2.3e-05` `dimensionless`. Feeds: PPN gamma.
- `FDB3777_6_beta_domain` `delta_beta_domain`: C_beta_EM epsilon_EM_tail + C_beta_theta epsilon_theta_source_norm + C_beta_bound epsilon_binding <= `7.8e-05` `dimensionless`. Feeds: PPN beta.

## Claim Gates
- `CG3777_0_sources` pass=`True`: all 3777 source paths exist - path hygiene
- `CG3777_1_projector_defined` pass=`True`: Pi_M_total conditional projector is defined - constructive route exists
- `CG3777_2_domain_rules` pass=`True`: total-system domain rules cover required support classes - matter-only tube replaced by total-domain map
- `CG3777_3_EM_source_map` pass=`True`: EM field classes are mapped to include/bound decisions - neutral, charged, stationary, radiative, material-response cases separated
- `CG3777_4_no_double_counting` pass=`True`: no-double-counting rule emitted - stress cannot be both M_H,total and mu_extra
- `CG3777_5_current_closure` pass=`False`: current branch closes Pi_M_total for measured GM - expected false until EM descent/tail/theta/flux certificates exist
- `CG3777_6_missing_bounds_nonclaim` pass=`True`: missing field/domain bounds remain blockers - no pass from placeholder tail/domain rows
- `CG3777_7_Newton_GM_claim` pass=`False`: measured-GM Newton claim allowed - blocked until Pi_M_total clauses close or bounds are numeric
- `CG3777_8_local_GR_claim` pass=`False`: local GR claim allowed - blocked until total source, EH operator, charge equality, and readout close

## Decisions
- `DEC3777_0`: Pi_M_total is now an explicit conditional projector over total Hilbert stress and a declared total-system domain, not a vague same-source phrase. Action: use PIM3777_2/PIM3777_3 as the source-normalization contract.
- `DEC3777_1`: EM field support must be classified: neutral bound tails, net charge tails, stationary Poynting momentum, and radiative flux have different closure/bound rules. Action: do not treat all EM stress as one generic residual.
- `DEC3777_2`: No double counting is mandatory: stress included in M_H,total must be removed from mu_extra; stress not included must remain a named Q_i bound. Action: protect the measured-GM bridge from fitted bookkeeping.
- `DEC3777_3`: The next physical proof target is MTS-to-Maxwell Hilbert descent with universal Z_EM and source/tail domain certificates. Action: attack EM descent and tail/flux bounds next.

## Next Target
- `3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md`: derive whether the MTS EM sector descends to universal Maxwell Hilbert stress with source-domain/tail certificates; if not, emit explicit EM field-energy, Poynting-flux, and material-response bounds

## Validation
- `sources_exist` `PASS`: all 3777 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3777 csvs parse
- `projector_defined` `PASS`: Pi_M_total projector definition emitted
- `domain_closure` `PASS`: total-system domain rule emitted
- `no_double_counting` `PASS`: no-double-counting rule emitted
- `domain_classes` `PASS`: eight total-system domain support classes emitted
- `em_classes` `PASS`: six EM/source classes emitted
- `net_charge_flagged` `PASS`: net charge field-energy case remains explicit
- `radiative_flux_flagged` `PASS`: radiative EM flux case remains explicit
- `closure_not_claimed` `PASS`: current branch does not close Pi_M_total
- `bounds_nonclaim` `PASS`: missing field/domain bounds remain nonclaim
- `claim_gates_closed` `PASS`: Newton/local-GR claims remain closed
- `next_target` `PASS`: 3778 EM descent/tail target emitted
- `no_formalization_leak` `PASS`: no 3777 files written to formalization-workbench
