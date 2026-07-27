# 3906 - EH Origin and Gstar Owner or Low-Energy GR Branch Contract

Generated: `2026-07-01T09:42:03+00:00`

## Result

3906 separates two fights that must not be blurred:

1. **EH operator shape**: why the public geometry equation is Einstein-Hilbert rather than an arbitrary metric operator.
2. **`G_*` value/owner**: why the coupling is constant/universal, and whether MTS derives its numerical value.

Conditional EH selector:

`If Q is the only public metric/coframe, S_Q is local, diffeomorphism invariant, second-order in the metric equations, and has no independent scalar/vector/tensor operator slots on the local branch, then E_Q^{mu nu}=A_* G^{mu nu}+B_* g^{mu nu}`

Action branch:

`S_Q=(1/(2*kappa_*)) int sqrt(-Q) (R[Q]-2 Lambda_*) + S_top[Q] + S_nonEH_residual`

Coupling owner:

`kappa_* = 8*pi*G_*/c^4, delta_local kappa_*=0, partial_{t,r,A,lambda,Y,H} G_*=0 on the local branch`

Same-frame source bridge:

`E_Q^{mu nu}=kappa_* T_vis^{mu nu}[E(Q),Psi] with T_vis from the same Hilbert variation used by matter and Maxwell`

Verdict: MTS now has a clean low-energy GR branch contract, but not a completed local-GR claim. EH shape can be conditionally selected; `G_*` is owned as a global parent coupling unless a deeper MTS normalization derives it. That is acceptable as a GR-reduction contract, but not as a claimed prediction of Newton's constant.

## EH Operator Selection Contract

| row_id | clause | statement | status | remaining_failure |
| --- | --- | --- | --- | --- |
| EH3906_0_selector | EH operator selector | If Q is the only public metric/coframe, S_Q is local, diffeomorphism invariant, second-order in the metric equations, and has no independent scalar/vector/tensor operator slots on the local branch, then E_Q^{mu nu}=A_* G^{mu nu}+B_* g^{mu nu} | CONDITIONAL_OPERATOR_SELECTION_THEOREM | locality/second-order/no-extra-operator assumptions must be parent-signed or residual-scored |
| EH3906_1_action | EH action normal form | S_Q=(1/(2*kappa_*)) int sqrt(-Q) (R[Q]-2 Lambda_*) + S_top[Q] + S_nonEH_residual | ACTION_FORM_CONSTRUCTED | S_nonEH_residual coefficients are not globally zeroed yet |
| EH3906_2_nonEH_filter | non-EH operator filter | R^2, R_mn R^mn, Weyl^2, nonlocal kernels, torsion/nonmetricity, projector/domain operators must be topological, field-redefinition redundant, zero, or executable residuals | RESIDUAL_FILTER_READY | not all residual coefficients are numerically bounded in current local tests |
| EH3906_3_Bianchi | Bianchi consistency | nabla_mu(G^{mu nu}+Lambda_* g^{mu nu})=0 requires nabla_mu(kappa_* T_vis^{mu nu})=0 | CONSERVATION_GATE_EXPLICIT | constant kappa/G owner not derived from deeper MTS scale |

## Gstar Owner Matrix

| row_id | piece | formula | result | status | open_part |
| --- | --- | --- | --- | --- | --- |
| G3906_0_definition | Gstar definition | kappa_* = 8*pi*G_*/c^4, delta_local kappa_*=0, partial_{t,r,A,lambda,Y,H} G_*=0 on the local branch | G_* is the local GR coupling associated with the EH block | OWNER_SLOT_DEFINED | numerical value of G_* is not derived from MTS scales |
| G3906_1_not_Newton_derivation | anti-circularity | do not derive G_* from orbital GM, fitted Newtonian mass, H0, or post-readout calibration | Newtonian agreement can measure G_*, not prove its parent origin | ANTI_CIRCULARITY_GUARD | need kappa_MTS/ell_J/topological normalization if predicting G |
| G3906_2_constant_owner | constant coupling owner | G_* in K_global, not Gamma(E_local); delta_local G_*=0 | kills local Gdot/fifth-force/source-composition leakage if parent-signed | CONDITIONAL_SUPERSELECTION_OWNER | global coupling sector is not derived as a theorem of the full MTS parent action |
| G3906_3_derivation_target | deeper MTS derivation target | G_* ?= F(kappa_MTS, ell_J, cell scale, action normalization, topological charge) | this is the next optional ambition beyond a low-energy GR branch contract | DERIVATION_OPEN_TARGET | no sourced function F exists in current inspected rows |

## Hilbert Source Coupling Bridge

| row_id | bridge | formula | result | status | remaining_failure |
| --- | --- | --- | --- | --- | --- |
| SRCBR3906_0_Hilbert | same-frame Hilbert source | E_Q^{mu nu}=kappa_* T_vis^{mu nu}[E(Q),Psi] with T_vis from the same Hilbert variation used by matter and Maxwell | ordinary matter and EM stress source the same public geometry | CONDITIONAL_SAME_FRAME_SOURCE_BRIDGE | same-frame/no-source-prefactor inheritance must be parent-signed |
| SRCBR3906_1_Maxwell | Maxwell/EM stress | T_EM^{mu nu}=2/sqrt(-Q) delta S_Maxwell[A,E(Q),alpha_*]/delta Q_{mu nu} | Poynting/vector EM stress is not an extra force; it is part of T_vis in the EH equation | EM_STRESS_INHERITS_HILBERT_SOURCE | alpha/clock calibration remains separate from stress sourcing |
| SRCBR3906_2_Poisson | Poisson coefficient | weak-field 00 equation gives nabla^2 Phi = (kappa_* c^4/2) rho_H = 4*pi*G_* rho_H | Newtonian coefficient follows once kappa_*=8*pi G_*/c^4 and source mass is Hilbert-normalized | CONDITIONAL_POISSON_COEFFICIENT | worldtube Hilbert mass and measured-source normalization remain parent-conditional |
| SRCBR3906_3_exchange | variable coupling exchange guard | if nabla_mu kappa_* != 0 then q_exchange^nu = T_vis^{mu nu} nabla_mu kappa_* / kappa_* | any nonconstant G branch becomes a scored residual instead of being hidden in measured GM | EXCHANGE_RESIDUAL_FORMULA_READY | requires numeric/source rows if G_* superselection is not signed |

## Low-Energy GR Branch Contract

| contract_id | contract | meaning | status | fallback_if_missing |
| --- | --- | --- | --- | --- |
| LEGR3906_0_scope | MTS local-GR branch = product chart + EH selector + constant G_* owner + same-frame Hilbert source + silent/bounded residual sectors | this is the honest local-GR branch contract, not a claim that full MTS has been globally derived | CONTRACT_WRITTEN_NONCLAIM | keep explicit non-EH/G/source residual vector active |
| LEGR3906_1_EH_origin | EH shape is derived by operator-selection assumptions; EH absolute normalization is G_* owner | operator form and coupling value are deliberately separated | SEPARATION_OF_FIGHTS | do not pretend deriving GR also derives numerical G |
| LEGR3906_2_public_claim_policy | public wording may say conditional local-GR branch exists; it may not say MTS derives G or passes local GR | keeps GitHub/journal-facing statements disciplined | CLAIM_DISCIPLINE_POLICY | overclaim risk |

## Non-EH and Gstar Residual Rows

| residual_id | symbol | definition | units | fallback_use | status |
| --- | --- | --- | --- | --- | --- |
| RES3906_0_nonEH | c_nonEH_operator_vector | coefficients for R^2/Ricci^2/Weyl^2/nonlocal/torsion/projector operators | dimensionless or length-scaled by operator | blocks EH-only/local PPN if nonzero | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_1_Gdot | dln_Gstar_dt | time derivative of local gravitational coupling | 1/time | Gdot/clock/source-coupling residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_2_radial | partial_r_ln_Gstar | radial derivative of G_* or measured source strength | 1/length | radial fifth-force/source-normalization residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_3_species | partial_A_ln_Gstar | species/material/source-label derivative of G_* or active source coupling | dimensionless per material coordinate | WEP/source-charge residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_4_range | alpha_Gstar_lambda | finite-range coupling amplitude if G_* is mediated by a local scalar/range field | dimensionless | R10/Yukawa residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_5_source_norm | epsilon_Hilbert_mass_norm | mismatch between Hilbert worldtube mass and measured orbital source mass | dimensionless | Newton/GM anti-circularity residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |
| RES3906_6_exchange | q_kappa_exchange^nu | Bianchi exchange current from nonconstant kappa_* | force density | conservation/source coupling residual | ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND |

## Local-GR Decision Gate

| gate_id | gate | result | status | claim_allowed |
| --- | --- | --- | --- | --- |
| GATE3906_0_EH_shape | EH operator shape | conditionally selected by local/diffeomorphic/second-order/no-extra-operator assumptions | PASS_CONDITIONAL | False |
| GATE3906_1_nonEH | non-EH residuals | not globally zero; residual vector emitted | BLOCKED_RESIDUALS_ACTIVE | False |
| GATE3906_2_Gstar_owner | G_* owner | owner slot and superselection route defined | PASS_CONDITIONAL_OWNER | False |
| GATE3906_3_Gstar_value | numerical G_* derivation | not derived from MTS scales | BLOCKED_VALUE_NOT_DERIVED | False |
| GATE3906_4_source_coupling | Hilbert/Maxwell source coupling | same-frame bridge written; source normalization still conditional | PARTIAL_CONDITIONAL | False |
| GATE3906_5_local_GR_claim | local GR/Newton promotion | not allowed until non-EH residuals and G/source normalization are theorem-zero or bounded | BLOCKED_NO_CLAIM | False |

## Source Register

Resolved `13/13` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3906_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3905_NEXT_TARGET.csv | True | 3905 selected EH/Gstar target |
| SRC3906_01_reduction | source-intake\mts_residuals\P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv | True | 3905 GR/Newton reduction and G owner distinction |
| SRC3906_02_normal_form | source-intake\mts_residuals\P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv | True | 3905 parent normal-form constants clause |
| SRC3906_03_local_eh_attempt | source-intake\mts_residuals\P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv | True | prior local EH reduction theorem attempt |
| SRC3906_04_local_eh_requirements | source-intake\mts_residuals\P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv | True | prior EH reduction requirements |
| SRC3906_05_local_eh_failures | source-intake\mts_residuals\P8_LOCAL_EH_REDUCTION_FAILURE_LEDGER.csv | True | prior EH failure ledger |
| SRC3906_06_kappa_contract | source-intake\mts_residuals\P8_constant_universal_Geff_kappa_CONTRACT.csv | True | constant universal coupling contract |
| SRC3906_07_global_superselection | source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv | True | global coupling superselection contract |
| SRC3906_08_hilbert_calibration | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | True | Hilbert monopole calibration contract |
| SRC3906_09_newton_stack | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | source-normalized Newton branch stack |
| SRC3906_10_source_owner | source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv | True | parent source owner action terms |
| SRC3906_11_source_norm | source-intake\mts_residuals\P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv | True | Hilbert worldtube source normalization theorem attempt |
| SRC3906_12_maxwell | source-intake\mts_residuals\P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv | True | Maxwell Hilbert stress same-frame row |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3906_0 | 3907-Y5-R2FR-Gstar-from-MTS-scales-or-measured-coupling-policy-runner.md | try to derive kappa_*/G_* from MTS scales such as kappa_MTS, ell_J, cell/action normalization or topological charge; if not, lock G_* as measured superselected coupling and run residual-policy gates | 3906 separates EH-shape derivation from G-value derivation; the next honest leap is to attempt the G_* scale map directly or accept a measured-coupling branch |

## Bottom Line

This improves the project because it stops asking the wrong question. GR does not normally derive the numerical value of `G`; it uses it as a measured coupling. MTS can still be stronger if it later derives `G_*` from MTS scales, but the honest local-GR route is now:

`product chart -> EH selector -> constant G_* owner -> same-frame Hilbert/Maxwell source -> bounded residual vector`.

If any arrow fails, the failure is not handwaved; it activates `c_nonEH_operator_vector`, `dln_Gstar_dt`, source-normalization, range, species, or exchange rows.
