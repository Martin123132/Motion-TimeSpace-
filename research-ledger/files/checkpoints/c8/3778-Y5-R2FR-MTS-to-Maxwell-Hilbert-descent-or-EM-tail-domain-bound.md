# 3778 - MTS To Maxwell Hilbert Descent Or EM Tail Domain Bound

## Status

`MTS_TO_MAXWELL_HILBERT_DESCENT_CONTRACT_DERIVED_EM_TAIL_BOUNDS_EMITTED_NOT_PARENT_SIGNED`.

3778 derives the exact contract for the MTS EM sector to become ordinary Maxwell Hilbert stress inside Pi_M_total. It requires q_obs-owned A_mu/F, U(1) gauge redundancy, Maxwell kinetic form in g_eff, universal Z_EM, same-source charged current, no EM shadow metric, no unbounded extra EM modes, and source-domain/tail certificates. It also emits explicit EM field-tail, net-charge, dipole, Poynting-flux, material-response, WEP, PPN, and Gdot bound rows. Current MTS does not claim EM/local-GR closure because all parent signatures remain unsigned.

## Result In Plain Terms

3778 pins down the EM bridge. To count EM as ordinary GR-like source mass, MTS must deliver a q_obs-owned Maxwell sector: one A_mu/F, U(1) gauge structure, Maxwell kinetic term in g_eff, universal Z_EM, same-source matter current, no EM shadow metric, no unbounded extra EM modes, and field-tail/domain certificates. If any part fails, EM stays as explicit tail, flux, material-response, WEP, PPN, Gdot, or Newton-GM residuals.

## Maxwell Hilbert Descent Theorem
- `MHD3778_0_low_energy_EM_variable` `EXACT_DESCENT_REQUIREMENT`: An MTS EM sector descends to Maxwell only if the observed electromagnetic readout is a q_obs-owned 1-form A_mu with field strength F=dA and gauge redundancy A -> A+dlambda. Meaning: Gauge redundancy prevents an extra longitudinal charge from becoming a hidden source mass or WEP channel.
- `MHD3778_1_Maxwell_action` `EXACT_CONDITIONAL_ACTION_FORM`: The low-energy action must reduce to S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab plus terms that are topological, higher-order, compactly supported, or explicitly bounded. Meaning: This is the unique local two-derivative gauge-invariant Maxwell stress route in the same observed metric/coframe.
- `MHD3778_2_Hilbert_stress` `EXACT_CONDITIONAL_HILBERT_STRESS`: If MHD3778_1 holds, variation with respect to g_eff gives T_EM^{ab}=Z_EM(F^{a c}F^b_c - (1/4)g_eff^{ab}F_cd F^cd), and this is the EM piece of T_total. Meaning: This imports the 3760 standard identity but ties it to MTS descent and Pi_M_total.
- `MHD3778_3_universal_normalization` `EXACT_UNIVERSALITY_REQUIREMENT`: Z_EM and charge/current normalization must be q_obs-owned or superselected, not species-, material-, frame-, or environment-labelled. Meaning: Otherwise EM binding and material response produce WEP, clock, PPN, and source-normalization residuals.
- `MHD3778_4_no_extra_EM_modes` `EXACT_RESIDUAL_EXCLUSION_RULE`: Massive Proca terms, disformal EM metrics, birefringent light cones, nonminimal RF^2 couplings, axion-like F wedge F readout effects, or hidden carrier stress must vanish or be bounded. Meaning: Any such term is not ordinary Maxwell Hilbert stress and must remain an explicit residual owner.
- `MHD3778_5_Ward_total_source` `EXACT_CONDITIONAL_WARD_THEOREM`: With one descended matter+EM action, nabla_a T_EM^{ab}=-F^b_c J^c cancels the matter Lorentz force inside nabla_a T_total^{ab}; only parent exchange or non-Hilbert owner currents remain. Meaning: This is the EM reason same-source descent can look GR-like locally.
- `MHD3778_6_tail_domain_law` `EXACT_DOMAIN_BOUND_LAW`: Even if Maxwell descent holds, EM field energy outside a chosen material radius contributes to M_H,total unless the source domain includes it or a tail/flux bound is supplied. Meaning: Maxwell descent fixes the stress tensor; it does not automatically make finite source domains safe.
- `MHD3778_7_local_GR_promotion` `EXACT_CONDITIONAL_EM_LOCAL_GR_PROMOTION`: If MHD3778_0 through MHD3778_6 hold, EM/Poynting contributes only as ordinary total Hilbert stress in Pi_M_total, and EM-owned mu_extra rows close except declared finite tail/flux bounds. Meaning: This is a local-GR-compatible EM source theorem, still conditional on parent signatures.

## MTS EM Descent Clause Audit
- `MCA3778_0_qobs_A` pass=`False`: A_mu and F=dA are q_obs-owned observed fields. Status: `MISSING_MTS_QOBS_EM_READOUT_CERTIFICATE`. Consequence: without it EM can use a shadow frame/source.
- `MCA3778_1_gauge_invariance` pass=`False`: U(1) gauge redundancy and current conservation hold in the local branch. Status: `MISSING_PARENT_GAUGE_INVARIANCE_CERTIFICATE`. Consequence: without it longitudinal/source leakage remains.
- `MCA3778_2_Maxwell_kinetic` pass=`False`: two-derivative low-energy kinetic term is -1/4 Z_EM F^2 in g_eff. Status: `MISSING_MTS_TO_MAXWELL_KINETIC_DERIVATION`. Consequence: without it stress need not be Maxwell Hilbert stress.
- `MCA3778_3_universal_ZEM` pass=`False`: Z_EM and charge normalization are universal/q_obs-owned/superselected. Status: `MISSING_UNIVERSAL_ZEM_SUPERSELECTION`. Consequence: without it WEP/clock/material response residuals remain.
- `MCA3778_4_same_source_matter` pass=`False`: charged matter current J^a comes from the same descended source action. Status: `MISSING_SAME_ACTION_CHARGED_MATTER_CURRENT`. Consequence: without it Lorentz exchange is not internal.
- `MCA3778_5_no_EM_shadow_metric` pass=`False`: EM light cone uses the same observed metric/coframe as matter/source readout. Status: `MISSING_NO_BIREFRINGENT_OR_DISFORMAL_EM_METRIC`. Consequence: without it gamma/frame/readout residuals remain.
- `MCA3778_6_no_extra_modes` pass=`False`: Proca/nonminimal/axion/hidden-carrier stress is zero or bounded. Status: `MISSING_EXTRA_EM_MODE_ZERO_OR_BOUND`. Consequence: without it EM mu_extra has extra owners.
- `MCA3778_7_tail_domain` pass=`False`: EM near/tail/flux support is included in Pi_M_total or bounded. Status: `MISSING_EM_TAIL_AND_FLUX_DOMAIN_CERTIFICATES`. Consequence: without it Maxwell stress still leaks through domain choice.
- `MCA3778_8_material_response` pass=`False`: polarization, magnetization, binding, and material coefficients descend or are bounded. Status: `MISSING_EM_MATERIAL_RESPONSE_DESCENT`. Consequence: without it WEP/clock/Newton source rows remain.
- `MCA3778_9_verdict` pass=`False`: current branch proves MTS-to-Maxwell Hilbert descent and EM tail/domain closure. Status: `CONDITIONAL_ROUTE_ONLY_PARENT_SIGNATURES_MISSING`. Consequence: do not claim EM/local-GR closure.

## EM Tail/Domain Formulas
- `ETF3778_0_general_tail` `general static EM tail`: E_EM_tail(R)=int_{r>R} [(epsilon0/2)|E|^2 + (1/(2 mu0))|B|^2] d^3x. Bound: `epsilon_EM_tail=E_EM_tail(R)/(M_H,total c^2)`. Use: requires field profile or multipole bound.
- `ETF3778_1_net_charge` `net electric charge`: E_tail^Q(R)=Q_net^2/(8*pi*epsilon0*R). Bound: `epsilon_Q_tail=Q_net^2/(8*pi*epsilon0*R*M_H,total*c^2)`. Use: not compact-source safe without boundary/renormalization convention.
- `ETF3778_2_electric_dipole` `electric dipole tail`: E_tail^p(R)=p^2/(12*pi*epsilon0*R^3). Bound: `epsilon_p_tail=p^2/(12*pi*epsilon0*R^3*M_H,total*c^2)`. Use: neutral multipole tail bound.
- `ETF3778_3_magnetic_dipole` `magnetic dipole tail`: E_tail^m(R)=mu0*m^2/(12*pi*R^3). Bound: `epsilon_m_tail=mu0*m^2/(12*pi*R^3*M_H,total*c^2)`. Use: stationary magnetic tail bound.
- `ETF3778_4_Poynting_flux` `Poynting flux through total-domain boundary`: Delta E_flux = int_dt int_boundary S_EM dot dA. Bound: `epsilon_flux=|Delta E_flux|/(M_H,total*c^2) or |P_flux|/(M_H,total*c^2)`. Use: radiative/nonstationary source exchange bound.
- `ETF3778_5_material_response` `material EM response`: delta ln M_EM_binding = sum_I K_I^EM delta ln theta_I + response-domain terms. Bound: `eta_EM_AB <= |Delta_AB f_EM||delta_kappa_EM| + |Delta_AB ln Z_EM| + material response residuals`. Use: WEP/clock/source-normalization bound interface.

## EM Descent And Tail Bound Vector
- `EDB3778_0_descent` `epsilon_EM_descent`: norm[S_EM^MTS - S_Maxwell(q_obs)] projected into local source sector <= `MISSING_PARENT_EM_ACTION_DESCENT_NORM` `dimensionless_or_action_norm`. Feeds: Newton GM; PPN; WEP.
- `EDB3778_1_ZEM` `epsilon_ZEM`: |delta ln Z_EM| plus species/material/frame dependence <= `MISSING_UNIVERSAL_ZEM_VALUE_OR_BOUND` `dimensionless`. Feeds: WEP; clocks; EM coupling drift.
- `EDB3778_2_shadow_metric` `epsilon_EM_shadow_metric`: norm[g_EM-g_eff] or birefringent/disformal readout projection <= `MISSING_EM_SHADOW_METRIC_BOUND` `dimensionless`. Feeds: PPN gamma; light; frame.
- `EDB3778_3_extra_modes` `epsilon_EM_extra_modes`: Proca + nonminimal RF^2 + axion/readout + hidden-carrier stress projections <= `MISSING_EXTRA_EM_MODE_BOUND` `dimensionless`. Feeds: Newton GM; PPN; polarization.
- `EDB3778_4_tail` `epsilon_EM_tail`: E_EM_tail(R)/(M_H,total c^2) <= `MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND` `dimensionless`. Feeds: Newton GM; radial hair; WEP.
- `EDB3778_5_flux` `epsilon_Poynting_flux`: |int S_EM dot dA dt|/(M_H,total c^2) <= `MISSING_POYNTING_OR_RADIATIVE_FLUX_BOUND` `dimensionless_or_rate`. Feeds: Gdot; source conservation.
- `EDB3778_6_material_response` `epsilon_EM_material_response`: polarization/magnetization/binding/material marker response residual <= `MISSING_EM_MATERIAL_RESPONSE_COEFFICIENTS` `dimensionless`. Feeds: WEP; clock; source mass.
- `EDB3778_7_WEP` `eta_EM_AB`: |Delta_AB f_EM||delta_kappa_EM| + |Delta_AB ln Z_EM| + |Delta_AB q_EM_exchange| + material response <= `2.8e-15` `dimensionless`. Feeds: WEP.
- `EDB3778_8_gamma` `delta_gamma_EM`: |epsilon_EM_metric| + |Pi_PPN q_EM_exchange| + |Delta_EM_source_frame| <= `2.3e-05` `dimensionless`. Feeds: PPN gamma.
- `EDB3778_9_beta` `delta_beta_EM`: |epsilon_EM_nonlinear| + |Delta_EM_binding_second_order| + |Pi_beta q_EM_exchange| <= `7.8e-05` `dimensionless`. Feeds: PPN beta.
- `EDB3778_10_Gdot` `dln_Geff_dt_EM`: |d_t ln Z_EM| + |R_EM_exchange| + |d_t ln Z_EM_frame| <= `9.6e-15` `yr^-1`. Feeds: Gdot/source drift.

## Observable Projection Matrix
- `EOM3778_0_Newton_GM` `delta_ln_mu_obs|EM`: epsilon_EM_descent + epsilon_EM_tail + epsilon_Poynting_flux + epsilon_EM_material_response + epsilon_EM_extra_modes <= `MISSING_COMPONENT_VALUES`. Arena: Newton/orbital GM.
- `EOM3778_1_WEP` `eta_EM_AB`: composition projection of Z_EM/material response/binding/tail residuals <= `2.8e-15`. Arena: WEP.
- `EOM3778_2_PPN_gamma` `delta_gamma_EM`: EM metric/readout/source-frame projection <= `2.3e-05`. Arena: PPN gamma.
- `EOM3778_3_PPN_beta` `delta_beta_EM`: EM nonlinear/binding/source projection <= `7.8e-05`. Arena: PPN beta.
- `EOM3778_4_Gdot` `dln_Geff_dt_EM`: time drift of Z_EM/exchange/frame source calibration <= `9.6e-15 yr^-1`. Arena: Gdot.
- `EOM3778_5_radial_hair` `partial_r_ln_mu_obs|EM`: partial_r epsilon_EM_tail + partial_r domain-wall/flux terms <= `MISSING_RADIAL_TAIL_PROFILE`. Arena: radial/source profile.
- `EOM3778_6_clocks` `delta_ln_clock_ratio|EM`: clock/material sensitivities to alpha/Z_EM/binding response <= `MISSING_CLOCK_RESPONSE_COEFFICIENTS`. Arena: clock/constant drift.

## Claim Gates
- `CG3778_0_sources` pass=`True`: all 3778 source paths exist - path hygiene
- `CG3778_1_descent_theorem` pass=`True`: Maxwell Hilbert descent theorem emitted - EM closure route is exact and conditional
- `CG3778_2_clause_audit` pass=`True`: all descent clauses are audited - q_obs A, gauge, Maxwell kinetic, Z_EM, same current, shadow metric, extra modes, tail/domain, material response, verdict
- `CG3778_3_tail_formulas` pass=`True`: EM tail/flux formulas emitted - field energy bounds have explicit formula owners
- `CG3778_4_net_charge_flagged` pass=`True`: net charge long-range field case remains explicit - not smuggled into compact source
- `CG3778_5_current_descent_claim` pass=`False`: current branch proves MTS-to-Maxwell Hilbert descent - expected false until parent signatures exist
- `CG3778_6_missing_bounds_nonclaim` pass=`True`: missing EM residual bounds remain blockers - no pass from placeholder EM coefficients
- `CG3778_7_EM_local_GR_claim` pass=`False`: EM part of local GR claim allowed - blocked until descent and tail/domain bounds close

## Decisions
- `DEC3778_0`: MTS-to-Maxwell descent requires q_obs-owned A_mu, U(1) gauge structure, Maxwell kinetic term, universal Z_EM, same-source charged current, no EM shadow metric, no extra unbounded EM modes, and tail/domain certificates. Action: use the 3778 clause audit as the EM parent-signature contract.
- `DEC3778_1`: Maxwell descent alone is insufficient for compact-source measured GM because EM field energy can live outside a material radius. Action: always pair EM descent with tail/domain bounds.
- `DEC3778_2`: Net charged sources are not compact local-GR sources by default; their Coulomb tail requires explicit boundary/renormalization treatment. Action: keep net-charge tail rows nonclaim until a convention or bound is supplied.
- `DEC3778_3`: The next best constructive route is to build the q_obs-owned EM readout/gauge certificate and universal Z_EM superselection test. Action: attack q_obs A_mu and Z_EM before fitting EM residuals.

## Next Target
- `3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md`: construct or reject the q_obs-owned EM readout/gauge certificate and universal Z_EM superselection needed for MTS-to-Maxwell Hilbert descent

## Validation
- `sources_exist` `PASS`: all 3778 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3778 csvs parse
- `descent_theorem` `PASS`: MTS-to-Maxwell Hilbert descent theorem emitted
- `clause_audit` `PASS`: ten EM descent clauses emitted
- `tail_formulas` `PASS`: six EM tail/domain formulas emitted
- `net_charge_formula` `PASS`: net charge tail formula emitted
- `poynting_formula` `PASS`: Poynting flux formula emitted
- `material_response` `PASS`: material response formula emitted
- `no_descent_claim` `PASS`: current branch does not claim EM descent
- `bounds_nonclaim` `PASS`: missing EM bounds remain nonclaim
- `numeric_envelopes` `PASS`: WEP/PPN/Gdot envelopes imported
- `claim_gates_closed` `PASS`: EM local-GR claim remains closed
- `next_target` `PASS`: 3779 qobs EM/ZEM certificate target emitted
- `no_formalization_leak` `PASS`: no 3778 files written to formalization-workbench
