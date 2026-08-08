# 1660 - Conservative L_D Curvature Frame Input Runner

**Private status:** nonclaim lower-input checkpoint. No `nabla_Ploc` bound, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1660` gets one real numerical foothold and then stops exactly where it should:

```text
L_D_upper = 2.6e-2 m
Riemann_norm proxy = 1.18820825e-22 m^-2
nabla_Riemann_norm proxy = 5.59507152e-29 m^-3
LD*Riemann proxy = 3.08934146e-24 m^-1
```

That is not a local-GR win. It is only an Earth-monopole curvature proxy built from source-backed constants. The actual finite-domain projector residual is still blocked by `C_Fermi`, `C_Fermi2`, the norm contract, and lab-frame/projection terms.

## Source Register

| source_id | path | source_url | path_exists | needles_found | role |
| --- | --- | --- | --- | --- | --- |
| 1659_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md | local_prior_checkpoint | True | True | 1660 conservative-LD curvature/frame input runner |
| 1659_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1659_VALIDATION.csv | local_prior_checkpoint | True | True | 1660 conservative-LD curvature/frame input runner |
| 1659_ld_row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1659_CONSERVATIVE_LD_ROW.csv | local_prior_checkpoint | True | True | 1660 conservative-LD curvature/frame input runner |
| 1659_nablaploc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1659_NABLAPLOC_READY_TEMPLATE.csv | local_prior_checkpoint | True | True | 1660 conservative-LD curvature/frame input runner |
| nist_pdf | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\lab-r10\NIST_CODATA_2022_wall_chart.pdf | https://pml.nist.gov/cuu/pdf/wall_2022.pdf | True | True | 1660 conservative-LD curvature/frame input runner |
| nist_text | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\lab-r10\NIST_CODATA_2022_wall_chart.txt | https://pml.nist.gov/cuu/pdf/wall_2022.pdf | True | True | 1660 conservative-LD curvature/frame input runner |
| jpl_html | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\lab-r10\JPL_planetary_physical_parameters.html | https://ssd.jpl.nasa.gov/planets/phys_par.html | True | True | 1660 conservative-LD curvature/frame input runner |

## Earth Monopole Inputs

| row_id | quantity | value | units | source | source_line | source_status |
| --- | --- | --- | --- | --- | --- | --- |
| CONST1660_0_c | speed_of_light | 2.99792458e+08 | m s^-1 | NIST_CODATA_2022_wall_chart | 7 | exact |
| CONST1660_1_G | Newtonian_constant_of_gravitation | 6.67430000e-11 | m^3 kg^-1 s^-2 | NIST_CODATA_2022_wall_chart | 8 | CODATA_2022 |
| CONST1660_2_Mearth | Earth_mass | 5.97217000e+24 | kg | JPL_planetary_physical_parameters | 909 | planetary_parameter |
| CONST1660_3_Rearth_mean | Earth_mean_radius | 6.37100840e+06 | m | JPL_planetary_physical_parameters | 894 | planetary_parameter |
| CONST1660_4_LD_upper | conservative_LD_upper | 2.60000000e-02 | m | 1659_conservative_LD_row | 2 | internal_nonclaim_method |

## Curvature Proxy

| row_id | formula_Riemann_norm | formula_nabla_Riemann_norm | Riemann_norm_m2 | nabla_Riemann_norm_m3 | LD_times_Riemann_m1 | LD2_times_nabla_Riemann_m1 | limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CURV1660_0_earth_monopole_proxy | sqrt(48)*G*M_E/(c^2*R_E^3) | 3*Riemann_norm/R_E | 1.18820825e-22 | 5.59507152e-29 | 3.08934146e-24 | 3.78226834e-32 | not full laboratory curvature model; ignores local masses, multipoles, apparatus frame motion, and parent projector constants |

## Fermi Constant Ledger

| row_id | quantity | value | status | blocker |
| --- | --- | --- | --- | --- |
| FERMI1660_0_C_Fermi | C_Fermi | MISSING | MISSING_PARENT_PROJECTOR_THEOREM | needs explicit local projector/Fermi-coordinate norm inequality |
| FERMI1660_1_C_Fermi2 | C_Fermi2 | MISSING | MISSING_PARENT_PROJECTOR_THEOREM | needs second-order projector drift theorem or conservative analytic bound |
| FERMI1660_2_norm_choice | operator_norm_choice | MISSING | MISSING_NORM_CONTRACT | must specify tensor/operator norm used in nabla_Ploc_Linf |

## Frame Term Ledger

| row_id | quantity | value | status | blocker |
| --- | --- | --- | --- | --- |
| FRAME1660_0_lab_motion | lab_frame_acceleration_rotation_terms | MISSING | MISSING_FRAME_CONTRACT | must decide whether Earth rotation, suspension turntable, and local acceleration enter q_loc residual |
| FRAME1660_1_apparatus_orientation | apparatus_orientation_projection | MISSING | MISSING_ARENA_PROJECTION | Lee-Adelberger geometry source does not by itself define MTS projector orientation terms |
| FRAME1660_2_local_masses | nearby_mass_curvature_terms | MISSING | MISSING_LOCAL_MASS_MODEL | near-apparatus density/multipole contribution not source-modelled |

## nablaPloc Partial Template

| row_id | partial_formula | LD_m | Riemann_norm_m2 | nabla_Riemann_norm_m3 | C_Fermi | C_Fermi2 | frame_terms | current_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NPLR1660_0_partial_conservative_LD_bound | nabla_Ploc_Linf <= C_Fermi*LD*Riemann_norm + C_Fermi2*LD^2*nabla_Riemann_norm + frame_terms | 2.60000000e-02 | 1.18820825e-22 | 5.59507152e-29 | MISSING | MISSING | MISSING | PARTIAL_NUMERIC_PROXY_BLOCKED_BY_CONSTANTS_AND_FRAME_TERMS |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1660_0_curvature_proxy | Earth-monopole curvature proxy is numeric | INTERNAL_SOURCE_PROXY_ONLY | NONCLAIM | not full lab curvature model |
| CG1660_1_fermi_constants | C_Fermi and C_Fermi2 are source-backed | False | BLOCKED | parent projector theorem missing |
| CG1660_2_frame_terms | frame terms are zero or bounded | False | BLOCKED | frame contract/silence theorem missing |
| CG1660_3_nabla_Ploc | nabla_Ploc_Linf numeric bound is accepted | False | BLOCKED | constants and frame terms missing |
| CG1660_4_local | local GR/Newton/PPN/R10/WEP follows | False | NO_CLAIM | no normalized residual vector or M_H_ref denominator |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1660_0_curvature | ACCEPT_EARTH_MONOPOLE_PROXY_NONCLAIM | sourced constants give a concrete curvature scale | carry as proxy input, not as local-GR evidence |
| DEC1660_1_constants | BLOCK_ON_FERMI_PROJECTOR_CONSTANTS | C_Fermi, C_Fermi2, and norm contract control the actual bound | derive a projector/Fermi norm theorem next |
| DEC1660_2_frame | BLOCK_ON_FRAME_TERMS_OR_SILENCE_THEOREM | lab rotation/projection terms may dominate if not silenced | derive frame silence or source apparatus frame model |
| DEC1660_3_next | NEXT_1661_FERMI_PROJECTOR_CONSTANT_THEOREM | the curvature proxy is no longer the main blocker | attempt analytic constants before more data plumbing |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md | scripts/Y5_R2FR_Fermi_projector_constant_theorem_or_frame_silence.py | derive or bound C_Fermi, C_Fermi2, the norm contract, and frame-term silence for the finite-domain local projector residual | constants/frame terms become theorem-backed or the local projector route stays explicitly closure-only |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1660_0_sources_exist | PASS | all cited 1660 source paths exist and needles are present |
| VAL1660_1_1659_passed | PASS | 1659 validation is source-registered as PASS |
| VAL1660_2_earth_inputs_positive | PASS | Earth constants and L_D input are positive and source-lined |
| VAL1660_3_curvature_proxy_numeric | PASS | Earth-monopole curvature and gradient proxy are positive |
| VAL1660_4_constants_block_scoring | PASS | Fermi constants and norm contract remain explicit blockers |
| VAL1660_5_frame_terms_block_scoring | PASS | frame terms remain explicit blockers |
| VAL1660_6_nablaploc_partial_nonclaim | PASS | nabla_Ploc template is partial and nonclaim |
| VAL1660_7_claim_gates_safe | PASS | all claim gates keep MTS claims false |
| VAL1660_8_next_target_selected | PASS | next target selects Fermi/projector constant theorem |
| VAL1660_9_csv_parse | PASS | all generated 1660 CSVs parse |
| VAL1660_10_no_mts_claim_flags | PASS | all 1660 generated rows keep MTS claim/no-score flags false |
| VAL1660_11_branch_copies | PASS | branch/quarantine copies exist |
| VAL1660_12_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1660_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1660_14_formalization_untouched | PASS | no 1660 outputs found under formalization-workbench |
| VAL1660_OVERALL | PASS | 1660 conservative-LD curvature/frame input validation |

## Working Interpretation

The geometry branch is no longer blocked by not knowing any curvature scale. It is blocked by the local projector theorem itself. The next proof attempt should therefore target the constants/frame silence, not more R10 geometry.
