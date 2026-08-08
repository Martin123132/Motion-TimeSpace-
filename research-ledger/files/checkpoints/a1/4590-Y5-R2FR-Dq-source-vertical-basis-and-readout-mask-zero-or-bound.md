# 4590 - Dq-source vertical basis and readout-mask zero or bound

Marker: `PPC4161_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590`  
Branch: `MTS_R2FR_Y5_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590`  
Generated: `2026-07-06T13:16:46.582719+00:00`  
Public claim: `False`

## Result

4590 tightens the source-worldtube kernel route. The actual source residual direction is not allowed to be called vertical unless it passes the real quotient test:

```text
v_X = v_X^V + v_X^H,        v_X^V in ker(Dq),        Dq(v_X^H)=Dq(v_X)
Y_source = Ybar(q(Phi))     =>     D_v Y_source = dYbar[Dq(v_X)].
```

So the clean branch is:

```text
Dq(v_X)=0  =>  E_Dq_source=0.
```

The readout/domain/support mask has the same discipline:

```text
Pi_mask = Pbar_mask(q(Phi), P_protocol),
D_v P_protocol=0, Dq(v_X)=0  =>  D_v Pi_mask=0  =>  E_readout_mask=0.
```

If the source probe is not actually vertical, or if the mask is selected after residual/readout inspection, both terms stay alive as operator bounds:

```text
E_Dq_source <= L_Y_source ||Dq(v_X)||_Q / N_Y_source,
E_readout_mask <= ||D_v Pi_mask||_op ||J_H|| / M_lower.
```

## Consequence for the source-worldtube kernel

Combining 4587, 4588, 4589 and 4590 gives a sharper but still nonclaim reduction:

```text
C_K_source_worldtube <= L_K_source * E_tau_eobs
```

only on the strict branch where density/Poynting, support-boundary, denominator, actual verticality and fixed readout-mask clauses are all active. Otherwise:

```text
C_K_source_worldtube <= L_K_source * (E_Dq_source + E_tau_eobs + E_readout_mask).
```

This is progress, not a local-GR claim. The next live target is the same `tau/e_obs` branch.

## Dq vertical theorem

| checkpoint | theorem_id | claim | derivation | zero_condition | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | DQV4590_0_actual_probe_decomposition | The actual source residual direction must be tested against the quotient map, not merely named vertical. | For a parent perturbation v_X, split v_X=v_X^V+v_X^H with v_X^V in ker(Dq) and Dq(v_X^H)=Dq(v_X). The source-worldtube q-basic bundle Y=Ybar(q(Phi)) changes as D_vY=dYbar[Dq(v_X)]. | Dq(v_X)=0 for the actual parent source residual direction. | E_Dq_source=0 only on the certified vertical branch. | ACTUAL_VERTICALITY_CONTRACT_DERIVED_NOT_SIGNED_GLOBALLY | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQV4590_1_qbasic_bundle_zero | A q-basic source-support bundle is vertically silent. | If Y_source=(M_H_ref,sigma^a,W_source)=Ybar(q(Phi)) and v_X in ker(Dq), then D_vY_source=dYbar[Dq(v_X)]=0. | rho_H dV_H, support regularity, M_H_ref and protocol data are q-basic, and Dq(v_X)=0. | The Dq part of the active source-worldtube kernel coefficient vanishes without fitting. | CONDITIONAL_ZERO_THEOREM_DERIVED | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQV4590_2_operator_norm_fallback | If actual verticality is unsigned, the source leakage is an operator norm, not a closure axiom. | ||D_vY_source|| <= L_Y_source ||Dq(v_X)||_Q, so E_Dq_source := L_Y_source ||Dq(v_X)||_Q / N_Y_source with N_Y_source>0. | None; this is the finite fallback when Dq(v_X) is nonzero or unknown. | The next empirical/source task is to fill L_Y_source, ||Dq(v_X)||_Q and N_Y_source, not to claim local GR. | BOUND_FORMULA_DERIVED_VALUES_MISSING | 2026-07-06T13:16:46.582719+00:00 | False |

## Readout-mask theorem

| checkpoint | theorem_id | claim | derivation | zero_condition | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | ROM4590_0_fixed_protocol_zero | A readout mask fixed before source variation and factoring through q is vertically silent. | Let Pi_mask=Pbar_mask(q(Phi),P_protocol) with P_protocol fixed before variation. Then D_v Pi_mask = D_q Pbar_mask[Dq(v)] + D_P Pbar_mask[D_vP_protocol]. If Dq(v)=0 and D_vP_protocol=0, D_vPi_mask=0. | fixed protocol, q-basic domain/support/mask, no post-fit thresholds, no moving Green/Hodge/domain selector. | E_readout_mask=0 on the fixed q-basic readout-mask branch. | CONDITIONAL_ZERO_THEOREM_DERIVED | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | ROM4590_1_active_mask_rejection | A mask chosen after inspecting residuals is not a zero theorem. | For a source/residual-dependent mask, D_v(Pi_mask J_H)=Pi_mask D_vJ_H+(D_vPi_mask)J_H. The second term survives unless separately bounded. | Rejected when the support window, threshold, comparison domain, kernel, Hodge/Green operator or mass mask is selected from the fitted residual/readout. | Delta_mask must be retained as E_readout_mask or a more detailed operator row. | ZERO_REJECTED_FOR_ACTIVE_OR_POSTFIT_MASK | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | ROM4590_2_operator_norm_fallback | The active mask fallback is an explicit product-rule operator bound. | E_readout_mask <= ||D_vPi_mask||_op ||J_H|| / M_lower, with D_vPi_mask split into Dq leakage, protocol drift, source-threshold drift and active Green/Hodge/domain terms. | None; this is the fallback if the fixed q-basic protocol cannot be certified. | Readout effects remain visible in the local bound vector and cannot be hidden in a local-GR claim. | BOUND_FORMULA_DERIVED_VALUES_MISSING | 2026-07-06T13:16:46.582719+00:00 | False |

## Operator-bound rows

| checkpoint | bound_id | symbol | definition | bound_or_value | units | numeric_value_present | source_path | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | OB4590_0_Dqv_norm | ||Dq(v_X)||_Q | actual quotient-map leakage of source residual direction | MISSING_ACTUAL_DQ_OF_SOURCE_PROBE | quotient units per source-probe norm | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_1_LY_source | L_Y_source | Lipschitz/operator norm of q-basic source-support bundle Ybar | MISSING_YBAR_OPERATOR_NORM | Y units per quotient unit | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_2_NY_source | N_Y_source | positive normalization for source-support bundle leakage | MISSING_POSITIVE_NORMALIZATION | Y units | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_3_E_Dq_source | E_Dq_source | normalized source verticality leakage | E_Dq_source <= L_Y_source*||Dq(v_X)||_Q/N_Y_source | dimensionless | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_4_DvPi_mask | ||D_v Pi_mask||_op | vertical derivative of readout/domain/support mask | MISSING_FIXED_PROTOCOL_OR_OPERATOR_NORM | inverse source-probe norm | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_5_JH_norm | ||J_H|| | Hilbert source/readout current norm seen by mask variation | MISSING_SOURCE_CURRENT_NORM | source-current units | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_6_Mlower | M_lower | positive same-frame denominator inherited from 4589 | MISSING_POSITIVE_MHREF_LOWER_BOUND | mass/charge units | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | OB4590_7_E_readout_mask | E_readout_mask | normalized active readout-mask leakage | E_readout_mask <= ||D_vPi_mask||_op*||J_H||/M_lower | dimensionless | False |  | False | False | 2026-07-06T13:16:46.582719+00:00 |

## Source-kernel reduction update

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | DQMR4590_0_E_Dq_source_zero | E_Dq_source | E_Dq_source=0 | actual source probe v_X satisfies Dq(v_X)=0 and Y_source descends through q | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQMR4590_1_E_Dq_source_bound | E_Dq_source | E_Dq_source <= L_Y_source*||Dq(v_X)||_Q/N_Y_source | actual verticality missing or Dq(v_X) nonzero | OPERATOR_BOUND_READY_VALUES_MISSING | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQMR4590_2_E_readout_mask_zero | E_readout_mask | E_readout_mask=0 | Pi_mask=Pbar_mask(q,P_protocol), Dq(v_X)=0 and D_vP_protocol=0 before readout | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQMR4590_3_E_readout_mask_bound | E_readout_mask | E_readout_mask <= ||D_vPi_mask||_op*||J_H||/M_lower | active/moving/postfit readout mask, Green/Hodge/domain selector or unsigned protocol | OPERATOR_BOUND_READY_VALUES_MISSING | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQMR4590_4_CKsource_strict_update | C_K_source_worldtube | strict 4587+4588+4589+4590 branch reduces C_K_source_worldtube <= L_K_source*E_tau_eobs | density/Poynting, support-boundary, denominator, actual verticality and fixed readout-mask zero branches active | PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED_REMAINING_TAU_EOBS | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | DQMR4590_5_CKsource_open_update | C_K_source_worldtube | C_K_source_worldtube <= L_K_source*(E_Dq_source+E_tau_eobs+E_readout_mask) after prior 4587-4589 reductions | Dq/mask zero branches unsigned or active | OPEN_OPERATOR_VECTOR_RETAINED_NONCLAIM | 2026-07-06T13:16:46.582719+00:00 | False |

## Controls

| checkpoint | control_id | scenario | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | CTRL4590_clean_vertical_fixed_mask | Dq(v_X)=0 and Pi_mask fixed q-basic before variation | E_Dq_source=0; E_readout_mask=0 | SYMBOLIC_CONTROL_PASS | 2026-07-06T13:16:46.582719+00:00 | False | False |
| 4590 | CTRL4590_named_vertical_only | v_X is called vertical but Dq(v_X) not computed | reject zero; retain E_Dq_source operator row | COUNTERMODEL_CAUGHT | 2026-07-06T13:16:46.582719+00:00 | False | False |
| 4590 | CTRL4590_postfit_threshold | support/readout window chosen after residual inspection | reject zero; retain E_readout_mask | COUNTERMODEL_CAUGHT | 2026-07-06T13:16:46.582719+00:00 | False | False |
| 4590 | CTRL4590_active_green_hodge | Pi_mask includes moving Green/Hodge/domain operator | product-rule term survives | COUNTERMODEL_CAUGHT | 2026-07-06T13:16:46.582719+00:00 | False | False |
| 4590 | CTRL4590_fixed_protocol_tau_open | mask fixed but same tau/e_obs not yet signed | Dq/mask branch can close but E_tau_eobs remains | PARTIAL_REDUCTION_ONLY | 2026-07-06T13:16:46.582719+00:00 | False | False |
| 4590 | CTRL4590_orbital_GM_mask | domain/mass mask defined by fitted orbital GM or comparison residual | reject as circular readout selector | FIREWALL_PASS | 2026-07-06T13:16:46.582719+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4590 | PROM4590_0_sources_exist | Every cited 3560/4580/4589/193/229/235/282/284/1701/1702 source exists. | PASS | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | PROM4590_1_vertical_theorem | Actual verticality law D_vY=dYbar[Dq(v_X)] derived. | PASSED_CONDITIONAL | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | PROM4590_2_mask_theorem | Fixed q-basic readout-mask law D_vPi_mask=0 derived. | PASSED_CONDITIONAL | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | PROM4590_3_active_fallback | Active/postfit mask and nonvertical source probe keep finite operator rows. | PASS | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | PROM4590_4_claim_firewall | No local-GR/R10/PPN claim is promoted from 4590. | PASS | False | False | 2026-07-06T13:16:46.582719+00:00 |
| 4590 | PROM4590_5_next_tau_eobs | Remaining strict source-kernel blocker is same tau/e_obs branch. | PASS | False | False | 2026-07-06T13:16:46.582719+00:00 |

## Decision

| checkpoint | branch | generated_utc | decision | summary | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4590 | MTS_R2FR_Y5_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590 | 2026-07-06T13:16:46.582719+00:00 | DQ_SOURCE_VERTICAL_PROJECTOR_AND_FIXED_READOUT_MASK_ZERO_CONTRACT_DERIVED_OPERATOR_BOUND_RETAINED_NONCLAIM | 4590 turns actual source verticality and readout-mask fixedness into theorem-or-bound contracts. If v_X is genuinely in ker(Dq) and the mask/protocol is q-basic and pre-variation, both E_Dq_source and E_readout_mask vanish. If either clause fails, explicit operator bounds survive. The strict source-kernel branch is now reduced to E_tau_eobs after 4587-4590, but no local-GR claim is made. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | MTS_R2FR_Y5_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590 | 2026-07-06T13:16:46.582719+00:00 | 4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md | After density/Poynting, support-boundary, denominator, Dq-source verticality and readout-mask branches, the remaining strict source-worldtube kernel blocker is same-frame tau/e_obs routing. | prove source density, support, Hamiltonian charge, readout and mask all use the same q-basic tau/e_obs branch | emit finite E_tau_eobs rows with frame/coframe/time mismatch norms and no fitted clock/orbit selectors | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4590 | SRC4590_00_4589_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md | True | 4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md | True | 4589 selected Dq/mask target | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_01_4589_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4589_SOURCE_KERNEL_REDUCTION_UPDATE.csv | True | MHRD4589_3_next_Dq_mask | True | 4589 reduction row selecting Dq and readout-mask blockers | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_02_3560_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md | True | SCL3560_4_actual_vertical_basis | True | 3560 exposed actual vertical-basis missing clause | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_03_3560_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv | True | BF3560_2_E_Dq_source | True | 3560 E_Dq_source and E_readout_mask bound vector | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_04_193_vertical | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\193-PPC4161-quotient-naturality-vertical-silence-theorem.md | True | V_q := ker(Dq) | True | quotient vertical silence theorem | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_05_229_presymplectic | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\229-PPC4161-qbasic-vertical-presymplectic-silence.md | True | Dq[v] = 0 | True | q-basic vertical presymplectic silence | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_06_235_marker | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md | True | Dq_source_readout[v]=0 | True | Dq component split and source-readout marker | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_07_282_hilbert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md | True | Dq_source_readout = 0 | True | Hilbert source-readout component branch | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_08_284_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | Dq_boundary_projector = 0 | True | fixed-collar boundary/projector branch | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_09_4580_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_1_fixed_qbasic_domain | True | fixed q-basic readout-domain certificate | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_10_1701_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md | True | GENERAL_NO_REENTRY_NOT_DERIVED | True | general readout no-reentry rejection | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_11_1702_commutator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md | True | branch_readout_functor | True | arena readout commutator/product split | 2026-07-06T13:16:46.582719+00:00 | False |
| 4590 | SRC4590_12_claim_431 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-431 | True | claim-register handoff from 4589 | 2026-07-06T13:16:46.582719+00:00 | False |

## Validation

| checkpoint | check_id | status | detail | generated_utc |
| --- | --- | --- | --- | --- |
| 4590 | VAL4590_00_doc_written | PASS | checkpoint doc exists | 2026-07-06T13:16:46.722720+00:00 |
| 4590 | VAL4590_01_formal_written | PASS | formal bridge exists | 2026-07-06T13:16:46.722832+00:00 |
| 4590 | VAL4590_02_marker_doc | PASS | doc marker present | 2026-07-06T13:16:46.722852+00:00 |
| 4590 | VAL4590_03_marker_formal | PASS | formal marker present | 2026-07-06T13:16:46.722866+00:00 |
| 4590 | VAL4590_04_all_sources_exist | PASS | all cited local paths exist | 2026-07-06T13:16:46.722889+00:00 |
| 4590 | VAL4590_05_all_source_needles | PASS | all source needles found | 2026-07-06T13:16:46.722910+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_SOURCE_REGISTER | PASS | P8_Y5_R2FR_4590_SOURCE_REGISTER.csv parses with rows | 2026-07-06T13:16:46.746468+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_DQ_VERTICAL_THEOREM | PASS | P8_Y5_R2FR_4590_DQ_VERTICAL_THEOREM.csv parses with rows | 2026-07-06T13:16:46.764338+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_READOUT_MASK_THEOREM | PASS | P8_Y5_R2FR_4590_READOUT_MASK_THEOREM.csv parses with rows | 2026-07-06T13:16:46.781717+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_OPERATOR_BOUND_ROWS | PASS | P8_Y5_R2FR_4590_OPERATOR_BOUND_ROWS.csv parses with rows | 2026-07-06T13:16:46.797838+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_SOURCE_KERNEL_REDUCTION_UPDATE | PASS | P8_Y5_R2FR_4590_SOURCE_KERNEL_REDUCTION_UPDATE.csv parses with rows | 2026-07-06T13:16:46.812670+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_CONTROL_ROWS | PASS | P8_Y5_R2FR_4590_CONTROL_ROWS.csv parses with rows | 2026-07-06T13:16:46.830484+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_PROMOTION_GATES | PASS | P8_Y5_R2FR_4590_PROMOTION_GATES.csv parses with rows | 2026-07-06T13:16:46.847266+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_DECISION | PASS | P8_Y5_R2FR_4590_DECISION.csv parses with rows | 2026-07-06T13:16:46.862662+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_NEXT_TARGET | PASS | P8_Y5_R2FR_4590_NEXT_TARGET.csv parses with rows | 2026-07-06T13:16:46.880010+00:00 |
| 4590 | VAL4590_csv_P8_Y5_R2FR_4590_STATUS | PASS | P8_Y5_R2FR_4590_STATUS.csv parses with rows | 2026-07-06T13:16:46.897143+00:00 |
| 4590 | VAL4590_20_no_generated_claim_true | PASS | generated rows do not promote claims | 2026-07-06T13:16:46.904542+00:00 |
| 4590 | VAL4590_21_zero_theorem_present | PASS | both zero contracts appear | 2026-07-06T13:16:46.904590+00:00 |
| 4590 | VAL4590_22_bound_formulas_present | PASS | both operator fallbacks appear | 2026-07-06T13:16:46.904636+00:00 |
| 4590 | VAL4590_23_strict_reduction_present | PASS | strict kernel reduction appears | 2026-07-06T13:16:46.904650+00:00 |
| 4590 | VAL4590_24_next_target_present | PASS | next target appears | 2026-07-06T13:16:46.904665+00:00 |
| 4590 | VAL4590_25_spine_marker | PASS | spine updated once | 2026-07-06T13:16:46.927867+00:00 |
| 4590 | VAL4590_26_packet_marker | PASS | packet updated once | 2026-07-06T13:16:46.953518+00:00 |
| 4590 | VAL4590_27_claim_register | PASS | claim register updated | 2026-07-06T13:16:46.984887+00:00 |
| 4590 | VAL4590_28_no_github_action | PASS | local-only checkpoint; no git push performed | 2026-07-06T13:16:46.984924+00:00 |
| 4590 | VAL4590_29_formal_workbench_updated_only_via_declared_files | PASS | formal updates limited to declared bridge/spine/packet/claim files | 2026-07-06T13:16:46.985208+00:00 |
| 4590 | VAL4590_OVERALL | PASS | 4590 Dq-source verticality/readout-mask theorem-or-bound validation | 2026-07-06T13:16:46.985229+00:00 |
