from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2775-Y5-R2FR-WEP-tau-source-worldtube-orbit-readout-acquisition-pack-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2775_SOURCE_REGISTER.csv",
    "pack": MTS / "P8_Y5_R2FR_2775_TAU_WEP_ACQUISITION_PACK.csv",
    "worldtube": MTS / "P8_Y5_R2FR_2775_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
    "orbit": MTS / "P8_Y5_R2FR_2775_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv",
    "material": MTS / "P8_Y5_R2FR_2775_MATERIAL_RESPONSE_REQUIREMENTS.csv",
    "force": MTS / "P8_Y5_R2FR_2775_OBSERVED_FRAME_FORCE_MAP.csv",
    "xhat": MTS / "P8_Y5_R2FR_2775_XHAT_NORMALIZATION_LEDGER.csv",
    "fallback": MTS / "P8_Y5_R2FR_2775_DIRECT_PRODUCT_FALLBACK.csv",
    "candidate": MTS / "P8_Y5_R2FR_2775_WEP_TAU_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2775_WEP_TAU_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2775_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2775_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2775_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2775_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2775_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2775_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2775_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "pack_queue": RAB_QUEUE / "JR2775_WEP_TAU_ACQUISITION_PACK_NONCLAIM.csv",
    "direct_queue": RAB_QUEUE / "JR2775_DIRECT_WEP_PRODUCT_FALLBACK_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_TAU_ACQUISITION_2775_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "wep_tau_acquisition_pack_2775_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2775_DIRECT_WEP_OR_FIRST_TAU_SOURCE_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2775_00_2774_next", "2774_next", MTS / "P8_Y5_R2FR_2774_NEXT_TARGET.csv", "NEXT2774_0_2775", "current handoff into tau acquisition pack"),
        ("SRC2775_01_2774_tau_functional", "2774_tau_functional", MTS / "P8_Y5_R2FR_2774_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv", "TWF2774_6_verdict", "current tau functional decomposition"),
        ("SRC2775_02_2774_acquisition", "2774_acquisition", MTS / "P8_Y5_R2FR_2774_TAU_WEP_ACQUISITION_SCHEMA.csv", "TAQ2774_1_tau_numeric_option", "current tau acquisition schema"),
        ("SRC2775_03_2773_tau_contract", "2773_tau_contract", MTS / "P8_Y5_R2FR_2773_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP2773_7_verdict", "current tau projection contract"),
        ("SRC2775_04_1068_doc", "1068_doc", WORK / "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md", "TAP1068_6_direct_product_fallback", "prior R10 tau acquisition pack"),
        ("SRC2775_05_1068_pack", "1068_pack", MTS / "P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv", "TAP1068_6_direct_product_fallback", "prior acquisition pack rows"),
        ("SRC2775_06_1068_worldtube", "1068_worldtube", MTS / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "prior source worldtube requirements"),
        ("SRC2775_07_1068_orbit", "1068_orbit", MTS / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv", "ORB1068_5_verdict", "prior orbit/readout requirements"),
        ("SRC2775_08_1068_material", "1068_material", MTS / "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv", "MAT1068_5_verdict", "prior material-response requirements"),
        ("SRC2775_09_1068_force", "1068_force", MTS / "P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv", "FRM1068_5_verdict", "prior force-map requirements"),
        ("SRC2775_10_1068_xhat", "1068_xhat", MTS / "P8_Y5_R10_1068_XHAT_NORMALIZATION_LEDGER.csv", "XHN1068_4_verdict", "prior Xhat normalization ledger"),
        ("SRC2775_11_1068_fallback", "1068_fallback", MTS / "P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv", "DPF1068_0_preferred_route", "prior direct-product fallback"),
        ("SRC2775_12_1053_tau", "1053_tau", MTS / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "tau_WEP definition-only source"),
        ("SRC2775_13_1061_tau", "1061_tau", MTS / "P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_2_tau_WEP", "tau derivation attempt"),
        ("SRC2775_14_1061_material_pair", "1061_material_pair", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material pair convention"),
        ("SRC2775_15_1061_deltaQ", "1061_deltaQ", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_1_delta_Q_alpha", "alpha/Coulomb smoke material value"),
        ("SRC2775_16_708_wep_map", "708_wep_map", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge map gap"),
        ("SRC2775_17_948_bound_runner", "948_bound_runner", MTS / "P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv", "WEP948_0_WAS651_0_alpha_Coulomb", "WEP bound/product runner precedent"),
        ("SRC2775_18_988_pressure", "988_pressure", MTS / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "WEP alpha pressure precedent"),
        ("SRC2775_19_1029_tau_req", "1029_tau_req", MTS / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_3_WEP_limit", "WEP tau projection requirement"),
        ("SRC2775_20_1033_tauR10", "1033_tauR10", MTS / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_5_universal_cg_limit", "unity tau shortcut rejection"),
        ("SRC2775_21_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound anchor"),
        ("SRC2775_22_393_common", "393_common", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard"),
    ]
    rows = []
    for row_id, source_key, path, needle, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": exists and needle in text,
            "source_role": role,
        }))
    return rows


def build_pack_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"pack_id": "TAP2775_0_source_worldtube", "component": "Earth/source worldtube", "needed_for": "source-leg normalization of the relative source-weight residual", "required_artifact": "source stress/profile/composition convention in the observed local frame", "current_status": "MISSING_SOURCE_WORLDTUBE", "claim_policy": "not scoreable"}),
        nonclaim({"pack_id": "TAP2775_1_orbit_average", "component": "MICROSCOPE orbit/environment average", "needed_for": "projection from source residual to measured acceleration channel", "required_artifact": "orbit/attitude/readout averaging kernel with source path", "current_status": "MISSING_ORBIT_AVERAGING_KERNEL", "claim_policy": "not scoreable"}),
        nonclaim({"pack_id": "TAP2775_2_eta_readout", "component": "eta_AB readout convention", "needed_for": "convert differential acceleration residual to the MICROSCOPE observable", "required_artifact": "eta_AB sign, normalization, frame, and absolute-value scoring convention", "current_status": "BOUND_ANCHOR_ONLY", "claim_policy": "bound available but not prediction"}),
        nonclaim({"pack_id": "TAP2775_3_material_response", "component": "Ti/Pt material response tensor", "needed_for": "test-body leg of the relative source-weight channel", "required_artifact": "full material/source response or parent theorem reducing it to Delta_w_TiPt", "current_status": "MATERIAL_PAIR_ONLY", "claim_policy": "smoke convention only"}),
        nonclaim({"pack_id": "TAP2775_4_observed_frame_force_map", "component": "observed-frame force map", "needed_for": "same-frame acceleration calculation and no hidden readout rescaling", "required_artifact": "force law in e_obs with units, calibration, and no measured-G relative absorption", "current_status": "MISSING_FORCE_READOUT_MAP", "claim_policy": "not scoreable"}),
        nonclaim({"pack_id": "TAP2775_5_Xhat_normalization", "component": "Xhat/chi_X normalization", "needed_for": "compatibility with clock, R10, and WEP finite branches", "required_artifact": "shared parent normalization or explicitly separate finite-branch convention", "current_status": "MISSING_XHAT_NORMALIZATION", "claim_policy": "not scoreable"}),
        nonclaim({"pack_id": "TAP2775_6_direct_product_fallback", "component": "direct P_WEP product", "needed_for": "avoid artificial split into Delta_w and tau if parent variation gives the observable directly", "required_artifact": "numeric or theorem-zero P_WEP_relative_source_weight with source path", "current_status": "MISSING_DIRECT_PRODUCT", "claim_policy": "runner refuses until numeric/theorem-zero"}),
    ]


def build_worldtube_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"worldtube_id": "SWT2775_0_source_stress_profile", "required_input": "T_source^Earth(x) or equivalent source-mass profile", "purpose": "source leg for WEP residual field", "accepted_form": "sourced profile/table or theorem reducing extended Earth to calibrated point-source convention", "current_status": "MISSING", "blocks": "tau_WEP"}),
        nonclaim({"worldtube_id": "SWT2775_1_source_composition", "required_input": "Earth/source composition or source-charge convention", "purpose": "distinguish universal mass source from retained composition/source-weight residual", "accepted_form": "species/source map or proof that source leg is universal/common-mode", "current_status": "MISSING", "blocks": "Delta_w source/test split"}),
        nonclaim({"worldtube_id": "SWT2775_2_GM_calibration", "required_input": "measured GM/G calibration convention", "purpose": "separate common mode from relative source weight", "accepted_form": "calibration row proving only common universal factors are absorbed", "current_status": "COMMON_MODE_GUARD_ONLY", "blocks": "fake measured-G absorption"}),
        nonclaim({"worldtube_id": "SWT2775_3_finite_source_correction", "required_input": "finite-size and altitude/source support correction", "purpose": "maps source profile to spacecraft location", "accepted_form": "integral kernel or justified point-source limit with error bound", "current_status": "MISSING", "blocks": "numeric tau_WEP"}),
        nonclaim({"worldtube_id": "SWT2775_4_frame_units", "required_input": "observed-frame units and source normalization", "purpose": "keep tau dimensionless and compatible with eta_AB", "accepted_form": "declared observed coframe and units conversion", "current_status": "MISSING", "blocks": "unit-safe runner input"}),
        nonclaim({"worldtube_id": "SWT2775_5_verdict", "required_input": "source worldtube pack", "purpose": "source-side of tau_WEP", "accepted_form": "all SWT2775_0..4 real or theorem-reduced", "current_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED", "blocks": "tau_WEP and WEP product scoring"}),
    ]


def build_orbit_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"orbit_id": "ORB2775_0_orbit_ephemeris", "required_input": "MICROSCOPE orbit/altitude/time sampling or averaged equivalent", "purpose": "turn Earth/source residual into instrument-frame acceleration", "accepted_form": "source-backed orbit parameters or official averaged kernel", "current_status": "MISSING", "blocks": "tau_WEP"}),
        nonclaim({"orbit_id": "ORB2775_1_attitude_axis", "required_input": "instrument sensitive axis/attitude convention", "purpose": "project residual acceleration into measured channel", "accepted_form": "axis convention or theorem that scalar residual is orientation independent", "current_status": "MISSING", "blocks": "sign/readout convention"}),
        nonclaim({"orbit_id": "ORB2775_2_eta_convention", "required_input": "eta_AB normalization/sign convention", "purpose": "define comparison to 2.8e-15 bound", "accepted_form": "eta_AB formula and absolute-value claim convention", "current_status": "BOUND_IMPORTED_BUT_FORMULA_NOT_PARENT_MAPPED", "blocks": "direct P_WEP row"}),
        nonclaim({"orbit_id": "ORB2775_3_environmental_model", "required_input": "known systematics/environment subtraction convention", "purpose": "avoid mixing MTS residual with experimental nuisance subtraction", "accepted_form": "official readout/systematics convention or conservative envelope", "current_status": "MISSING", "blocks": "claim-grade tau"}),
        nonclaim({"orbit_id": "ORB2775_4_average_kernel", "required_input": "time/orbit averaging kernel", "purpose": "define tau_WEP as an averaged projection, not an instantaneous guess", "accepted_form": "kernel K_orb(t) or stated averaged scalar convention", "current_status": "MISSING", "blocks": "numeric tau_WEP"}),
        nonclaim({"orbit_id": "ORB2775_5_verdict", "required_input": "orbit/readout pack", "purpose": "experiment-side of tau_WEP", "accepted_form": "all ORB2775_0..4 real or theorem-reduced", "current_status": "ORBIT_READOUT_NOT_ACQUIRED", "blocks": "tau_WEP and WEP product scoring"}),
    ]


def build_material_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"material_id": "MAT2775_0_pair_convention", "quantity": "MICROSCOPE Ti/Pt test pair", "value_or_status": "TA6V_minus_PtRh10", "source": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair", "current_status": "SMOKE_CONTEXT_AVAILABLE", "blocks": "does not itself provide material tensor"}),
        nonclaim({"material_id": "MAT2775_1_alpha_charge_smoke", "quantity": "Delta_Q_alpha_Coulomb_abs", "value_or_status": "0.001989808886825", "source": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_1_delta_Q_alpha", "current_status": "SMOKE_VALUE_AVAILABLE", "blocks": "alpha/Coulomb smoke channel is not the full relative source-weight tensor"}),
        nonclaim({"material_id": "MAT2775_2_full_tensor", "quantity": "Ti/Pt relative-source material response tensor", "value_or_status": "MISSING_FULL_MATERIAL_TENSOR", "source": "needed: source-backed MICROSCOPE/material model or parent theorem", "current_status": "MISSING", "blocks": "Delta_w_TiPt mapping"}),
        nonclaim({"material_id": "MAT2775_3_source_weight_response", "quantity": "Delta_w_TiPt response convention", "value_or_status": "MISSING_DELTA_W_RESPONSE_MAP", "source": "needed: source-only weight theorem or finite prior convention", "current_status": "MISSING", "blocks": "WEP product prediction"}),
        nonclaim({"material_id": "MAT2775_4_no_cancellation", "quantity": "signed material cancellation", "value_or_status": "FORBIDDEN_WITHOUT_FULL_SIGNED_MODEL", "source": "2773/2774 refusal gates", "current_status": "ABSOLUTE_VALUE_GUARD", "blocks": "fake WEP pass by sign tuning"}),
        nonclaim({"material_id": "MAT2775_5_verdict", "quantity": "material response pack", "value_or_status": "MATERIAL_PAIR_ONLY_NOT_CLAIM_READY", "source": "1061 convention rows", "current_status": "NOT_ACQUIRED", "blocks": "tau_WEP/direct product scoring"}),
    ]


def build_force_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"force_id": "FRM2775_0_observed_frame", "required_clause": "same observed coframe for source variation, force law, clocks, and readout", "formula_or_rule": "e_obs = e_source = e_force = e_readout through WEP order", "current_status": "CONDITIONAL_FROM_PRIOR_SPINE", "blocks": "frame-safe tau_WEP"}),
        nonclaim({"force_id": "FRM2775_1_eta_mapping", "required_clause": "map residual force to eta_AB", "formula_or_rule": "eta_AB = readout[(a_A-a_B), calibration] in MICROSCOPE convention", "current_status": "BOUND_OBSERVABLE_KNOWN_MAP_NOT_DERIVED", "blocks": "direct product scoring"}),
        nonclaim({"force_id": "FRM2775_2_common_mode_separation", "required_clause": "common source normalization removed only by universal calibration", "formula_or_rule": "relative w_A/w_B cannot be absorbed into measured G or GM", "current_status": "GUARD_ACTIVE", "blocks": "fake local-GR pass"}),
        nonclaim({"force_id": "FRM2775_3_units", "required_clause": "dimensionless tau/product convention", "formula_or_rule": "P_WEP_relative_source_weight must be dimensionless and comparable to eta_bound", "current_status": "SCHEMA_ONLY", "blocks": "runner validity"}),
        nonclaim({"force_id": "FRM2775_4_direct_variation", "required_clause": "direct parent variation option", "formula_or_rule": "derive delta a_AB or eta_AB directly from parent action instead of split Delta_w*tau", "current_status": "MISSING_DIRECT_PRODUCT", "blocks": "fallback remains nonclaim"}),
        nonclaim({"force_id": "FRM2775_5_verdict", "required_clause": "observed-frame force/readout map", "formula_or_rule": "source residual -> a_A-a_B -> eta_AB with units and calibration", "current_status": "FORCE_MAP_NOT_DERIVED", "blocks": "tau_WEP/direct product scoring"}),
    ]


def build_xhat_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"xhat_id": "XHN2775_0_shared_parent_norm", "quantity": "Xhat/chi_X normalization", "required_form": "same parent normalization used by clocks, WEP, and R10 or explicitly separated", "current_status": "MISSING_SHARED_NORMALIZATION", "risk": "tau_WEP cannot be compared to clock/R10 factors"}),
        nonclaim({"xhat_id": "XHN2775_1_clock_transfer_guard", "quantity": "clock-to-WEP transfer", "required_form": "no clock screening imported into WEP without source/readout map", "current_status": "TRANSFER_BLOCKED", "risk": "fake tau_WEP via clock branch"}),
        nonclaim({"xhat_id": "XHN2775_2_R10_transfer_guard", "quantity": "R10-to-WEP transfer", "required_form": "no tau_R10 unity or profile factor imported into WEP", "current_status": "TRANSFER_BLOCKED", "risk": "profile/unit contamination"}),
        nonclaim({"xhat_id": "XHN2775_3_direct_product_escape", "quantity": "direct P_WEP product", "required_form": "parent variation gives dimensionless eta_AB product directly", "current_status": "MISSING_DIRECT_PRODUCT", "risk": "split-factor ambiguity persists"}),
        nonclaim({"xhat_id": "XHN2775_4_verdict", "quantity": "Xhat normalization pack", "required_form": "shared normalization or direct product", "current_status": "NOT_ACQUIRED", "risk": "tau_WEP remains a free symbol"}),
    ]


def build_fallback_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"fallback_id": "DPF2775_0_preferred_route", "route": "derive P_WEP_relative_source_weight directly", "accepted_evidence": "parent variation produces eta_AB residual or theorem-zero with units/source path", "current_status": "MISSING_DIRECT_PARENT_PRODUCT", "why_it_matters": "bypasses arbitrary split into Delta_w and tau_WEP"}),
        nonclaim({"fallback_id": "DPF2775_1_split_route", "route": "P = abs(Delta_w_TiPt * tau_WEP)", "accepted_evidence": "both factors numeric/sourced or theorem-zero; no unity shortcut", "current_status": "MISSING_BOTH_FACTORS", "why_it_matters": "finite branch can still be tested if direct product is not derived"}),
        nonclaim({"fallback_id": "DPF2775_2_theorem_zero_route", "route": "P=0", "accepted_evidence": "parent source-scalar/action-scale theorem or WEP projection silence theorem", "current_status": "THEOREM_ZERO_UNSIGNED", "why_it_matters": "would close WEP branch without data-fitting"}),
        nonclaim({"fallback_id": "DPF2775_3_refusal_rule", "route": "reject non-evidence", "accepted_evidence": "no tau=1, no Delta_w=0 by taste, no measured-G absorption, no cancellation", "current_status": "REFUSAL_ACTIVE", "why_it_matters": "prevents local-GR/WEP false positives"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2775_0_WEP_tau_acquisition_pack_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_DELTA_W_TiPt_TIMES_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": rel(OUTPUTS["fallback"]),
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10;alpha_smoke_deltaQ=0.001989808886825",
            "required_inputs": "source worldtube;orbit/readout kernel;material response tensor;force map;Xhat normalization;direct product or Delta_w*tau",
            "derivation_status": "MISSING_TAU_WEP_ACQUISITION_PACK_INPUTS",
            "notes": "2775 is an acquisition pack; the row is intentionally nonclaim until the pack is filled.",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "bound_id": "BOUND2775_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": rel(LOCAL_BOUNDS / "local_bound_claims.csv"),
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_internal_runner_only",
            "bound_valid_for_internal_runner": True,
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction.",
        })
    ]


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if row.get("bound_valid_for_internal_runner") is True
        and is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [
        nonclaim({
            "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
            "arena": "",
            "product_symbol": "",
            "product_value": "",
            "bound_value": "",
            "comparison_status": "not_run",
            "pass_for_claim": False,
            "issues": "no valid MTS tau acquisition product prediction rows",
        })
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2775_0_WEP_tau_acquisition_pack",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "comparison_rows": len(comparisons),
            "passed_rows": 0,
            "blocked_or_failed_rows": len(comparisons),
            "claim_allowed": False,
            "generated_utc": ts(),
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2775_0_tau_acquisition_pack", "claim": "tau_WEP acquisition pack is complete", "gate_pass": False, "reason": "source worldtube, orbit/readout, material tensor, force map, and Xhat normalization remain missing", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2775_1_tau_numeric", "claim": "tau_WEP is numeric or theorem-zero", "gate_pass": False, "reason": "tau_WEP remains definition-only and tau=1 is explicitly forbidden", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2775_2_direct_product", "claim": "direct P_WEP product is derived", "gate_pass": False, "reason": "no parent variation produces eta_AB residual directly yet", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2775_3_runner_score", "claim": "WEP product can be scored", "gate_pass": False, "reason": "strict runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2775_4_local_GR_WEP", "claim": "local GR/WEP coupling branch is derived", "gate_pass": False, "reason": "finite WEP projection and source-scalar theorem routes remain open", "claim_allowed": False}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2775_0_pack_status", "decision": "tau_WEP acquisition pack is explicit but empty of claim-grade data", "because": "each required component has a named row and refusal gate", "next_action": "source real MICROSCOPE/source/readout rows or derive direct product"}),
        nonclaim({"decision_id": "DEC2775_1_best_route", "decision": "direct P_WEP derivation remains the cleanest theory route", "because": "it avoids arbitrary split-factor priors; if unavailable, tau pack components must be sourced", "next_action": "attempt direct eta_AB product theorem before web/data acquisition"}),
        nonclaim({"decision_id": "DEC2775_2_best_next", "decision": "next target is direct WEP product theorem or first real tau source row", "because": "2775 names the missing pack; 2776 should either derive P_WEP or acquire the first real component", "next_action": "2776-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2775_0_2776",
            "next_target": "2776-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_direct_WEP_product_theorem_or_first_real_tau_source_row_under_AX1090_2776.py",
            "objective": "attempt a direct parent variation theorem for P_WEP_relative_source_weight; if it fails, acquire the first real tau_WEP source row, starting with MICROSCOPE eta/readout convention or Earth/source worldtube metadata",
            "include": "direct eta_AB variation theorem, no split-factor shortcut, official MICROSCOPE readout/source row requirements, source URL/DOI provenance, units, valid_for_claim refusal gates",
            "exclude": "setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    pack: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    orbit: list[dict[str, Any]],
    material: list[dict[str, Any]],
    force: list[dict[str, Any]],
    xhat: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pack_rows = pack + worldtube + orbit + material + force + xhat + gates
    direct_rows = fallback + candidate + bounds + gates
    beta_rows = pack + fallback + next_rows
    microscope_rows = pack + worldtube + orbit + material + force + xhat + fallback + candidate + bounds + next_rows
    specs = [
        ("BR2775_0_pack_queue", "pack", pack_rows, OUTPUTS["pack"], BRANCH_OUTPUTS["pack_queue"], "WEP tau acquisition pack nonclaim copy"),
        ("BR2775_1_direct_queue", "direct", direct_rows, OUTPUTS["fallback"], BRANCH_OUTPUTS["direct_queue"], "direct WEP product fallback nonclaim copy"),
        ("BR2775_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["pack"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing WEP tau acquisition copy"),
        ("BR2775_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE tau acquisition pack copy"),
        ("BR2775_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next direct WEP or first tau source target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    pack = rows_by_name["pack"]
    worldtube = rows_by_name["worldtube"]
    orbit = rows_by_name["orbit"]
    material = rows_by_name["material"]
    force = rows_by_name["force"]
    xhat = rows_by_name["xhat"]
    fallback = rows_by_name["fallback"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2775_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2775_1_pack_components_written", len(pack) == 7 and any(row["pack_id"] == "TAP2775_6_direct_product_fallback" for row in pack), "tau_WEP acquisition pack components are written as nonclaim rows"),
        ("VAL2775_2_worldtube_missing_explicit", any(row["worldtube_id"] == "SWT2775_5_verdict" and row["current_status"] == "SOURCE_WORLDTUBE_NOT_ACQUIRED" for row in worldtube), "source worldtube remains explicitly missing"),
        ("VAL2775_3_orbit_readout_missing_explicit", any(row["orbit_id"] == "ORB2775_5_verdict" and row["current_status"] == "ORBIT_READOUT_NOT_ACQUIRED" for row in orbit), "orbit/readout pack remains explicitly missing"),
        ("VAL2775_4_material_response_guarded", any(row["material_id"] == "MAT2775_5_verdict" and row["current_status"] == "NOT_ACQUIRED" for row in material), "material tensor is not claim-ready"),
        ("VAL2775_5_force_map_missing", any(row["force_id"] == "FRM2775_5_verdict" and row["current_status"] == "FORCE_MAP_NOT_DERIVED" for row in force), "observed-frame force map is not derived"),
        ("VAL2775_6_xhat_missing", any(row["xhat_id"] == "XHN2775_4_verdict" and row["current_status"] == "NOT_ACQUIRED" for row in xhat), "Xhat normalization pack remains missing"),
        ("VAL2775_7_direct_product_fallback_written", any(row["fallback_id"] == "DPF2775_0_preferred_route" and "MISSING" in row["current_status"] for row in fallback), "direct product fallback is written and missing"),
        ("VAL2775_8_prediction_nonclaim", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "WEP tau acquisition prediction remains nonclaim"),
        ("VAL2775_9_bound_anchor_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True and bounds[0]["valid_for_claim"] is False, "WEP bound anchor is numeric and internal-runner only"),
        ("VAL2775_10_runner_refuses_placeholder", runner[0]["valid_prediction_rows"] == 0 and runner[0]["valid_bound_rows"] == 1 and runner[0]["claim_allowed"] is False, "strict runner refuses missing tau acquisition product"),
        ("VAL2775_11_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all tau/WEP/local-GR claim gates remain blocked"),
        ("VAL2775_12_next_target_written", any(row["row_id"] == "NEXT2775_0_2776" and "direct-WEP-product" in row["next_target"] for row in next_rows), "next target selects direct WEP theorem or first real tau source row"),
        ("VAL2775_13_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2775_14_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2775_15_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2775_16_generated_files_in_post_checkpoint", generated_files_under_work(), "all generated files are under post-checkpoint-work"),
        ("VAL2775_17_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2775_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2775_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2775 builds the live R2/f(R) tau_WEP acquisition pack, decomposes source worldtube, MICROSCOPE orbit/readout, material response, observed-frame force map, Xhat normalization, and direct-product fallback, keeps every component nonclaim/missing where appropriate, refuses tau=1 and missing direct products, blocks WEP/local-GR claims, and selects direct WEP product theorem or first real tau source row as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2775 - Y5 R2/f(R): WEP tau Source-Worldtube / Orbit / Readout Acquisition Pack Under AX1090",
        "## Private Verdict\n\n`tau_WEP` is now decomposed into concrete acquisition components. None are claim-ready, and `tau_WEP=1` remains forbidden.\n\nBest route: derive `P_WEP_relative_source_weight` directly from parent variation if possible; otherwise source every tau component before scoring.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Acquisition Pack\n\n" + markdown_table(rows_by_name["pack"], ["pack_id", "component", "needed_for", "required_artifact", "current_status", "claim_policy", "valid_for_claim"]),
        "## Earth / Source Worldtube\n\n" + markdown_table(rows_by_name["worldtube"], ["worldtube_id", "required_input", "purpose", "accepted_form", "current_status", "blocks", "valid_for_claim"]),
        "## MICROSCOPE Orbit / Readout\n\n" + markdown_table(rows_by_name["orbit"], ["orbit_id", "required_input", "purpose", "accepted_form", "current_status", "blocks", "valid_for_claim"]),
        "## Material Response\n\n" + markdown_table(rows_by_name["material"], ["material_id", "quantity", "value_or_status", "source", "current_status", "blocks", "valid_for_claim"]),
        "## Observed-Frame Force Map\n\n" + markdown_table(rows_by_name["force"], ["force_id", "required_clause", "formula_or_rule", "current_status", "blocks", "valid_for_claim"]),
        "## Xhat Normalization\n\n" + markdown_table(rows_by_name["xhat"], ["xhat_id", "quantity", "required_form", "current_status", "risk", "valid_for_claim"]),
        "## Direct Product Fallback\n\n" + markdown_table(rows_by_name["fallback"], ["fallback_id", "route", "accepted_evidence", "current_status", "why_it_matters", "valid_for_claim"]),
        "## WEP Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes"]),
        "## WEP Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim", "notes"]),
        "## Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc", "valid_for_claim"]),
        "## Runner Comparisons\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis turns `tau_WEP` from a loose symbol into a shopping list with locks on every drawer. The best attack is still to derive the direct WEP product from the parent variation; if that fails, the first real acquisition row should be MICROSCOPE eta/readout convention or Earth/source worldtube metadata.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    pack = build_pack_rows()
    worldtube = build_worldtube_rows()
    orbit = build_orbit_rows()
    material = build_material_rows()
    force = build_force_rows()
    xhat = build_xhat_rows()
    fallback = build_fallback_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("pack", pack), ("worldtube", worldtube), ("orbit", orbit),
        ("material", material), ("force", force), ("xhat", xhat), ("fallback", fallback),
        ("candidate", candidate), ("bounds", bounds), ("runner", runner), ("comparisons", comparisons),
        ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(pack, worldtube, orbit, material, force, xhat, fallback, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "pack": pack,
        "worldtube": worldtube,
        "orbit": orbit,
        "material": material,
        "force": force,
        "xhat": xhat,
        "fallback": fallback,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2775_OVERALL")
    print(f"2775 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
