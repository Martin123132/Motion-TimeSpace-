from __future__ import annotations

import csv
import shutil
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICRO = ROOT / "source-intake" / "microscope"
MICRO_COEFF = MICRO / "branch_locked_wep" / "coefficients"
MICRO_OFFICIAL = MICRO / "official_readout"
MICRO_SOURCE = MICRO / "source_worldtube"
MICRO_DERIVED = MICRO / "derived"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2983"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CMSM_URL = "https://cmsm-ds.onera.fr/"

DOC = ROOT / "2983-Y5-R2FR-WEP-live-file-acquisition-or-parent-measure-owner-closure-demotion-under-AX1090.md"

SRC_2982_DOC = ROOT / "2982-Y5-R2FR-parent-hbar-measure-owner-source-search-or-wep-tau-product-convention-completion-under-AX1090.md"
SRC_2982_NEXT = RESIDUALS / "P8_Y5_R2FR_2982_NEXT_TARGET.csv"
SRC_2982_PRODUCT = RESIDUALS / "P8_Y5_R2FR_2982_WEP_TAU_PRODUCT_CONVENTION_COMPLETION_AUDIT.csv"
SRC_2982_HBAR = RESIDUALS / "P8_Y5_R2FR_2982_PARENT_HBAR_MEASURE_OWNER_SOURCE_SEARCH.csv"
SRC_2982_DELTAWE = RESIDUALS / "P8_Y5_R2FR_2982_DELTAWE_DEPROXY_STATUS_NONCLAIM.csv"
SRC_2982_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2982_VALIDATION.csv"

SRC_PRODUCT_STATUS = MICRO / "branch_locked_wep" / "product" / "P_WEP_eta_product_status_1482.csv"
SRC_PRODUCT_CONVENTION = MICRO / "product_convention" / "P_WEP_eta_product_convention.csv"
SRC_C_PARENT = MICRO_COEFF / "C_parent.csv"
SRC_C_PARENT_SCHEMA = MICRO_COEFF / "C_parent_import_schema.csv"
SRC_C_PARENT_TEMPLATE = MICRO_COEFF / "C_parent_WEP_slot_import_TEMPLATE.csv"
SRC_C_PARENT_REFUSED = MICRO_COEFF / "C_parent_WEP_slot_import_REFUSED_1447.csv"
SRC_C_PARENT_ROUTE = MICRO_COEFF / "official_data_acquisition_route_nonclaim_1460.csv"
SRC_K_REQ = MICRO_OFFICIAL / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
SRC_K_LEDGER = MICRO_COEFF / "official_KCMSM_bound_inputs_nonclaim_1456.csv"
SRC_SOURCE_LEDGER = MICRO_COEFF / "source_worldtube_pilot_ledger_nonclaim_1457.csv"
SRC_MATERIAL_PACK = MICRO_COEFF / "WEP_material_context_pack_nonclaim_1481.csv"
SRC_1080_INPUTS = RESIDUALS / "P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv"
SRC_1080_MATERIAL = RESIDUALS / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv"
SRC_1081_DD = RESIDUALS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv"
SRC_1437_ACQ = RESIDUALS / "P8_Y5_R10_1437_SOURCE_ACQUISITION_LEDGER.csv"

LIVE_TARGETS = {
    "official_readout": MICRO_OFFICIAL / "P_WEP_K_CMSM_readout.csv",
    "source_worldtube": MICRO_SOURCE / "P_WEP_R_source_Earth_worldtube.csv",
    "material_tensor": MICRO_DERIVED / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
    "c_parent_import": MICRO_COEFF / "C_parent_WEP_slot_import.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2983_SOURCE_REGISTER.csv",
    "live_discovery": RESIDUALS / "P8_Y5_R2FR_2983_WEP_LIVE_FILE_DISCOVERY.csv",
    "c_parent_audit": RESIDUALS / "P8_Y5_R2FR_2983_C_PARENT_PROMOTION_AUDIT.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2983_WEP_LIVE_FILE_ACQUISITION_LEDGER.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2983_PARENT_MEASURE_OWNER_CLOSURE_DEMOTION.csv",
    "portal_probe": RESIDUALS / "P8_Y5_R2FR_2983_CMSM_PORTAL_PROBE_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2983_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2983_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2983_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2983_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2983_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "acquisition_copy": LOCAL_BOUNDS / "wep_live_file_acquisition_ledger_2983_NONCLAIM.csv",
    "closure_copy": PARENT_ACTION / "parent_measure_owner_closure_demotion_2983_CLOSURE_ONLY.csv",
    "next_copy": RAB_QUEUE / "JR2983_CMSM_and_Cparent_source_acquisition_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def clean_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def is_claim_ready_value(value: str) -> bool:
    value = str(value).strip()
    if not value:
        return False
    blocked = ["MISSING", "PENDING", "PLACEHOLDER", "NOT_SCOREABLE", "PROXY", "TEMPLATE"]
    if any(token in value.upper() for token in blocked):
        return False
    if value.upper() == "DERIVED_ZERO":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2983_00_2982_doc", SRC_2982_DOC, ["Status:", "NEXT2982_0_2983"], "2982 handoff"),
        ("SRC2983_01_2982_next", SRC_2982_NEXT, ["NEXT2982_0_2983", "WEP live files"], "selected 2983 target"),
        ("SRC2983_02_2982_product", SRC_2982_PRODUCT, ["WEP2982_verdict", "PRODUCT_CONVENTION_NOT_COMPLETE"], "2982 product verdict"),
        ("SRC2983_03_2982_hbar", SRC_2982_HBAR, ["HMO2982_5_search_verdict", "NO_PARENT_SIGNED_OWNER_FOUND"], "2982 parent owner search"),
        ("SRC2983_04_2982_deltawe", SRC_2982_DELTAWE, ["DW2982_4_acceptance", "DEPROXY_NOT_COMPLETE"], "2982 delta_w_e status"),
        ("SRC2983_05_2982_validation", SRC_2982_VALIDATION, ["VAL2982_OVERALL"], "2982 validation"),
        ("SRC2983_06_status1482", SRC_PRODUCT_STATUS, ["MAN1482_0_live_readout", "MAN1482_6_C_parent_import"], "live-file manifest"),
        ("SRC2983_07_product_convention", SRC_PRODUCT_CONVENTION, ["tau_eff", "PRODUCT_CONVENTION_OFFICIAL_PARTIAL_EXTRACTION_NONCLAIM"], "partial product convention"),
        ("SRC2983_08_cparent", SRC_C_PARENT, ["CP1430_6_verdict", "PLACEHOLDER_ROWS_ONLY_RUNNER_BLOCKED"], "existing C_parent rows"),
        ("SRC2983_09_cparent_schema", SRC_C_PARENT_SCHEMA, ["schema_version", "zero_certificate_status"], "C_parent import schema"),
        ("SRC2983_10_cparent_template", SRC_C_PARENT_TEMPLATE, ["C_PARENT_WEP_SLOT_IMPORT_TEMPLATE", "TEMPLATE_ONLY_NOT_IMPORTABLE"], "C_parent import template"),
        ("SRC2983_11_cparent_refusal", SRC_C_PARENT_REFUSED, ["REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE", "target_exists"], "C_parent import refusal"),
        ("SRC2983_12_k_requirements", SRC_K_REQ, ["KREQ1445_0", "live_target_exists"], "K_CMSM readout requirements"),
        ("SRC2983_13_k_ledger", SRC_K_LEDGER, ["KBI1456_6_data_portal", "POINTER_ONLY_ACCESS_UNVERIFIED"], "K_CMSM acquisition ledger"),
        ("SRC2983_14_source_ledger", SRC_SOURCE_LEDGER, ["PILOT1457_7_verdict", "PILOT_BLOCKED_NONCLAIM"], "source-worldtube pilot ledger"),
        ("SRC2983_15_material_pack", SRC_MATERIAL_PACK, ["MAT1481_6_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"], "material context pack"),
        ("SRC2983_16_1080_inputs", SRC_1080_INPUTS, ["FIP1080_1_C_parent", "FIP1080_4_K_readout"], "finite WEP input pack"),
        ("SRC2983_17_1080_material", SRC_1080_MATERIAL, ["MAT1080_4_full_tensor_upgrade", "MISSING_FULL_MATERIAL_TENSOR"], "material tensor candidates"),
        ("SRC2983_18_1081_dd", SRC_1081_DD, ["DDM1081_0_delta_alpha", "NUMERIC_SMOKE_DELTA_NONCLAIM"], "DD smoke deltas"),
        ("SRC2983_19_1437_acq", SRC_1437_ACQ, ["ACQ1437_0_C_parent", "ACQ1437_3_K_CMSM_readout"], "prior acquisition ledger"),
        ("SRC2983_20_acq_route", SRC_C_PARENT_ROUTE, ["ACQ1460_0_CMSM_portal_inventory", "ACQ1460_7_checksum_and_extractor"], "official acquisition route"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def live_file_discovery_rows() -> list[dict[str, Any]]:
    manifest_by_pack = {row.get("pack_item", ""): row for row in rows(SRC_PRODUCT_STATUS)}
    expectations = {
        "official_readout": "official or reproducibly generated K_CMSM/readout matrix with time, orbit, masks, units, source path",
        "source_worldtube": "Earth/source stress-composition/worldtube vector in same parent/source basis",
        "material_tensor": "full TA6V-minus-PtRh10 material response tensor, not two DD smoke components",
        "c_parent_import": "C_parent WEP slot value or DERIVED_ZERO with exact source certificate",
    }
    pack_map = {
        "official_readout": "official_readout",
        "source_worldtube": "source_worldtube",
        "material_tensor": "material_tensor",
        "c_parent_import": "C_parent",
    }
    out_rows: list[dict[str, Any]] = []
    for target_id, path in LIVE_TARGETS.items():
        manifest = manifest_by_pack.get(pack_map[target_id], {})
        exists = path.exists()
        if exists:
            out_status = "EXISTS_REQUIRES_SEPARATE_SCHEMA_AUDIT"
        else:
            out_status = "LIVE_FILE_ABSENT"
        out_rows.append(
            add(
                {
                    "live_id": f"LIVE2983_{target_id}",
                    "object": target_id,
                    "target_path": str(path),
                    "target_exists": exists,
                    "manifest_status": manifest.get("current_status", "NO_MANIFEST_ROW"),
                    "expected_content": expectations[target_id],
                    "promotion_status": out_status,
                    "created_in_2983": False,
                }
            )
        )
    return out_rows


def c_parent_audit_rows() -> list[dict[str, Any]]:
    required_schema_fields = [row.get("field", "") for row in rows(SRC_C_PARENT_SCHEMA)]
    source_rows_in = rows(SRC_C_PARENT)
    out_rows: list[dict[str, Any]] = []
    for row in source_rows_in:
        value = row.get("value", "")
        row_ready = (
            is_claim_ready_value(value)
            and row.get("units", "").strip()
            and "PENDING" not in row.get("units", "").upper()
            and row.get("sign_convention", "").strip()
            and "PENDING" not in row.get("sign_convention", "").upper()
            and row.get("source_path", "").strip()
            and row.get("parent_status", "") in {"PARENT_DERIVED", "SOURCE_BACKED_NUMERIC", "DERIVED_ZERO"}
            and clean_bool(row.get("valid_for_claim", "false"))
        )
        out_rows.append(
            add(
                {
                    "audit_id": f"CPA2983_{row.get('coefficient_id', 'unknown')}",
                    "coefficient_id": row.get("coefficient_id", ""),
                    "component": row.get("component", ""),
                    "value": value,
                    "units": row.get("units", ""),
                    "parent_status": row.get("parent_status", ""),
                    "sign_convention": row.get("sign_convention", ""),
                    "basis": row.get("basis", ""),
                    "source_path": row.get("source_path", ""),
                    "schema_fields_available": ";".join(field for field in required_schema_fields if field in row),
                    "promotable_to_C_parent_WEP_slot_import": row_ready,
                    "audit_status": "PROMOTABLE_REVIEW_REQUIRED" if row_ready else "NOT_PROMOTABLE_PLACEHOLDER_OR_UNSIGNED",
                }
            )
        )
    out_rows.append(
        add(
            {
                "audit_id": "CPA2983_verdict",
                "coefficient_id": "C_parent_WEP_slot_import",
                "component": "C_parent_WEP_TiPt",
                "value": "NOT_IMPORTED",
                "units": "NOT_CLAIM_UNITS",
                "parent_status": "NO_PROMOTABLE_SOURCE_ROW",
                "sign_convention": "missing",
                "basis": BRANCH_ID,
                "source_path": str(SRC_C_PARENT),
                "schema_fields_available": ";".join(required_schema_fields),
                "promotable_to_C_parent_WEP_slot_import": any(row.get("promotable_to_C_parent_WEP_slot_import") for row in out_rows),
                "audit_status": "C_PARENT_IMPORT_REMAINS_ABSENT",
            }
        )
    )
    return out_rows


def cmsm_probe_rows() -> list[dict[str, Any]]:
    status = "NOT_RUN"
    detail = ""
    final_url = CMSM_URL
    try:
        request = urllib.request.Request(CMSM_URL, method="HEAD", headers={"User-Agent": "MTS-private-audit/2983"})
        with urllib.request.urlopen(request, timeout=8) as response:
            status = f"HTTP_{response.status}"
            final_url = response.geturl()
            detail = response.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        status = f"HTTP_ERROR_{exc.code}"
        final_url = getattr(exc, "url", CMSM_URL)
        detail = str(exc)
    except Exception as exc:  # network and TLS failures are acquisition evidence, not validation failures
        status = "TIMEOUT_OR_REQUEST_FAILED"
        detail = str(exc)
    return [
        add(
            {
                "probe_id": "CMSM2983_0_head_probe",
                "url": CMSM_URL,
                "method": "HEAD",
                "status": status,
                "final_url": final_url,
                "detail": detail,
                "acquisition_use": "portal reachability only; not a data import",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "acquisition_id": "ACQ2983_0_C_parent_WEP",
                "needed_live_file": str(LIVE_TARGETS["c_parent_import"]),
                "current_best_source": str(SRC_C_PARENT),
                "current_status": "existing C_parent.csv is placeholder/unsigned; template/refusal exist",
                "required_next_evidence": "functional derivative or theorem-zero certificate with value, uncertainty/exact tag, units, sign convention, basis, source path, parent_status",
                "priority": "HIGHEST",
                "route": "derive_or_import_parent_signed_C_parent",
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "acquisition_id": "ACQ2983_1_K_CMSM_readout",
                "needed_live_file": str(LIVE_TARGETS["official_readout"]),
                "current_best_source": str(SRC_K_REQ),
                "current_status": "requirements file only; CMSM portal probe did not import data",
                "required_next_evidence": "official or reproducibly reconstructed time/orbit/readout arrays with masks, units, sign/body order, source URL/path, checksum",
                "priority": "HIGH",
                "route": "CMSM_inventory_then_extractor",
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "acquisition_id": "ACQ2983_2_R_source_Earth",
                "needed_live_file": str(LIVE_TARGETS["source_worldtube"]),
                "current_best_source": str(SRC_SOURCE_LEDGER),
                "current_status": "pilot ledger only; source profile/composition/orbit worldtube not numeric",
                "required_next_evidence": "Earth source composition/profile/worldtube vector in same basis with finite-size/orbit weighting and units",
                "priority": "HIGH",
                "route": "source_worldtube_model_or_common_mode_theorem",
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "acquisition_id": "ACQ2983_3_R_material_full_tensor",
                "needed_live_file": str(LIVE_TARGETS["material_tensor"]),
                "current_best_source": str(SRC_MATERIAL_PACK),
                "current_status": "composition and DD smoke components exist, full MTS parent tensor missing",
                "required_next_evidence": "full TA6V-minus-PtRh10 response tensor with parent basis, isotope/alloy averaging, no-double-count rule, units, source paths",
                "priority": "HIGH",
                "route": "material_tensor_builder_after_basis_lock",
                "promotion_allowed_now": False,
            }
        ),
        add(
            {
                "acquisition_id": "ACQ2983_4_eta_product_guard",
                "needed_live_file": str(SRC_PRODUCT_CONVENTION),
                "current_best_source": str(SRC_PRODUCT_CONVENTION),
                "current_status": "partial formula exists; sign/units/masks pending",
                "required_next_evidence": "eta formula, body order, sensitive-axis sign, tau_eff convention, official masks/orbit weighting",
                "priority": "HIGH",
                "route": "finish_product_convention_after_K_CMSM",
                "promotion_allowed_now": False,
            }
        ),
    ]


def closure_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "closure_id": "CLOS2983_0_parent_measure_owner",
                "object": "parent hbar/action-measure owner",
                "closure_statement": "Until a parent source explicitly constructs hbar_parent, dmu_parent, action-density line, connected matter graph, and current owner, the route is a closure clause.",
                "effect": "2981 theorem remains exact conditional; not a derived local-GR bridge",
                "status": "DEMOTED_TO_EXPLICIT_CLOSURE_CLAUSE",
                "can_reopen_if": "new parent action source signs the owner stack",
            }
        ),
        add(
            {
                "closure_id": "CLOS2983_1_wep_residual_route",
                "object": "finite WEP residual route",
                "closure_statement": "Because theorem-zero is not parent-signed, WEP must proceed through a finite product with real C_parent, R_source, R_material, K_CMSM, and product convention.",
                "effect": "delta_w_e proxy may guide pressure estimates only",
                "status": "FINITE_PRODUCT_ROUTE_SELECTED_NONCLAIM",
                "can_reopen_if": "C_parent theorem-zero or single-action owner theorem closes",
            }
        ),
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2983_0_live_files", "all four WEP live files acquired/promoted", False, "all required live files absent or nonclaim", False),
        ("CG2983_1_C_parent", "C_parent WEP slot imported", False, "C_parent.csv is placeholder/unsigned and target import absent", False),
        ("CG2983_2_measure_owner", "parent measure owner derived", False, "demoted to explicit closure clause", False),
        ("CG2983_3_deltawe", "delta_w_e deproxied", False, "tau/product inputs remain missing", False),
        ("CG2983_4_local_GR", "local GR/Newton reduction claim", False, "coupling bridge still closure/residual", False),
        ("CG2983_5_empirical", "WEP/R10/PPN/clock/orbital scoring", False, "no claim-grade product row", False),
    ]
    return [add({"claim_gate_id": gate_id, "claim": claim, "condition_passed": passed, "status": status, "claim_allowed": allowed}) for gate_id, claim, passed, status, allowed in data]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2983_0_no_live_write",
                "decision": "Do not create any of the four target live files in 2983.",
                "because": "existing evidence is requirements/template/proxy only; writing live targets would make fake claim infrastructure.",
                "next_action": "build/import only when source-backed rows satisfy schema and no MISSING/PENDING markers remain",
            }
        ),
        add(
            {
                "decision_id": "DEC2983_1_Cparent",
                "decision": "Do not promote existing C_parent.csv to C_parent_WEP_slot_import.csv.",
                "because": "rows are placeholders or external comparator slots, with pending units/sign/basis and no zero certificate.",
                "next_action": "derive C_parent theorem-zero/functional derivative, or keep WEP as bound-only plumbing",
            }
        ),
        add(
            {
                "decision_id": "DEC2983_2_route",
                "decision": "Demote parent measure-owner route to explicit closure unless new parent action text appears.",
                "because": "multiple exact conditionals exist, but the owner source is not in the current corpus.",
                "next_action": "attack the concrete acquisition path: CMSM inventory/extractor plus C_parent theorem/source",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2983_0_2984",
                "priority": "selected_primary",
                "next_doc": "2984-Y5-R2FR-CMSM-inventory-extractor-or-Cparent-theorem-zero-source-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_CMSM_inventory_extractor_or_Cparent_theorem_zero_source_under_AX1090_2984.py",
                "objective": "Make one real acquisition leap: either download/catalog the CMSM official inventory and build a checksummed K_CMSM extractor stub, or derive/source a claim-grade C_parent_WEP slot/DERIVED_ZERO certificate.",
                "include": "CMSM portal inventory;download URL;checksum manifest;K_CMSM schema map;C_parent functional derivative;DERIVED_ZERO certificate;no placeholders",
                "exclude": "fake live files;unit tau shortcut;DD smoke promotion;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for p in FORMALIZATION.rglob("*2983*") if p.is_file()) if FORMALIZATION.exists() else 0
    live_absent_count = sum(1 for row in all_rows["live_discovery"] if not row["target_exists"])
    cparent_promoted = any(row.get("promotable_to_C_parent_WEP_slot_import") for row in all_rows["c_parent_audit"] if row.get("audit_id") != "CPA2983_verdict")
    checks = [
        ("VAL2983_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2983_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2983_2_live_targets_not_faked", live_absent_count == 4, f"four target live files remain absent rather than fabricated (missing={live_absent_count})", True),
        ("VAL2983_3_cparent_not_promoted", not cparent_promoted, "existing C_parent rows are not promotable", True),
        ("VAL2983_4_closure_demoted", any(row["status"] == "DEMOTED_TO_EXPLICIT_CLOSURE_CLAUSE" for row in all_rows["closure"]), "parent measure owner route demoted to explicit closure", True),
        ("VAL2983_5_acquisition_written", len(all_rows["acquisition"]) >= 5, "WEP live-file acquisition ledger written", True),
        ("VAL2983_6_portal_probe_written", len(all_rows["portal_probe"]) == 1, "CMSM portal probe recorded", True),
        ("VAL2983_7_claims_blocked", all(not row["claim_allowed"] for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2983_8_next_written", any(row["next_id"] == "NEXT2983_0_2984" for row in all_rows["next"]), "2984 concrete acquisition target selected", True),
        ("VAL2983_9_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2983_10_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2983_11_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2983_12_formalization_clean", formal_count == 0, f"no 2983 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2983_13_doc_written", DOC.exists(), "2983 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2983_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2983 validation overall", "required": True}))
    return out_rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2983 - WEP Live-File Acquisition or Parent Measure-Owner Closure Demotion

Status: `Y5_R2FR_2983_no_live_files_promoted_Cparent_not_promotable_measure_owner_demoted_to_closure_CMSM_probe_recorded_nonclaim`

Claim ceiling: `no_live_WEP_product_no_Cparent_import_no_measure_owner_theorem_zero_no_deltawe_deproxy_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- 2983 did not fabricate live WEP files: the four required targets remain absent unless real source-backed rows are available.
- Existing `C_parent.csv` is not the missing import; it is placeholder/unsigned and cannot become `C_parent_WEP_slot_import.csv`.
- The parent `hbar_parent`/measure-owner route is now explicitly closure-only unless a new parent action source signs it.
- The finite WEP route remains the honest path: acquire/build `C_parent`, `K_CMSM`, `R_source`, `R_material`, and the product convention in one branch.
- The CMSM portal route was probed and recorded as acquisition evidence only, not data import.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Live-File Discovery

{table(all_rows["live_discovery"], ["live_id", "object", "target_exists", "manifest_status", "promotion_status", "created_in_2983"])}

## C_parent Promotion Audit

{table(all_rows["c_parent_audit"], ["audit_id", "coefficient_id", "value", "parent_status", "promotable_to_C_parent_WEP_slot_import", "audit_status"])}

## WEP Acquisition Ledger

{table(all_rows["acquisition"], ["acquisition_id", "needed_live_file", "current_status", "priority", "route", "promotion_allowed_now"])}

## Parent Measure-Owner Closure

{table(all_rows["closure"], ["closure_id", "object", "closure_statement", "effect", "status", "can_reopen_if"])}

## CMSM Portal Probe

{table(all_rows["portal_probe"], ["probe_id", "url", "method", "status", "final_url", "detail"])}

## Claim Gates

{table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows = {
        "sources": source_rows(),
        "live_discovery": live_file_discovery_rows(),
        "c_parent_audit": c_parent_audit_rows(),
        "acquisition": acquisition_rows(),
        "closure": closure_rows(),
        "portal_probe": cmsm_probe_rows(),
        "claims": claim_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"])
    shutil.copyfile(OUTPUTS["closure"], BRANCH_OUTPUTS["closure_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2983 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
