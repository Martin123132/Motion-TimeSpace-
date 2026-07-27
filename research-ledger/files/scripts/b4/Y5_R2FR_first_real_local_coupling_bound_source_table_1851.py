from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1851"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md"


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_SOURCE_REGISTER.csv",
    "observable_bounds": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_OBSERVABLE_BOUND_SOURCE_TABLE.csv",
    "translation_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_MTS_TRANSLATION_GATES.csv",
    "conditional_translations": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_CONDITIONAL_BOUND_TRANSLATIONS.csv",
    "component_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_COMPONENT_BOUND_STATUS.csv",
    "local_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_LOCAL_TEST_MATRIX.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1851_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def two_sigma_abs(central: float, sigma: float) -> float:
    return abs(central) + 2.0 * sigma


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    microscope_sigma = math.sqrt(2.3e-15**2 + 1.5e-15**2)
    microscope_2sigma = two_sigma_abs(-1.5e-15, microscope_sigma)
    cassini_2sigma = two_sigma_abs(2.1e-5, 2.3e-5)
    rosenband_2sigma = two_sigma_abs(-1.6e-17, 2.3e-17)
    llr_gdot_2sigma = two_sigma_abs(7.1e-14, 7.6e-14)
    llr_ep_2sigma = two_sigma_abs(-0.8e-13, 1.3e-13)
    cassini_scalar_proxy = math.sqrt(cassini_2sigma / 2.0)

    source_rows = [
        {
            "source_id": "SRC1851_0_1850_handoff",
            "source_type": "local_checkpoint",
            "source_path": source_path("1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"),
            "source_url": "",
            "needle": "NEXT1850_0_primary",
            "use": "selected 1851 target and component/projection rows",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_1_1850_bound_pack",
            "source_type": "local_csv",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"),
            "source_url": "",
            "needle": "FMB1850_10_total_qbarXT_envelope",
            "use": "component envelope handoff",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_2_eotwash_2020",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "needle": "gravitational-strength Yukawa interactions to ranges < 38.6",
            "use": "R10 short-range Yukawa alpha(lambda) anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_3_microscope_2022",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "needle": "eta(Ti, Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15",
            "use": "WEP/source-charge differential acceleration anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_4_cassini_2003",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "needle": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "use": "PPN gamma/common-frame anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_5_rosenband_2008",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://tf.nist.gov/general/pdf/2280.pdf",
            "needle": "alpha_dot/alpha = (-1.6 +/- 2.3) x 10^-17/year",
            "use": "clock/fine-structure drift anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_6_llr_hofmann_2018",
            "source_type": "primary_paper_metadata",
            "source_path": "",
            "source_url": "https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H",
            "needle": "Gdot/G0 = (7.1 +/- 7.6) x 10^-14 yr^-1",
            "use": "orbital/source-support Gdot anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1851_7_llr_ep_2012",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://arxiv.org/abs/1203.2150",
            "needle": "(-0.8 +/- 1.3) x 10^{-13}",
            "use": "Earth-Moon EP/orbital differential source anchor",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
    ]

    observable_rows = [
        {
            "bound_id": "OBS1851_0_R10_EOTWASH_2020",
            "arena": "R10_short_range",
            "observable": "Yukawa alpha(lambda) gravitational-strength threshold",
            "central_value": "",
            "one_sigma": "",
            "conservative_bound_value": 1.0,
            "bound_rule": "95pct anchor: alpha=1 excluded for lambda >= 38.6 micrometer; not a full digitized curve",
            "lambda_value": 38.6,
            "lambda_units": "micrometer",
            "observable_units": "dimensionless",
            "confidence": "95pct",
            "source_id": "SRC1851_2_eotwash_2020",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "extraction_method": "abstract_threshold_anchor",
            "full_curve": False,
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OBS1851_1_WEP_MICROSCOPE_2022",
            "arena": "WEP",
            "observable": "Eotvos eta(Ti,Pt)",
            "central_value": -1.5e-15,
            "one_sigma": microscope_sigma,
            "conservative_bound_value": microscope_2sigma,
            "bound_rule": "|central| + 2*sqrt(stat^2+syst^2)",
            "lambda_value": "",
            "lambda_units": "",
            "observable_units": "dimensionless",
            "confidence": "derived_conservative_2sigma_from_reported_1sigma",
            "source_id": "SRC1851_3_microscope_2022",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "extraction_method": "abstract_reported_central_stat_syst",
            "full_curve": "",
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OBS1851_2_PPN_CASSINI_2003",
            "arena": "PPN",
            "observable": "gamma_minus_1",
            "central_value": 2.1e-5,
            "one_sigma": 2.3e-5,
            "conservative_bound_value": cassini_2sigma,
            "bound_rule": "|central| + 2*sigma",
            "lambda_value": "",
            "lambda_units": "",
            "observable_units": "dimensionless",
            "confidence": "derived_conservative_2sigma_from_reported_1sigma",
            "source_id": "SRC1851_4_cassini_2003",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "extraction_method": "abstract_reported_gamma_minus_one",
            "full_curve": "",
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OBS1851_3_CLOCK_ROSENBAND_2008",
            "arena": "clock_fine_structure",
            "observable": "alpha_dot_over_alpha",
            "central_value": -1.6e-17,
            "one_sigma": 2.3e-17,
            "conservative_bound_value": rosenband_2sigma,
            "bound_rule": "|central| + 2*sigma",
            "lambda_value": "",
            "lambda_units": "",
            "observable_units": "per_year",
            "confidence": "derived_conservative_2sigma_from_reported_preliminary_1sigma",
            "source_id": "SRC1851_5_rosenband_2008",
            "source_url": "https://tf.nist.gov/general/pdf/2280.pdf",
            "extraction_method": "paper_text_reported_alpha_drift",
            "full_curve": "",
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OBS1851_4_ORBITAL_LLR_GDOT_2018",
            "arena": "orbital_Gdot",
            "observable": "Gdot_over_G",
            "central_value": 7.1e-14,
            "one_sigma": 7.6e-14,
            "conservative_bound_value": llr_gdot_2sigma,
            "bound_rule": "|central| + 2*sigma",
            "lambda_value": "",
            "lambda_units": "",
            "observable_units": "per_year",
            "confidence": "derived_conservative_2sigma_from_reported_1sigma",
            "source_id": "SRC1851_6_llr_hofmann_2018",
            "source_url": "https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H",
            "extraction_method": "ADS_abstract_reported_result",
            "full_curve": "",
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OBS1851_5_ORBITAL_LLR_EP_2012",
            "arena": "orbital_EP",
            "observable": "(mG/mI)_Earth_minus_(mG/mI)_Moon",
            "central_value": -0.8e-13,
            "one_sigma": 1.3e-13,
            "conservative_bound_value": llr_ep_2sigma,
            "bound_rule": "|central| + 2*sigma",
            "lambda_value": "",
            "lambda_units": "",
            "observable_units": "dimensionless",
            "confidence": "derived_conservative_2sigma_from_reported_solution",
            "source_id": "SRC1851_7_llr_ep_2012",
            "source_url": "https://arxiv.org/abs/1203.2150",
            "extraction_method": "abstract_reported_solution",
            "full_curve": "",
            "source_backed_observable": True,
            "direct_mts_component_bound": False,
            "valid_for_claim": False,
        },
    ]

    translation_rows = [
        {
            "gate_id": "TRG1851_0_cg_to_PPN",
            "mts_component": "c_g",
            "observable_bound_id": "OBS1851_2_PPN_CASSINI_2003",
            "needed_translation": "derive tau_PPN and show c_g is the scalar/common-frame parameter entering gamma_minus_1",
            "current_translation_status": "MISSING_MTS_TO_PPN_MAP",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TRG1851_1_cg_to_R10",
            "mts_component": "c_g",
            "observable_bound_id": "OBS1851_0_R10_EOTWASH_2020",
            "needed_translation": "derive alpha_R10(lambda_X)=K_X Qbar_XH qbar_XT tau_R10 and map c_g contribution",
            "current_translation_status": "MISSING_TAU_R10_AND_KX_QBAR_LAMBDA",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TRG1851_2_bA_to_WEP",
            "mts_component": "b_A",
            "observable_bound_id": "OBS1851_1_WEP_MICROSCOPE_2022",
            "needed_translation": "derive material sensitivity vector s_A(Ti,Pt) and source/test charge projection",
            "current_translation_status": "MISSING_MATERIAL_SENSITIVITY_MAP",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TRG1851_3_balpha_to_clock",
            "mts_component": "b_alpha",
            "observable_bound_id": "OBS1851_3_CLOCK_ROSENBAND_2008",
            "needed_translation": "derive Xdot or environmental X-profile coupling to clock/fine-structure residual",
            "current_translation_status": "MISSING_X_PROFILE_OR_TIME_PROJECTION",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TRG1851_4_delta_kappa_to_orbital_EP",
            "mts_component": "delta_kappa_A",
            "observable_bound_id": "OBS1851_5_ORBITAL_LLR_EP_2012",
            "needed_translation": "derive Earth/Moon source-current composition projection",
            "current_translation_status": "MISSING_SOURCE_COMPOSITION_MAP",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TRG1851_5_qnonH_support_to_Gdot",
            "mts_component": "q_nonH;Delta_W_support;q_boundary",
            "observable_bound_id": "OBS1851_4_ORBITAL_LLR_GDOT_2018",
            "needed_translation": "derive non-Hilbert/support/source-tail projection into secular GM or Gdot",
            "current_translation_status": "MISSING_ORBITAL_SOURCE_SUPPORT_MAP",
            "source_bound_available": True,
            "direct_component_bound_now": False,
            "valid_for_claim": False,
        },
    ]

    conditional_rows = [
        {
            "conditional_id": "CBT1851_0_scalar_tensor_cg_proxy",
            "assumption": "If MTS c_g exactly reduces to a massless scalar-tensor alpha0 with gamma-1=-2 alpha0^2/(1+alpha0^2)",
            "input_bound_id": "OBS1851_2_PPN_CASSINI_2003",
            "derived_proxy_quantity": "alpha0_abs_proxy",
            "derived_proxy_bound": cassini_scalar_proxy,
            "units": "dimensionless",
            "translation_valid_for_MTS": False,
            "why_not_claim": "MTS has not derived this scalar-tensor reduction or tau_PPN normalization",
            "valid_for_claim": False,
        },
        {
            "conditional_id": "CBT1851_1_R10_alpha_anchor_proxy",
            "assumption": "If the MTS R10 branch produces a single Yukawa alpha(lambda) with lambda_X=38.6 micrometer",
            "input_bound_id": "OBS1851_0_R10_EOTWASH_2020",
            "derived_proxy_quantity": "abs_alpha_R10_proxy",
            "derived_proxy_bound": 1.0,
            "units": "dimensionless_at_lambda_38p6um",
            "translation_valid_for_MTS": False,
            "why_not_claim": "only an alpha=1 threshold anchor, not a digitized curve or MTS K_X Qbar_XH qbar_XT product",
            "valid_for_claim": False,
        },
        {
            "conditional_id": "CBT1851_2_WEP_differential_charge_proxy",
            "assumption": "If eta_AB maps directly to a differential material coupling with unit source normalization",
            "input_bound_id": "OBS1851_1_WEP_MICROSCOPE_2022",
            "derived_proxy_quantity": "abs_delta_q_material_proxy",
            "derived_proxy_bound": microscope_2sigma,
            "units": "dimensionless",
            "translation_valid_for_MTS": False,
            "why_not_claim": "MTS material sensitivity and source-current normalization are not derived",
            "valid_for_claim": False,
        },
        {
            "conditional_id": "CBT1851_3_clock_alpha_proxy",
            "assumption": "If b_alpha couples to monotonic time drift with unit Xdot per year",
            "input_bound_id": "OBS1851_3_CLOCK_ROSENBAND_2008",
            "derived_proxy_quantity": "abs_balpha_time_proxy",
            "derived_proxy_bound": rosenband_2sigma,
            "units": "per_year",
            "translation_valid_for_MTS": False,
            "why_not_claim": "MTS X-profile/time projection is not derived",
            "valid_for_claim": False,
        },
    ]

    component_rows = [
        {
            "component_id": "CBS1851_0_cg",
            "symbol": "c_g",
            "source_backed_observable_anchors": "OBS1851_2_PPN_CASSINI_2003;OBS1851_0_R10_EOTWASH_2020",
            "component_numeric_bound": "MISSING_MTS_PROJECTION",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_1_bdis",
            "symbol": "b_dis",
            "source_backed_observable_anchors": "OBS1851_2_PPN_CASSINI_2003;OBS1851_3_CLOCK_ROSENBAND_2008",
            "component_numeric_bound": "MISSING_DISFORMAL_PROJECTION",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_2_bA",
            "symbol": "b_A",
            "source_backed_observable_anchors": "OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012",
            "component_numeric_bound": "MISSING_MATERIAL_SENSITIVITY_MAP",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_3_balpha",
            "symbol": "b_alpha",
            "source_backed_observable_anchors": "OBS1851_3_CLOCK_ROSENBAND_2008",
            "component_numeric_bound": "MISSING_X_PROFILE_OR_TIME_PROJECTION",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_4_delta_kappa_A",
            "symbol": "delta_kappa_A",
            "source_backed_observable_anchors": "OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012",
            "component_numeric_bound": "MISSING_SOURCE_COMPOSITION_MAP",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_5_qnonH_support_boundary",
            "symbol": "q_nonH;Delta_W_support;q_boundary",
            "source_backed_observable_anchors": "OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012",
            "component_numeric_bound": "MISSING_ORBITAL_SOURCE_SUPPORT_MAP",
            "best_current_status": "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CBS1851_6_total_qbarXT",
            "symbol": "qbar_XT_bound_abs",
            "source_backed_observable_anchors": "OBS1851_0_R10_EOTWASH_2020;OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_2_PPN_CASSINI_2003;OBS1851_3_CLOCK_ROSENBAND_2008;OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012",
            "component_numeric_bound": "MISSING_ALL_TRANSLATION_GATES",
            "best_current_status": "SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    local_matrix_rows = [
        {
            "arena_id": "LTM1851_0_R10",
            "arena": "short_range_R10",
            "real_source_bound": "OBS1851_0_R10_EOTWASH_2020",
            "mts_inputs_needed": "lambda_X;K_X;Qbar_XH;qbar_XT_bound_abs;tau_R10",
            "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "LTM1851_1_WEP",
            "arena": "WEP",
            "real_source_bound": "OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012",
            "mts_inputs_needed": "material sensitivities;source-current composition;delta_kappa_A;b_A;b_marker",
            "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "LTM1851_2_PPN",
            "arena": "PPN",
            "real_source_bound": "OBS1851_2_PPN_CASSINI_2003",
            "mts_inputs_needed": "tau_PPN;c_g;b_dis;q_nonH;support/boundary mapping",
            "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "LTM1851_3_clock_EM",
            "arena": "clock_fine_structure_EM",
            "real_source_bound": "OBS1851_3_CLOCK_ROSENBAND_2008",
            "mts_inputs_needed": "Xdot/profile;b_alpha;b_A;clock sensitivity map",
            "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "LTM1851_4_orbital",
            "arena": "orbital_source_support",
            "real_source_bound": "OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012",
            "mts_inputs_needed": "q_nonH;Delta_W_support;q_boundary;source support and GM calibration mapping",
            "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1851_0_real_sources",
            "claim": "real local observable bound sources exist",
            "gate_pass": True,
            "reason": "R10, WEP, PPN, clock and orbital anchors are recorded with numeric observable bounds",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1851_1_direct_mts_component_bounds",
            "claim": "MTS component bounds are numeric",
            "gate_pass": False,
            "reason": "all direct MTS component translations remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1851_2_local_GR_claim",
            "claim": "local GR recovered from bounded couplings",
            "gate_pass": False,
            "reason": "qbar_XT_bound_abs cannot be evaluated until translation/projection gates close",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1851_3_R10_claim",
            "claim": "R10 alpha(lambda) branch passes",
            "gate_pass": False,
            "reason": "Eöt-Wash anchor is real but MTS alpha product and digitized curve are incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1851_0_source_table_win",
            "decision": "1851 succeeds as real source acquisition, not as an MTS pass.",
            "because": "local observable bounds are now explicit, numeric and source-linked across R10/WEP/PPN/clock/orbital arenas.",
            "next_action": "derive the MTS projection maps that turn those observable bounds into component bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1851_1_no_overclaim",
            "decision": "No direct component or local-GR claim is allowed yet.",
            "because": "every component row still says translation missing.",
            "next_action": "start with the least ambiguous projection: PPN/common-frame c_g or WEP/material b_A",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1851_2_best_next",
            "decision": "Next target should derive the PPN/common-frame translation gate.",
            "because": "Cassini gives the cleanest weak-field common-frame anchor and can also reject over-large c_g branches quickly.",
            "next_action": "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            "valid_for_claim": False,
        },
    ]

    next_target_rows = [
        {
            "route_id": "NEXT1851_0_primary",
            "next_target": "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            "script": "scripts/Y5_R2FR_PPN_common_frame_cg_translation_gate_1852.py",
            "objective": "derive or reject the mapping from MTS common frame coupling c_g into PPN gamma/tau_PPN, using Cassini as a real source-backed observable bound",
            "selection_status": "selected",
            "success_condition": "either c_g obtains a conditional/numeric PPN translation with clear assumptions, or the PPN/common-frame route is demoted to source-only closure",
        },
        {
            "route_id": "NEXT1851_1_parallel",
            "next_target": "1852b-Y5-R2FR-WEP-material-sensitivity-bA-translation-gate.md",
            "script": "scripts/Y5_R2FR_WEP_material_sensitivity_bA_translation_gate_1852b.py",
            "objective": "derive material sensitivity map from b_A/delta_kappa_A to MICROSCOPE/LLR WEP observables",
            "selection_status": "held",
            "success_condition": "material/source charge projection becomes explicit enough for a bound row",
        },
    ]

    return {
        "source_register": source_rows,
        "observable_bounds": observable_rows,
        "translation_gates": translation_rows,
        "conditional_translations": conditional_rows,
        "component_status": component_rows,
        "local_matrix": local_matrix_rows,
        "claim_gate": claim_gate_rows,
        "decision": decision_rows,
        "next_target": next_target_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1851_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        source_type = str(row["source_type"])
        if source_type.startswith("local"):
            path = ROOT / str(row["source_path"])
            if not path.exists():
                missing.append(str(row["source_path"]))
        else:
            if not str(row["source_url"]).startswith("http"):
                missing.append(str(row["source_id"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all local paths exist and web source URLs are recorded"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        source_type = str(row["source_type"])
        if not source_type.startswith("local"):
            continue
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all local source needles are present"


def check_observable_bounds(rows: list[dict[str, Any]]) -> tuple[bool, str]:
    bad: list[str] = []
    for row in rows:
        try:
            value = float(row["conservative_bound_value"])
            if value <= 0:
                bad.append(f"{row['bound_id']}: nonpositive bound")
        except Exception:
            bad.append(f"{row['bound_id']}: nonnumeric bound")
        if not row["source_url"] or not row["observable_units"]:
            bad.append(f"{row['bound_id']}: missing source or units")
        if boolish(row["direct_mts_component_bound"]):
            bad.append(f"{row['bound_id']}: wrongly marked direct MTS bound")
    return not bad, "bad rows: " + "; ".join(bad) if bad else "observable bounds are positive, sourced and not direct MTS component claims"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1851 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1851_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1851_0_sources_recorded", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1851_1_local_needles_present", ok, detail))
    ok, detail = check_observable_bounds(rows_map["observable_bounds"])
    checks.append(("VAL1851_2_observable_bounds_numeric", ok, detail))
    checks.append(
        (
            "VAL1851_3_arena_coverage",
            len({row["arena"] for row in rows_map["observable_bounds"]}) >= 5,
            "R10/WEP/PPN/clock/orbital anchors are represented",
        )
    )
    checks.append(
        (
            "VAL1851_4_translation_gates_block",
            all(not boolish(row["direct_component_bound_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["translation_gates"]),
            "translation gates keep direct component bounds blocked",
        )
    )
    checks.append(
        (
            "VAL1851_5_conditionals_nonclaim",
            all(not boolish(row["translation_valid_for_MTS"]) and not boolish(row["valid_for_claim"]) for row in rows_map["conditional_translations"]),
            "conditional proxy translations are nonclaim",
        )
    )
    checks.append(
        (
            "VAL1851_6_components_nonclaim",
            all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["component_status"]),
            "component rows remain claim-blocked",
        )
    )
    checks.append(
        (
            "VAL1851_7_local_matrix_nonclaim",
            all(str(row["status"]) == "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING" and not boolish(row["claim_allowed"]) for row in rows_map["local_matrix"]),
            "local test matrix records real anchors but missing MTS translations",
        )
    )
    checks.append(
        (
            "VAL1851_8_claim_gates_safe",
            any(row["gate_id"] == "CG1851_0_real_sources" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "only real-source acquisition passes; no MTS claim passes",
        )
    )
    checks.append(
        (
            "VAL1851_9_decision_next",
            any(row["decision_id"] == "DEC1851_2_best_next" and "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md" in row["next_action"] for row in rows_map["decision"]),
            "decision ledger selects PPN/common-frame translation gate",
        )
    )
    checks.append(
        (
            "VAL1851_10_next_target_selected",
            any(row["route_id"] == "NEXT1851_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1851_11_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    checks.append(
        (
            "VAL1851_12_missing_rows_nonclaim",
            all(
                not boolish(row.get("valid_for_claim", False))
                for rows in rows_map.values()
                for row in rows
                if "MISSING_" in " ".join(str(value) for value in row.values())
            ),
            "MISSING_* rows stay nonclaim",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1851_13_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1851_14_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1851_15_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1851*")) if FORMALIZATION.exists() else []
    checks.append(
        (
            "VAL1851_16_formalization_untouched",
            not formalization_outputs,
            "no 1851 outputs found under formalization-workbench",
        )
    )

    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1851_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1851 first real local coupling bound source table",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1851: First Real Local Coupling Bound Source Table",
            "",
            "**Current verdict:** this is a genuine source-acquisition win, not a physics-claim win. R10, WEP, PPN, clock/fine-structure and orbital anchors now have real numeric observable bounds attached. But every MTS component bound still waits on a translation/projection theorem, so `c_g`, `b_A`, `b_alpha`, `q_nonH`, `qbar_XT`, local GR and R10 pass claims remain blocked.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_type", "source_path", "source_url", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Observable Bound Source Table",
            markdown_table(rows_map["observable_bounds"], ["bound_id", "arena", "observable", "central_value", "one_sigma", "conservative_bound_value", "bound_rule", "lambda_value", "lambda_units", "observable_units", "confidence", "source_id", "source_url", "extraction_method", "source_backed_observable", "direct_mts_component_bound", "valid_for_claim"]),
            "",
            "## MTS Translation Gates",
            markdown_table(rows_map["translation_gates"], ["gate_id", "mts_component", "observable_bound_id", "needed_translation", "current_translation_status", "source_bound_available", "direct_component_bound_now", "valid_for_claim"]),
            "",
            "## Conditional Bound Translations",
            markdown_table(rows_map["conditional_translations"], ["conditional_id", "assumption", "input_bound_id", "derived_proxy_quantity", "derived_proxy_bound", "units", "translation_valid_for_MTS", "why_not_claim", "valid_for_claim"]),
            "",
            "## Component Bound Status",
            markdown_table(rows_map["component_status"], ["component_id", "symbol", "source_backed_observable_anchors", "component_numeric_bound", "best_current_status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Local Test Matrix",
            markdown_table(rows_map["local_matrix"], ["arena_id", "arena", "real_source_bound", "mts_inputs_needed", "status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is exactly the Mayweather route: not a knockout, but clean footwork. The project now has real local-test ropes around the coupling gap. The next fight is not hunting more bounds; it is deriving one translation map cleanly enough that the first component can actually be constrained.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1851 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
