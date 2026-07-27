from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1481"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1481-Y5-R10-RAB-same-branch-WEP-material-tau-source-pack-or-Hom-parent-generator-proof.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1480_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1480_VALIDATION.csv"
PREV_INPUTS = OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_INPUT_MATRIX.csv"
PREV_SMOKE = OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv"
PREV_PROXY = OUT / "P8_Y5_R10_1480_PROXY_SMOKE_QUARANTINE_RESULTS.csv"
PREV_REJECTION = OUT / "P8_Y5_R10_1480_RUNNER_REJECTION_LEDGER.csv"
PREV_HOM = OUT / "P8_Y5_R10_1480_COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT.csv"
PREV_HOM_OBS = OUT / "P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv"

MAT_651 = OUT / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv"
MAT_983 = OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv"
PROXY_983 = OUT / "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv"
MCON_1061 = OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv"
MREQ_1068 = OUT / "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv"
MAT_1080 = OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv"
NO_CANCEL_1087 = OUT / "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv"
WCM_1053 = OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"
MAT_1424 = OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv"
FSP_1232 = OUT / "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"
FORM_1232 = OUT / "P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv"

WAIT_1335 = OUT / "P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv"
MAN_1335 = OUT / "P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv"
WPN_1335 = OUT / "P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv"
TAU_TABLE_1335 = OUT / "P8_Y5_R10_1335_EPSILON_E_BOUND_RESCALING_TABLE.csv"
INTAKE_1228 = OUT / "P8_Y5_R10_1228_INTAKE_DIRECTORY_CONTRACT.csv"
ACCEPT_1228 = OUT / "P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv"
FEED_1228 = OUT / "P8_Y5_R10_1228_TAU_WEP_FEED_UPDATE.csv"
PACK_1426 = OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv"

PFT_1050 = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
NMM_1051 = OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
VOE_1058 = OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
NMF_980 = OUT / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1481_SOURCE_REGISTER.csv"
MATERIAL_CONTEXT = OUT / "P8_Y5_R10_1481_WEP_MATERIAL_CONTEXT_PACK.csv"
TAU_SOURCE_PACK = OUT / "P8_Y5_R10_1481_WEP_TAU_SOURCE_READOUT_PACK.csv"
SAME_BRANCH_CONTRACT = OUT / "P8_Y5_R10_1481_SAME_BRANCH_WEP_PRODUCT_CONTRACT.csv"
UPDATED_SMOKE = OUT / "P8_Y5_R10_1481_SAME_BRANCH_WEP_SMOKE_UPDATE_NONCLAIM.csv"
HOM_GENERATOR = OUT / "P8_Y5_R10_1481_HOM_PARENT_GENERATOR_PROOF_SHARPENING.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1481_REJECTION_LEDGER.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1481_REDUCTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1481_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1481_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1481_VALIDATION.csv"

QUAR_MATERIAL = QUARANTINE / "WEP_MATERIAL_CONTEXT_PACK_NONCLAIM.csv"
QUAR_SMOKE = QUARANTINE / "SAME_BRANCH_WEP_SMOKE_UPDATE_NONCLAIM.csv"
BRANCH_MATERIAL = COEFF / "WEP_material_context_pack_nonclaim_1481.csv"
BRANCH_SMOKE = COEFF / "same_branch_WEP_smoke_update_nonclaim_1481.csv"
BRANCH_GATES = COEFF / "same_branch_WEP_reduction_gates_1481.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def find_row(path: Path, column: str, value: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    for row in read_csv(path):
        if row.get(column) == value:
            return row
    return None


def as_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_INPUT"
    return f"{value:.12e}"


def copy_nonclaim(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1481_0_prev_next", PREV_NEXT, "1480 handoff selecting same-branch WEP pack or Hom generator proof"),
        ("SRC1481_1_prev_validation", PREV_VALIDATION, "1480 validation baseline"),
        ("SRC1481_2_prev_inputs", PREV_INPUTS, "same-branch WEP input matrix"),
        ("SRC1481_3_prev_smoke", PREV_SMOKE, "1480 WEP smoke results"),
        ("SRC1481_4_prev_proxy", PREV_PROXY, "quarantined proxy smoke results"),
        ("SRC1481_5_prev_rejection", PREV_REJECTION, "runner rejection ledger"),
        ("SRC1481_6_prev_Hom", PREV_HOM, "coefficient-domain Hom attempt"),
        ("SRC1481_7_prev_Hom_obstructions", PREV_HOM_OBS, "Hom obstruction ledger"),
        ("SRC1481_8_local_bounds", LOCAL_BOUNDS, "eta bound and local bound anchors"),
        ("SRC1481_9_MAT651", MAT_651, "MICROSCOPE material model context"),
        ("SRC1481_10_MAT983", MAT_983, "MICROSCOPE material constituents"),
        ("SRC1481_11_PROXY983", PROXY_983, "proxy material charge vectors"),
        ("SRC1481_12_MCON1061", MCON_1061, "WEP material convention"),
        ("SRC1481_13_MREQ1068", MREQ_1068, "material response requirements"),
        ("SRC1481_14_MAT1080", MAT_1080, "material tensor candidates"),
        ("SRC1481_15_NOCANCEL1087", NO_CANCEL_1087, "all-material no-cancellation policy"),
        ("SRC1481_16_WCM1053", WCM_1053, "WEP composition charge matrix"),
        ("SRC1481_17_MAT1424", MAT_1424, "Ti/Pt material vector candidates"),
        ("SRC1481_18_FSP1232", FSP_1232, "Ti/Pt component fraction source pack"),
        ("SRC1481_19_FORM1232", FORM_1232, "component fraction formula ledger"),
        ("SRC1481_20_WAIT1335", WAIT_1335, "readout/source waitstate"),
        ("SRC1481_21_MAN1335", MAN_1335, "official input request manifest"),
        ("SRC1481_22_WPN1335", WPN_1335, "electron WEP product normalization contract"),
        ("SRC1481_23_TAU1335", TAU_TABLE_1335, "epsilon_e tau sensitivity table"),
        ("SRC1481_24_INTAKE1228", INTAKE_1228, "MICROSCOPE intake directory contract"),
        ("SRC1481_25_ACCEPT1228", ACCEPT_1228, "MICROSCOPE acceptance gates"),
        ("SRC1481_26_FEED1228", FEED_1228, "tau_WEP feed update"),
        ("SRC1481_27_PACK1426", PACK_1426, "finite WEP coefficient input pack"),
        ("SRC1481_28_PFT1050", PFT_1050, "product functor theorem attempt"),
        ("SRC1481_29_NMM1051", NMM_1051, "no mixed morphism lemma"),
        ("SRC1481_30_VOE1058", VOE_1058, "visible operator-domain exhaustion attempt"),
        ("SRC1481_31_NMF980", NMF_980, "no-marker functor theorem attempt"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def material_sums() -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in read_csv(MAT_983):
        material = row["material_id"]
        totals[material] = totals.get(material, 0.0) + float(row["mass_fraction"])
    return totals


def numeric_context() -> dict[str, float | None]:
    r1 = find_row(LOCAL_BOUNDS, "row_id", "R1_WEP_source_charge")
    alpha = find_row(WCM_1053, "matrix_id", "WCM1053_4")
    surface = find_row(WCM_1053, "matrix_id", "WCM1053_5")
    electron = find_row(MAT_1424, "candidate_id", "MAT1424_2_electron_mass_fraction")
    proxy_pt = find_row(PROXY_983, "material_id", "M983_0_PtRh10")
    proxy_ti = find_row(PROXY_983, "material_id", "M983_1_TiAlloy")
    eta = as_float(r1.get("upper_bound") if r1 else None)
    delta_alpha = as_float(alpha.get("delta_Q_abs_for_pair") if alpha else None)
    delta_surface = as_float(surface.get("delta_Q_abs_for_pair") if surface else None)
    delta_e = as_float(electron.get("numeric_value") if electron else None)
    y_e_pt = as_float(proxy_pt.get("Y_e_proxy") if proxy_pt else None)
    y_e_ti = as_float(proxy_ti.get("Y_e_proxy") if proxy_ti else None)
    return {
        "eta": eta,
        "delta_alpha": delta_alpha,
        "delta_surface": delta_surface,
        "delta_e": delta_e,
        "y_e_delta": (y_e_ti - y_e_pt) if y_e_ti is not None and y_e_pt is not None else None,
        "electron_proxy_bound": eta / delta_e if eta is not None and delta_e not in (None, 0.0) else None,
        "alpha_smoke_bound": eta / delta_alpha if eta is not None and delta_alpha not in (None, 0.0) else None,
        "surface_smoke_bound": eta / delta_surface if eta is not None and delta_surface not in (None, 0.0) else None,
    }


def material_context_rows(ctx: dict[str, float | None]) -> list[dict[str, Any]]:
    totals = material_sums()
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_0_pair_convention",
            "object": "MICROSCOPE Ti/Pt pair convention",
            "value_or_status": "TA6V_minus_PtRh10",
            "source_path": rel(MCON_1061),
            "source_anchor": "MCON1061_0_test_pair",
            "filled_level": "SMOKE_CONTEXT_FILLED",
            "missing_for_claim": "same-branch parent material tensor and readout/source convention",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_1_mass_fraction_sums",
            "object": "PtRh10 and TA6V alloy mass-fraction sums",
            "value_or_status": f"PtRh10={totals.get('M983_0_PtRh10', float('nan')):.6f};TA6V={totals.get('M983_1_TiAlloy', float('nan')):.6f}",
            "source_path": rel(MAT_983),
            "source_anchor": "M983_0_PtRh10;M983_1_TiAlloy",
            "filled_level": "COMPOSITION_CONTEXT_FILLED",
            "missing_for_claim": "isotopic/energy-fraction tensor and parent response basis",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_2_electron_fraction_proxy",
            "object": "electron rest-mass fraction contrast",
            "value_or_status": fmt(ctx["delta_e"]),
            "source_path": rel(MAT_1424),
            "source_anchor": "MAT1424_2_electron_mass_fraction",
            "filled_level": "AUDITED_NUMERIC_PROXY",
            "missing_for_claim": "parent mass functional, tau/readout/source normalization, and same-branch coefficient",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_3_Ye_proxy_delta",
            "object": "Z/A proxy contrast",
            "value_or_status": fmt(ctx["y_e_delta"]),
            "source_path": rel(PROXY_983),
            "source_anchor": "M983_0_PtRh10;M983_1_TiAlloy",
            "filled_level": "TOY_PROXY_ONLY",
            "missing_for_claim": "not an energy/source tensor; parent basis and no-double-counting rule missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_4_DD_alpha_smoke",
            "object": "external DD alpha/Coulomb contrast",
            "value_or_status": fmt(ctx["delta_alpha"]),
            "source_path": rel(WCM_1053),
            "source_anchor": "WCM1053_4",
            "filled_level": "EXTERNAL_SMOKE_NUMERIC",
            "missing_for_claim": "MTS parent EM/Coulomb source basis and readout/source normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_5_DD_surface_smoke",
            "object": "external DD surface/binding contrast",
            "value_or_status": fmt(ctx["delta_surface"]),
            "source_path": rel(WCM_1053),
            "source_anchor": "WCM1053_5",
            "filled_level": "EXTERNAL_SMOKE_NUMERIC",
            "missing_for_claim": "full nuclear/isotopic source tensor and MTS basis map",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "MAT1481_6_full_tensor",
            "object": "full R_TA6V_minus_PtRh10 material tensor",
            "value_or_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "source_path": rel(MAT_1080),
            "source_anchor": "MAT1080_4_full_tensor_upgrade",
            "filled_level": "BLOCKED",
            "missing_for_claim": "parent response basis, full material tensor, isotope/alloy averaging, and source/readout environment stack",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def tau_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_0_official_arrays",
            "object": "official MICROSCOPE CMSM/export arrays",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source_path": rel(WAIT_1335),
            "source_anchor": "WAIT1335_0_official_arrays",
            "needed_for": "K_CMSM/readout kernel",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_1_product_convention",
            "object": "eta_AB product normalization",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source_path": rel(WAIT_1335),
            "source_anchor": "WAIT1335_1_product_convention",
            "needed_for": "same-branch product convention and units/sign",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_2_source_worldtube",
            "object": "Earth/source stress worldtube",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source_path": rel(WAIT_1335),
            "source_anchor": "WAIT1335_2_source_worldtube",
            "needed_for": "R_source source leg",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_3_orbit_average",
            "object": "MICROSCOPE orbit/session average",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source_path": rel(WAIT_1335),
            "source_anchor": "WAIT1335_3_orbit_average",
            "needed_for": "O_orbit/tau_WEP",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_4_branch_classifier",
            "object": "same parent branch classifier",
            "current_status": "MISSING_BRANCH_CLASSIFIER",
            "source_path": rel(WAIT_1335),
            "source_anchor": "WAIT1335_4_parent_branch",
            "needed_for": "anti-branch-mixing gate",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_5_intake_acceptance",
            "object": "MICROSCOPE official data intake gates",
            "current_status": "BLOCKED_LOCAL_FILE_COUNT_0",
            "source_path": rel(ACCEPT_1228),
            "source_anchor": "ACCEPT1228_0_files_present;ACCEPT1228_4_tau_WEP",
            "needed_for": "parser/tau_WEP evaluation permission",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "TAU1481_6_symbolic_tau",
            "object": "tau_eff_e := K_readout*S_source*O_orbit",
            "current_status": "TAU_EFF_NOT_FILLED",
            "source_path": rel(WPN_1335),
            "source_anchor": "WPN1335_1_tau_eff_definition",
            "needed_for": "convert proxy epsilon_e into same-branch WEP bound",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def same_branch_contract_rows() -> list[dict[str, Any]]:
    factors = [
        ("SBC1481_0_formula", "eta_pred = |K_CMSM * R_source dot C_parent dot R_material|", "contract", "FORMULA_READY_INPUTS_MISSING", "all factors below"),
        ("SBC1481_1_C_parent", "parent delta_w/component coefficient vector", "dimensionless source/action coefficients", "MISSING_PARENT_COEFFICIENT", "PACK1426_0_C_parent"),
        ("SBC1481_2_R_source", "Earth/source vector in same basis", "dimensionless/source units declared by parent basis", "MISSING_SOURCE_VECTOR", "PACK1426_3_R_source"),
        ("SBC1481_3_R_material", "TA6V-PtRh10 material tensor", "dimensionless material response", "PARTIAL_CONTEXT_ONLY", "MAT1481_0 through MAT1481_6"),
        ("SBC1481_4_K_CMSM", "readout/orbit/source projection kernel", "dimensionless tau/readout", "MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY", "TAU1481_0 through TAU1481_6"),
        ("SBC1481_5_covariance", "component covariance/no-cancellation envelope", "dimensionless covariance/norm", "MISSING_NO_CANCELLATION_ENVELOPE", "AMC1087_0 through AMC1087_2"),
        ("SBC1481_6_eta_bound", "MICROSCOPE eta source-charge bound", "dimensionless", "BOUND_ANCHOR_FILLED_NONCLAIM", "R1_WEP_source_charge"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "factor": factor,
            "units_or_domain": units,
            "current_status": status,
            "source_anchor": anchor,
            "score_ready": False if contract_id != "SBC1481_6_eta_bound" else False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, factor, units, status, anchor in factors
    ]


def updated_smoke_rows(ctx: dict[str, float | None]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WUP1481_0_same_branch_claim_grade",
            "row_type": "claim_grade_target",
            "eta_bound": fmt(ctx["eta"]),
            "material_context": "COMPOSITION_AND_PROXY_CONTEXT_FILLED",
            "tau_source_context": "OFFICIAL_ARRAYS_SOURCE_WORLDTUBE_PRODUCT_CONVENTION_MISSING",
            "computed_value": "NOT_COMPUTED",
            "status": "BLOCKED_MISSING_C_PARENT_R_SOURCE_K_CMSM_COVARIANCE_FULL_TENSOR",
            "why_nonclaim": "same-branch product factors remain missing or proxy-only",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WUP1481_1_electron_tau_rescaling_template",
            "row_type": "sensitivity_template",
            "eta_bound": fmt(ctx["eta"]),
            "material_context": f"DeltaF_e_abs={fmt(ctx['delta_e'])}",
            "tau_source_context": "epsilon_e_bound(tau_eff)=eta/(DeltaF_e_abs*abs(tau_eff))",
            "computed_value": fmt(ctx["electron_proxy_bound"]),
            "status": "UNIT_TAU_ONLY_QUARANTINED",
            "why_nonclaim": "unit tau_eff=1 is a smoke convention only",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WUP1481_2_DD_alpha_quarantine",
            "row_type": "external_smoke_quarantine",
            "eta_bound": fmt(ctx["eta"]),
            "material_context": f"DeltaQ_alpha_abs={fmt(ctx['delta_alpha'])}",
            "tau_source_context": "tau/readout/source not supplied in MTS branch",
            "computed_value": fmt(ctx["alpha_smoke_bound"]),
            "status": "EXTERNAL_SMOKE_QUARANTINED",
            "why_nonclaim": "DD alpha basis is external and not same-branch MTS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WUP1481_3_DD_surface_quarantine",
            "row_type": "external_smoke_quarantine",
            "eta_bound": fmt(ctx["eta"]),
            "material_context": f"DeltaQ_surface_abs={fmt(ctx['delta_surface'])}",
            "tau_source_context": "tau/readout/source not supplied in MTS branch",
            "computed_value": fmt(ctx["surface_smoke_bound"]),
            "status": "EXTERNAL_SMOKE_QUARANTINED",
            "why_nonclaim": "DD surface basis is external and not full MTS tensor",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def hom_generator_rows() -> list[dict[str, Any]]:
    rows = [
        ("HPG1481_0_parent_generator_image", "Allowed source coefficients are generated only by ParentGenerate[q_loc, fixed representation/topological data, declared matter currents]", "would forbid arbitrary source coefficient target", "CONTRACT_EXACT_NOT_DERIVED", "construct ParentGenerate functor and prove image exhaustion", "VOE1058_1_declared_parent_domain"),
        ("HPG1481_1_no_hidden_generator", "hidden invariant scalars are not generators for visible/source coefficients", "kills I_hid -> c(I) O_source", "BLOCKED_BY_SCALAR_OBSTRUCTION", "prove O(C_hid)^inv=R or target exclusion", "NMM1051_2_scalar_counterexample"),
        ("HPG1481_2_no_species_generator", "species labels classify matter fields/representations but are not source-prefactor generators", "kills A -> w_A or kappa_A", "CONDITIONAL_TYPING_NOT_PARENT_SIGNED", "derive no-source-only prefactor grammar", "CDH1480_2_target_forbidden"),
        ("HPG1481_3_readout_closure", "readout/EFT maps stay inside ParentGenerate image", "prevents post-variation K_CMSM from recreating source labels", "UNSIGNED_CLOSURE", "derive radiative/readout closure or keep finite residuals", "PFT1050_3_radiative_readout_closure"),
        ("HPG1481_4_verdict", "Parent-generator proof would close Hom exclusion if HPG1481_0..3 are signed", "would move Hom source coefficients toward theorem-zero", "NOT_CLOSED", "same-branch WEP pack remains needed", "CDH1480_5_verdict"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": proof_id,
            "required_statement": statement,
            "if_signed": effect,
            "current_status": status,
            "next_action": next_action,
            "source_anchor": anchor,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for proof_id, statement, effect, status, next_action, anchor in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1481_0_C_parent", "MISSING_PARENT_COEFFICIENT", "no parent coefficient vector/theorem-zero certificate"),
        ("REJ1481_1_R_source", "MISSING_SOURCE_VECTOR", "source worldtube/profile not accepted in parent basis"),
        ("REJ1481_2_K_CMSM", "MISSING_READOUT_KERNEL", "official MICROSCOPE arrays/product convention/orbit average missing"),
        ("REJ1481_3_tau", "TAU_EFF_NOT_FILLED", "tau_eff_e remains symbolic; unit tau is quarantine only"),
        ("REJ1481_4_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR", "composition and DD smoke context are not full MTS material tensor"),
        ("REJ1481_5_covariance", "MISSING_NO_CANCELLATION_ENVELOPE", "no same-basis covariance/norm policy"),
        ("REJ1481_6_Hom", "HOM_PARENT_GENERATOR_NOT_DERIVED", "source coefficient Hom remains live"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def gate_rows(
    material: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    hom: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    material_context = any(row["row_id"] == "MAT1481_1_mass_fraction_sums" and "1.000000" in row["value_or_status"] for row in material)
    full_tensor_missing = any(row["row_id"] == "MAT1481_6_full_tensor" and row["value_or_status"] == "MISSING_FULL_PARENT_MATERIAL_TENSOR" for row in material)
    tau_blocked = all(not row["score_ready"] for row in tau)
    product_blocked = all(not row["score_ready"] for row in contract)
    smoke_blocked = any(row["smoke_id"] == "WUP1481_0_same_branch_claim_grade" and row["status"].startswith("BLOCKED") for row in smoke)
    hom_not_closed = any(row["proof_id"] == "HPG1481_4_verdict" and row["current_status"] == "NOT_CLOSED" for row in hom)
    rejection_complete = all(row["blocks_claim"] for row in rejection)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_0_material_context",
            "gate": "composition/material context harvested",
            "gate_pass": material_context,
            "claim_effect": "context only; not material tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_1_full_tensor_missing",
            "gate": "full parent material tensor remains missing",
            "gate_pass": full_tensor_missing,
            "claim_effect": "blocks WEP score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_2_tau_blocked",
            "gate": "tau/source/readout pack remains blocked",
            "gate_pass": tau_blocked,
            "claim_effect": "K_CMSM/tau_WEP not score-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_3_product_blocked",
            "gate": "same-branch product contract remains blocked",
            "gate_pass": product_blocked and smoke_blocked,
            "claim_effect": "same-branch WEP runner refuses claim score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_4_Hom_not_closed",
            "gate": "Hom parent-generator proof remains open",
            "gate_pass": hom_not_closed,
            "claim_effect": "source coefficient residuals remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1481_5_rejection_complete",
            "gate": "rejection ledger blocks all claim paths",
            "gate_pass": rejection_complete,
            "claim_effect": "no WEP/local-GR promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1481_0_material_status",
            "decision": "material context is harvested but not upgraded to claim-grade tensor",
            "reason": "composition, electron proxy, and DD smoke deltas exist; parent response tensor/isotopic energy fractions do not",
            "consequence": "R_material remains partial/proxy-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1481_1_tau_status",
            "decision": "tau/readout/source pack remains blocked",
            "reason": "official arrays, source worldtube, orbit average, product convention, and branch classifier are not imported",
            "consequence": "unit-kernel proxy remains quarantine only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1481_2_next_step",
            "decision": "build an official MICROSCOPE intake/acquisition runner next",
            "reason": "the shortest empirical path is to make the readout/source/tau gate mechanically fillable",
            "consequence": "1482 should stage official file acquisition/provenance/schema checks or continue Hom generator proof if data remains unavailable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1481_0_1482",
            "next_target": "1482-Y5-R10-RAB-MICROSCOPE-official-readout-source-intake-runner-or-Hom-generator-closure.md",
            "script": "scripts/Y5_R10_RAB_MICROSCOPE_official_readout_source_intake_runner_or_Hom_generator_closure.py",
            "objective": "try to acquire or stage official MICROSCOPE readout/source-worldtube/product-convention inputs with provenance/schema gates; if unavailable, sharpen the parent-generator closure proof for Hom exclusion",
            "include": "official arrays; source worldtube; product convention; orbit average; branch classifier; checksums; parser precheck; Hom generator fallback",
            "exclude": "GitHub action; formalization-workbench edits; WEP/local-GR claim promotion; unit-kernel/DD-smoke promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    material: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    hom: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        MATERIAL_CONTEXT,
        TAU_SOURCE_PACK,
        SAME_BRANCH_CONTRACT,
        UPDATED_SMOKE,
        HOM_GENERATOR,
        REJECTION_LEDGER,
        REDUCTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    branch_copies = all(path.exists() for path in [QUAR_MATERIAL, QUAR_SMOKE, BRANCH_MATERIAL, BRANCH_SMOKE, BRANCH_GATES])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = not any(
        file.stat().st_mtime >= START_TS
        for file in FORMALIZATION.rglob("*")
        if file.is_file()
    ) if FORMALIZATION.exists() else True

    mass_sums_ok = any(row["row_id"] == "MAT1481_1_mass_fraction_sums" and "PtRh10=1.000000;TA6V=1.000000" == row["value_or_status"] for row in material)
    material_nonclaim = all(not row["score_ready"] and not row["valid_for_claim"] for row in material)
    full_tensor_missing = any(row["row_id"] == "MAT1481_6_full_tensor" and row["value_or_status"] == "MISSING_FULL_PARENT_MATERIAL_TENSOR" for row in material)
    tau_blocked = all(not row["score_ready"] and not row["claim_allowed"] for row in tau)
    product_blocked = all(not row["score_ready"] and not row["valid_for_claim"] for row in contract)
    smoke_nonclaim = all(not row["score_ready"] and not row["valid_for_claim"] for row in smoke)
    hom_open = any(row["proof_id"] == "HPG1481_4_verdict" and row["current_status"] == "NOT_CLOSED" for row in hom)
    rejection_blocks = all(row["blocks_claim"] and not row["claim_allowed"] for row in rejection)
    gates_claim_false = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in gates)

    checks = [
        ("VAL1481_0_sources", all(row["exists"] for row in sources), "all cited local source paths exist"),
        ("VAL1481_1_mass_sums", mass_sums_ok, "PtRh10 and TA6V mass fractions sum to 1.0"),
        ("VAL1481_2_material_nonclaim", material_nonclaim and full_tensor_missing, "material context harvested but full tensor remains missing/nonclaim"),
        ("VAL1481_3_tau_blocked", tau_blocked, "tau/source/readout pack remains blocked"),
        ("VAL1481_4_product_blocked", product_blocked, "same-branch product contract not score-ready"),
        ("VAL1481_5_smoke_nonclaim", smoke_nonclaim, "updated smoke rows remain nonclaim"),
        ("VAL1481_6_Hom_open", hom_open, "Hom parent-generator proof remains open"),
        ("VAL1481_7_rejection_blocks", rejection_blocks, "rejection ledger blocks claim"),
        ("VAL1481_8_gates_claim_false", gates_claim_false, "all gates keep claim flags false"),
        ("VAL1481_9_generated_csv_parse", csv_parse_ok, "all generated 1481 CSVs parse cleanly"),
        ("VAL1481_10_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1481_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1481_12_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1481_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1481 stages same-branch WEP material/tau/source pack as nonclaim and keeps Hom generator proof open",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    material: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    hom: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1481 — R10/RAB Same-Branch WEP Material/Tau/Source Pack Or Hom Parent Generator Proof")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- WEP material context is now staged: alloy composition, electron proxy, and DD alpha/surface smoke contrasts are locally available.")
    lines.append("- The same-branch claim-grade WEP product is still blocked: `C_parent`, `R_source`, full `R_material`, `K_CMSM/tau_WEP`, covariance, and branch convention are not filled.")
    lines.append("- The Hom parent-generator route is sharpened but still open; it needs a real parent-generator image/exhaustion proof, not just a grammar contract.")
    lines.append("")
    lines.append("## Material Context")
    lines.append("| row_id | value_or_status | filled_level | missing_for_claim |")
    lines.append("|---|---|---|---|")
    for row in material:
        lines.append(f"| {row['row_id']} | {row['value_or_status']} | {row['filled_level']} | {row['missing_for_claim']} |")
    lines.append("")
    lines.append("## Tau Source Readout Pack")
    lines.append("| pack_id | current_status | needed_for |")
    lines.append("|---|---|---|")
    for row in tau:
        lines.append(f"| {row['pack_id']} | {row['current_status']} | {row['needed_for']} |")
    lines.append("")
    lines.append("## Same-Branch Contract")
    lines.append("| contract_id | current_status | factor |")
    lines.append("|---|---|---|")
    for row in contract:
        lines.append(f"| {row['contract_id']} | {row['current_status']} | {row['factor']} |")
    lines.append("")
    lines.append("## Smoke Update")
    lines.append("| smoke_id | status | computed_value | why_nonclaim |")
    lines.append("|---|---|---|---|")
    for row in smoke:
        lines.append(f"| {row['smoke_id']} | {row['status']} | {row['computed_value']} | {row['why_nonclaim']} |")
    lines.append("")
    lines.append("## Hom Parent Generator")
    lines.append("| proof_id | current_status | next_action |")
    lines.append("|---|---|---|")
    for row in hom:
        lines.append(f"| {row['proof_id']} | {row['current_status']} | {row['next_action']} |")
    lines.append("")
    lines.append("## Rejection Ledger")
    lines.append("| rejection_id | blocking_marker | reason |")
    lines.append("|---|---|---|")
    for row in rejection:
        lines.append(f"| {row['rejection_id']} | {row['blocking_marker']} | {row['reason']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} — {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    ctx = numeric_context()
    material = material_context_rows(ctx)
    tau = tau_source_rows()
    contract = same_branch_contract_rows()
    smoke = updated_smoke_rows(ctx)
    hom = hom_generator_rows()
    rejection = rejection_rows()
    gates = gate_rows(material, tau, contract, smoke, hom, rejection)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MATERIAL_CONTEXT, material)
    write_csv(TAU_SOURCE_PACK, tau)
    write_csv(SAME_BRANCH_CONTRACT, contract)
    write_csv(UPDATED_SMOKE, smoke)
    write_csv(HOM_GENERATOR, hom)
    write_csv(REJECTION_LEDGER, rejection)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_nonclaim(MATERIAL_CONTEXT, QUAR_MATERIAL)
    copy_nonclaim(UPDATED_SMOKE, QUAR_SMOKE)
    copy_nonclaim(MATERIAL_CONTEXT, BRANCH_MATERIAL)
    copy_nonclaim(UPDATED_SMOKE, BRANCH_SMOKE)
    copy_nonclaim(REDUCTION_GATES, BRANCH_GATES)

    validation = validation_rows(sources, material, tau, contract, smoke, hom, rejection, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, material, tau, contract, smoke, hom, rejection, gates, decisions, validation, next_target)
    print("Y5_R10_1481_same_branch_WEP_pack_staged_nonclaim_Hom_generator_open")


if __name__ == "__main__":
    main()
