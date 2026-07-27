# 3907 - Gstar from MTS Scales or Measured Coupling Policy Runner

Generated: `2026-07-01T09:45:25+00:00`

## Result

3907 tries the direct `G_*` derivation route and rejects it for now.

Candidate map:

`kappa_* ?= N_top * kappa_MTS * w_common * ell_J * R_frame * C_extra`

No-cheat lemma:

`local GR/Newton reduction fixes only the product kappa_* T_H; an absolute value for G_* is underdetermined until a parent action normalization, source-current unit, and Hilbert mass calibration are independently fixed`

Measured-coupling policy:

`G_* may be a measured superselected coupling: claim derivative/source/range silence if proved, but do not claim prediction of the numerical value of G`

Verdict: the current corpus can own `G_*` as a constant low-energy coupling, but cannot honestly claim to predict its numerical value. This is not fatal: GR also measures `G`. The real MTS local-test obligation is now sharper: prove or bound all derivatives and hidden source-dependences of `G_*`.

## Gstar Scale Candidate Map

| row_id | candidate | meaning | status | failure |
| --- | --- | --- | --- | --- |
| GMAP3907_0_product | kappa_* ?= N_top * kappa_MTS * w_common * ell_J * R_frame * C_extra | only known plausible product chain joining EH coupling, source-current normalization, action scale and frame/source factors | CANDIDATE_MAP_NOT_DERIVED | N_top, kappa_MTS, w_common, ell_J, R_frame and C_extra are not all parent-owned with units and no fitted-GM dependence |
| GMAP3907_1_ellJ | ell_J fixes current normalization J_M=ell_J T_H[tau] | ell_J can cancel in Hilbert mass readout only if fixed before readout and not fitted from orbital GM | CONDITIONAL_FACTOR_UNSIGNED | Pi_M/H_tau/reference/frame chain still carries residuals |
| GMAP3907_2_kappa | kappa_MTS or kappa_* as parent action prefactor | can own the GR coupling but does not compute its value without a normalization law | OWNER_NOT_VALUE_DERIVATION | no inspected source supplies kappa_*=F(MTS primitive scales) |
| GMAP3907_3_topological | N_top/topological charge fixes absolute normalization | would be the strongest route because an integer/cohomology class could remove continuous fitting | OPEN_NO_SOURCE_ROW | current rows use topological/source class conditionally but not as an absolute G normalization |

## Gstar Underdetermination Lemma

| lemma_id | statement | proof_sketch | consequence | status |
| --- | --- | --- | --- | --- |
| NG3907_0_statement | local GR/Newton reduction fixes only the product kappa_* T_H; an absolute value for G_* is underdetermined until a parent action normalization, source-current unit, and Hilbert mass calibration are independently fixed | rescale kappa_* -> lambda kappa_* and T_H -> T_H/lambda by changing source-current normalization; the field equation and orbital GM product are unchanged until source units are fixed independently | a local GR/Newton recovery can validate the coupling product but cannot by itself predict numerical G | UNDERDETERMINATION_DERIVED |
| NG3907_1_anti_circularity | measured orbital GM cannot be used as both input source mass and proof of G_* | choosing G_* or ell_J from the same exterior motion being explained makes the Newton bridge tautological | G_* value claim requires parent scale map or independent metrology/source calibration | ANTI_CIRCULARITY_PROVED_AS_POLICY |
| NG3907_2_not_fatal | failure to derive numerical G is not a failure of GR reduction | GR itself treats G as a coupling measured by experiment; MTS can do the same if it proves derivative/source/range silence | local branch can still be competitive as a GR-reduction branch, but not as a prediction of G's value | MEASURED_COUPLING_BRANCH_ALLOWED |

## Measured Coupling Policy Runner

| policy_id | quantity | rule | runner_effect | status |
| --- | --- | --- | --- | --- |
| POL3907_0_value | G_* numerical value | MEASURED_NOT_PREDICTED unless a source-backed F(kappa_MTS,ell_J,...) exists | do not score failure to predict G as local-GR failure; do score any drift/source/range dependence | MEASURED_COUPLING_POLICY_ACTIVE |
| POL3907_1_derivatives | partial G_* residuals | must be theorem-zero or bounded: time, radius, species/material, range, frame/domain | activate derivative zero gates before any local-GR/Newton claim | DERIVATIVE_GATES_ACTIVE |
| POL3907_2_source_mass | Hilbert mass/source normalization | source mass must be Hilbert/worldtube calibrated independently of orbital GM | epsilon_Hilbert_mass_norm remains active until source current and Pi_M/H_tau lock | SOURCE_NORMALIZATION_GATE_ACTIVE |

## Gstar Derivative Zero Gates

| gate_id | symbol | definition | zero_route | observable_link | status |
| --- | --- | --- | --- | --- | --- |
| DG3907_0_time | dln_Gstar_dt | partial_t ln G_* | zero if G_* in global superselection sector | Gdot/clock | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |
| DG3907_1_radial | partial_r_ln_Gstar | partial_r ln G_* | zero if no radial/domain/boundary dependence of coupling | orbital/R10/radial source | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |
| DG3907_2_species | partial_A_ln_Gstar | material/source-label derivative | zero if source functor forgets species labels | WEP/source charge | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |
| DG3907_3_range | alpha_Gstar_lambda | finite-range coupling amplitude | zero if G_* is not mediated by local range field | R10/Yukawa | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |
| DG3907_4_frame | partial_frame_ln_Gstar | frame/tau/readout derivative | zero if same observed frame/tau/source/orbit branch is fixed before readout | PPN/clocks/orbits | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |
| DG3907_5_product | Dln_Z_product | D ln(G_ref*w_common*ell_J*R_frame*C_extra) | zero only if every product factor is independently zero-owned | Newton/Gdot/PPN/R10 | MISSING_ZERO_PROOF_OR_NUMERIC_BOUND |

## Branch Decision

| decision_id | decision | reason | effect | status |
| --- | --- | --- | --- | --- |
| DEC3907_0_no_prediction | do not claim MTS predicts the numerical value of Newton's constant | current inspected corpus lacks a parent scale map fixing kappa_* absolutely | G_* is a measured superselected coupling in the local GR branch | VALUE_DERIVATION_REJECTED_FOR_NOW |
| DEC3907_1_keep_competitive | keep the local GR branch alive | a measured coupling is standard for GR; the nontrivial MTS obligation is derivative/source/range silence | shift pressure to derivative gates and source normalization, not pointless re-circling over G's number | LOW_ENERGY_BRANCH_RETAINED |
| DEC3907_2_next | attack measured-coupling derivative zero gates next | these are testable and required for local GR/Newton even if G itself is measured | next step should prove or bound dG/dt, radial G, species coupling, range dependence and product-factor drift | NEXT_ROUTE_SELECTED |

## Source Register

Resolved `12/12` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3907_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3906_NEXT_TARGET.csv | True | 3906 selected Gstar scale target |
| SRC3907_01_gstar | source-intake\mts_residuals\P8_Y5_R2FR_3906_GSTAR_OWNER_MATRIX.csv | True | 3906 Gstar derivation target |
| SRC3907_02_residuals | source-intake\mts_residuals\P8_Y5_R2FR_3906_NON_EH_AND_GSTAR_RESIDUAL_ROWS.csv | True | 3906 active Gstar residual rows |
| SRC3907_03_ellJ | source-intake\mts_residuals\P8_EM_ellJ_source_current_owner_residual_law.csv | True | ellJ source-current owner residual law |
| SRC3907_04_product | source-intake\mts_residuals\P8_EM_product_lock_factor_vector_ellJ_Rframe.csv | True | G/w/ellJ/frame/source product factor |
| SRC3907_05_y5y6 | source-intake\mts_residuals\P8_Y5_Y6_source_coupling_lock_status.csv | True | Y5/Y6 source coupling lock status |
| SRC3907_06_source_current | source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv | True | source current Ward universality |
| SRC3907_07_ward | source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv | True | Ward source owner identity |
| SRC3907_08_worldtube | source-intake\mts_residuals\P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv | True | worldtube Hilbert coupling selector |
| SRC3907_09_kappa_contract | source-intake\mts_residuals\P8_constant_universal_Geff_kappa_CONTRACT.csv | True | constant-only calibration policy |
| SRC3907_10_global_superselection | source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv | True | global coupling constant offset policy |
| SRC3907_11_validation | source-intake\mts_residuals\P8_Y5_BRR545_3906_VALIDATION.csv | True | 3906 validation |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3907_0 | 3908-Y5-R2FR-measured-Gstar-derivative-zero-gates-or-bound-runner.md | prove or bound the measured-coupling derivative gates: dG/dt, radial G, species/source coupling, range dependence, frame drift and product-factor drift | 3907 rejects a numerical G prediction for now but makes local-GR competitiveness depend on derivative/source/range silence, which is testable and directly tied to existing residual rows |

## Bottom Line

Do not spend another hundred checkpoints trying to magic `G` out of local GR alone. The only honest routes are:

1. derive a real parent scale map for `kappa_*`;
2. or treat `G_*` as measured and prove it is universal, constant, source-blind and range-blind.

Given current evidence, route 2 is the disciplined route. It keeps MTS competitive without pretending to predict something it has not derived.
