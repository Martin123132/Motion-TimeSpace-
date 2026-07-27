# 1072 - MICROSCOPE data portal schema or reconstructed gxS kernel

## Current verdict
1072 does not yet obtain the official CMSM schema or arrays. It does, however, stage the REGARDS/CMSM route, preserve the exact missing requirements, and build a segment-210 `gx/gz/Sxx/Sxz` dry-run preview that exercises the reconstruction path without claiming it is a physical tau_WEP kernel.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1072_0_1071_next | source-intake/mts_residuals/P8_Y5_R10_1071_NEXT_TARGET.csv | true | true | 1071 handoff. |
| SRC1072_1_1071_validation | source-intake/mts_residuals/P8_Y5_BRR545_1071_VALIDATION.csv | true | true | 1071 validation summary. |
| SRC1072_2_1071_kernel | source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | true | true | official kernel skeleton. |
| SRC1072_3_1071_segments | source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | true | true | segment 210 source-backed row. |
| SRC1072_4_1071_portal | source-intake/mts_residuals/P8_Y5_R10_1071_DATA_PORTAL_PROBE.csv | true | true | portal probe result. |
| SRC1072_5_1071_tau | source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv | true | true | numeric tau still missing. |
| SRC1072_6_1071_product | source-intake/mts_residuals/P8_Y5_R10_1071_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv | true | true | prior product refusal. |
| SRC1072_7_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## External source ledger
| external_id | source_url | source_lines | use_for_1072 | extracted_item |
| --- | --- | --- | --- | --- |
| EXT1072_0_OCA_data_inventory_pointer | https://www.oca.eu/fr/microscope | OCA page lines 198-203 | schema/file inventory target | OCA says raw, calibrated, and auxiliary data for analyses are associated with the CMSM REGARDS portal and user support. |
| EXT1072_1_ONERA_data_available | https://microscope.onera.fr/fr/publication/microscope-data-are-available | ONERA public data page | portal provenance | ONERA points mission users to https://cmsm-ds.onera.fr/user/microscope for MICROSCOPE data. |
| EXT1072_2_REGARDS_search_download | https://regardsoss.github.io/ | REGARDS docs lines 48-64 | candidate schema/API route | REGARDS advertises OpenSearch/GeoJSON/STAC discovery and HTTP file serving. |
| EXT1072_3_REGARDS_access_project | https://regardsoss.github.io/docs/development/services/access-project/overview | REGARDS access-project docs lines 91-99 | candidate API host service | rs-access-project proxies rs-catalog and rs-storage for search/product access and quotas. |
| EXT1072_4_REGARDS_api_endpoints | https://regardsoss.github.io/docs/development/services/access-project/api-swagger | REGARDS API docs lines 111-116 and 1515-1523 | candidate endpoint ledger | access-project exposes catalogue search endpoints, including dataobjects/datasets search. |
| EXT1072_5_CQG_data_product_requirements | https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf | CQG 2022 PDF lines 341-351 | numeric kernel product requirements | MICROSCOPE analysis used 4 Hz accelerometer measurements, same-stamp attitude/angular velocity/angular acceleration, and minute-sampled satellite position/velocity. |
| EXT1072_6_CQG_fit_basis | https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf | CQG 2022 PDF lines 491-543 | dry-run kernel basis | corrected X-axis model uses polynomial drift plus gx,gz,Sxx,Sxz columns. |

## Portal route probe
| url | probe_status | http_status | content_type | bytes_sampled | schema_or_data_inventory_acquired | error |
| --- | --- | --- | --- | --- | --- | --- |
| https://microscope.onera.fr/fr/publication/microscope-data-are-available | HTTP_OK | 200 | text/html; charset=UTF-8 | 1024 | false |  |
| https://www.oca.eu/fr/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)> |
| https://cmsm-ds.onera.fr/user/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| https://cmsm-ds.onera.fr/user/microscope/modules/7 | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/datasets/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |

## REGARDS candidate endpoints
| endpoint_id | candidate_url | regards_basis | expected_payload | auth_or_access_risk | schema_inventory_acquired |
| --- | --- | --- | --- | --- | --- |
| API1072_0_user_module | https://cmsm-ds.onera.fr/user/microscope/modules/7 | OCA direct module link; JS REGARDS UI route | browser UI metadata and module configuration | may require reachable REGARDS frontend/session | false |
| API1072_1_dataset_search | https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search | access-project catalogue dataset search endpoint | dataset catalogue entries | REGARDS_OAUTH2 or public tenant routing may be required | false |
| API1072_2_dataobject_search | https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search | access-project product/dataobject search endpoint | dataobject/product catalogue entries | query parameters and auth may be required | false |
| API1072_3_joined_dataobject_dataset_search | https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/datasets/search | documented joined OpenSearch request returning datasets associated with dataobject criteria | dataset records matching dataobject criteria | allParams query object required; may require OAuth2 | false |
| API1072_4_module_config | https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules | documented UI module retrieval endpoint pattern | UI modules for application id microscope if public and correctly named | application id may differ; OAuth2 likely | false |

## Reconstruction requirements
| requirement_id | object | why_needed | current_status | source_hint |
| --- | --- | --- | --- | --- |
| REQ1072_0_exact_time_grid | exact segment timestamps | phase of gx,gz,Sxx,Sxz depends on actual timestamps and segment masks | MISSING_EXACT_TIMESTAMPS | CMSM 4 Hz accelerometer products |
| REQ1072_1_orbit_ephemeris | J2000 satellite position/velocity | compute g(Osat) and gravity-gradient tensor T at satellite centre | MISSING_NUMERIC_EPHEMERIS | CMSM minute-sampled orbit products |
| REQ1072_2_attitude_angular_rates | attitude, angular velocity, angular acceleration | rotate gravity into instrument frame and build inertia gradient In | MISSING_NUMERIC_ATTITUDE_RATES | CMSM same-stamp attitude products |
| REQ1072_3_gravity_model | official gravity model convention | MICROSCOPE computes deterministic gx,gz,Sxx,Sxz accurately; MTS must not substitute a guessed spherical model for a claim | MISSING_OFFICIAL_GRAVITY_MODEL_OR_APPROVED_SURROGATE | MICROSCOPE processing references and CMSM auxiliary data |
| REQ1072_4_glitch_masks | removed-sample masks | segment table gives removed percentages, not exact masked samples | MISSING_EXACT_MASKS | CMSM data products or MICROSCOPE processing metadata |
| REQ1072_5_material_parent_map | MTS material/source response tensor | turn official MICROSCOPE design matrix into an MTS product rather than an external fit basis | MISSING_PARENT_MATERIAL_MAP | MTS parent action/theorem route |

## Dry-run kernel metadata
| dry_run_id | segment | spin_mode | full_grid_samples | preview_rows_written | phase_convention | kernel_status |
| --- | --- | --- | --- | --- | --- | --- |
| DRY1072_0_segment210_kernel_preview | 210 | V3 | 1189200 | 32 | dry_run_zero_phase_not_claim | DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU |

## Dry-run gxS preview
| preview_id | sample_index | t_sec_from_segment_start | gx_unit | gz_unit | Sxx_unit | Sxz_unit | phase_convention |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GXS1072_210_00 | 0 | 0.0 | 1.0 | 0.0 | 1.0 | 0.0 | dry_run_zero_phase_not_claim |
| GXS1072_210_01 | 38361 | 9590.25 | 0.527485419956 | -0.849564083359 | -0.443518263467 | -0.896265334581 | dry_run_zero_phase_not_claim |
| GXS1072_210_02 | 76722 | 19180.5 | -0.443518263467 | -0.896265334581 | -0.606583099942 | 0.795020089598 | dry_run_zero_phase_not_claim |
| GXS1072_210_03 | 115083 | 28770.75 | -0.995384254883 | -0.095969709448 | 0.981579629737 | 0.191053475461 | dry_run_zero_phase_not_claim |
| GXS1072_210_04 | 153444 | 38361.0 | -0.606583099942 | 0.795020089598 | -0.264113885729 | -0.964491500929 | dry_run_zero_phase_not_claim |
| GXS1072_210_05 | 191805 | 47951.25 | 0.35545677246 | 0.934692721119 | -0.747300965825 | 0.664485715781 | dry_run_zero_phase_not_claim |
| GXS1072_210_06 | 230166 | 57541.5 | 0.981579629737 | 0.191053475461 | 0.926997139029 | 0.375068399405 | dry_run_zero_phase_not_claim |
| GXS1072_210_07 | 268527 | 67131.75 | 0.680081113965 | -0.733136875644 | -0.074979356857 | -0.997185086153 | dry_run_zero_phase_not_claim |

## Numeric tau status
| status_id | object | status | next_action | claim_allowed |
| --- | --- | --- | --- | --- |
| NTS1072_0_schema_inventory | CMSM schema/file inventory | NOT_ACQUIRED_FROM_LOCAL_PROBE | use browser/manual session or find public API query parameters | false |
| NTS1072_1_dry_run_preview | segment 210 gx/gz/Sxx/Sxz preview | DRY_RUN_NUMERIC_PREVIEW_ONLY | replace zero-phase/unit-amplitude columns with official arrays | false |
| NTS1072_2_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | acquire CMSM products or reconstruct official arrays from sourced ephemeris/attitude/gravity-model inputs | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1072_0_WEP_gxS_dry_run_kernel_nonclaim_product | P_WEP_relative_source_weight | MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY | DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_CLAIM | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1072_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1072_0_WEP_gxS_dry_run_product_stub | 0 | 1 | false | reject dry-run/placeholder prediction and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1072_0_portal_schema | CMSM data schema/file inventory | false | false | portal route known but schema/product inventory not acquired by local probe |
| CG1072_1_dry_run_kernel | gx/gz/Sxx/Sxz dry-run numeric preview | true | false | code path exists, but phase/amplitude/timestamps/masks are dry-run placeholders |
| CG1072_2_official_numeric_kernel | official numeric kernel arrays | false | false | MISSING_OFFICIAL_GX_GZ_SXX_SXZ_ARRAYS |
| CG1072_3_tau_WEP_numeric | numeric tau_WEP or direct parent product | false | false | MISSING_OFFICIAL_NUMERIC_TAU_WEP_KERNEL_DRY_RUN_ONLY |
| CG1072_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1072_0_portal_route_not_enough | CMSM/REGARDS route is source-backed but not locally inventory-readable yet | P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv; P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv | need browser/manual session or exact public API parameters |
| DEC1072_1_dry_run_kernel_path | segment 210 dry-run kernel preview establishes the reconstruction code path | DRY1072_0_segment210_kernel_preview | future run can replace unit zero-phase columns with official arrays |
| DEC1072_2_no_claim | do not score WEP/local-GR claim | NTS1072_2_tau_WEP; APR1072_0_WEP_gxS_dry_run_product_stub | numeric tau_WEP remains the barrier |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1072_0_sources_exist | pass | all cited local source paths and needles are present |
| V1072_1_external_sources_recorded | pass | OCA/REGARDS/CQG source rows recorded |
| V1072_2_portal_probes_recorded | pass | CMSM portal and API route probes recorded |
| V1072_3_endpoint_candidates | pass | REGARDS candidate API endpoints staged |
| V1072_4_requirements_block_claim | pass | core numeric reconstruction requirements remain explicit |
| V1072_5_dry_run_metadata | pass | dry-run metadata has expected segment 210 sample count and nonclaim status |
| V1072_6_preview_rows | pass | 32 nonclaim preview rows written |
| V1072_7_tau_not_acquired | pass | numeric tau_WEP remains not acquired |
| V1072_8_prediction_nonclaim_missing | pass | prediction row remains nonclaim and missing official numeric kernel |
| V1072_9_bound_numeric | pass | bound import is positive numeric |
| V1072_10_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1072_11_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1072_12_next_target | pass | 1073 handoff written |
| V1072_13_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1072_14_csv_parse | pass | all 1072 CSV outputs parse cleanly |
| V1072_15_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1072_SUMMARY | pass | portal/API route staged and dry-run gxS kernel preview built; official numeric tau/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1072_0_1073 | 1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md | use a browser/manual CMSM session or a discovered public REGARDS query to obtain the actual MICROSCOPE file/schema inventory, then replace the segment-210 dry-run gx/gz/Sxx/Sxz preview with official or source-reconstructed arrays for one pilot segment. | CMSM UI screenshots or API response; dataset/file names; schema columns; one segment exact timestamps/masks; official gx/gz/Sxx/Sxz array extraction; runner refusal gates | public WEP/local-GR claim; zero-phase dry-run as evidence; guessed masks; guessed amplitudes; tau=1; GitHub; formalization edits |

