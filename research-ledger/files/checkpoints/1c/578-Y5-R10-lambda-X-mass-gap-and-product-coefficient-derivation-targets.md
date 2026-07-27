# 578 Y5 R10 lambda-X mass-gap and product coefficient derivation targets

Generated: 2026-06-04T23:57:09.410534+00:00  
Status: `Y5_R10_lambda_X_product_law_derived_conditionally_numeric_coefficients_missing`  
Claim ceiling: `lambda_product_derivation_targets_only_no_R10_pass_no_WEP_PPN_or_local_GR_pass`  
Next target: `579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md`

## Verdict
- The derivation path works at the structural level.
- From the local quadratic parent action, the finite range is:

```text
(-Z_X Delta + M_X^2) X = J_X,
mu_X^2 = M_X^2 / Z_X,
lambda_X = sqrt(Z_X / M_X^2).
```

- From the Green-function exterior field, the fifth-force strength is:

```text
X(r) = Q_X^H exp(-r/lambda_X)/(4 pi Z_X r),
alpha_X(lambda_X) = K_X Qbar_XH(lambda_X) qbar_XT.
```

- So we have derived the exact local target law, not the numeric pass. The missing machine is now precise: parent Hessian ratio `M_X^2/Z_X`, positive `Z_X`, source charge `Qbar_XH`, and test charge `qbar_XT`.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 577-Y5-R10-qbar-XT-finite-envelope-after-source-current-failure.md | True | finite qbar_XT product wall and next target |
| source-intake/mts_residuals/P8_Y5_BRR545_577_VALIDATION.csv | True | prior finite-envelope validation |
| source-intake/mts_residuals/P8_Y5_R10_577_NONCLAIM_SUMMARY.csv | True | qbar retained and finite product ceiling summary |
| source-intake/mts_residuals/P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv | True | parent Hessian extraction formula for Z_X and M_X^2 |
| source-intake/mts_residuals/P8_Y5_R10_MASS_GAP_THEOREM_ZERO_GATE.csv | True | mass-gap and no-hair gate status |
| source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv | True | static operator, lambda, Green profile, and prefactor formulas |
| source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_FACTOR_REGISTER.csv | True | source/test/projection numerator factors |
| source-intake/mts_residuals/P8_Y5_R10_577_QBAR_BUDGET_MATRIX.csv | True | qbar budgets from previous pressure wall |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | True | review-candidate curve for reverse lambda windows |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | live claim curve placeholder, expected claim-blocked |

## Local Quadratic Derivation
| step_id | derivation_step | formula | result | remaining_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LD578_0_parent_expansion | expand the parent action around the compact local branch | S_X^(2)=1/2 int sqrt(g)[Z_X nabla_i X nabla^i X + M_X^2 X^2] - int sqrt(g) J_X X | conditional_quadratic_form_derived | parent action must supply numeric Z_X, M_X^2, and source split J_X | false |
| LD578_1_static_operator | vary X in the static weak-field exterior | (-Z_X Delta + M_X^2) X = J_X | conditional_operator_derived | Z_X>0 and M_X^2>0 must be parent-owned in the same branch | false |
| LD578_2_range_law | canonicalize the operator | mu_X^2=M_X^2/Z_X; lambda_X=1/mu_X=sqrt(Z_X/M_X^2) | lambda_law_derived_conditionally | numeric Hessian ratio M_X^2/Z_X is missing | false |
| LD578_3_green_function | solve exterior point-source Green function | X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r) | profile_derived_conditionally | projected source charge Q_X^H(lambda_X) must be derived or bounded | false |
| LD578_4_test_potential | couple test body to the finite X profile | V_X(r)=-q_X^T X(r); V_N(r)=-G_obs M_H m_T/r | force_ratio_setup_derived | test charge q_X^T and source mass calibration must be parent-owned | false |
| LD578_5_alpha_law | divide by Newtonian potential | alpha_X(lambda_X)=s_X Q_X^H q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)=K_X Qbar_XH(lambda_X) qbar_XT | product_law_derived_conditionally | K_X, Qbar_XH(lambda_X), and qbar_XT remain symbolic | false |
| LD578_6_nohair_fork | test theorem-zero alternative | int[Z_X\|grad X\|^2+M_X^2 X^2]=int_boundary Z_X X n.gradX + int X J_X | conditional_nohair_identity_only | J_X=0 and boundary flux=0 failed to be parent-derived earlier | false |
| LD578_7_verdict | combine local law with R10 | abs(K_X Qbar_XH(lambda_X) qbar_XT)<=alpha_bound(lambda_X) | exact_nonclaim_target_law | derive lambda_X and product coefficients before scoring | false |

## Mass-Gap Targets
| target_id | lambda_X_m | lambda_X_um | M_X2_over_Z_X_m_minus2 | canonical_m_X_eV | alpha_bound_review_candidate | unsuppressed_product_allowed_at_lambda | required_parent_relation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MGT578_0 | 5.900000e-06 | 5.9 | 2.872738e+10 | 0.0334452509153 | 8.869376e+05 | true | M_X^2/Z_X=2.872738e+10 m^-2 | false |
| MGT578_1 | 1.000000e-05 | 10 | 1.000000e+10 | 0.01973269804 | 4.154017e+04 | true | M_X^2/Z_X=1.000000e+10 m^-2 | false |
| MGT578_2 | 2.000000e-05 | 20 | 2.500000e+09 | 0.00986634902 | 21.0084392198 | true | M_X^2/Z_X=2.500000e+09 m^-2 | false |
| MGT578_3 | 3.860000e-05 | 38.6 | 6.711590e+08 | 0.00511209793782 | 1.13811631033 | true | M_X^2/Z_X=6.711590e+08 m^-2 | false |
| MGT578_4 | 5.000000e-05 | 50 | 4.000000e+08 | 0.003946539608 | 1.56064161526 | true | M_X^2/Z_X=4.000000e+08 m^-2 | false |
| MGT578_5 | 7.500000e-05 | 75 | 1.777778e+08 | 0.00263102640533 | 0.304425754822 | false | M_X^2/Z_X=1.777778e+08 m^-2 | false |
| MGT578_6 | 1.000000e-04 | 100 | 1.000000e+08 | 0.001973269804 | 0.0766587862265 | false | M_X^2/Z_X=1.000000e+08 m^-2 | false |
| MGT578_7 | 2.000000e-04 | 200 | 2.500000e+07 | 9.866349e-04 | 0.0338737034454 | false | M_X^2/Z_X=2.500000e+07 m^-2 | false |
| MGT578_8 | 5.000000e-04 | 500 | 4.000000e+06 | 3.946540e-04 | 0.0448930602318 | false | M_X^2/Z_X=4.000000e+06 m^-2 | false |
| MGT578_9 | 6.080783e-04 | 608.0783 | 2.704463e+06 | 3.245092e-04 | 0.00234471960478 | false | M_X^2/Z_X=2.704463e+06 m^-2 | false |
| MGT578_10 | 0.001 | 1000 | 1.000000e+06 | 1.973270e-04 | 0.00998986313981 | false | M_X^2/Z_X=1.000000e+06 m^-2 | false |

## Reverse Lambda Windows
| window_id | constant_abs_product | allowed_lambda_intervals_m_review_candidate | allowed_canonical_mX_eV_intervals | passes_entire_review_candidate_range | number_of_allowed_intervals | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RLW578_0 | 1 | 5.894419e-06..3.865927e-05;3.866457e-05..3.998863e-05;4.117031e-05..4.240255e-05;4.271045e-05..4.367521e-05;4.409747e-05..4.498606e-05;4.546971e-05..4.640256e-05;4.698118e-05..4.779960e-05;4.849444e-05..5.000688e-05;...(+24 more raw fragments) | 0.0051042603591..0.0334769170587;0.00493457729943..0.00510356081239;0.00465365808849..0.00479294399553;0.00451805478056..0.00462010978292;0.00438640282805..0.00447479160259;0.0042525024232..0.004339746208;0.00412821444342..0.00420012813288;0.00394599666428..0.00406906384169;...(+24 more raw fragments) | false | 32 | false |
| RLW578_1 | 0.3 | 5.894419e-06..5.807226e-05;5.822060e-05..6.044705e-05;6.077886e-05..6.258523e-05;6.308518e-05..6.529349e-05;6.603606e-05..6.736671e-05;6.823512e-05..7.030724e-05;7.217122e-05..7.265662e-05;7.493709e-05..7.502174e-05;...(+29 more raw fragments) | 0.00339795578785..0.0334769170587;0.00326445993019..0.0033892982161;0.00315293233375..0.00324663835071;0.00302215378003..0.00312794496876;0.0029291469098..0.00298816999976;0.00280663803383..0.00289186832938;0.00271588425128..0.00273415037684;0.00263026412447..0.00263323516111;...(+29 more raw fragments) | false | 37 | false |
| RLW578_2 | 0.1 | 5.894419e-06..8.890167e-05;8.904863e-05..9.201959e-05;9.268193e-05..9.509494e-05;9.634811e-05..9.999939e-05;1.001566e-04..1.032125e-04;1.037682e-04..1.065256e-04;1.077142e-04..1.100000e-04;1.117783e-04..1.144893e-04;...(+33 more raw fragments) | 0.0022196094908..0.0334769170587;0.0021444017831..0.0022159462481;0.00207505228785..0.00212907719309;0.00197328184068..0.00204806273391;0.00191185168903..0.0019701852031;0.00185238953952..0.00190161234354;0.0017938811733..0.00183194918246;0.00172354116473..0.00176534191375;...(+33 more raw fragments) | false | 41 | false |
| RLW578_3 | 0.03 | 5.894419e-06..1.500232e-04;1.500292e-04..1.549363e-04;1.558668e-04..1.609361e-04;1.619837e-04..1.670454e-04;1.683914e-04..1.750154e-04;1.789165e-04..1.817770e-04;1.857607e-04..1.888497e-04;1.926384e-04..1.961738e-04;...(+27 more raw fragments) | 0.00131530989729..0.0334769170587;0.00127360079941..0.00131525704353;0.00122612024312..0.00126599750058;0.0011812775983..0.00121819047316;0.00112748377537..0.00117183534658;0.00108554417816..0.00110289989042;0.00104488903328..0.00106226413952;0.00100587816361..0.00102433894968;...(+27 more raw fragments) | false | 35 | false |
| RLW578_4 | 0.01 | 5.894419e-06..2.302178e-04;2.303255e-04..2.398500e-04;2.399592e-04..2.499445e-04;2.499445e-04..2.606782e-04;2.618491e-04..2.717336e-04;2.735144e-04..2.832191e-04;2.857069e-04..2.960405e-04;2.986141e-04..3.093824e-04;...(+26 more raw fragments) | 8.571317e-04..0.0334769170587;8.227099e-04..8.567310e-04;7.894831e-04..8.223356e-04;7.569753e-04..7.894831e-04;7.261781e-04..7.535906e-04;6.967290e-04..7.214501e-04;6.665541e-04..6.906623e-04;6.378093e-04..6.608094e-04;...(+26 more raw fragments) | false | 34 | false |
| RLW578_5 | 0.003 | 5.894419e-06..4.127390e-04;4.127515e-04..4.329144e-04;4.331040e-04..4.538884e-04;4.543221e-04..4.758215e-04;4.766883e-04..5.000734e-04;5.000734e-04..5.242519e-04;5.258307e-04..5.500485e-04;5.516186e-04..5.773481e-04;...(+13 more raw fragments) | 4.780914e-04..0.0334769170587;4.558106e-04..4.780770e-04;4.347478e-04..4.556111e-04;4.147080e-04..4.343328e-04;3.945961e-04..4.139539e-04;3.763973e-04..3.945961e-04;3.587447e-04..3.752671e-04;3.417816e-04..3.577236e-04;...(+13 more raw fragments) | false | 21 | false |
| RLW578_6 | 0.001 | 5.894419e-06..0.00100991533518 | 1.953896e-04..0.0334769170587 | true | 1 | false |

## Product Coefficient Derivation
| factor_id | factor | derived_form | meaning | status | zero_or_suppression_route | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PCD578_0_KX | K_X | K_X=s_X/(4*pi*Z_X*G_obs) after chosen X normalization | kinetic normalization and sign convention prefactor | conditional_prefactor_derived_numeric_ZX_missing | large Z_X, canonical normalization, or parent source normalization can suppress K_X | false |
| PCD578_1_Qbar_XH | Qbar_XH(lambda_X) | Qbar_XH=Pi_M^H[Q_X^H(lambda_X)]/M_H | projected source charge per measured source mass | not_parent_derived | source neutrality, screening, boundary no-flux, or Hamiltonian projector orthogonality | false |
| PCD578_2_qbar_XT | qbar_XT | qbar_XT=q_X^T/m_T=-m_T^-1 delta S_T/dX | ordinary test-body charge per inertial mass | retained_after_576 | trivial MTS action on matter constants, selector-blind matter, or small finite matter coupling | false |
| PCD578_3_lambda_X | lambda_X | lambda_X=sqrt(Z_X/M_X^2) | range selecting the R10 bound ordinate | conditional_law_derived_numeric_Hessian_missing | large M_X^2/Z_X gives short range; no fifth-force if source/test charge zero | false |
| PCD578_4_alpha_abs_gate | abs(alpha_X) | abs(alpha_X)=abs(K_X Qbar_XH(lambda_X) qbar_XT) | R10 comparison magnitude | gate_locked | sign cannot remove magnitude bound | false |
| PCD578_5_claim_evidence | alpha_bound(lambda) | external R10 curve ordinate at derived lambda_X | empirical comparison wall | review_candidate_nonclaim | claim needs official/supplemental or QA-promoted curve rows | false |

## Repair Queue
| queue_id | missing_item | why_needed | acceptable_fill | failure_mode | next_action |
| --- | --- | --- | --- | --- | --- |
| RQ578_0_parent_Hessian | numeric or symbolic parent Hessian ratio M_X^2/Z_X | sets lambda_X and therefore which R10 bound applies | derive from local parent potential/action second variation with units and sign | lambda remains a scan knob only | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |
| RQ578_1_ZX_normalization | Z_X sign and normalization | ghost/ellipticity, range canonicalization, and alpha prefactor all depend on Z_X | positive parent kinetic residue or canonical field convention with transformed charges | wrong-sign or convention-dependent alpha | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |
| RQ578_2_source_charge | Qbar_XH(lambda_X) | determines whether host/source sector actually sources the finite X mode | derive neutrality/screening or compute finite projected source charge | finite branch remains symbolic | derive source charge profile |
| RQ578_3_test_charge | qbar_XT | 576 retained test-body charge instead of proving it zero | derive tiny amplitude law from matter coupling or provide bounded coefficient | R10 cannot score MTS alpha | derive qbar_XT amplitude law |
| RQ578_4_curve_promotion | claim-grade alpha_bound(lambda) | review candidate is useful for pressure but not public evidence | supplemental table, official data, or manual QA-promoted digitization | private diagnostic only | promote bound curve later, after coefficients exist |
| RQ578_5_local_GR_separation | PPN/source/calibration gates beyond R10 | R10 pass would still not be full local GR | measured-GM, beta/gamma, conservation, and frame residuals pass separately | overclaim | keep claim ceiling locked |

## Decision
| decision_id | decision | meaning | status | next_target |
| --- | --- | --- | --- | --- |
| D578_0_lambda_law_derived | accept lambda_X=sqrt(Z_X/M_X^2) as conditionally derived | range is no longer conceptually vague; it is the parent Hessian ratio | conditional_derivation_progress | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |
| D578_1_product_law_derived | accept alpha_X=K_X Qbar_XH qbar_XT as conditionally derived | R10 force strength is an exact Green-function product once coefficients are parent-filled | conditional_derivation_progress | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |
| D578_2_numeric_claim_blocked | do not claim R10 pass or fail | lambda_X, Z_X, Qbar_XH, qbar_XT, and claim-grade curve rows remain missing | blocked_for_claim | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |
| D578_3_next_best_derivation | derive parent Hessian/source charge or return to theorem-zero | the next real fork is mass gap plus product coefficients, not more prose around R10 | next_derivation_target | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |

## Route Update
| route_id | allowed_after_578 | forbidden_after_578 | next_action |
| --- | --- | --- | --- |
| RU578_0_allowed | use lambda_X=sqrt(Z_X/M_X^2) as the canonical local range law | choose lambda_X by fit without parent Hessian provenance | derive M_X^2/Z_X |
| RU578_1_allowed | use Green-function alpha product as the coefficient target | treat symbolic K_X Qbar_XH qbar_XT as numeric evidence | fill K_X, Qbar_XH, qbar_XT |
| RU578_2_allowed | use reverse lambda windows to guide derivation pressure | claim windows are exclusions before lambda/product are derived | derive range first, then compare |
| RU578_3_allowed | keep theorem-zero route as a possible rescue only if parent identities close | erase finite branch pressure by saying qbar_XT should vanish | 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V578_0_source_paths_exist | pass | missing=0 |
| V578_1_prior_577_validated | pass | prior_rows=9;qbar_retained=True |
| V578_2_lambda_law_derived_conditionally | pass | lambda_X=sqrt(Z_X/M_X^2) |
| V578_3_product_law_derived_conditionally | pass | alpha_X=K_X Qbar_XH qbar_XT |
| V578_4_mass_gap_targets_numeric | pass | target_rows=11 |
| V578_5_reverse_windows_sane | pass | product_1_not_global_safe;product_0p001_global_safe_on_review_candidate |
| V578_6_coefficients_still_block_claim | pass | repair_items=6;claim_allowed=false |
| V578_7_live_claim_curve_still_blocked | pass | live_claim_rows=0 |
| V578_8_no_overclaim | pass | conditional_laws_only;no_R10_pass;no_WEP;no_PPN;no_local_GR |

## Practical Read
This is a better position than “we need a miracle”. The local range and force law are now proper engineering targets. If the parent action gives `lambda_X` near tens of microns, an order-one product is not immediately murdered by this private R10 pressure curve. If it gives `lambda_X` around `0.1-1 mm`, the product needs percent-to-per-mille suppression unless a stronger zero theorem returns. The next move is therefore very specific: derive the parent Hessian ratio `M_X^2/Z_X` and the source/test product, or explicitly demote the finite branch to a scored residual.
