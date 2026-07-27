from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1409-Y5-R10-RAB-Ua-kernel-first-fill-or-official-readout-blocker-ledger.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1409_SOURCE_REGISTER.csv"
WEB_PROBE_PATH = SRC_DIR / "P8_Y5_R10_1409_WEB_SOURCE_PROBE_LEDGER.csv"
UA_FILL_PATH = SRC_DIR / "P8_Y5_R10_1409_UA_FIRST_FILL_ATTEMPT.csv"
BLOCKER_PATH = SRC_DIR / "P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv"
TEMPLATE_UPDATE_PATH = SRC_DIR / "P8_Y5_R10_1409_UA_TEMPLATE_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1409_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1409_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1409_VALIDATION.csv"

STATUS = "Y5_R10_1409_Ua_kernel_first_fill_blocked_official_readout_ledger_written_nonclaim"
CLAIM_CEILING = (
    "Ua_kernel_blocker_ledger_only_no_WEP_pass_no_Ps_products_no_clock_transfer_"
    "no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1409_0_1408_doc",
            "source_path": "1408-Y5-R10-RAB-sector-beta-source-fill-queue-and-Ua-kernel-contract.md",
            "anchor": "NEXT1408_0_1409",
            "role": "prior checkpoint selecting U_a official kernel/readout fill attempt",
        },
        {
            "source_id": "SRC1409_1_1408_ua_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1408_UA_KERNEL_CONTRACT.csv",
            "anchor": "UAK1408_8_verdict",
            "role": "U_a kernel contract ready but missing source/readout/material values",
        },
        {
            "source_id": "SRC1409_2_1225_tau_attempt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
            "anchor": "TAU1225_6_verdict",
            "role": "tau_WEP projection attempt remains not derived",
        },
        {
            "source_id": "SRC1409_3_1225_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "anchor": "ACQ1225_0_official_readout_arrays",
            "role": "official arrays, product convention, source worldtube, and orbit-average acquisition rows",
        },
        {
            "source_id": "SRC1409_4_1225_formula",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "anchor": "FORM1225_0_tau_WEP_functional",
            "role": "symbolic tau_WEP functional needing official source/readout kernel",
        },
        {
            "source_id": "SRC1409_5_1225_shortcuts",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv",
            "anchor": "SHORT1225_0_no_tau_unity",
            "role": "anti-shortcut policy forbidding tau_WEP=1 and surrogate promotion",
        },
        {
            "source_id": "SRC1409_6_1325_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1325_FIRST_FILL_INPUT_MATRIX.csv",
            "anchor": "IN1325_8_readout_arrays",
            "role": "first-fill matrix showing official readout arrays not imported",
        },
        {
            "source_id": "SRC1409_7_1325_decomposition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1325_WEP_PRODUCT_DECOMPOSITION.csv",
            "anchor": "DECOMP1325_3_full_finite_tensor",
            "role": "finite tensor formula-ready but blocked by missing source/kernel/material inputs",
        },
        {
            "source_id": "SRC1409_8_1071_kernel_skeleton",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
            "anchor": "KER1071_6_verdict",
            "role": "official MICROSCOPE kernel skeleton acquired, numeric tau not acquired",
        },
        {
            "source_id": "SRC1409_9_1072_requirements",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv",
            "anchor": "REQ1072_5_material_parent_map",
            "role": "exact reconstruction requirements for time grid, ephemeris, attitude, masks, gravity model, and material map",
        },
        {
            "source_id": "SRC1409_10_1074_surrogate_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv",
            "anchor": "STAT1074_3_tau_WEP",
            "role": "surrogate preview exists but official arrays and tau_WEP remain not acquired",
        },
        {
            "source_id": "SRC1409_11_1071_validation",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_1071_VALIDATION.csv",
            "anchor": "V1071_SUMMARY",
            "role": "prior validation: kernel skeleton and SUEP table acquired; numeric tau/product blocked",
        },
        {
            "source_id": "SRC1409_12_1072_validation",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_1072_VALIDATION.csv",
            "anchor": "V1072_SUMMARY",
            "role": "prior validation: portal/API route staged and dry-run preview built; official numeric tau/product blocked",
        },
        {
            "source_id": "SRC1409_13_1074_validation",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_1074_VALIDATION.csv",
            "anchor": "V1074_SUMMARY",
            "role": "prior validation: no local CMSM export found; surrogate preview nonclaim",
        },
        {
            "source_id": "SRC1409_14_this_script",
            "source_path": "scripts/Y5_R10_RAB_Ua_kernel_first_fill_or_official_readout_blocker_ledger.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def web_probe_rows() -> list[dict[str, Any]]:
    return [
        {
            "probe_id": "WEB1409_0_mission_scenario_data_flow",
            "source_url": "https://arxiv.org/abs/2201.10841",
            "source_label": "MICROSCOPE mission scenario, ground segment, and data processing",
            "what_it_supports": "public description of data flow and processing roles",
            "what_it_does_not_supply": "claim-grade local CMSM time arrays for gx, gz, Sxx, Sxz, masks, calibration flags, and exact observed-frame convention",
            "acquisition_result": "CONTEXT_ONLY_NO_MACHINE_READABLE_KERNEL_ARRAYS_ACQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "WEB1409_1_final_result_kernel_context",
            "source_url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "source_label": "MICROSCOPE final results in Classical and Quantum Gravity 2022",
            "what_it_supports": "final eta result, SUEP/SUREF segment counts, measurement model, regression basis, and material context",
            "what_it_does_not_supply": "downloaded segment-level official numeric gx/gz/Sxx/Sxz arrays and masks in this checkpoint",
            "acquisition_result": "SOURCE_BACKED_FORM_YES_NUMERIC_ARRAYS_NO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "WEB1409_2_onera_portal_pointer",
            "source_url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "source_label": "ONERA public pointer to MICROSCOPE data portal",
            "what_it_supports": "a route to a CMSM data portal exists",
            "what_it_does_not_supply": "local authenticated or machine-readable export inside post-checkpoint-work",
            "acquisition_result": "PORTAL_POINTER_ONLY_NO_LOCAL_CMSM_EXPORT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "WEB1409_3_prior_false_positive_filter",
            "source_url": "local_search_record",
            "source_label": "search hits containing unrelated microbial MicroScope resources",
            "what_it_supports": "filtering discipline for source acquisition",
            "what_it_does_not_supply": "physics mission arrays or WEP readout information",
            "acquisition_result": "IRRELEVANT_FALSE_POSITIVES_FILTERED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ua_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "UFF1409_0_definition",
            "component": "U_a",
            "attempt": "use U_a := K_ab(lambda,lab) alpha_source^b as the common WEP source/readout contraction",
            "status": "SYMBOLIC_ONLY",
            "evidence": "FORM1225_0_tau_WEP_functional; UAK1408_0_definition",
            "missing": "numeric K_ab; numeric alpha_source^b; normalization to eta_AB",
            "next_action": "keep as formula until official readout/source arrays or exact equivalent are available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_1_official_readout_arrays",
            "component": "K_ab(lambda,lab)",
            "attempt": "reuse prior MICROSCOPE official-kernel intake attempts",
            "status": "OFFICIAL_ARRAYS_NOT_ACQUIRED",
            "evidence": "KER1071_6_verdict; NTS1072_2_tau_WEP; STAT1074_2_official_arrays",
            "missing": "time; segment/session id; gx; gz; Sxx; Sxz; masks; calibration flags; attitude/orbit convention",
            "next_action": "only promote after CMSM export or an exact source-backed reconstruction is present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_2_source_worldtube",
            "component": "alpha_source^b",
            "attempt": "map Earth/source gravity leg into parent source-current basis",
            "status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "evidence": "TAU1225_0_source_worldtube; KER1071_2_source_gravity_leg",
            "missing": "source stress/current profile in same parent basis as beta_s and U_a",
            "next_action": "derive source-current owner or source an Earth profile/operator compatible with the parent basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_3_orbit_average",
            "component": "lab/orbit average",
            "attempt": "match U_a contraction to selected SUEP readout windows",
            "status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "evidence": "TAU1225_1_orbit_average; KER1071_4_segment_window; REQ1072_0_exact_time_grid",
            "missing": "exact time grid, segment masks, and orbit-average weights",
            "next_action": "acquire exact CMSM segment files or keep only nonclaim shape smoke previews",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_4_product_normalization",
            "component": "N_eta/product convention",
            "attempt": "normalize source response x material response x readout kernel to reported Eotvos eta",
            "status": "NORMALIZATION_NOT_FILLED",
            "evidence": "TAU1225_5_normalization; ACQ1225_1_product_convention",
            "missing": "official product convention and MTS response-to-eta normalization",
            "next_action": "derive product convention or source it from the experiment/model interface before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_5_observed_frame",
            "component": "e_obs/source frame",
            "attempt": "reuse observed-frame convention from prior spine",
            "status": "CONDITIONAL_ONLY",
            "evidence": "TAU1225_2_observed_coframe; REQ1072_2_attitude_angular_rates",
            "missing": "source-backed observed-frame convention tied to exact attitude/orbit arrays",
            "next_action": "frame convention can be kept symbolic, but not used for a numeric claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_6_material_tensor",
            "component": "Delta f_s,AB / R_material",
            "attempt": "contract U_a with Ti/Pt material response",
            "status": "MISSING_FULL_MATERIAL_TENSOR",
            "evidence": "DECOMP1325_3_full_finite_tensor; FQ1408_3_Delta_f_tensor",
            "missing": "full material contrast tensor in the same parent basis, not one alpha/surface smoke row",
            "next_action": "fill material tensor or keep WEP branch nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_7_public_papers",
            "component": "external source context",
            "attempt": "check public papers/portal route for claim-grade arrays",
            "status": "CONTEXT_YES_ARRAYS_NO",
            "evidence": "WEB1409_0_mission_scenario_data_flow; WEB1409_1_final_result_kernel_context; WEB1409_2_onera_portal_pointer",
            "missing": "local claim-grade official CMSM export or machine-readable equivalent",
            "next_action": "record blocker ledger rather than fabricating tau_WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "UFF1409_8_verdict",
            "component": "U_a first-fill status",
            "attempt": "decide whether U_a can be filled now",
            "status": "UA_FIRST_FILL_BLOCKED_OFFICIAL_READOUT_LEDGER_WRITTEN",
            "evidence": "UFF1409_1_official_readout_arrays; UFF1409_2_source_worldtube; UFF1409_4_product_normalization",
            "missing": "official readout arrays, source worldtube, orbit-average, product normalization, observed-frame lock, and material tensor",
            "next_action": "do not score P_s; move parallel derivation pressure to beta_EM/beta_nuc owner/bound route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "ORB1409_0_CMSM_export",
            "required_object": "official or exactly equivalent CMSM export",
            "required_fields": "time;segment/session;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude/orbit_convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_ACQUIRED",
            "why_it_blocks": "K_ab cannot be built or normalized without the actual WEP readout/design arrays",
            "acceptable_resolution": "download/import official CMSM files or reproduce arrays with source-backed ephemeris, attitude, gravity model, and masks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_1_exact_equivalent_proof",
            "required_object": "exact-equivalent reconstruction certificate",
            "required_fields": "time_grid;orbit_ephemeris;attitude_rates;gravity_model;masks;frequency_convention;validation_against_official_basis",
            "current_status": "NOT_PROVED",
            "why_it_blocks": "surrogate gx/S previews cannot be promoted to a claim-grade MICROSCOPE kernel",
            "acceptable_resolution": "reconstruction reproduces official kernel columns within declared tolerance and provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_2_product_convention",
            "required_object": "WEP product normalization",
            "required_fields": "N_eta;sign_convention;readout_axis;material_pair;source_response_basis;eta_mapping",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "why_it_blocks": "beta_s^a U_a cannot be compared to eta_AB bound",
            "acceptable_resolution": "derive or source the map from source/material/readout contraction to reported eta",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_3_source_worldtube",
            "required_object": "Earth/source stress-current worldtube",
            "required_fields": "source_profile;parent_basis;lab_frame_projection;lambda_or_domain;uncertainty",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "why_it_blocks": "alpha_source^b is not a number or vector in the parent basis",
            "acceptable_resolution": "derive source-current owner or import a compatible source model with units and uncertainty",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_4_orbit_average",
            "required_object": "orbit/session averaging operator",
            "required_fields": "segment_windows;exact_masks;sample_weights;orbit_average_rule;calibration_flags",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "why_it_blocks": "U_a cannot be matched to the reported experiment channel",
            "acceptable_resolution": "official segment files or exact reconstruction with masks and sampling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_5_material_tensor",
            "required_object": "full material response tensor",
            "required_fields": "Delta_f_s_AB;sector_basis;uncertainties;basis_map_to_beta_s;TiPt_material_definition",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "why_it_blocks": "one pair or one composition scalar cannot certify all WEP sector products",
            "acceptable_resolution": "fill tensor rows in the same basis as beta_s and U_a",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_6_anti_shortcuts",
            "required_object": "shortcut guard",
            "required_fields": "no_tau_unity;no_surrogate_claim;no_G_absorption;no_one_pair_cancellation",
            "current_status": "ENFORCED",
            "why_it_blocks": "prevents a fake WEP pass from tau_WEP=1 or surrogate kernels",
            "acceptable_resolution": "guard remains active even after numeric fills; claims need all gates clear",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ORB1409_7_verdict",
            "required_object": "U_a blocker verdict",
            "required_fields": "all ORB1409_0 through ORB1409_5 resolved without MISSING or NOT_PROVED statuses",
            "current_status": "UA_KERNEL_BLOCKED",
            "why_it_blocks": "P_s products and WEP pressure scores would be numerology without these inputs",
            "acceptable_resolution": "return with official data or a parent derivation that removes the finite source leg",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def template_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "TEMPLATE1409_0_Ua",
            "quantity": "U_a",
            "parent_definition": "K_ab(lambda,lab) alpha_source^b",
            "units": "inverse response-coordinate or arena-normalized source factor",
            "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
            "value": "MISSING_SOURCE_VALUE",
            "uncertainty": "MISSING_UNCERTAINTY",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
            "source_anchor": "ORB1409_7_verdict",
            "arena_projection": "WEP only until transfer theorem and official readout gate close",
            "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
            "fill_status": "BLOCKER_LEDGER_RECORDED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "TEMPLATE1409_1_Ps_products",
            "quantity": "P_s := beta_s^a U_a",
            "parent_definition": "sector response product",
            "units": "dimensionless Eotvos-response coefficient",
            "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
            "value": "MISSING_DEPENDENT_ON_Ua_AND_BETA_s",
            "uncertainty": "MISSING_UNCERTAINTY",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_UA_FIRST_FILL_ATTEMPT.csv",
            "source_anchor": "UFF1409_8_verdict",
            "arena_projection": "WEP pressure only after all inputs are source-backed",
            "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
            "fill_status": "DEPENDENT_PRODUCTS_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "TEMPLATE1409_2_verdict",
            "quantity": "U_a template update verdict",
            "parent_definition": "source-ready row remains template-only",
            "units": "not_applicable",
            "dimension_basis": "not_applicable",
            "value": "NO_NUMERIC_PROMOTION",
            "uncertainty": "not_applicable",
            "sign_convention": "not_applicable",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_CLAIM_GATE.csv",
            "source_anchor": "GATE1409_6_verdict",
            "arena_projection": "no transfer to clocks/R10/PPN/local_GR",
            "lambda_or_domain": "not_applicable",
            "fill_status": "TEMPLATE_UPDATE_WRITTEN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1409_0_Ua",
            "claim": "U_a kernel/source contraction is derived or sourced",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "official arrays, source worldtube, orbit average, normalization, observed frame, and material tensor remain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_1_Ps_products",
            "claim": "P_s := beta_s^a U_a products can be scored",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "U_a and required beta/material inputs are not claim-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_2_WEP_pass",
            "claim": "WEP branch passes MICROSCOPE/local WEP",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1409 is blocker-ledger only and contains no claim-grade tau_WEP or eta product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_3_transfer",
            "claim": "WEP rows transfer to clocks, R10, PPN, orbital, or local GR arenas",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "arena isolation remains active and WEP source kernel is itself unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_4_surrogate",
            "claim": "surrogate gx/S preview is good enough for a claim",
            "status": "REFUSED",
            "reason": "surrogate previews may test schema only; they cannot replace official arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_5_local_GR",
            "claim": "local GR/Newton reduction can be claimed from the WEP branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "U_a blocker does not close q_loc, lambda_A, EM residuals, source kernel, PPN projection, or parent GR limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1409_6_verdict",
            "claim": "1409 promotes a WEP/local result",
            "status": "NO_PROMOTION",
            "reason": "checkpoint records exact external-data blockers and redirects derivation pressure to beta_EM/beta_nuc while U_a waits",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1409_0_1410",
            "target_doc": "1410-Y5-R10-RAB-betaEM-or-betaNuc-owner-bound-after-Ua-blocker.md",
            "target_script": "scripts/Y5_R10_RAB_betaEM_or_betaNuc_owner_bound_after_Ua_blocker.py",
            "task": "because U_a needs official external readout arrays, move the derivation-first pressure to beta_EM/beta_nuc owner-or-bound while keeping the U_a blocker active",
            "success_condition": "derive a zero/lock theorem for beta_EM or beta_nuc, or write source-ready finite bound rows with units, sign, source anchors, and nonclaim gates",
            "do_not_claim": "WEP pass; P_s products; clock/R10/PPN transfer; Newton limit; local GR; GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1409_1_data_route_parallel",
            "target_doc": "future-official-MICROSCOPE-CMSM-import-or-exact-reconstruction.md",
            "target_script": "future_manual_or_import_route",
            "task": "if official CMSM export becomes available, import or reconstruct gx/gz/Sxx/Sxz/masks/attitude/orbit arrays and rerun the U_a gate",
            "success_condition": "all ORB1409 blockers are resolved with source-backed arrays or an exact-equivalent certificate",
            "do_not_claim": "surrogate-only WEP score or tau_WEP=1 shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    web: list[dict[str, Any]],
    ua_fill: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        WEB_PROBE_PATH,
        UA_FILL_PATH,
        BLOCKER_PATH,
        TEMPLATE_UPDATE_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1409_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1409_1_web_probe_nonclaim",
        all(row["source_url"] and row["valid_for_claim"] == False for row in web),
        "web/source probe rows are recorded but remain nonclaim",
    )
    add(
        "VAL1409_2_Ua_fill_blocked",
        any(row["fill_id"] == "UFF1409_8_verdict" and row["status"] == "UA_FIRST_FILL_BLOCKED_OFFICIAL_READOUT_LEDGER_WRITTEN" for row in ua_fill)
        and all(row["valid_for_claim"] == False for row in ua_fill),
        "U_a first-fill attempt explicitly blocks promotion and keeps every row nonclaim",
    )
    required_blockers = {
        "ORB1409_0_CMSM_export",
        "ORB1409_1_exact_equivalent_proof",
        "ORB1409_2_product_convention",
        "ORB1409_3_source_worldtube",
        "ORB1409_4_orbit_average",
        "ORB1409_5_material_tensor",
        "ORB1409_6_anti_shortcuts",
        "ORB1409_7_verdict",
    }
    add(
        "VAL1409_3_blocker_ledger",
        required_blockers.issubset({row["blocker_id"] for row in blockers}) and all(row["valid_for_claim"] == False for row in blockers),
        "official readout blocker ledger includes required objects and anti-shortcut guard",
    )
    add(
        "VAL1409_4_template_update",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in templates)
        and any(row["template_id"] == "TEMPLATE1409_0_Ua" for row in templates),
        "U_a template update records blocker ledger but does not promote a numeric value",
    )
    add(
        "VAL1409_5_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "WEP, P_s, transfer, surrogate, and local-GR claims are refused",
    )
    add(
        "VAL1409_6_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1409_7_overall",
        True,
        "1409 records exact U_a official-readout/source blockers and redirects next work to beta_EM/beta_nuc derivation",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    web: list[dict[str, Any]],
    ua_fill: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1409 - U_a Kernel First Fill Or Official Readout Blocker Ledger

**Status:** `{STATUS}`

**Current verdict:** `U_a := K_ab(lambda,lab) alpha_source^b` cannot be filled as a claim-grade WEP object in this checkpoint. Prior work gives a source-backed MICROSCOPE measurement/kernel skeleton and nonclaim surrogate previews, but the official or exactly equivalent local arrays needed for `K_ab` are still not present.

**Discipline move:** this checkpoint refuses the tempting shortcut. No `tau_WEP=1`, no surrogate-kernel promotion, no one-pair cancellation, and no product score `P_s := beta_s^a U_a` are allowed. The useful result is a precise acquisition ledger: it names the exact objects needed before U_a can become numeric.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Web / External Source Probe Ledger

{md_table(web)}

## U_a First Fill Attempt

{md_table(ua_fill)}

## Official Readout Blocker Ledger

{md_table(blockers)}

## U_a Template Update

{md_table(templates)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    web = web_probe_rows()
    ua_fill = ua_fill_rows()
    blockers = blocker_rows()
    templates = template_update_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, web, ua_fill, blockers, templates, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(WEB_PROBE_PATH, web)
    write_csv(UA_FILL_PATH, ua_fill)
    write_csv(BLOCKER_PATH, blockers)
    write_csv(TEMPLATE_UPDATE_PATH, templates)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, web, ua_fill, blockers, templates, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1409 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
