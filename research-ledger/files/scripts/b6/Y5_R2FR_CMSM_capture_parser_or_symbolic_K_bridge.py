from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1599"
INPUT_DIR = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1599-Y5-R2FR-CMSM-capture-parser-or-symbolic-K-bridge.md"

SOURCE_FILES = {
    "1598_doc": ROOT / "1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy.md",
    "1598_validation": OUT / "P8_Y5_BRR545_1598_VALIDATION.csv",
    "1598_portal": OUT / "P8_Y5_PARENT_QLOC_1598_CMSM_PORTAL_PROBE_SYNTHESIS.csv",
    "1598_kernel": OUT / "P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv",
    "1598_alignment": OUT / "P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv",
    "1598_next": OUT / "P8_Y5_PARENT_QLOC_1598_NEXT_TARGET.csv",
    "1084_readout": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1467_evidence": OUT / "P8_Y5_R10_1467_CMSM_CAPTURE_EVIDENCE_REQUIREMENTS.csv",
}

NEEDLES = {
    "1598_doc": ["NEXT_1599_CMSM_CAPTURE_OR_SYMBOLIC_K_BRIDGE", "symbolic readout-kernel"],
    "1598_validation": ["VAL1598_OVERALL", "PASS"],
    "1598_portal": ["CPS1598_2_module7_route", "filelist_acquired"],
    "1598_kernel": ["MKS1598_0_published_measurement_equation", "SYMBOLIC_KERNEL_STRUCTURE_AVAILABLE"],
    "1598_alignment": ["AIR1598_4_alignment", "MISSING_CRITICAL_ALIGNMENT"],
    "1598_next": ["1599-Y5-R2FR-CMSM-capture-parser-or-symbolic-K-bridge", "parse real filelist"],
    "1084_readout": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1467_evidence": ["EV1467_1_filelist_rows", "MISSING"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1599_SOURCE_REGISTER.csv"
INPUT_INVENTORY = OUT / "P8_Y5_PARENT_QLOC_1599_CMSM_INPUT_INVENTORY.csv"
PARSED_FILELIST = OUT / "P8_Y5_PARENT_QLOC_1599_CMSM_PARSED_FILELIST_CANDIDATE.csv"
SYMBOLIC_K_BRIDGE = OUT / "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv"
PARSER_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1599_CAPTURE_PARSER_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1599_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1599_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1599_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1599_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1599_VALIDATION.csv"

COPY_TARGETS = {
    INPUT_INVENTORY: [
        QUARANTINE / "CMSM_INPUT_INVENTORY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_input_inventory_nonclaim_1599.csv",
    ],
    PARSED_FILELIST: [
        QUARANTINE / "CMSM_PARSED_FILELIST_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_parsed_filelist_candidate_nonclaim_1599.csv",
    ],
    SYMBOLIC_K_BRIDGE: [
        QUARANTINE / "SYMBOLIC_K_BRIDGE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_symbolic_K_bridge_nonclaim_1599.csv",
    ],
    PARSER_CONTRACT: [
        QUARANTINE / "CAPTURE_PARSER_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_capture_parser_contract_nonclaim_1599.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1599.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1599_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1599_CMSM_capture_parser_or_symbolic_K_bridge_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def input_inventory_rows() -> list[dict[str, Any]]:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    files = [path for path in INPUT_DIR.iterdir() if path.is_file()]
    if not files:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "input_id": "INV1599_0_no_input_files",
                "path": INPUT_DIR.relative_to(ROOT).as_posix(),
                "file_type": "none",
                "byte_count": 0,
                "parse_status": "NO_CMSM_CAPTURE_OR_FILELIST_INPUT",
                "claim_impact": "parser contract ready but no official evidence ingested",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]
    rows = []
    for index, path in enumerate(sorted(files)):
        suffix = path.suffix.lower()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "input_id": f"INV1599_{index}_{path.stem}",
                "path": path.relative_to(ROOT).as_posix(),
                "file_type": suffix.lstrip(".") or "unknown",
                "byte_count": path.stat().st_size,
                "parse_status": "SUPPORTED_CANDIDATE" if suffix in {".har", ".json", ".csv"} else "UNSUPPORTED_EXTENSION",
                "claim_impact": "quarantine parse only",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def flatten_json_filelist(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    rows = []
    entries = []
    if path.suffix.lower() == ".har":
        entries = data.get("log", {}).get("entries", [])
    elif isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        for key in ("files", "data", "results", "content", "items", "features"):
            value = data.get(key)
            if isinstance(value, list):
                entries = value
                break
        if not entries:
            entries = [data]
    for index, entry in enumerate(entries):
        text = json.dumps(entry, ensure_ascii=False)
        looks_download = any(token in text.lower() for token in ("download", "checksum", "filename", "file_name", "dataobject", "product"))
        if looks_download:
            rows.append(
                {
                    "row_id": f"PFL1599_JSON_{path.stem}_{index}",
                    "source_input": path.relative_to(ROOT).as_posix(),
                    "dataset_id": find_json_value(entry, ["dataset_id", "datasetId", "dataset", "product_id", "productId"]),
                    "file_name": find_json_value(entry, ["file_name", "filename", "name", "label"]),
                    "download_url": find_json_value(entry, ["download_url", "downloadUrl", "url", "href"]),
                    "checksum": find_json_value(entry, ["checksum", "sha256", "md5"]),
                    "byte_count": find_json_value(entry, ["byte_count", "byteCount", "size", "contentLength"]),
                    "parse_status": "CANDIDATE_ROW_NEEDS_REVIEW",
                }
            )
    return rows


def find_json_value(obj: Any, keys: list[str]) -> str:
    if isinstance(obj, dict):
        for key in keys:
            if key in obj and obj[key] not in (None, ""):
                return str(obj[key])
        for value in obj.values():
            found = find_json_value(value, keys)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_json_value(value, keys)
            if found:
                return found
    return ""


def parse_csv_filelist(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader):
            lower = {key.lower(): value for key, value in row.items()}
            rows.append(
                {
                    "row_id": f"PFL1599_CSV_{path.stem}_{index}",
                    "source_input": path.relative_to(ROOT).as_posix(),
                    "dataset_id": lower.get("dataset_id", lower.get("datasetid", lower.get("product_id", ""))),
                    "file_name": lower.get("file_name", lower.get("filename", lower.get("name", ""))),
                    "download_url": lower.get("download_url", lower.get("downloadurl", lower.get("url", ""))),
                    "checksum": lower.get("checksum", lower.get("sha256", lower.get("md5", ""))),
                    "byte_count": lower.get("byte_count", lower.get("bytecount", lower.get("size", ""))),
                    "parse_status": "CANDIDATE_ROW_NEEDS_REVIEW",
                }
            )
    return rows


def parsed_filelist_rows() -> list[dict[str, Any]]:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for path in sorted(INPUT_DIR.iterdir()):
        if not path.is_file():
            continue
        try:
            if path.suffix.lower() in {".har", ".json"}:
                rows.extend(flatten_json_filelist(path))
            elif path.suffix.lower() == ".csv":
                rows.extend(parse_csv_filelist(path))
        except Exception as exc:
            rows.append(
                {
                    "row_id": f"PFL1599_ERROR_{path.stem}",
                    "source_input": path.relative_to(ROOT).as_posix(),
                    "dataset_id": "",
                    "file_name": "",
                    "download_url": "",
                    "checksum": "",
                    "byte_count": "",
                    "parse_status": f"PARSE_ERROR_{type(exc).__name__}",
                }
            )
    if not rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "row_id": "PFL1599_0_no_filelist_rows",
                "source_input": INPUT_DIR.relative_to(ROOT).as_posix(),
                "dataset_id": "",
                "file_name": "",
                "download_url": "",
                "checksum": "",
                "byte_count": "",
                "parse_status": "NO_PARSEABLE_OFFICIAL_FILELIST",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    for row in rows:
        row.setdefault("same_parent_branch_id", BRANCH_ID)
        row.setdefault("valid_for_claim", False)
        row.setdefault("claim_allowed", False)
    return rows


def symbolic_k_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": "SKB1599_0_EP_signal_template",
            "published_component": "Earth-gravity EP signal template",
            "symbolic_object": "g_x,g_y,g_z projected onto the differential readout through common-mode sensitivity coefficients",
            "MTS_tau_slot": "K_EP_gravity_dot_V_MTS_source_material",
            "required_numeric_inputs": "time series or templates for g_x,g_y,g_z; sensitivity matrix a_c1j; attitude/instrument-frame convention",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": "SKB1599_1_gravity_gradient_terms",
            "published_component": "gravity-gradient/off-centering correction",
            "symbolic_object": "Sxx,Sxy,Sxz and off-centering terms entering the sensitive-axis differential acceleration",
            "MTS_tau_slot": "readout contamination/correction operator inside K_CMSM",
            "required_numeric_inputs": "Sxx/Sxy/Sxz or equivalent; off-centering vector; calibration/session masks",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": "SKB1599_2_masks_gaps_calibration",
            "published_component": "mission/session masks, gaps and calibration flags",
            "symbolic_object": "windowing operator W_session applied before inner product",
            "MTS_tau_slot": "defines which time samples enter <K,V>",
            "required_numeric_inputs": "session ids; masks; gaps; calibration flags; weighting rule",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": "SKB1599_3_alignment_object",
            "published_component": "branch readout/source-material projection",
            "symbolic_object": "c_min or nonzero projection = |<K_CMSM,V_MTS>|/(||K_CMSM|| ||V_MTS||)",
            "MTS_tau_slot": "tau_min lower-bound gate",
            "required_numeric_inputs": "K_CMSM; V_MTS; norm convention; projection uncertainty",
            "current_status": "MISSING_CRITICAL_ALIGNMENT",
            "claim_allowed": False,
        },
    ]


def parser_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CPC1599_0_input_location",
            "requirement": "place official CMSM HAR/JSON/CSV filelist evidence under source-intake/microscope/quarantine/1599/input",
            "promotion_rule": "quarantine parse only; no live promotion without checksums and schema review",
            "current_status": "READY_WAITING_FOR_INPUT",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CPC1599_1_required_filelist_fields",
            "requirement": "dataset_id, product_id/file_name, file_role, download_url, checksum or byte_count, row_count, metadata schema",
            "promotion_rule": "rows missing file_name/download_url/checksum remain nonclaim",
            "current_status": "CONTRACT_WRITTEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CPC1599_2_K_extraction",
            "requirement": "map official files to time/session/gx/gz/Sxx/Sxz/masks/calibration/attitude columns",
            "promotion_rule": "K_CMSM remains missing until parser extracts reviewed numeric arrays with units",
            "current_status": "CONTRACT_WRITTEN",
            "claim_allowed": False,
        },
    ]


def runner_rows(parsed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    has_candidate = any(row.get("parse_status") == "CANDIDATE_ROW_NEEDS_REVIEW" for row in parsed)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1599_0_parser",
            "acceptance_rule": "parse HAR/JSON/CSV filelist evidence into quarantine candidate rows",
            "input_state": "candidate rows present" if has_candidate else "no parseable official filelist input",
            "runner_result": "PARSED_CANDIDATES_NEED_REVIEW" if has_candidate else "NO_FILELIST_PARSED",
            "effect": "no claim or live import",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1599_1_symbolic_K",
            "acceptance_rule": "symbolic bridge may define required K components but cannot evaluate tau_WEP",
            "input_state": "symbolic K bridge written; numeric arrays absent",
            "runner_result": "ACCEPT_SYMBOLIC_BRIDGE_ONLY",
            "effect": "keeps K_CMSM missing but better specified",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1599_2_alignment",
            "acceptance_rule": "tau_min requires official projection or parent nondegeneracy theorem",
            "input_state": "alignment object still missing",
            "runner_result": "REJECT_TAU_MIN_CLAIM",
            "effect": "no Delta_w/WEP/local-GR score",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1599_0_filelist", "official CMSM file list imported", "no reviewed filelist/download/checksum/schema yet"),
        ("CG1599_1_K", "official K_CMSM extracted", "numeric readout arrays absent"),
        ("CG1599_2_tau", "tau_WEP or tau_min computed", "alignment object absent"),
        ("CG1599_3_WEP", "MTS passes MICROSCOPE/WEP", "product-bound only"),
        ("CG1599_4_local_GR", "derived local GR branch", "readout/coupling residual remains open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "BLOCKED",
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows(parsed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    has_candidate = any(row.get("parse_status") == "CANDIDATE_ROW_NEEDS_REVIEW" for row in parsed)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1599_0_parser_status",
            "decision": "PARSER_READY_NO_REVIEWED_IMPORT" if not has_candidate else "PARSER_FOUND_CANDIDATES_NEED_REVIEW",
            "reason": "no official input files are present yet" if not has_candidate else "candidate rows require checksum/schema review",
            "next_action": "attach/export official CMSM HAR/filelist evidence or keep symbolic bridge route",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1599_1_symbolic_bridge",
            "decision": "SYMBOLIC_K_BRIDGE_WRITTEN",
            "reason": "K components are now named: EP gravity template, gravity-gradient corrections, masks/gaps/calibration, and alignment object",
            "next_action": "fill official numeric arrays or prove parent nondegeneracy for those components",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1599_2_next",
            "decision": "NEXT_1600_MICROSCOPE_HAR_INTAKE_OR_PARENT_K_VECTOR_PROOF",
            "reason": "we now have a parser target and a symbolic bridge; next work must either feed it evidence or prove the K-vector alignment theorem",
            "next_action": "attempt browser/HAR capture with app browser/VS Code route, or derive parent K-vector non-null theorem",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_HAR_intake_or_parent_K_vector_proof.py",
            "objective": "either ingest authenticated CMSM HAR/filelist evidence into the 1599 parser, or prove the parent K-vector non-null/alignment theorem",
            "success_condition": "reviewed filelist/checksum/schema rows or parent theorem forcing the branch source vector outside ker(K_CMSM)",
            "do_not": "do not claim WEP/local GR, do not promote unreviewed parser candidates, do not use tau_WEP=1",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    truthy = {"true", "1", "yes", "y"}
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "claim_allowed"):
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1599() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1599*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    inventory = read_csv(INPUT_INVENTORY)
    parsed = read_csv(PARSED_FILELIST)
    bridge = read_csv(SYMBOLIC_K_BRIDGE)
    contract = read_csv(PARSER_CONTRACT)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1599_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1599 local source paths exist"),
        ("VAL1599_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1599 source needles found"),
        ("VAL1599_2_input_inventory", bool(inventory), "input inventory written"),
        ("VAL1599_3_filelist_status", any(row["parse_status"] in {"NO_PARSEABLE_OFFICIAL_FILELIST", "CANDIDATE_ROW_NEEDS_REVIEW"} for row in parsed), "filelist parser produced quarantine status"),
        ("VAL1599_4_symbolic_K_bridge", any(row["bridge_id"] == "SKB1599_3_alignment_object" and row["current_status"] == "MISSING_CRITICAL_ALIGNMENT" for row in bridge), "symbolic K bridge includes alignment object"),
        ("VAL1599_5_parser_contract", any(row["contract_id"] == "CPC1599_2_K_extraction" for row in contract), "K extraction contract written"),
        ("VAL1599_6_runner_no_claim", any(row["runner_id"] == "RUN1599_2_alignment" and row["runner_result"] == "REJECT_TAU_MIN_CLAIM" for row in runner), "runner rejects tau_min claim"),
        ("VAL1599_7_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1599 claim gates remain closed"),
        ("VAL1599_8_decision_next", any(row["decision"] == "NEXT_1600_MICROSCOPE_HAR_INTAKE_OR_PARENT_K_VECTOR_PROOF" for row in decisions), "decision selects 1600 HAR intake or K-vector proof"),
        ("VAL1599_9_csv_parse", csv_parses(generated_csvs), "all generated 1599 CSVs parse"),
        ("VAL1599_10_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1599 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1599_11_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1599_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1599_13_formalization_untouched", no_formalization_1599(), "no 1599 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1599_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1599 CMSM capture parser or symbolic K bridge validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    parsed: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1599 - R2/fR CMSM Capture Parser Or Symbolic K Bridge",
                "## Verdict\n"
                "- 1599 creates a quarantine intake point for official CMSM HAR/JSON/CSV file-list evidence at `source-intake/microscope/quarantine/1599/input`.\n"
                "- No official CMSM input files are present yet, so no file list, checksum, download URL, or numeric `K_CMSM` array is imported.\n"
                "- The symbolic `K` bridge is now explicit: EP gravity template, gravity-gradient corrections, masks/gaps/calibration, and the alignment object all have named MTS `tau_WEP` slots.\n"
                "- The missing object remains the alignment/projection row `c_min` or a parent proof that the branch source vector is outside `ker(K_CMSM)`.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Input Inventory",
                md_table(inventory, ["input_id", "path", "file_type", "byte_count", "parse_status", "claim_impact"]),
                "## Parsed Filelist Candidate",
                md_table(parsed, ["row_id", "source_input", "file_name", "download_url", "checksum", "parse_status"]),
                "## Symbolic K Bridge",
                md_table(bridge, ["bridge_id", "published_component", "symbolic_object", "MTS_tau_slot", "required_numeric_inputs", "current_status"]),
                "## Parser Contract",
                md_table(contract, ["contract_id", "requirement", "promotion_rule", "current_status"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    inventory = input_inventory_rows()
    parsed = parsed_filelist_rows()
    bridge = symbolic_k_bridge_rows()
    contract = parser_contract_rows()
    runner = runner_rows(parsed)
    gates = claim_gate_rows()
    decisions = decision_rows(parsed)
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        INPUT_INVENTORY,
        PARSED_FILELIST,
        SYMBOLIC_K_BRIDGE,
        PARSER_CONTRACT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(INPUT_INVENTORY, inventory)
    write_csv(PARSED_FILELIST, parsed)
    write_csv(SYMBOLIC_K_BRIDGE, bridge)
    write_csv(PARSER_CONTRACT, contract)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, inventory, parsed, bridge, contract, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
