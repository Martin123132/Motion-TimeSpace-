from __future__ import annotations

import csv
import math
import re
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1205"
TITLE = "1205-Y5-R10-first-BT-or-epsP-source-row-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CORPUS_SCAN_PATH = OUT_DIR / f"{PACK_ID}_CORPUS_SCAN_CANDIDATES.csv"
SOURCE_FILL_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_FILL_ATTEMPT.csv"
BOUND_PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_BOUND_PRESSURE_TARGETS.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
COMPARISON_PATH = OUT_DIR / f"{PACK_ID}_COMPARISON_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1205_VALIDATION.csv"


KEYWORDS = [
    "b_t",
    "boundary_norm",
    "trace_pairing_bound",
    "k_t_normal",
    "p_locv",
    "delta_p",
    "projector_leakage",
    "eps_p",
    "c_ck",
    "c0 eps_p",
]
NUMERIC_FIELD_HINTS = [
    "b_t_norm",
    "boundary_norm",
    "trace_pairing_bound",
    "k_t_normal_trace_norm",
    "p_locv_trace_norm",
    "delta_p_norm",
    "projector_leakage_norm",
    "eps_p",
    "c_ck",
    "c_ck_eps_p",
]
NON_SOURCE_PACK_MARKERS = ["1203", "1204", "1205", "VALIDATION", "CLAIM_GATES", "NEXT_TARGET", "DECISION"]


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_float(value: object) -> float | None:
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", text):
        number = float(text)
        if math.isfinite(number):
            return number
    return None


def local_path_exists(value: object) -> bool:
    text = str(value).strip().strip('"')
    if not text or text.upper().startswith("MISSING"):
        return False
    candidate = Path(text)
    if candidate.is_absolute():
        return candidate.exists()
    return (ROOT / text).exists()


def row_has_real_source_path(row: dict[str, str]) -> bool:
    for key, value in row.items():
        key_lower = key.lower()
        if "source_path" in key_lower or key_lower.endswith("_path") or key_lower == "source_file":
            if local_path_exists(value):
                return True
    return False


def is_non_source_target_file(name: str) -> bool:
    upper = name.upper()
    return any(marker in upper for marker in NON_SOURCE_PACK_MARKERS)


def scan_candidate_csvs() -> list[dict[str, object]]:
    rows_out: list[dict[str, object]] = []
    for csv_path in sorted(OUT_DIR.glob("*.csv")):
        if csv_path == CORPUS_SCAN_PATH:
            continue
        try:
            rows = load_csv(csv_path)
        except Exception:  # noqa: BLE001
            continue
        keyword_rows = 0
        numeric_hint_cells: list[str] = []
        accepted_rows = 0
        missing_markers = 0
        examples: list[str] = []
        for row_index, row in enumerate(rows):
            line = ";".join(f"{key}={value}" for key, value in row.items()).lower()
            if "missing" in line or "source_ready" in line or "placeholder" in line:
                missing_markers += 1
            if not any(keyword in line for keyword in KEYWORDS):
                continue
            keyword_rows += 1
            if len(examples) < 2:
                first_value = next((str(value) for value in row.values() if str(value).strip()), "")
                examples.append(f"row{row_index}:{first_value[:90]}")
            row_numeric_values: list[float] = []
            for key, value in row.items():
                key_lower = key.lower()
                if any(hint in key_lower for hint in NUMERIC_FIELD_HINTS):
                    number = parse_float(value)
                    if number is not None and number >= 0:
                        row_numeric_values.append(number)
                        if len(numeric_hint_cells) < 6:
                            numeric_hint_cells.append(f"{key}={fmt(number)}")
            if row_numeric_values and row_has_real_source_path(row) and not is_non_source_target_file(csv_path.name):
                accepted_rows += 1
        if keyword_rows:
            rows_out.append(
                {
                    "scan_id": f"SCAN1205_{len(rows_out):03d}",
                    "file": rel(csv_path),
                    "row_count": len(rows),
                    "keyword_rows": keyword_rows,
                    "numeric_hint_cells": ";".join(numeric_hint_cells),
                    "missing_marker_rows": missing_markers,
                    "accepted_source_rows": accepted_rows,
                    "classification": "HAS_ACCEPTED_NUMERIC_SOURCE_ROW" if accepted_rows else ("TARGET_OR_TEMPLATE_ONLY" if is_non_source_target_file(csv_path.name) else "SYMBOLIC_OR_MISSING_INPUTS_ONLY"),
                    "example_rows": " | ".join(examples),
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return rows_out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1205_0_1204_next",
            "local_path": "1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound.md",
            "needle": "NEXT1204_0_1205",
            "purpose": "handoff requesting first B_T or eps_P source-row fill",
        },
        {
            "source_id": "SRC1205_1_1204_schemas",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1204_SOURCE_READY_BOUND_ROWS.csv",
            "needle": "SBR1204_3_projector_finite_bound",
            "purpose": "source-ready boundary/projector row schemas",
        },
        {
            "source_id": "SRC1205_2_1204_targets",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1204_BOUNDARY_PROJECTOR_FINITE_TARGETS.csv",
            "needle": "FBP1204_WR10F1202_2_brutal_100x_boundary_projector_split",
            "purpose": "finite target inequalities for B_T and Delta_P",
        },
        {
            "source_id": "SRC1205_3_1204_epsilon",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1204_PROJECTOR_EPSILON_TARGETS.csv",
            "needle": "EPT1204_WR10F1202_2_brutal_100x_G1",
            "purpose": "eps_P target grid for projector leakage",
        },
        {
            "source_id": "SRC1205_4_1171_bc_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1171_FIRST_FINITE_BC_BOUND_ROW.csv",
            "needle": "FBC1171_0_first_boundary_bound_row",
            "purpose": "older finite boundary-bound schema precedent",
        },
        {
            "source_id": "SRC1205_5_1172_bc_symbolic",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1172_BC_BOUND_FILLED_FROM_JC_SCHEMA.csv",
            "needle": "BCF1172_0_symbolic_bound",
            "purpose": "symbolic finite-bound route with numeric inputs missing",
        },
        {
            "source_id": "SRC1205_6_1175_projector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1175_PROJECTOR_LEAK_BOUND_ROWS.csv",
            "needle": "PLB1175_0_first_projector_leak_row",
            "purpose": "older projector leakage bound schema precedent",
        },
        {
            "source_id": "SRC1205_7_1197_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1197_COKERNEL_BOUND_INPUT_TEMPLATE.csv",
            "needle": "MISSING_B_T_BOUNDARY_NORM",
            "purpose": "R10/PPN/clock/orbital q_DT input template still missing B_T",
        },
    ]
    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    scan_rows = scan_candidate_csvs()
    accepted_source_row_count = sum(int(row["accepted_source_rows"]) for row in scan_rows)

    targets = load_csv(OUT_DIR / "P8_Y5_R10_1204_BOUNDARY_PROJECTOR_FINITE_TARGETS.csv")
    harsh_split = next(row for row in targets if row["target_id"] == "FBP1204_WR10F1202_2_brutal_100x_boundary_projector_split")
    harsh_boundary_only = next(row for row in targets if row["target_id"] == "FBP1204_WR10F1202_2_brutal_100x_boundary_only")
    harsh_projector_only = next(row for row in targets if row["target_id"] == "FBP1204_WR10F1202_2_brutal_100x_projector_only")
    q_split = float(harsh_split["q_boundary_max"])
    q_boundary_only = float(harsh_boundary_only["q_boundary_max"])
    q_projector_only = float(harsh_projector_only["q_projector_max"])

    source_fill_attempts = [
        {
            "attempt_id": "FILL1205_0_boundary_finite_BT",
            "component": "q_boundary=||B_T||",
            "candidate_source_status": "NO_ACCEPTED_NUMERIC_SOURCE_ROW_FOUND",
            "filled_value": "",
            "units": "dimensionless q_DT budget units after same-frame normalization",
            "source_path": "",
            "comparison_target": q_split,
            "target_context": "harsh W=100 boundary/projector equal split",
            "passes_target": False,
            "blocked_by": "missing K_T_normal_trace_norm;missing P_locV_trace_norm;missing trace_pairing_bound;missing source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FILL1205_1_projector_epsP",
            "component": "q_projector=||Delta_P|| or eps_P||G_res||",
            "candidate_source_status": "NO_ACCEPTED_NUMERIC_SOURCE_ROW_FOUND",
            "filled_value": "",
            "units": "dimensionless q_DT budget units after same-frame normalization",
            "source_path": "",
            "comparison_target": q_split,
            "target_context": "harsh W=100 boundary/projector equal split",
            "passes_target": False,
            "blocked_by": "missing Delta_P_norm;missing eps_P;missing G_res_norm;missing C_CK;missing C_CK_eps_P;missing source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_rows = [
        {
            "pressure_id": "PRS1205_0_boundary_only_trace_bound",
            "component": "q_boundary",
            "target_context": "harsh W=100, only q_boundary live",
            "required_bound": q_boundary_only,
            "factorized_condition": "||n.K_T||_{H-1/2} * ||P_loc V||_{H1/2} <= required_bound",
            "if_second_factor_normalized_to_1": q_boundary_only,
            "if_equal_factors_each_less_than": math.sqrt(q_boundary_only),
            "status": "TARGET_ONLY_NO_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PRS1205_1_boundary_split_trace_bound",
            "component": "q_boundary",
            "target_context": "harsh W=100, q_boundary/q_projector equal split",
            "required_bound": q_split,
            "factorized_condition": "||n.K_T||_{H-1/2} * ||P_loc V||_{H1/2} <= required_bound",
            "if_second_factor_normalized_to_1": q_split,
            "if_equal_factors_each_less_than": math.sqrt(q_split),
            "status": "TARGET_ONLY_NO_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PRS1205_2_projector_only_delta_bound",
            "component": "q_projector",
            "target_context": "harsh W=100, only q_projector live",
            "required_bound": q_projector_only,
            "factorized_condition": "||Delta_P|| <= required_bound",
            "if_second_factor_normalized_to_1": q_projector_only,
            "if_equal_factors_each_less_than": "",
            "status": "TARGET_ONLY_NO_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PRS1205_3_projector_split_eps_G1",
            "component": "eps_P",
            "target_context": "harsh W=100, q_projector split, assumed ||G_res||=1",
            "required_bound": q_split,
            "factorized_condition": "eps_P * ||G_res|| <= required_bound and C_CK*eps_P < 1",
            "if_second_factor_normalized_to_1": q_split,
            "if_equal_factors_each_less_than": "",
            "status": "TARGET_ONLY_NO_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    blocker_rows = [
        {
            "blocker_id": "BLK1205_0_boundary_missing_trace_norms",
            "component": "q_boundary",
            "missing_input": "K_T_normal_trace_norm and P_locV_trace_norm or direct trace_pairing_bound",
            "why_it_blocks": "1204 finite row can compare only after the boundary pairing bound is numeric in the same local norm",
            "best_derivation_route": "derive n_mu K_T^(mu nu)=0 from parent boundary action, or derive a trace estimate from a sourced K_T boundary equation",
            "fallback_source_route": "fill SBR1204_1 with boundary_geometry_path, K_T normal norm, P_locV trace norm, units, and source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1205_1_projector_missing_eps_constants",
            "component": "q_projector",
            "missing_input": "Delta_P_norm or eps_P, G_res_norm, C_CK, and C_CK_eps_P",
            "why_it_blocks": "projector absorption needs C_CK eps_P<1 and finite scoring needs eps_P||G_res|| below threshold",
            "best_derivation_route": "derive nabla P_loc=0/coframe lock/domain-motion silence from parent quotient geometry",
            "fallback_source_route": "fill SBR1204_3 with Delta_P_norm or eps_P*G_res_norm plus C_CK and source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1205_2_same_domain_guard",
            "component": "q_boundary and q_projector",
            "missing_input": "single parent-owned local domain/norm for boundary, projector, q_DT, and R10 readout",
            "why_it_blocks": "a boundary estimate in one domain cannot be combined with a projector estimate in another",
            "best_derivation_route": "define the local test domain and P_loc from the parent quotient map before numeric comparison",
            "fallback_source_route": "carry all rows as nonclaim until domain_id and norm_id match",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    comparison_rows = [
        {
            "comparison_id": "CMP1205_0_current_BT",
            "component": "q_boundary",
            "candidate_value": "MISSING",
            "target": q_split,
            "comparison_status": "BLOCKED_NO_NUMERIC_SOURCE_ROW",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1205_1_current_epsP",
            "component": "q_projector",
            "candidate_value": "MISSING",
            "target": q_split,
            "comparison_status": "BLOCKED_NO_NUMERIC_SOURCE_ROW",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1205_2_scan_verdict",
            "component": "corpus_scan",
            "candidate_value": accepted_source_row_count,
            "target": "at least one accepted source row",
            "comparison_status": "NO_ACCEPTED_SOURCE_ROWS_IN_SCAN" if accepted_source_row_count == 0 else "ACCEPTED_SOURCE_ROW_FOUND_REVIEW_REQUIRED",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1205_0_BT_source",
            "gate": "real numeric B_T finite-bound row",
            "status": "BLOCKED",
            "reason": "scan found symbolic templates/targets but no source-backed trace_pairing_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1205_1_epsP_source",
            "gate": "real numeric eps_P/C_CK/Delta_P row",
            "status": "BLOCKED",
            "reason": "scan found symbolic projector-leak rows/targets but no source-backed eps_P or Delta_P_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1205_2_no_fabrication",
            "gate": "no placeholder promoted",
            "status": "ACTIVE_GUARD",
            "reason": "1205 refuses to fill a numeric source row from target thresholds or symbolic formulas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1205_3_R10_local_GR",
            "gate": "R10/local-GR branch",
            "status": "BLOCKED",
            "reason": "boundary/projector components remain missing; R10/local-GR pass is not claimable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1205_0_verdict",
            "condition": "no accepted numeric source row found for B_T or eps_P/C_CK/Delta_P",
            "decision": "do not fill the component value; convert the attempt into a stricter blocker ledger plus pressure targets",
            "result": f"target remains q_boundary or q_projector <= {fmt(q_split)} for harsh equal split; accepted_source_rows={accepted_source_row_count}",
            "next_action": "derive the missing value from parent geometry rather than keep scanning: either K_T boundary trace law or P_loc/coframe leakage smallness",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_rows = [
        {
            "next_id": "NEXT1205_0_1206",
            "target_file": "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            "target_script": "scripts/Y5_R10_KT_boundary_trace_law_or_Ploc_leakage_smallness_derivation.py",
            "task": "derive one of the two missing numeric/source laws from parent geometry: either a K_T normal trace zero/bound or a P_loc leakage eps_P/C_CK smallness theorem",
            "success_condition": "one component gets a parent-derived zero theorem or a formula whose remaining inputs are lower-level geometric constants, not an undefined B_T/eps_P placeholder",
            "do_not_do": "do not rescan templates as evidence, do not claim R10/local-GR pass, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    scan_fields = ["scan_id", "file", "row_count", "keyword_rows", "numeric_hint_cells", "missing_marker_rows", "accepted_source_rows", "classification", "example_rows", "valid_for_claim", "claim_allowed"]
    fill_fields = ["attempt_id", "component", "candidate_source_status", "filled_value", "units", "source_path", "comparison_target", "target_context", "passes_target", "blocked_by", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["pressure_id", "component", "target_context", "required_bound", "factorized_condition", "if_second_factor_normalized_to_1", "if_equal_factors_each_less_than", "status", "valid_for_claim", "claim_allowed"]
    blocker_fields = ["blocker_id", "component", "missing_input", "why_it_blocks", "best_derivation_route", "fallback_source_route", "valid_for_claim", "claim_allowed"]
    comparison_fields = ["comparison_id", "component", "candidate_value", "target", "comparison_status", "claim_status", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(CORPUS_SCAN_PATH, scan_rows, scan_fields)
    write_csv(SOURCE_FILL_ATTEMPT_PATH, source_fill_attempts, fill_fields)
    write_csv(BOUND_PRESSURE_PATH, pressure_rows, pressure_fields)
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows, blocker_fields)
    write_csv(COMPARISON_PATH, comparison_rows, comparison_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(DECISION_LEDGER_PATH, decision_rows, decision_fields)
    write_csv(NEXT_TARGET_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        CORPUS_SCAN_PATH,
        SOURCE_FILL_ATTEMPT_PATH,
        BOUND_PRESSURE_PATH,
        BLOCKER_LEDGER_PATH,
        COMPARISON_PATH,
        CLAIM_GATES_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    scan_nonempty = len(scan_rows) > 0
    no_accepted_sources = accepted_source_row_count == 0
    fill_attempts_blocked = all(row["candidate_source_status"] == "NO_ACCEPTED_NUMERIC_SOURCE_ROW_FOUND" and not row["passes_target"] for row in source_fill_attempts)
    pressure_positive = all(float(row["required_bound"]) > 0 for row in pressure_rows)
    blockers_cover_components = {"q_boundary", "q_projector"}.issubset({row["component"] for row in blocker_rows})
    comparison_blocked = all("BLOCKED" in row["comparison_status"] or row["comparison_status"] == "NO_ACCEPTED_SOURCE_ROWS_IN_SCAN" for row in comparison_rows)
    claim_policy_ok = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in scan_rows + source_fill_attempts + pressure_rows + blocker_rows + comparison_rows + claim_gates
    )
    formalization_untouched = len(formalization_recent) == 0

    validation_rows = [
        validation_row("VAL1205_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1205_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1205_2_scan_nonempty", "corpus scan found candidate/template rows", scan_nonempty, f"scan_rows={len(scan_rows)}"),
        validation_row("VAL1205_3_no_accepted_sources", "no numeric source row is falsely accepted", no_accepted_sources, f"accepted_source_rows={accepted_source_row_count}"),
        validation_row("VAL1205_4_fill_attempts_blocked", "source-fill attempts remain blocked rather than fabricated", fill_attempts_blocked, f"attempt_rows={len(source_fill_attempts)}"),
        validation_row("VAL1205_5_pressure_positive", "pressure targets are positive", pressure_positive, f"pressure_rows={len(pressure_rows)}"),
        validation_row("VAL1205_6_blockers_cover_components", "blocker ledger covers boundary and projector", blockers_cover_components, ",".join(row["component"] for row in blocker_rows)),
        validation_row("VAL1205_7_comparison_blocked", "current comparison does not claim pass", comparison_blocked, ";".join(row["comparison_status"] for row in comparison_rows)),
        validation_row("VAL1205_8_nonclaim_policy", "all generated rows remain nonclaim", claim_policy_ok, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1205_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1205_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1205_11_overall",
            "overall 1205 validation",
            validation_pass,
            "1205 source-fill audit is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1205 Y5/R10 First B_T Or eps_P Source Row Fill

**Current verdict:** 1205 does not find an accepted numeric source row for either `||B_T||` or `eps_P/C_CK/Delta_P`. It therefore refuses to fill a fake value and converts the result into a stricter blocker ledger plus pressure targets.

**Main progress:** the corpus scan distinguishes templates/target thresholds from evidence rows. The harsh equal-split target remains `q_boundary <= {fmt(q_split)}` and `q_projector <= {fmt(q_split)}`, while the boundary trace product route requires `||n.K_T|| ||P_loc V|| <= {fmt(q_split)}`.

## Source Register

{markdown_table(source_rows, source_fields)}

## Corpus Scan Candidates

{markdown_table(scan_rows[:80], scan_fields)}

## Source Fill Attempt

{markdown_table(source_fill_attempts, fill_fields)}

## Bound Pressure Targets

{markdown_table(pressure_rows, pressure_fields)}

## Blocker Ledger

{markdown_table(blocker_rows, blocker_fields)}

## Comparison Ledger

{markdown_table(comparison_rows, comparison_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Decision Ledger

{markdown_table(decision_rows, decision_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"accepted_source_rows={accepted_source_row_count}")
    print(f"harsh_equal_split_target={fmt(q_split)}")


if __name__ == "__main__":
    main()
