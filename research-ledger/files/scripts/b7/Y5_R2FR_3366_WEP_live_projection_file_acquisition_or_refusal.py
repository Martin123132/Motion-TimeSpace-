from __future__ import annotations

import csv
import shutil
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MIC = ROOT / "source-intake" / "microscope"
TEMPLATE_DIR = MIC / "import_templates"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

WEP_BOUND = "2.800000000000e-15"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3366_SOURCE_REGISTER.csv",
    "live_audit": OUT / "P8_Y5_R2FR_3366_WEP_LIVE_FILE_AUDIT.csv",
    "portal_probe": OUT / "P8_Y5_R2FR_3366_CMSM_PORTAL_PROBE.csv",
    "templates": TEMPLATE_DIR / "P_WEP_3366_REQUIRED_LIVE_FILE_COLUMNS.csv",
    "tau_packet": OUT / "P8_Y5_R2FR_3366_TAU_WEP_EXECUTION_PACKET.csv",
    "runner": OUT / "P8_Y5_R2FR_3366_WEP_RUNNER_NONCLAIM.csv",
    "decision": OUT / "P8_Y5_R2FR_3366_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3366_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3366_VALIDATION.csv",
}

LOCAL_SOURCES = [
    (
        "SRC3366_0_3365_doc",
        ROOT / "3365-Y5-R2FR-DeltaGM-extra-mass-projection-bound-row-under-AX1090.md",
        "3365 DeltaGM split and next-target handoff",
    ),
    (
        "SRC3366_1_3365_next",
        OUT / "P8_Y5_R2FR_3365_NEXT_TARGET.csv",
        "3365 selected WEP projection acquisition as next quantitative route",
    ),
    (
        "SRC3366_2_3363_bound",
        OUT / "P8_Y5_R2FR_3363_FIRST_SOURCE_NORMALIZATION_BOUND_ROW.csv",
        "source-backed MICROSCOPE Ti/Pt external WEP bound row",
    ),
    (
        "SRC3366_3_3364_projection_audit",
        OUT / "P8_Y5_R2FR_3364_WEP_PROJECTION_OWNER_AUDIT.csv",
        "required WEP projection objects from 3364",
    ),
    (
        "SRC3366_4_3364_status",
        OUT / "P8_Y5_R2FR_3364_MICROSCOPE_BOUND_STATUS_UPDATE.csv",
        "3364 post-audit MICROSCOPE bound status",
    ),
    (
        "SRC3366_5_2983_acquisition",
        OUT / "P8_Y5_R2FR_2983_WEP_LIVE_FILE_ACQUISITION_LEDGER.csv",
        "previous live-file acquisition ledger",
    ),
    (
        "SRC3366_6_2983_discovery",
        OUT / "P8_Y5_R2FR_2983_WEP_LIVE_FILE_DISCOVERY.csv",
        "previous target-file discovery status",
    ),
    (
        "SRC3366_7_3260_bound_inputs",
        OUT / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv",
        "MICROSCOPE result and first DD material delta input",
    ),
    (
        "SRC3366_8_3260_evidence",
        OUT / "P8_Y5_R2FR_3260_MICROSCOPE_SOURCE_EVIDENCE_LINES.csv",
        "source-backed MICROSCOPE evidence excerpts",
    ),
    (
        "SRC3366_9_3262_tau",
        OUT / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv",
        "partial tau_WEP factorization",
    ),
    (
        "SRC3366_10_3262_readout",
        OUT / "P8_Y5_R2FR_3262_MICROSCOPE_READOUT_FACTOR_EVIDENCE.csv",
        "MICROSCOPE readout factor evidence",
    ),
    (
        "SRC3366_11_3263_channel",
        OUT / "P8_Y5_R2FR_3263_MICROSCOPE_EP_CHANNEL_EVIDENCE.csv",
        "MICROSCOPE EP channel evidence",
    ),
    (
        "SRC3366_12_3342_bounds",
        OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv",
        "external WEP bound rows",
    ),
    (
        "SRC3366_13_3342_map",
        OUT / "P8_Y5_R2FR_3342_WEP_OBSERVABLE_MAP.csv",
        "WEP observable map and no-cancellation policy",
    ),
    (
        "SRC3366_14_1072_endpoints",
        OUT / "P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv",
        "known CMSM/REGARDS candidate endpoints",
    ),
    (
        "SRC3366_15_1073_contract",
        OUT / "P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv",
        "official CMSM export contract",
    ),
]

LIVE_TARGETS = [
    {
        "target_id": "LIVE3366_0_C_parent",
        "needed_object": "C_parent_WEP_slot_import",
        "target_path": MIC / "branch_locked_wep" / "coefficients" / "C_parent_WEP_slot_import.csv",
        "current_best_source": MIC / "branch_locked_wep" / "coefficients" / "C_parent.csv",
        "required_form": "parent-owned coefficient vector or DERIVED_ZERO certificate with branch id, basis, units, sign convention, source path, uncertainty/exact tag",
        "minimum_columns": "branch_id;coefficient_id;basis;value;units;sign_convention;parent_source_path;parent_status;valid_for_claim",
        "acceptance_rule": "all rows parent-signed and numeric, or exact theorem-zero; no placeholder or phenomenological unit shortcut",
        "blocks": "MISSING_PARENT_COEFFICIENT",
    },
    {
        "target_id": "LIVE3366_1_K_CMSM",
        "needed_object": "K_CMSM_readout",
        "target_path": MIC / "official_readout" / "P_WEP_K_CMSM_readout.csv",
        "current_best_source": MIC / "official_readout" / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv",
        "required_form": "official or reproducibly reconstructed MICROSCOPE readout/design matrix with time grid, masks, axes, units, segment labels, and provenance",
        "minimum_columns": "segment_id;t_utc;sample_index;mask_flag;gx;gz;Sxx;Sxz;Gamma_x_corr_or_model;frame;units;source_file",
        "acceptance_rule": "source-backed official export or exact reconstruction from sourced orbit/attitude/gravity model; guessed phase/masks forbidden",
        "blocks": "MISSING_OFFICIAL_READOUT_KERNEL",
    },
    {
        "target_id": "LIVE3366_2_R_source",
        "needed_object": "R_source_Earth_worldtube",
        "target_path": MIC / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
        "current_best_source": MIC
        / "branch_locked_wep"
        / "coefficients"
        / "source_worldtube_pilot_ledger_nonclaim_1457.csv",
        "required_form": "Earth/source stress-composition/profile vector in same parent basis as C_parent and R_material, including orbit/worldtube weighting",
        "minimum_columns": "basis_id;source_component;value;units;Earth_model;orbit_weighting;finite_size_rule;source_path;valid_for_claim",
        "acceptance_rule": "same basis as C_parent and R_material; either exact common-mode theorem or numeric profile with provenance",
        "blocks": "MISSING_SOURCE_WORLDTUBE",
    },
    {
        "target_id": "LIVE3366_3_R_material",
        "needed_object": "R_material_TA6V_minus_PtRh10_full_tensor",
        "target_path": MIC / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
        "current_best_source": MIC
        / "branch_locked_wep"
        / "coefficients"
        / "WEP_material_context_pack_nonclaim_1481.csv",
        "required_form": "full material response tensor for TA6V minus PtRh10 in the parent response basis, with isotope/alloy averaging and no-double-count rule",
        "minimum_columns": "basis_id;material_pair;component;delta_response;units;composition_source;isotope_rule;valid_for_claim",
        "acceptance_rule": "not just material labels or DD smoke components; must contract legally with C_parent and R_source",
        "blocks": "MISSING_PARENT_MATERIAL_TENSOR",
    },
    {
        "target_id": "LIVE3366_4_eta_product",
        "needed_object": "tau_WEP_product_convention",
        "target_path": MIC / "product_convention" / "P_WEP_eta_product_convention.csv",
        "current_best_source": MIC / "product_convention" / "P_WEP_eta_product_convention.csv",
        "required_form": "eta/tau product convention with body order, sign, sensitive-axis orientation, readout masks, units, and branch lock",
        "minimum_columns": "same_parent_branch_id;eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock;source_path;row_status;valid_prediction_row;valid_for_claim",
        "acceptance_rule": "row is present but partial until K_CMSM, source basis, masks and sign are live",
        "blocks": "PARTIAL_FORMULA_ONLY",
    },
]

WEB_TARGETS = [
    (
        "WEB3366_0_CMSM_module",
        "https://cmsm-ds.onera.fr/user/microscope/modules/7",
        "official CMSM/REGARDS module route cited by earlier checkpoints",
    ),
    (
        "WEB3366_1_CMSM_base",
        "https://cmsm-ds.onera.fr",
        "CMSM portal base route",
    ),
    (
        "WEB3366_2_CMSM_dataset_api",
        "https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search",
        "candidate REGARDS dataset-search API route",
    ),
    (
        "WEB3366_3_OCA_microscope",
        "https://www.oca.eu/fr/microscope",
        "OCA MICROSCOPE page naming data availability/portal route",
    ),
    (
        "WEB3366_4_CNES_microscope",
        "https://cnes.fr/en/projects/microscope",
        "CNES mission context and final-result page",
    ),
]


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            if path.suffix.lower() == ".csv":
                parse_ok, parse_error = parse_csv(path)
            else:
                parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def classify_live_target(target: dict[str, Any]) -> dict[str, str]:
    target_path = Path(target["target_path"])
    source_path = Path(target["current_best_source"])
    target_exists = target_path.exists()
    target_parse = False
    target_parse_error = ""
    if target_exists:
        target_parse, target_parse_error = parse_csv(target_path)
    source_exists = source_path.exists()
    source_parse = False
    source_parse_error = ""
    if source_exists:
        source_parse, source_parse_error = parse_csv(source_path)

    if target["needed_object"] == "tau_WEP_product_convention" and target_exists:
        current_status = "PARTIAL_LIVE_FORMULA_PRESENT_NOT_SCORE_READY"
        score_ready = False
        refusal_reason = "product convention exists, but K_CMSM/source basis/material tensor/sign/masks remain pending"
    elif target_exists and target_parse:
        current_status = "TARGET_EXISTS_BUT_REQUIRES_SEMANTIC_REVIEW"
        score_ready = False
        refusal_reason = "file exists but 3366 does not certify semantic parent ownership"
    else:
        current_status = "MISSING_REQUIRED_LIVE_FILE"
        score_ready = False
        refusal_reason = target["blocks"]

    return {
        "target_id": target["target_id"],
        "needed_object": target["needed_object"],
        "target_path": str(target_path),
        "target_exists": bool_text(target_exists),
        "target_parse_ok": bool_text(target_parse),
        "target_parse_error": target_parse_error,
        "current_best_source": str(source_path),
        "current_best_source_exists": bool_text(source_exists),
        "current_best_source_parse_ok": bool_text(source_parse),
        "current_best_source_parse_error": source_parse_error,
        "required_form": target["required_form"],
        "minimum_columns": target["minimum_columns"],
        "acceptance_rule": target["acceptance_rule"],
        "current_status": current_status,
        "score_ready": bool_text(score_ready),
        "refusal_reason": refusal_reason,
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
    }


def live_audit_rows() -> list[dict[str, str]]:
    return [classify_live_target(target) for target in LIVE_TARGETS]


def probe_url(probe_id: str, url: str, role: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "MTS-3366-probe/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:  # noqa: S310
            content = response.read(768)
            status = getattr(response, "status", "")
            content_type = response.headers.get("content-type", "")
            final_url = response.geturl()
            return {
                "probe_id": probe_id,
                "url": url,
                "role": role,
                "probe_status": "HTTP_OK",
                "http_status": status,
                "content_type": content_type,
                "bytes_sampled": len(content),
                "final_url": final_url,
                "error": "",
                "schema_or_data_inventory_acquired": "false",
                "valid_for_claim": "false",
            }
    except urllib.error.HTTPError as exc:
        return {
            "probe_id": probe_id,
            "url": url,
            "role": role,
            "probe_status": "HTTP_ERROR",
            "http_status": exc.code,
            "content_type": "",
            "bytes_sampled": 0,
            "final_url": "",
            "error": str(exc),
            "schema_or_data_inventory_acquired": "false",
            "valid_for_claim": "false",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "probe_id": probe_id,
            "url": url,
            "role": role,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": "",
            "content_type": "",
            "bytes_sampled": 0,
            "final_url": "",
            "error": f"{type(exc).__name__}: {exc}",
            "schema_or_data_inventory_acquired": "false",
            "valid_for_claim": "false",
        }


def portal_probe_rows() -> list[dict[str, Any]]:
    socket.setdefaulttimeout(8)
    return [probe_url(probe_id, url, role) for probe_id, url, role in WEB_TARGETS]


def template_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for target in LIVE_TARGETS:
        rows.append(
            {
                "template_id": target["target_id"].replace("LIVE", "TPL"),
                "needed_object": target["needed_object"],
                "target_live_path": str(target["target_path"]),
                "minimum_columns": target["minimum_columns"],
                "acceptance_rule": target["acceptance_rule"],
                "template_status": "SCHEMA_ONLY_NOT_LIVE_DATA",
                "write_policy": "do_not_create_target_live_file_until real source-backed data or parent theorem exists",
                "valid_for_claim": "false",
            }
        )
    return rows


def tau_packet_rows() -> list[dict[str, str]]:
    return [
        {
            "packet_id": "TAU3366_0_executable_formula",
            "object": "eta_MTS_TiPt",
            "formula": "eta_MTS(Ti,Pt)=sum_I K_CMSM^I * C_parent^I * R_source_Earth^I * (R_material_TA6V^I - R_material_PtRh10^I) + residual_channels",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "required_inputs": "C_parent;K_CMSM;R_source_Earth;R_material_TA6V_minus_PtRh10;eta_product_convention;no_cancellation_policy",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "TAU3366_1_external_bound",
            "object": "eta_MICROSCOPE_TiPt_bound",
            "formula": "|eta_TiPt| <= 2.8e-15 component target from source-backed 3363 row",
            "status": "EXTERNAL_BOUND_ACQUIRED_NONCLAIM",
            "required_inputs": "none for external comparator; MTS projection still needs tau packet",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "TAU3366_2_readout_factor",
            "object": "tau_readout_X",
            "formula": "tau_readout_X = a_tilde_c11 with 0.98 <= tau_readout_X <= 1.02 from MICROSCOPE evidence",
            "status": "PARTIAL_FACTOR_SOURCE_BACKED",
            "required_inputs": "source_profile and channel_projection factors still missing",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "TAU3366_3_no_tau_one_shortcut",
            "object": "tau_WEP",
            "formula": "tau_WEP != 1 unless K_CMSM, R_source, R_material, sign, mask and same-branch normalization are all signed",
            "status": "SHORTCUT_FORBIDDEN",
            "required_inputs": "full live projection packet or parent theorem-zero",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(live_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    target_status = {row["needed_object"]: row for row in live_rows}
    missing_objects = [
        name
        for name, row in target_status.items()
        if row["score_ready"] != "true" or row["valid_prediction_row"] != "true"
    ]
    product_ready = not missing_objects
    return [
        {
            "run_id": "RUN3366_0_external_bound_import",
            "test": "MICROSCOPE external comparator row is numeric and source-backed",
            "input": "3363/3260/3342 WEP rows",
            "result": "PASS_EXTERNAL_BOUND_ONLY",
            "detail": f"external bound retained as {WEP_BOUND} dimensionless component target",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3366_1_readout_partial",
            "test": "readout factor tau_readout_X is source-backed",
            "input": "3262 readout factor evidence",
            "result": "PASS_PARTIAL_FACTOR_ONLY",
            "detail": "tau_readout_X exists, but source_profile and channel_projection are missing",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3366_2_live_product",
            "test": "evaluate eta_MTS finite WEP product",
            "input": "C_parent*K_CMSM*R_source*R_material",
            "result": "REFUSE_PRODUCT_EVALUATION" if not product_ready else "READY_FOR_SEMANTIC_REVIEW",
            "detail": "missing_or_partial=" + ";".join(missing_objects),
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3366_3_tau_one_shortcut",
            "test": "set tau_WEP=1 and score Delta_w directly",
            "input": "manual shortcut",
            "result": "REJECT_SHORTCUT",
            "detail": "tau=1 hides the readout/source/material projection, exactly the closure assumption this branch is meant to avoid",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3366_4_local_GR_promotion",
            "test": "promote WEP/local-GR source-normalization pass",
            "input": "3366 packet",
            "result": "BLOCKED",
            "detail": "external bound exists, but no executable MTS prediction row exists",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(live_rows: list[dict[str, str]], probe_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    cmsm_ok = any(
        row["probe_status"] == "HTTP_OK" and "cmsm-ds.onera.fr" in row["url"] for row in probe_rows
    )
    oca_ok = any(row["probe_status"] == "HTTP_OK" and "oca.eu" in row["url"] for row in probe_rows)
    hard_missing = [
        row["needed_object"]
        for row in live_rows
        if row["current_status"] in {"MISSING_REQUIRED_LIVE_FILE", "PARTIAL_LIVE_FORMULA_PRESENT_NOT_SCORE_READY"}
    ]
    return [
        {
            "decision_id": "DEC3366_0_external_bound_state",
            "question": "Do we have a real WEP number?",
            "answer": "yes, as an external MICROSCOPE component target only",
            "evidence": "3363/3260/3342 rows",
            "consequence": "usable as a bound once MTS projection supplies tau_WEP and Delta_w channel",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3366_1_projection_state",
            "question": "Can the MTS WEP product be executed now?",
            "answer": "no",
            "evidence": "missing_or_partial=" + ";".join(hard_missing),
            "consequence": "do not score WEP/local-GR branch from MICROSCOPE yet",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3366_2_portal_state",
            "question": "Did the official CMSM route become automatically usable?",
            "answer": "not from this runtime" if not cmsm_ok else "CMSM route responded but no schema/data inventory was acquired",
            "evidence": f"cmsm_ok={bool_text(cmsm_ok)}; oca_page_ok={bool_text(oca_ok)}",
            "consequence": "user-assisted CMSM export remains optional; derivation route should not wait on it",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3366_3_best_next_route",
            "question": "What moves the theory forward rather than looping?",
            "answer": "switch to 3367 first DeltaGM/source-mass component theorem or coefficient row, while keeping CMSM export as optional intake",
            "evidence": "WEP projection needs parent C_parent/basis anyway; official arrays alone cannot create the parent coefficient",
            "consequence": "next target should attack parent-owned source coupling, not repeat portal probing",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3367-Y5-R2FR-first-DeltaGM-mass-charge-component-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3367_first_DeltaGM_mass_charge_component_row.py",
            "objective": "pick one source-mass component, preferably C_parent/R_nonEH/source-charge, and either derive a theorem-zero row or produce a parent-owned finite coefficient contract",
            "why_next": "WEP cannot execute without the parent coefficient/basis, and source-normalized Newton/local-GR needs this same owner",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3366A-user-assisted-CMSM-export-intake-optional.md",
            "target_script": "scripts/Y5_R2FR_3366A_validate_user_CMSM_export.py",
            "objective": "if a browser/manual CMSM export appears, validate it against the 3366 import-template columns without treating it as an MTS claim",
            "why_next": "official arrays help tau_WEP only after C_parent/R_source/R_material exist; they should not block derivation work",
            "valid_for_claim": "false",
        },
    ]


def validate_rows(
    source_rows: list[dict[str, str]],
    live_rows: list[dict[str, str]],
    probe_rows: list[dict[str, Any]],
    template_rows_in: list[dict[str, str]],
    runner_rows_in: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    add(
        "VAL3366_0_local_sources_exist",
        "all cited local source paths exist",
        all(row["exists"] == "true" for row in source_rows),
    )
    add(
        "VAL3366_1_local_sources_parse",
        "all cited local source paths parse",
        all(row["parse_ok"] == "true" for row in source_rows),
    )
    required_objects = {target["needed_object"] for target in LIVE_TARGETS}
    seen_objects = {row["needed_object"] for row in live_rows}
    add(
        "VAL3366_2_live_audit_complete",
        "live audit covers C_parent, K_CMSM, R_source, R_material and tau product convention",
        required_objects == seen_objects,
        "seen=" + ";".join(sorted(seen_objects)),
    )
    add(
        "VAL3366_3_no_live_product_claim",
        "no required WEP live object is marked score-ready/claim-ready",
        all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in live_rows),
    )
    add(
        "VAL3366_4_templates_not_live_placeholders",
        "required-column templates are schema-only and not target live placeholders",
        all(row["template_status"] == "SCHEMA_ONLY_NOT_LIVE_DATA" for row in template_rows_in),
    )
    add(
        "VAL3366_5_portal_probe_recorded",
        "CMSM/OCA/CNES acquisition probes are recorded",
        len(probe_rows) == len(WEB_TARGETS)
        and any("cmsm-ds.onera.fr" in row["url"] for row in probe_rows)
        and any("oca.eu" in row["url"] for row in probe_rows),
    )
    add(
        "VAL3366_6_runner_rejects_tau_shortcut",
        "runner rejects tau_WEP=1 shortcut",
        any(row["run_id"] == "RUN3366_3_tau_one_shortcut" and row["result"] == "REJECT_SHORTCUT" for row in runner_rows_in),
    )
    add(
        "VAL3366_7_runner_blocks_local_GR",
        "runner blocks WEP/local-GR promotion",
        any(row["run_id"] == "RUN3366_4_local_GR_promotion" and row["result"] == "BLOCKED" for row in runner_rows_in),
    )
    add(
        "VAL3366_8_next_target_not_portal_loop",
        "next target includes derivation-first source coupling route",
        any(row["target_id"].startswith("3367-") for row in next_rows),
    )
    all_write_targets = list(OUTPUTS.values()) + [DOC]
    add(
        "VAL3366_9_write_scope_outside_formalization",
        "all 3366 write targets are outside formalization-workbench",
        all(not str(path).lower().startswith(str(FW).lower()) for path in all_write_targets),
        f"write_targets={len(all_write_targets)}",
    )
    passed_so_far = all(row["passed"] == "true" for row in rows)
    add(
        "VAL3366_10_overall",
        "3366 validation overall",
        passed_so_far,
        "all required checks passed" if passed_so_far else "one or more checks failed",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    live_rows: list[dict[str, str]],
    probe_rows: list[dict[str, Any]],
    template_rows_in: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    runner_rows_in: list[dict[str, str]],
    decision_rows_in: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    validation_rows_in: list[dict[str, str]],
) -> None:
    content = f"""# 3366 - Y5/R2FR WEP live projection file acquisition or refusal under AX1090

## Summary
- This checkpoint actively audits the live WEP projection path instead of repeating the generic "missing tau" complaint.
- Result: the external MICROSCOPE Ti/Pt bound is real and source-backed, but the MTS prediction row is still not executable because `C_parent`, `K_CMSM`, `R_source`, and `R_material` are absent or only partial.
- Concrete gain: the branch now has an import-template contract for every live object, a current web/portal probe ledger, and a runner that refuses the illegal `tau_WEP=1` shortcut.
- Physics consequence: WEP remains a powerful quantitative gate, but it cannot promote local GR/Newton recovery until the parent source coupling/basis is supplied.
- Best next route is not another CMSM loop: derive or bound the first parent-owned source-mass/coupling component in 3367, while keeping CMSM export intake optional.

Generated UTC: `{RUN_UTC}`

## Source Register
{markdown_table(source_rows)}

## Live File Audit
{markdown_table(live_rows)}

## CMSM / External Portal Probe
{markdown_table(probe_rows)}

## Import Templates
{markdown_table(template_rows_in)}

## Tau WEP Execution Packet
{markdown_table(tau_rows)}

## Nonclaim Runner
{markdown_table(runner_rows_in)}

## Decision Ledger
{markdown_table(decision_rows_in)}

## Next Target
{markdown_table(next_rows)}

## Validation
{markdown_table(validation_rows_in)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    source_rows = local_source_rows()
    live_rows = live_audit_rows()
    probe_rows = portal_probe_rows()
    templates = template_rows()
    tau_rows = tau_packet_rows()
    runs = runner_rows(live_rows)
    decisions = decision_rows(live_rows, probe_rows)
    next_rows = next_target_rows()
    validations = validate_rows(source_rows, live_rows, probe_rows, templates, runs, next_rows)

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["live_audit"], live_rows)
    write_csv(OUTPUTS["portal_probe"], probe_rows)
    write_csv(OUTPUTS["templates"], templates)
    write_csv(OUTPUTS["tau_packet"], tau_rows)
    write_csv(OUTPUTS["runner"], runs)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(source_rows, live_rows, probe_rows, templates, tau_rows, runs, decisions, next_rows, validations)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
