# 3265 - Second material arena or parent no-cancellation theorem under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3265` finds the missing second punch: Eot-Wash Be/Ti supplies a second DD material-difference vector.
- The two-row matrix `[(TA6V-PtRh10),(Be-Ti)]` is rank two in `(Q'_hatm,Q'_e)`, so the pure algebraic cancellation escape is broken **conditionally**.
- The conditional inversion gives finite bounds on `D_hatm` and `D_e`, but they remain non-claim because the parent MTS source-convention lock is unsigned.
- This is a real advance over `3264`: the blocker is no longer "one material pair cannot bound two channels"; it is now specifically "prove both arenas share the same parent coupling coordinates and residual convention."

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | source_url | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3265_3264_handoff | true | true | 3264 established Ti/Pt as a two-channel DD strip, not an EM-only bound | L7:- The source-backed two-channel form is `eta_TiPt = Delta_Qhatm D_hatm + Delta_Qe D_e + residual`. \| L8:- A single Ti/Pt WEP pair gives a **strip**, not independent bounds on `D_hatm` and `D_e`; cancellation directions remain. \| L42:\| delta_id \| left_minus_right \| Delta_Qhatm_prime \| Delta_Qe_prime \| delta_vector_norm \| eta_formula \| valid_for_claim \| \| L44:\| DELTA3264_TA6V_minus_PtRh10 \| TA6V_minus_PtRh10 \| -3.314967641189e-03 \| -1.982376296945e-03 \| 3.862489643328e-03 \| eta_TiPt = Delta_Qhatm_prime*D_hatm + Delta_Qe_prime*D_e + residual \| false \| |  | false |
| SRC3265_DD_tex | true | true | Damour-Donoghue two-charge basis and WEP formula | L1063:{\alpha}_A \simeq d_g^* + \left[ (d_{\hat m} - d_g) Q'_{\hat m} + d_e Q'_e \right]_A \| L1071:Q'_{\hat m} = -\frac{0.036}{A^{1/3}} - 1.4 \times 10^{-4} \, \frac{Z(Z-1)}{A^{4/3}} \| L1075:Q'_{e} = + 7.7 \times 10^{-4} \frac{Z(Z-1)}{A^{4/3}} . \| L1090:{\rm Material} &$A$ &$Z$ &$-Q'_{\hat m}$ &$Q'_e$ \\ \\ | https://arxiv.org/abs/1007.2792 | false |
| SRC3265_EOTWASH_tex | true | true | Eot-Wash Be/Ti torsion-balance second material arena | L37:We used a continuously rotating torsion balance instrument to measure the acceleration difference of beryllium and titanium test bodies towards sources at a variety of distances. Our result $\Delta a_{N,Be-Ti}=(0.6\pm 3.1)\times 10^{-15}\;\ms$ improves limits on equivalence-princ \| L60:Figure~\ref{fig:schematics} shows a schematic drawing of the apparatus and the $70.3\;\mbox{g}$ pendulum. The pendulum body is a thin aluminum shell with fourfold azimuthal symmetry and up down reflection symmetry. It carries four beryllium and four titanium test masses in a hori \| L61:The optical beam of the autocollimator is reflected from one of four mirrors located at the pendulum's midplane. The entire pendulum and all surfaces near the pendulum are plated with $\approx 300$~nm of gold. \| L65:\caption{Cross section of the apparatus (upper part). The entire torsion balance is suspended below a continuously rotating turntable. Gravity gradient compensator masses were placed around the pendulum to reduce coupling to ambient gravitational gradients. The pendulum (lower pa | https://arxiv.org/abs/0712.0607 | false |
| SRC3265_3264_delta | true | true | MICROSCOPE TA6V/PtRh10 DD vector from 3264 | L2:DELTA3264_TA6V_minus_PtRh10,TA6V_minus_PtRh10,-3.314967641189e-03,-1.982376296945e-03,3.862489643328e-03,eta_TiPt = Delta_Qhatm_prime*D_hatm + Delta_Qe_prime*D_e + residual,false |  | false |
| SRC3265_3264_bounds | true | true | MICROSCOPE conservative eta strip bound from 3264 | L2:MB3264_0_two_channel_strip,two DD channels retained; conservative eta bound; no residual,\|Delta_Qhatm*D_hatm + Delta_Qe*D_e\| <= eta_bound,2.755102040816e-15,"one Ti/Pt WEP pair gives a strip, not separate D_hatm/D_e bounds",false |  | false |

## Eot-Wash Evidence
| evidence_id | line_number | text_excerpt | role | source_url | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EOT3265_0_materials_abstract | 37 | We used a continuously rotating torsion balance instrument to measure the acceleration difference of beryllium and titanium test bodies towards sources at a variety of distances. Our result $\Delta a_{N,Be-Ti}=(0.6\pm 3.1)\times 10^{-15}\;\ms$ improves limits on equivalence-principle violations with ranges from 1~m to $\infty$ by an order of magnitude. The E\"otv\"os parameter is $\eta_{Earth,Be-Ti}= (0.3 \pm 1.8)\times 10^{-13}.$ | Eot-Wash compares Be and Ti test bodies. | https://arxiv.org/abs/0712.0607 | false |
| EOT3265_1_pendulum_materials | 60 | Figure~\ref{fig:schematics} shows a schematic drawing of the apparatus and the $70.3\;\mbox{g}$ pendulum. The pendulum body is a thin aluminum shell with fourfold azimuthal symmetry and up down reflection symmetry. It carries four beryllium and four titanium test masses in a horizontal dipole configuration. These two materials were chosen primarily to maximize the difference in baryon number ($B/\mu$ is $0.99868$ for Be and $1.001077$ for Ti), and secondly for experimental reasons, such as densities, magnetic properties and machinability. The Ti test bodies are hollow to match the external shape and mass of the $4.84$~g Be test bodies to within $50$~$\mu$g. The test body shape allows us to reproducibly interchange the test bodies, to minimize alignment errors, and to equalize their gravitational interaction. | Be/Ti material pair is explicit in the apparatus. | https://arxiv.org/abs/0712.0607 | false |
| EOT3265_2_eta_result | 141 | \eta(\mbox{Be}-\mbox{Ti})= \frac{\Delta a_{N}}{a_{\perp}^g}= (0.3\pm 1.8)\times 10^{-13}. | Earth-directed Eotvos parameter used as a 95 percent second-row bound. | https://arxiv.org/abs/0712.0607 | false |
| EOT3265_3_source_model | 147 | interaction (Eq.~1) as a function of range $\lambda$. To establish these limits we used the mass density and charge content of the environment surrounding the torsion balance to create a source model. For $\lambda= 1-100$~m the source is dominated by a hill sloping towards the East. For $\lambda<10\;$km the local topography and bedrock become significant. At ranges between 10~km and 1000~km, preliminary results using large scale density and composition models indicate that the limit on $\alpha$ is better than the dashed line shown in Fig.~\ref{fig:results}. A detailed description of the model and limits will be included in a future publication. We used an elliptical layered Earth model\cite{Su94, Dzi81, Mor80} for $\lambda>1000\;$km. For this range the source mass is located towards the North. | Long-range source convention is Earth-model based, but not yet parent-locked to MTS. | https://arxiv.org/abs/0712.0607 | false |
| EOT3265_4_eta_bound_95 | derived_from_EOT3265_2_eta_result | \|eta_Earth_BeTi\| <= \|3.000e-14\| + 1.96*1.800e-13 = 3.828000000000e-13 | Conservative Gaussian 95 percent absolute upper bound for matrix smoke inversion. | https://arxiv.org/abs/0712.0607 | false |

## DD Material Charges
| material_charge_id | arena | material_id | composition_basis | A_context | Z | Qhatm_prime | Qe_prime | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAT3265_from3264_PtRh10 | MICROSCOPE_TIPT | PtRh10 | DD approximate two-charge basis; mass-fraction alloy average | alloy_from_3264 | alloy_from_3264 | -7.080823850881e-03 | 3.994438870705e-03 | false |
| MAT3265_from3264_TA6V | MICROSCOPE_TIPT | TA6V | DD approximate two-charge basis; mass-fraction alloy average | alloy_from_3264 | alloy_from_3264 | -1.039579149207e-02 | 2.012062573760e-03 | false |
| MAT3265_EOTWASH_Be | EOTWASH_BETI | EOTWASH_Be | nominal pure natural element; Eot-Wash source identifies test-body element, not isotope/binding tensor | 9.012200000000e+00 | 4.000000000000e+00 | -1.738875973841e-02 | 4.926791798304e-04 | false |
| MAT3265_EOTWASH_Ti | EOTWASH_BETI | EOTWASH_Ti | nominal pure natural element; Eot-Wash source identifies test-body element, not isotope/binding tensor | 4.786700000000e+01 | 2.200000000000e+01 | -1.028710095158e-02 | 2.046842478469e-03 | false |

## Two-Arena Delta Matrix
| row_id | arena | left_minus_right | Delta_Qhatm_prime | Delta_Qe_prime | eta_abs_bound | eta_bound_basis | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DM3265_0_MICROSCOPE_TA6V_minus_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | TA6V_minus_PtRh10 | -3.314967641189e-03 | -1.982376296945e-03 | 2.755102040816e-15 | MICROSCOPE final eta divided by tau_readout_min=0.98 from 3264 | false |
| DM3265_1_EOTWASH_Be_minus_Ti | EOTWASH_BETI_EARTH_FIELD | Be_minus_Ti | -7.101658786830e-03 | -1.554163298639e-03 | 3.828000000000e-13 | \|0.3e-13\| + 1.96*1.8e-13 from Eot-Wash eta(Be-Ti) | false |

## Rank and Conditioning
| rank_id | determinant | row1_norm | row2_norm | cos_angle | sin_angle_abs | condition_number | rank_two | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RANK3265_0_two_arena_DD_matrix | -8.926159003891e-06 | 3.862489643328e-03 | 7.269730468415e-03 | 9.481270819649e-01 | 3.178915482438e-01 | 7.457960818153e+00 | true | The Eot-Wash Be/Ti vector is not parallel to the MICROSCOPE Ti/Pt vector; cancellation cannot hide both channels if the same D basis and residual silence are signed. | false |

## Conditional Two-Channel Bounds
| bound_id | assumption | formula | matrix_equation | eta_bounds | value | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CB3265_0_conditional_two_row_system | same DD D_hatm/D_e coordinates across MICROSCOPE and Eot-Wash; residuals silent; source convention locked |  | A D = eta, A rows are DeltaQ(TA6V-PtRh10) and DeltaQ(Be-Ti) | b_MICROSCOPE=2.755102040816e-15; b_EOTWASH=3.828000000000e-13 |  | CONDITIONAL_MATRIX_THEOREM_ONLY | false |
| CB3265_1_D_hatm_component_bound | CB3265_0 assumptions | \|D_hatm\| <= \|A^{-1}_{00}\| b1 + \|A^{-1}_{01}\| b2 |  |  | 8.549427862687e-11 | NONCLAIM_UNTIL_PARENT_SOURCE_CONVENTION_LOCK | false |
| CB3265_2_D_e_component_bound | CB3265_0 assumptions | \|D_e\| <= \|A^{-1}_{10}\| b1 + \|A^{-1}_{11}\| b2 |  |  | 1.443549691533e-10 | NONCLAIM_UNTIL_PARENT_SOURCE_CONVENTION_LOCK | false |

## No-Cancellation Theorem Status
| clause_id | clause | status | evidence | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NCT3265_0_linear_algebra_core | Two nonparallel DD material-difference rows give finite component bounds by A^{-1}. | PROVED_CONDITIONAL | det(A)=-8.926159003891e-06; rank_two=true | none for the algebraic theorem | false |
| NCT3265_1_same_coupling_coordinates | MICROSCOPE and Eot-Wash must project onto the same parent D_hatm/D_e coordinates. | UNSIGNED_PARENT_CONVENTION | Both are Earth-field WEP arenas, but the MTS parent source map has not signed equality of calibration coordinates. | derive/source parent source-convention lock | false |
| NCT3265_2_residual_silence | Residual source/profile/readout terms must be zero or bounded below the eta rows. | UNSIGNED_RESIDUAL | 3263 closed MICROSCOPE eta-level projection; Eot-Wash source/profile residuals are not imported into MTS convention. | derive residual transport or add residual terms to matrix | false |
| NCT3265_3_material_exactness | Be/Ti and Ti/Pt material charge rows must be exact enough for public bounds. | SOURCE_BACKED_SMOKE_NOT_FULL_MATERIAL_TENSOR | DD approximate charges and nominal pure-element Be/Ti are enough for a rank smoke test, not a final material tensor. | upgrade to exact material/isotope/binding tensor if promoting | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3265_0_second_vector | second independent material arena exists | true | Eot-Wash Be/Ti vector is nonparallel to MICROSCOPE Ti/Pt in DD two-charge space | false |
| CG3265_1_conditional_bounds | finite two-channel component bounds derived | true | matrix inverse gives finite conditional \|D_hatm\| and \|D_e\| bounds | false |
| CG3265_2_parent_source_convention | MTS parent D coordinates locked across arenas | false | external DD coordinates are still calibration coordinates until parent source map signs equality | false |
| CG3265_3_local_GR | local GR/Newton/Maxwell promotion | false | 3265 breaks the algebraic cancellation route conditionally; it does not yet derive the local parent action | false |

## Decision
| decision_id | verdict | what_moved | best_next | fallback_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3265_0 | SECOND_VECTOR_FOUND_RANK_TWO_BUT_PARENT_LOCK_UNSIGNED | det(A)=-8.926159003891e-06; conditional CB3265_1_D_hatm_component_bound=8.549427862687e-11; CB3265_2_D_e_component_bound=1.443549691533e-10 | derive/source the common parent source-convention lock so MICROSCOPE and Eot-Wash rows share one D_hatm/D_e vector | add R10/clock cross-channel rows with explicit D-coordinate maps instead of relying on WEP alone | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3265_0_3266 | primary | 3266-Y5-R2FR-source-convention-lock-or-two-channel-bound-promotion-under-AX1090.md | scripts/Y5_R2FR_3266_source_convention_lock_or_two_channel_bound_promotion.py | Prove that the MICROSCOPE and Eot-Wash DD rows use the same parent MTS source-coupling coordinates, or explicitly retain arena-specific residual/source-map terms. | Do not promote the conditional two-row inversion into a WEP/local-GR claim until parent source convention and residual silence are signed. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3265_0_sources_exist | all cited source paths exist | true |  |
| VAL3265_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3265_2_eotwash_lines_found | Eot-Wash materials/eta/source evidence lines are found | true | EOT3265_0_materials_abstract:37;EOT3265_1_pendulum_materials:60;EOT3265_2_eta_result:141;EOT3265_3_source_model:147;EOT3265_4_eta_bound_95:derived_from_EOT3265_2_eta_result |
| VAL3265_3_outputs_parse | all 3265 output CSVs parse | true |  |
| VAL3265_4_material_rows_finite | all DD material charge rows are finite numeric | true | PtRh10;TA6V;EOTWASH_Be;EOTWASH_Ti |
| VAL3265_5_delta_matrix_rank_two | two-arena DD matrix is rank two | true | determinant=-8.926159003891e-06; sin_angle_abs=3.178915482438e-01; condition=7.457960818153e+00 |
| VAL3265_6_conditional_bounds_finite | conditional two-channel bounds are finite | true | CB3265_0_conditional_two_row_system=matrix;CB3265_1_D_hatm_component_bound=8.549427862687e-11;CB3265_2_D_e_component_bound=1.443549691533e-10 |
| VAL3265_7_claim_gates_false | no 3265 claim gate allows WEP/local-GR promotion | true | all claim_allowed=false |
| VAL3265_8_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3265_9_overall | 3265 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T06:19:51.874919+00:00
