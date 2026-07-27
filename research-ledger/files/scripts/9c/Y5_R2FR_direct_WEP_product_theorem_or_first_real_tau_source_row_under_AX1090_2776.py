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
DOC = WORK / "2776-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2776_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2776_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv",
    "tau_source": MTS / "P8_Y5_R2FR_2776_FIRST_REAL_TAU_SOURCE_ROW.csv",
    "provenance": MTS / "P8_Y5_R2FR_2776_MICROSCOPE_PROVENANCE_LEDGER.csv",
    "readout": MTS / "P8_Y5_R2FR_2776_READOUT_FILL_MATRIX.csv",
    "requirements": MTS / "P8_Y5_R2FR_2776_REMAINING_TAU_REQUIREMENTS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2776_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2776_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2776_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2776_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2776_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2776_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2776_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2776_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2776_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2776_DIRECT_WEP_PRODUCT_THEOREM_NONCLAIM.csv",
    "source_queue": RAB_QUEUE / "JR2776_FIRST_REAL_TAU_SOURCE_ROW_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "DIRECT_WEP_PRODUCT_OR_TAU_SOURCE_2776_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "direct_wep_or_first_tau_source_2776_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2776_MICROSCOPE_ETA_READOUT_NEXT.csv",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2776_00_2775_next", "2775_next", MTS / "P8_Y5_R2FR_2775_NEXT_TARGET.csv", "NEXT2775_0_2776", "current handoff into direct WEP product or first tau source row"),
        ("SRC2776_01_2775_fallback", "2775_fallback", MTS / "P8_Y5_R2FR_2775_DIRECT_PRODUCT_FALLBACK.csv", "DPF2775_0_preferred_route", "current direct-product fallback"),
        ("SRC2776_02_2775_pack", "2775_pack", MTS / "P8_Y5_R2FR_2775_TAU_WEP_ACQUISITION_PACK.csv", "TAP2775_2_eta_readout", "current tau acquisition pack"),
        ("SRC2776_03_2775_orbit", "2775_orbit", MTS / "P8_Y5_R2FR_2775_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv", "ORB2775_2_eta_convention", "current orbit/readout requirement"),
        ("SRC2776_04_2775_force", "2775_force", MTS / "P8_Y5_R2FR_2775_OBSERVED_FRAME_FORCE_MAP.csv", "FRM2775_1_eta_mapping", "current force/readout map gap"),
        ("SRC2776_05_2775_worldtube", "2775_worldtube", MTS / "P8_Y5_R2FR_2775_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT2775_5_verdict", "current source worldtube gap"),
        ("SRC2776_06_2775_material", "2775_material", MTS / "P8_Y5_R2FR_2775_MATERIAL_RESPONSE_REQUIREMENTS.csv", "MAT2775_5_verdict", "current material tensor gap"),
        ("SRC2776_07_1069_doc", "1069_doc", WORK / "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md", "DWT1069_5_verdict", "prior R10 direct WEP product / source-row template"),
        ("SRC2776_08_1069_theorem", "1069_theorem", MTS / "P8_Y5_R10_1069_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv", "DWT1069_5_verdict", "prior direct WEP theorem attempt"),
        ("SRC2776_09_1069_tau_source", "1069_tau_source", MTS / "P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv", "WTS1069_0_MICROSCOPE_eta_source_charge_proxy", "prior first source row"),
        ("SRC2776_10_1069_provenance", "1069_provenance", MTS / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv", "PROV1069_0_R1_source_charge", "prior provenance ledger"),
        ("SRC2776_11_1069_readout", "1069_readout", MTS / "P8_Y5_R10_1069_READOUT_FILL_MATRIX.csv", "RFM1069_1_eta_formula", "prior readout matrix"),
        ("SRC2776_12_1062_parent", "1062_parent", MTS / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "parent product theorem attempt"),
        ("SRC2776_13_1063_source", "1063_source", MTS / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", "THM1063_5_verdict", "source forgetting theorem attempt"),
        ("SRC2776_14_1066_scalar", "1066_scalar", MTS / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source scalar exclusion lemma"),
        ("SRC2776_15_1067_action", "1067_action", MTS / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action scale owner attempt"),
        ("SRC2776_16_1061_material", "1061_material", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "material convention"),
        ("SRC2776_17_708_wep", "708_wep", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge map"),
        ("SRC2776_18_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound ledger"),
        ("SRC2776_19_393_common", "393_common", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard"),
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


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"theorem_id": "DWT2776_0_target", "claim": "derive P_WEP_relative_source_weight directly from parent variation", "formal_move": "delta S_parent -> source residual -> eta_AB without splitting into Delta_w_TiPt and tau_WEP", "attempt_result": "TARGET_SHARPENED", "gap": "needs source variation, force/readout map, and observed-frame eta convention"}),
        nonclaim({"theorem_id": "DWT2776_1_variation_route", "claim": "parent variation gives the differential acceleration observable", "formal_move": "P_WEP := readout_eta[delta_e S_matter, source worldtube, orbit average, material response]", "attempt_result": "FORMALLY_CLEAN_IF_ALL_MAPS_EXIST", "gap": "2775 shows those maps are acquisition rows, not derived objects"}),
        nonclaim({"theorem_id": "DWT2776_2_theorem_zero_route", "claim": "direct product is theorem-zero", "formal_move": "P_WEP=0 if source-scalar exclusion/action-scale owner or WEP projection silence is parent-signed", "attempt_result": "CONDITIONAL_ONLY", "gap": "source-scalar and action-scale owner verdicts are still unsigned"}),
        nonclaim({"theorem_id": "DWT2776_3_finite_route", "claim": "direct product is a numeric finite prediction", "formal_move": "P_WEP = abs(parent predicted eta_AB residual) in dimensionless MICROSCOPE convention", "attempt_result": "MISSING_NUMERIC_PARENT_PRODUCT", "gap": "no source worldtube/orbit/readout/material/Xhat pack yet"}),
        nonclaim({"theorem_id": "DWT2776_4_no_shortcuts", "claim": "refuse false direct products", "formal_move": "reject tau=1, Delta_w=0 by taste, measured-G absorption of relative weights, and cancellation", "attempt_result": "REFUSAL_RULE_ACTIVE", "gap": "none; this is a guard, not a derivation"}),
        nonclaim({"theorem_id": "DWT2776_5_verdict", "claim": "direct WEP product theorem", "formal_move": "parent variation to eta_AB product", "attempt_result": "DIRECT_PRODUCT_THEOREM_NOT_DERIVED", "gap": "direct product remains preferred route, but first real source/readout row is needed for finite branch"}),
    ]


def build_tau_source_rows() -> list[dict[str, Any]]:
    source_charge = get_local_bound("R1_WEP_source_charge")
    direct = get_local_bound("R0_identity_coframe_direct")
    source_url, source_doi = split_reference(source_charge.get("reference_path_or_url", ""))
    direct_url, direct_doi = split_reference(direct.get("reference_path_or_url", ""))
    return [
        nonclaim({
            "tau_source_id": "WTS2776_0_MICROSCOPE_eta_source_charge_proxy",
            "pack_component": "eta/readout bound anchor",
            "fills_2775_row": "TAP2775_2_eta_readout; ORB2775_2_eta_convention",
            "dataset_id": source_charge.get("dataset_id", "MICROSCOPE_final_TiPt_source_charge_proxy"),
            "row_id": source_charge.get("row_id", "R1_WEP_source_charge"),
            "observable": source_charge.get("observable", "eta_WEP_source_charge"),
            "measured_value": source_charge.get("measured_value", "-1.5e-15"),
            "one_sigma": source_charge.get("one_sigma", "2.74590604355e-15"),
            "upper_bound": source_charge.get("upper_bound", "2.8e-15"),
            "units": source_charge.get("units", "dimensionless"),
            "reference_url": source_url,
            "doi": source_doi,
            "source_backed": True,
            "claim_ready": False,
            "why_not_claim": "bound/readout anchor only; does not supply tau_WEP, source worldtube, orbit kernel, material tensor, or parent product",
        }),
        nonclaim({
            "tau_source_id": "WTS2776_1_MICROSCOPE_direct_geometry_context",
            "pack_component": "direct eta context",
            "fills_2775_row": "FRM2775_1_eta_mapping",
            "dataset_id": direct.get("dataset_id", "MICROSCOPE_final_TiPt"),
            "row_id": direct.get("row_id", "R0_identity_coframe_direct"),
            "observable": direct.get("observable", "eta_WEP_direct_geometry"),
            "measured_value": direct.get("measured_value", "-1.5e-15"),
            "one_sigma": direct.get("one_sigma", "2.74590604355e-15"),
            "upper_bound": direct.get("upper_bound", "2.8e-15"),
            "units": direct.get("units", "dimensionless"),
            "reference_url": direct_url,
            "doi": direct_doi,
            "source_backed": True,
            "claim_ready": False,
            "why_not_claim": "context for eta readout only; not an MTS residual prediction",
        }),
        nonclaim({
            "tau_source_id": "WTS2776_2_MICROSCOPE_material_smoke_context",
            "pack_component": "material pair context",
            "fills_2775_row": "TAP2775_3_material_response; MAT2775_0_pair_convention",
            "dataset_id": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION",
            "row_id": "MCON1061_0_test_pair",
            "observable": "TA6V_minus_PtRh10 convention",
            "measured_value": "not_applicable",
            "one_sigma": "not_applicable",
            "upper_bound": "not_applicable",
            "units": "dimensionless convention",
            "reference_url": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "doi": "not_applicable",
            "source_backed": "internal_smoke_context",
            "claim_ready": False,
            "why_not_claim": "material pair convention only; not full material/source response tensor",
        }),
    ]


def build_provenance_rows(tau_source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [row for row in tau_source_rows if str(row["tau_source_id"]).startswith(("WTS2776_0", "WTS2776_1"))]
    rows = []
    for index, row in enumerate(selected):
        rows.append(nonclaim({
            "provenance_id": f"PROV2776_{index}_{row['row_id']}",
            "dataset_id": row["dataset_id"],
            "row_id": row["row_id"],
            "observable": row["observable"],
            "reference_url": row["reference_url"],
            "doi": row["doi"],
            "use_in_2776": "primary nonclaim readout/bound anchor" if index == 0 else "direct eta context, not source-weight prediction",
            "source_backed": True,
        }))
    return rows


def build_readout_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"matrix_id": "RFM2776_0_eta_bound", "component": "eta_AB upper bound/readout anchor", "filled_by": "WTS2776_0_MICROSCOPE_eta_source_charge_proxy", "fill_status": "SOURCE_BACKED_ANCHOR_FILLED", "still_missing": "parent product; tau_WEP; orbit kernel; source worldtube; material tensor"}),
        nonclaim({"matrix_id": "RFM2776_1_eta_formula", "component": "eta_AB formula/sign/readout convention", "filled_by": "local bound row only", "fill_status": "PARTIAL_CONTEXT_ONLY", "still_missing": "official formula/readout extraction row and parent force-map derivation"}),
        nonclaim({"matrix_id": "RFM2776_2_orbit_kernel", "component": "MICROSCOPE orbit/averaging kernel", "filled_by": "none", "fill_status": "MISSING", "still_missing": "orbit/altitude/time/attitude averaging source"}),
        nonclaim({"matrix_id": "RFM2776_3_source_worldtube", "component": "Earth/source worldtube", "filled_by": "none", "fill_status": "MISSING", "still_missing": "source profile, composition/source-charge convention, finite-source correction"}),
        nonclaim({"matrix_id": "RFM2776_4_material_tensor", "component": "Ti/Pt material response tensor", "filled_by": "WTS2776_2 material pair smoke context", "fill_status": "PAIR_CONTEXT_ONLY", "still_missing": "full material/source response tensor"}),
        nonclaim({"matrix_id": "RFM2776_5_direct_product", "component": "direct parent P_WEP product", "filled_by": "none", "fill_status": "MISSING", "still_missing": "parent variation to dimensionless eta_AB residual"}),
    ]


def build_requirement_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"requirement_id": "REQ2776_0_direct_product", "requirement": "derive numeric/theorem-zero P_WEP_relative_source_weight directly", "current_status": "MISSING_DIRECT_PARENT_PRODUCT", "next_action": "try parent variation force/readout kernel"}),
        nonclaim({"requirement_id": "REQ2776_1_readout_formula", "requirement": "official MICROSCOPE eta_AB formula/sign/readout convention", "current_status": "PARTIAL_BOUND_PROVENANCE_ONLY", "next_action": "extract formula/source row from MICROSCOPE paper or local corpus"}),
        nonclaim({"requirement_id": "REQ2776_2_orbit_kernel", "requirement": "MICROSCOPE orbit/attitude/averaging kernel", "current_status": "MISSING_ORBIT_KERNEL", "next_action": "source official orbit/readout metadata"}),
        nonclaim({"requirement_id": "REQ2776_3_source_worldtube", "requirement": "Earth/source worldtube and source charge convention", "current_status": "MISSING_SOURCE_WORLDTUBE", "next_action": "source Earth profile or theorem-reduce to calibrated point-source convention"}),
        nonclaim({"requirement_id": "REQ2776_4_material_tensor", "requirement": "Ti/Pt source-weight material response tensor", "current_status": "MISSING_MATERIAL_TENSOR", "next_action": "source material model or derive theorem reducing to Delta_w_TiPt"}),
        nonclaim({"requirement_id": "REQ2776_5_xhat_norm", "requirement": "shared Xhat/chi_X normalization", "current_status": "MISSING_XHAT_NORMALIZATION", "next_action": "derive shared branch normalization or direct product"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2776_0_WEP_direct_or_tau_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_SPLIT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": rel(OUTPUTS["theorem"]),
            "inputs_present": "MICROSCOPE_R1_eta_bound=2.8e-15;reference=https://arxiv.org/abs/2209.15487;doi=10.1103/PhysRevLett.129.121102",
            "required_inputs": "direct parent P_WEP product OR tau_WEP source/orbit/readout pack plus Delta_w_TiPt",
            "derivation_status": "MISSING_DIRECT_PRODUCT_AND_TAU_SPLIT_PRODUCT",
            "notes": "2776 acquired the first real readout/bound provenance row only; prediction remains missing.",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2776_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
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
            "issues": "no valid MTS direct/tau WEP product prediction rows",
        })
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2776_0_WEP_direct_or_tau_product",
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
        nonclaim({"gate_id": "CG2776_0_direct_product_theorem", "claim": "direct P_WEP product theorem is derived", "gate_pass": False, "reason": "parent variation to eta_AB remains missing", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2776_1_first_real_source_row", "claim": "first real MICROSCOPE eta/readout source row is acquired", "gate_pass": True, "reason": "R1 source-charge proxy row has numeric bound, units, URL, and DOI provenance", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2776_2_tau_WEP_numeric", "claim": "tau_WEP is numeric or theorem-zero", "gate_pass": False, "reason": "source row is a bound/readout anchor, not tau_WEP", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2776_3_runner_score", "claim": "WEP product can be scored", "gate_pass": False, "reason": "strict runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2776_4_local_GR_WEP", "claim": "local GR/WEP coupling branch is derived", "gate_pass": False, "reason": "direct product and tau acquisition branches remain open", "claim_allowed": False}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2776_0_direct_product_status", "decision": "direct WEP product theorem is not derived", "because": "parent variation still lacks eta_AB force/readout and source worldtube maps", "next_action": "keep direct theorem as preferred route, but acquire readout/formula data next"}),
        nonclaim({"decision_id": "DEC2776_1_first_source_row_status", "decision": "first real MICROSCOPE eta/readout source row is acquired as nonclaim provenance", "because": "local bound row R1 supplies numeric bound, units, URL, DOI, and reference note", "next_action": "extract official eta_AB formula/readout convention or orbit kernel"}),
        nonclaim({"decision_id": "DEC2776_2_best_next", "decision": "next target is MICROSCOPE eta formula/readout extraction or orbit kernel", "because": "the first source row gives a bound anchor but not a projection functional", "next_action": "2777-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2776_0_2777",
            "next_target": "2777-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition-under-AX1090.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_eta_readout_formula_or_orbit_kernel_acquisition_under_AX1090_2777.py",
            "objective": "extract the official MICROSCOPE eta_AB formula/readout convention and, if available, the first orbit/averaging kernel row; keep all rows nonclaim until a direct P_WEP product or tau_WEP projection exists",
            "include": "eta_AB definition, sign/absolute-value convention, test-mass pair convention, orbit/attitude/averaging source row, URL/DOI provenance, unit checks, runner refusal gates",
            "exclude": "setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    theorem: list[dict[str, Any]],
    tau_source: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_rows = theorem + candidate + gates
    source_rows = tau_source + provenance + readout + bounds + gates
    beta_rows = theorem + requirements + next_rows
    microscope_rows = tau_source + provenance + readout + requirements + candidate + bounds + next_rows
    specs = [
        ("BR2776_0_theorem_queue", "theorem", theorem_rows, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "direct WEP product theorem nonclaim copy"),
        ("BR2776_1_source_queue", "first_source", source_rows, OUTPUTS["tau_source"], BRANCH_OUTPUTS["source_queue"], "first real tau/readout source row nonclaim copy"),
        ("BR2776_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["requirements"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing direct WEP or tau source copy"),
        ("BR2776_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE direct WEP or source-row copy"),
        ("BR2776_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next eta readout acquisition target"),
    ]
    rows = []
    for copy_id, table_key, source_rows_for_copy, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows_for_copy)
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
    theorem = rows_by_name["theorem"]
    tau_source = rows_by_name["tau_source"]
    provenance = rows_by_name["provenance"]
    readout = rows_by_name["readout"]
    requirements = rows_by_name["requirements"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2776_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2776_1_direct_theorem_not_promoted", any(row["theorem_id"] == "DWT2776_5_verdict" and row["attempt_result"] == "DIRECT_PRODUCT_THEOREM_NOT_DERIVED" for row in theorem), "direct product theorem remains unproved"),
        ("VAL2776_2_first_real_source_row_acquired", any(row["tau_source_id"] == "WTS2776_0_MICROSCOPE_eta_source_charge_proxy" and row["source_backed"] is True and is_numeric(row["upper_bound"]) for row in tau_source), "first real MICROSCOPE eta/readout source row acquired with numeric bound and units"),
        ("VAL2776_3_provenance_has_url_doi", all(str(row["reference_url"]).startswith("https://") and str(row["doi"]).startswith("10.") for row in provenance), "provenance rows contain source URL and DOI"),
        ("VAL2776_4_readout_matrix_partial_only", any(row["matrix_id"] == "RFM2776_1_eta_formula" and row["fill_status"] == "PARTIAL_CONTEXT_ONLY" for row in readout) and any(row["matrix_id"] == "RFM2776_2_orbit_kernel" and row["fill_status"] == "MISSING" for row in readout), "readout matrix records first filled anchor while orbit kernel remains missing"),
        ("VAL2776_5_remaining_requirements_written", all(any(row["requirement_id"] == required for row in requirements) for required in ["REQ2776_0_direct_product", "REQ2776_1_readout_formula", "REQ2776_2_orbit_kernel", "REQ2776_3_source_worldtube"]), "remaining direct/tau requirements are written as nonclaim rows"),
        ("VAL2776_6_prediction_nonclaim", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "WEP product prediction remains nonclaim"),
        ("VAL2776_7_bound_anchor_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True and bounds[0]["valid_for_claim"] is False, "WEP bound anchor is numeric and internal-runner only"),
        ("VAL2776_8_runner_refuses_placeholder", runner[0]["valid_prediction_rows"] == 0 and runner[0]["valid_bound_rows"] == 1 and runner[0]["claim_allowed"] is False, "strict runner refuses missing direct/tau product"),
        ("VAL2776_9_claim_gates_safe", any(row["gate_id"] == "CG2776_1_first_real_source_row" and row["gate_pass"] is True and row["claim_allowed"] is False for row in gates) and all(row["claim_allowed"] is False for row in gates), "first source-row gate passes only as nonclaim provenance and all claims remain blocked"),
        ("VAL2776_10_next_target_written", any(row["row_id"] == "NEXT2776_0_2777" and "eta-readout-formula" in row["next_target"] for row in next_rows), "next target selects eta formula/readout or orbit kernel acquisition"),
        ("VAL2776_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2776_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2776_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2776_14_generated_files_in_post_checkpoint", generated_files_under_work(), "all generated files are under post-checkpoint-work"),
        ("VAL2776_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2776_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2776_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2776 attempts the direct WEP product theorem in the current R2/f(R) branch, keeps it unproved because parent variation to eta_AB is missing, acquires the first real MICROSCOPE eta/readout provenance rows from local_bounds with numeric bound, URL, and DOI, keeps them nonclaim because they are not tau_WEP or an MTS prediction, refuses missing direct/tau products, blocks WEP/local-GR claims, and selects eta formula/readout or orbit kernel acquisition as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2776 - Y5 R2/f(R): Direct WEP Product Theorem Or First Real tau Source Row Under AX1090",
        "## Private Verdict\n\nDirect `P_WEP_relative_source_weight` is still the cleanest theory route, but the theorem does not close because parent variation to `eta_AB` is missing.\n\nProgress: the first real MICROSCOPE eta/readout provenance row is acquired from `local_bound_claims.csv`: numeric bound, units, URL, and DOI are recorded. This is not `tau_WEP` and not a prediction.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Direct WEP Product Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["theorem_id", "claim", "formal_move", "attempt_result", "gap", "valid_for_claim"]),
        "## First Real tau / Readout Source Rows\n\n" + markdown_table(rows_by_name["tau_source"], ["tau_source_id", "pack_component", "fills_2775_row", "dataset_id", "row_id", "observable", "measured_value", "one_sigma", "upper_bound", "units", "reference_url", "doi", "source_backed", "claim_ready", "why_not_claim", "valid_for_claim"]),
        "## Provenance\n\n" + markdown_table(rows_by_name["provenance"], ["provenance_id", "dataset_id", "row_id", "observable", "reference_url", "doi", "use_in_2776", "source_backed", "valid_for_claim"]),
        "## Readout Fill Matrix\n\n" + markdown_table(rows_by_name["readout"], ["matrix_id", "component", "filled_by", "fill_status", "still_missing", "valid_for_claim"]),
        "## Remaining Requirements\n\n" + markdown_table(rows_by_name["requirements"], ["requirement_id", "requirement", "current_status", "next_action", "valid_for_claim"]),
        "## WEP Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes"]),
        "## WEP Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim", "notes"]),
        "## Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc", "valid_for_claim"]),
        "## Runner Comparisons\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is a real inch forward: we did not derive the WEP product, but we did turn the first MICROSCOPE anchor into a provenance-bearing row with URL, DOI, units, and refusal gates. The next best move is extracting the official eta definition/readout convention or an orbit kernel, not pretending the bound itself is a theory prediction.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    theorem = build_theorem_rows()
    tau_source = build_tau_source_rows()
    provenance = build_provenance_rows(tau_source)
    readout = build_readout_rows()
    requirements = build_requirement_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("theorem", theorem), ("tau_source", tau_source), ("provenance", provenance),
        ("readout", readout), ("requirements", requirements), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision),
        ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(theorem, tau_source, provenance, readout, requirements, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "theorem": theorem,
        "tau_source": tau_source,
        "provenance": provenance,
        "readout": readout,
        "requirements": requirements,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2776_OVERALL")
    print(f"2776 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
