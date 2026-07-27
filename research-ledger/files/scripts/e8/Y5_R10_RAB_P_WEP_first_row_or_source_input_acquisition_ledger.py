from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
PRODUCT_ROOT = BRANCH_ROOT / "product"
GUARD_ROOT = BRANCH_ROOT / "guards"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
C_PARENT_FILE = COEFFICIENT_ROOT / "C_parent.csv"
C_PARENT_IMPORT_SCHEMA = COEFFICIENT_ROOT / "C_parent_import_schema.csv"
ETA_PRODUCT_CONVENTION = PRODUCT_ROOT / "eta_product_convention.csv"
MEASURED_G_GUARD = GUARD_ROOT / "measured_G_guard.csv"
FIRST_TARGET_1436 = RESIDUAL_ROOT / "first_projection_matrix_target.csv"
ROW_SCHEMA_1436 = RESIDUAL_ROOT / "projection_row_contract_schema.csv"

NEXT_1436 = OUT / "P8_Y5_R10_1436_NEXT_TARGET.csv"
CONTRACT_1436 = OUT / "P8_Y5_R10_1436_FIRST_TARGET_CONTRACT.csv"
REQUIRED_1436 = OUT / "P8_Y5_R10_1436_REQUIRED_SOURCE_ROWS.csv"
VALIDATION_1436 = OUT / "P8_Y5_BRR545_1436_VALIDATION.csv"
BOUND_SOURCES_871 = OUT / "P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv"
WEB_SOURCE_983 = OUT / "P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv"
WEP_INPUT_PACK_1080 = OUT / "P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv"
MATERIAL_1080 = OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv"
WEP_MATRIX_1053 = OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS / "local_bound_claims.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1437_SOURCE_REGISTER.csv"
P_WEP_ROW_ATTEMPT = OUT / "P8_Y5_R10_1437_P_WEP_ROW_ATTEMPT.csv"
INPUT_READINESS_AUDIT = OUT / "P8_Y5_R10_1437_INPUT_READINESS_AUDIT.csv"
SOURCE_ACQUISITION_LEDGER = OUT / "P8_Y5_R10_1437_SOURCE_ACQUISITION_LEDGER.csv"
BOUND_PROJECTION_SEPARATION = OUT / "P8_Y5_R10_1437_BOUND_VS_PROJECTION_SEPARATION.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1437_PROMOTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1437_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1437_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1437_VALIDATION.csv"

BRANCH_ROW_ATTEMPT = RESIDUAL_ROOT / "P_WEP_first_row_attempt.csv"
BRANCH_ACQUISITION_LEDGER = RESIDUAL_ROOT / "P_WEP_source_acquisition_ledger.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1437_0_1436_next", NEXT_1436, "NEXT1436_0_1437", "1436 handoff selecting P_WEP first-row attempt."),
        ("SRC1437_1_1436_validation", VALIDATION_1436, "VAL1436_11_overall", "1436 validation summary."),
        ("SRC1437_2_branch_id", BRANCH_ID_FILE, branch, "active same-parent branch lock."),
        ("SRC1437_3_1436_contract", CONTRACT_1436, "FTC1436_0_P_WEP_FIRST_ROW", "WEP first target contract."),
        ("SRC1437_4_1436_required", REQUIRED_1436, "REQ1436_6_official_sign_convention", "required-source rows from 1436."),
        ("SRC1437_5_branch_first_target", FIRST_TARGET_1436, "FTC1436_0_P_WEP_FIRST_ROW", "branch copy of selected WEP target."),
        ("SRC1437_6_branch_schema", ROW_SCHEMA_1436, "PRS1436_14", "branch copy of projection row schema."),
        ("SRC1437_7_c_parent", C_PARENT_FILE, "CP1430_6_verdict", "placeholder C_parent refusal rows."),
        ("SRC1437_8_c_parent_import_schema", C_PARENT_IMPORT_SCHEMA, "C_PARENT_IMPORT_SCHEMA_1431", "strict future coefficient import schema."),
        ("SRC1437_9_eta_product", ETA_PRODUCT_CONVENTION, "tau_eff = branch_locked_orbit_average", "eta product convention guard."),
        ("SRC1437_10_measured_g_guard", MEASURED_G_GUARD, "MGG1429_0_no_relative_absorption", "measured-G absorption guard."),
        ("SRC1437_11_bound_sources", BOUND_SOURCES_871, "SRC871_WEP_MICROSCOPE_FINAL", "MICROSCOPE WEP final source candidate."),
        ("SRC1437_12_web_sources", WEB_SOURCE_983, "WEB983_0_MICROSCOPE_CQG_COMPOSITION", "MICROSCOPE composition and eta source register."),
        ("SRC1437_13_finite_pack_1080", WEP_INPUT_PACK_1080, "FIP1080_0_product_formula", "older finite WEP input pack."),
        ("SRC1437_14_material_1080", MATERIAL_1080, "MAT1080_4_full_tensor_upgrade", "material composition/tensor candidate audit."),
        ("SRC1437_15_wep_matrix_1053", WEP_MATRIX_1053, "WCM1053_6", "WEP composition charge smoke matrix."),
        ("SRC1437_16_local_bound_claims", LOCAL_BOUND_CLAIMS, "MICROSCOPE_final_TiPt", "local WEP bound source row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def input_readiness_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        (
            "IRA1437_0_C_parent",
            "C_parent same-basis coupling vector or parent zero theorem",
            C_PARENT_FILE,
            "CP1430_6_verdict",
            "MISSING_PARENT_INPUT",
            "placeholder vector only; no theorem-zero or numeric coefficient",
            "BLOCKS_P_WEP_ROW",
        ),
        (
            "IRA1437_1_R_material",
            "full TA6V-minus-PtRh10 material response tensor in MTS parent basis",
            MATERIAL_1080,
            "MAT1080_4_full_tensor_upgrade",
            "PARTIAL_SMOKE_ONLY",
            "composition and two DD-smoke deltas exist, but full same-basis tensor is missing",
            "BLOCKS_P_WEP_ROW",
        ),
        (
            "IRA1437_2_R_source",
            "Earth/source worldtube vector in same parent basis",
            WEP_INPUT_PACK_1080,
            "FIP1080_2_R_source",
            "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "Earth source role is identified but no same-basis source vector exists",
            "BLOCKS_P_WEP_ROW",
        ),
        (
            "IRA1437_3_K_CMSM",
            "official or reproducibly derived MICROSCOPE readout/orbit kernel",
            WEP_INPUT_PACK_1080,
            "FIP1080_4_K_readout",
            "SURROGATE_ONLY_NONCLAIM",
            "readout candidate exists only as parked/surrogate route, not official arrays",
            "BLOCKS_P_WEP_ROW",
        ),
        (
            "IRA1437_4_sign_convention",
            "official Ti/Pt body order, sensitive-axis, and eta sign convention",
            WEB_SOURCE_983,
            "WEB983_1_MICROSCOPE_PRL_FINAL",
            "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "source candidate exists but the row is not extracted into branch convention",
            "BLOCKS_P_WEP_ROW",
        ),
        (
            "IRA1437_5_eta_product_guard",
            "branch eta product convention and no tau shortcut",
            ETA_PRODUCT_CONVENTION,
            "tau_eff = branch_locked_orbit_average",
            "GUARD_EXISTS_PENDING_OFFICIAL_DETAILS",
            "guard exists and blocks tau_eff=1 shortcut",
            "BLOCKS_UNTIL_OFFICIAL_DETAILS_FILLED",
        ),
        (
            "IRA1437_6_measured_G_guard",
            "guard forbidding relative residual absorption into measured G",
            MEASURED_G_GUARD,
            "MGG1429_0_no_relative_absorption",
            "GUARD_EXISTS",
            "relative Ti/Pt residual cannot be absorbed into common measured G",
            "PASS_GUARD_ONLY_NOT_A_PREDICTION",
        ),
        (
            "IRA1437_7_WEP_bound",
            "published MICROSCOPE eta_Ti_Pt bound/source row",
            BOUND_SOURCES_871,
            "SRC871_WEP_MICROSCOPE_FINAL",
            "BOUND_SOURCE_AVAILABLE_NONCLAIM",
            "external observable bound exists; MTS projection row does not",
            "BOUND_EXISTS_PROJECTION_MISSING",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "audit_id": audit_id,
            "required_input": required_input,
            "source_path": str(path),
            "path_exists": path.exists(),
            "anchor": anchor,
            "anchor_found": text_has(path, anchor),
            "readiness_status": status,
            "detail": detail,
            "effect": effect,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, required_input, path, anchor, status, detail, effect in rows
    ]


def p_wep_row_attempt_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "attempt_id": "PWA1437_0_first_row",
            "projection_matrix_id": "P_WEP_TRACE_TO_ETA_TIPT_1436",
            "observable": "eta_Ti_Pt",
            "symbolic_product": "eta_TiPt^MTS = sum_I C_parent^I * R_source_Earth,I * DeltaR_material_TA6V_minus_PtRh10,I * K_CMSM,I with eta_product_convention and measured_G_guard",
            "available_bound": "MICROSCOPE_final_eta_TiPt_source_candidate_available_nonclaim",
            "available_partial_inputs": "composition_context; DD-smoke material deltas; eta product guard; measured-G guard",
            "missing_blockers": "C_parent same-basis vector or zero theorem; full material tensor; Earth source vector; official K_CMSM/readout; extracted sign convention",
            "row_status": "REFUSED_FIRST_ROW_MISSING_INPUTS",
            "runner_effect": "WRITE_SOURCE_ACQUISITION_LEDGER_NOT_NUMERIC_SCORE",
            "source_path": str(DOC),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def source_acquisition_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ACQ1437_0_C_parent",
            "C_parent same-basis vector or WEP-slot zero theorem",
            "derive/import",
            "C_parent_import_schema.csv; parent action theorem route",
            "same_parent_branch_id; component; value or DERIVED_ZERO; uncertainty/exact tag; units; sign convention; basis; source_path; parent_status; zero_certificate_status",
            "HIGHEST",
            "without this, all WEP material/source/readout work is bound-only plumbing",
        ),
        (
            "ACQ1437_1_R_material_full_tensor",
            "full TA6V-minus-PtRh10 material response tensor",
            "source/build",
            "MICROSCOPE composition source plus parent-basis response model",
            "mass fractions; isotope/atomic inputs; response channels; parent-basis map; double-count rule; source paths",
            "HIGH",
            "existing DD-smoke deltas cannot be promoted as MTS parent tensor",
        ),
        (
            "ACQ1437_2_R_source_Earth",
            "Earth/source worldtube vector",
            "source/build",
            "Earth composition/geophysics candidate plus MICROSCOPE orbit/source role",
            "source basis; finite-size/worldtube averaging; orbit weighting; units; source paths",
            "HIGH",
            "no source vector means no differential source-normalized eta prediction",
        ),
        (
            "ACQ1437_3_K_CMSM_readout",
            "official or reproducibly derived MICROSCOPE readout/orbit kernel",
            "acquire/extract",
            "MICROSCOPE official readout arrays or reproducible reconstruction",
            "K_CMSM; time/orbit mask; body order; sensitive axis; session/run metadata; units",
            "HIGH",
            "tau_eff=1 and surrogate readout remain forbidden",
        ),
        (
            "ACQ1437_4_sign_convention",
            "official eta sign/body-axis convention",
            "extract",
            "MICROSCOPE final PRL/CQG source candidate",
            "eta formula; Ti/Pt order; sensitive-axis sign; coordinate/readout convention",
            "HIGH",
            "wrong sign/body order would make any comparison meaningless",
        ),
        (
            "ACQ1437_5_eta_bound_row",
            "published eta_TiPt bound row",
            "already_source_candidate",
            "SRC871_WEP_MICROSCOPE_FINAL; local_bound_claims.csv",
            "measured value; statistical/systematic uncertainty; bound convention; DOI/source URL",
            "MEDIUM",
            "bound exists but cannot stand in for the MTS projection",
        ),
        (
            "ACQ1437_6_guard_rows",
            "eta product and measured-G guards",
            "already_local_guard_needs_official_completion",
            "eta_product_convention.csv; measured_G_guard.csv",
            "official product details; no relative measured-G absorption rule",
            "MEDIUM",
            "guards are necessary but not prediction rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "acquisition_id": acquisition_id,
            "needed_input": needed_input,
            "route": route,
            "candidate_source_or_route": candidate_source_or_route,
            "required_fields": required_fields,
            "priority": priority,
            "why_it_matters": why_it_matters,
            "status": "OPEN_NOT_SCORE_READY",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, needed_input, route, candidate_source_or_route, required_fields, priority, why_it_matters in specs
    ]


def bound_projection_separation_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "separation_id": "BPS1437_0_bound_exists",
            "item": "MICROSCOPE eta_TiPt bound",
            "status": "AVAILABLE_AS_EXTERNAL_BOUND_NONCLAIM",
            "meaning": "the experiment constrains WEP violation at the eta_TiPt level",
            "not_meaning": "does not provide an MTS prediction for eta_TiPt",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "separation_id": "BPS1437_1_projection_missing",
            "item": "P_WEP MTS projection",
            "status": "MISSING_INPUTS",
            "meaning": "the formula shape is known but same-basis coefficients/tensors/readout are absent",
            "not_meaning": "cannot compare MTS to MICROSCOPE yet",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def promotion_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE1437_0_parent", "C_parent must be DERIVED_ZERO or source-backed numeric in the exact branch basis."),
        ("GATE1437_1_material", "R_material must be full same-basis tensor, not two DD-smoke components."),
        ("GATE1437_2_source", "R_source must be Earth/worldtube same-basis source vector."),
        ("GATE1437_3_readout", "K_CMSM/readout must be official or reproducibly derived; tau_eff=1 remains forbidden."),
        ("GATE1437_4_sign", "eta body order and sensitive-axis sign must be extracted before comparison."),
        ("GATE1437_5_measured_G", "relative Ti/Pt residual cannot be absorbed into measured G."),
        ("GATE1437_6_no_bound_as_prediction", "MICROSCOPE bound cannot be used as MTS prediction."),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1437_0_first_row_refused",
            "decision": "refuse first numeric P_WEP row",
            "why": "the bound and some composition/smoke ingredients exist, but the same-basis parent coupling, source vector, material tensor, readout kernel, and sign convention are not complete",
            "consequence": "write source-acquisition ledger; no WEP/local-GR claim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1437_1_next_route",
            "decision": "prioritize C_parent WEP-slot zero/numeric source and official MICROSCOPE source-pack intake",
            "why": "C_parent is the physics bottleneck; official readout/material/source/sign rows are the empirical bottleneck",
            "consequence": "next checkpoint should either close the WEP coupling slot or make the intake manifest executable",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1437_0_1438",
            "next_target": "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md",
            "script": "scripts/Y5_R10_RAB_WEP_slot_C_parent_zero_or_official_source_pack_intake.py",
            "objective": "try to close the WEP-specific C_parent slot as DERIVED_ZERO or source-backed numeric; if not possible, make the official MICROSCOPE source-pack intake manifest executable for material tensor, source worldtube, readout kernel, and sign convention.",
            "include": "C_parent WEP-slot theorem attempt; official source-pack manifest; acquisition statuses; anti-claim gates",
            "exclude": "numeric WEP pass; local-GR claim; bound-as-prediction substitution; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(row_attempt: list[dict[str, Any]], acquisition: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_ROW_ATTEMPT, row_attempt)
    write_csv(BRANCH_ACQUISITION_LEDGER, acquisition)


def validation_rows(
    sources: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    row_attempt: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    separation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        P_WEP_ROW_ATTEMPT,
        INPUT_READINESS_AUDIT,
        SOURCE_ACQUISITION_LEDGER,
        BOUND_PROJECTION_SEPARATION,
        PROMOTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_ROW_ATTEMPT,
        BRANCH_ACQUISITION_LEDGER,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    row_refused = (
        len(row_attempt) == 1
        and row_attempt[0]["row_status"] == "REFUSED_FIRST_ROW_MISSING_INPUTS"
        and row_attempt[0]["valid_prediction_row"] is False
    )
    hard_blockers_visible = {
        "MISSING_PARENT_INPUT",
        "PARTIAL_SMOKE_ONLY",
        "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
        "SURROGATE_ONLY_NONCLAIM",
        "SOURCE_CANDIDATE_NOT_EXTRACTED",
    }.issubset({row["readiness_status"] for row in readiness})
    acquisition_open = all(row["status"] == "OPEN_NOT_SCORE_READY" for row in acquisition)
    bound_separated = any(row["status"] == "AVAILABLE_AS_EXTERNAL_BOUND_NONCLAIM" for row in separation) and any(
        row["status"] == "MISSING_INPUTS" for row in separation
    )
    gates_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    branch_files_ok = BRANCH_ROW_ATTEMPT.exists() and BRANCH_ACQUISITION_LEDGER.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1437_0_source_register", sources_ok, "all 1437 cited source paths and anchors resolve"),
        ("VAL1437_1_first_row_refused", row_refused, "P_WEP first row is explicitly refused as missing-inputs"),
        ("VAL1437_2_hard_blockers_visible", hard_blockers_visible, "parent/material/source/readout/sign blockers are visible"),
        ("VAL1437_3_acquisition_open", acquisition_open, "all acquisition rows remain open and non-score-ready"),
        ("VAL1437_4_bound_projection_separated", bound_separated, "external MICROSCOPE bound is separated from MTS projection"),
        ("VAL1437_5_claim_gates", gates_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1437_6_csv_parse", parse_ok, "all generated 1437 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1437_7_branch_files", branch_files_ok, "branch-locked P_WEP attempt and acquisition ledger written"),
        ("VAL1437_8_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1437_9_next_target", True, "1438 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1437_10_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1437 refuses first P_WEP row and writes the WEP source-acquisition ledger without claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1437 - P_WEP first row or source-input acquisition ledger",
            "**Current verdict:** the first numeric `P_WEP` row is refused. The MICROSCOPE bound and partial material/composition rows exist, but the MTS same-basis projection ingredients are not complete.",
            "**Main progress:** the WEP coupling bottleneck is now split into explicit hard inputs: `C_parent`, full material tensor, Earth/source worldtube vector, official readout kernel, sign convention, product guard, and measured-G guard.",
            "## Source register\n" + md_table(sections["sources"]),
            "## P_WEP row attempt\n" + md_table(sections["row_attempt"]),
            "## Input readiness audit\n" + md_table(sections["readiness"]),
            "## Source acquisition ledger\n" + md_table(sections["acquisition"]),
            "## Bound versus projection separation\n" + md_table(sections["separation"]),
            "## Promotion gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    readiness = input_readiness_rows(branch)
    row_attempt = p_wep_row_attempt_rows(branch)
    acquisition = source_acquisition_rows(branch)
    separation = bound_projection_separation_rows(branch)
    gates = promotion_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(P_WEP_ROW_ATTEMPT, row_attempt)
    write_csv(INPUT_READINESS_AUDIT, readiness)
    write_csv(SOURCE_ACQUISITION_LEDGER, acquisition)
    write_csv(BOUND_PROJECTION_SEPARATION, separation)
    write_csv(PROMOTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(row_attempt, acquisition)

    validation = validation_rows(sources, readiness, row_attempt, acquisition, separation, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "row_attempt": row_attempt,
            "readiness": readiness,
            "acquisition": acquisition,
            "separation": separation,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1437_P_WEP_first_row_refused_source_acquisition_ledger_written_nonclaim")


if __name__ == "__main__":
    main()
