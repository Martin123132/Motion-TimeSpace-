from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
DOCS = RAB_SECTOR / "docs"
QUARANTINE = MICROSCOPE / "quarantine" / "1626"
INPUT_1626 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md"

SOURCE_FILES = {
    "1625_doc": ROOT / "1625-Y5-R2FR-finite-ZR-prior-row-builder-and-arena-projection-schema.md",
    "1625_validation": OUT / "P8_Y5_BRR545_1625_VALIDATION.csv",
    "1625_next": OUT / "P8_Y5_PARENT_QLOC_1625_NEXT_TARGET.csv",
    "1625_prior_builder": OUT / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv",
    "1625_arena_schema": OUT / "P8_Y5_PARENT_QLOC_1625_ARENA_PROJECTION_SCHEMA.csv",
    "1625_intake_template": OUT / "P8_Y5_PARENT_QLOC_1625_LIVE_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
    "1625_runner_gates": OUT / "P8_Y5_PARENT_QLOC_1625_RUNNER_REFUSAL_GATES.csv",
    "1625_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1625_CLAIM_GATE.csv",
    "1567_acquisition_queue": QUEUE / "ZR1567_LIVE_SOURCE_ACQUISITION_QUEUE_NONCLAIM.csv",
    "1568_external_bound": QUEUE / "ZR1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW_NONCLAIM.csv",
    "1569_external_metadata": QUEUE / "ZR1569_EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv",
    "04_vacuum_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
}

NEEDLES = {
    "1625_doc": ["FINITE_ZR_PRIOR_ROW_BUILDER_STAGED_NONCLAIM", "VAL1625_OVERALL"],
    "1625_validation": ["VAL1625_OVERALL", "PASS"],
    "1625_next": ["1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md", "accept none unless 1625 gates pass"],
    "1625_prior_builder": ["PB1625_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1625_arena_schema": ["AP1625_0_tau_R10", "MISSING_ARENA_PROJECTION"],
    "1625_intake_template": ["MISSING_LOCAL_SOURCE_PATH", "TEMPLATE_REJECTED_NONCLAIM"],
    "1625_runner_gates": ["DOCS_TEMPLATE_NOT_LIVE_INTAKE", "LOCAL_GR_CLAIM_BLOCKED"],
    "1625_claim_gate": ["CG1625_5_local_GR", "BLOCKED"],
    "1567_acquisition_queue": ["ACQ1567_1_ZR", "MISSING_ZR_THEOREM_OR_COEFFICIENT"],
    "1568_external_bound": ["external_arena_bound_only", "not an MTS Z_R/J_R/B_R/tau coefficient"],
    "1569_external_metadata": ["external_metadata_localized_nonclaim", "not a digitized bound curve and not an MTS tau_R10 projection"],
    "04_vacuum_contract": ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "J_R = 0 in local vacuum"],
    "05_reciprocity_attempt": ["d/dr [W(r) R_AB'] = J_R", "J_R = 0"],
    "06_source_neutrality": ["J_R = 0 -> W R_AB' = Q_R", "source neutrality"],
    "07_constraint": ["0.5 W (R_AB')^2 + J_R R_AB", "nonpropagating"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1626_SOURCE_REGISTER.csv"
LIVE_INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1626_LIVE_INTAKE_SCAN.csv"
CORPUS_SYMBOL_HUNT = OUT / "P8_Y5_PARENT_QLOC_1626_CORPUS_SYMBOL_HUNT.csv"
CANDIDATE_VALIDATION = OUT / "P8_Y5_PARENT_QLOC_1626_CANDIDATE_ROW_VALIDATION.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1626_BLOCKER_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1626_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1626_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1626_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1626_VALIDATION.csv"

COPY_TARGETS = {
    LIVE_INTAKE_SCAN: [
        QUARANTINE / "LIVE_INTAKE_SCAN.csv",
        BRANCH_RESIDUALS / "R2FR_live_intake_scan_1626.csv",
    ],
    CORPUS_SYMBOL_HUNT: [
        QUARANTINE / "CORPUS_SYMBOL_HUNT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_corpus_symbol_hunt_nonclaim_1626.csv",
    ],
    CANDIDATE_VALIDATION: [
        QUARANTINE / "CANDIDATE_ROW_VALIDATION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_candidate_row_validation_nonclaim_1626.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "BLOCKER_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_blocker_ledger_nonclaim_1626.csv",
        QUEUE / "ZR1626_BLOCKER_LEDGER_NONCLAIM.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1626.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1626.csv",
    ],
}

REQUIRED_LIVE_COLUMNS = {
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization_convention",
    "parent_action_block",
    "source_path",
    "source_anchor",
    "arena_projection",
    "evidence_type",
}
VALID_TARGET_SYMBOLS = {"Z_R", "M_R^2", "J_R", "B_R", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital"}
MISSING_MARKERS = ("MISSING", "TBD", "PLACEHOLDER", "TEMPLATE")
TEXT_SUFFIXES = {".md", ".csv", ".txt"}
MAX_FILE_BYTES = 1_000_000
_HUNT_CACHE: list[dict[str, Any]] | None = None

SYMBOL_PATTERNS = {
    "Z_R": re.compile(r"\bZ_R\b"),
    "M_R^2": re.compile(r"\bM_R\^2\b|\bM_R2\b|\bM_R²\b"),
    "J_R": re.compile(r"\bJ_R\b"),
    "B_R": re.compile(r"\bB_R\b"),
    "tau_R10": re.compile(r"\btau_R10\b"),
    "tau_PPN": re.compile(r"\btau_PPN\b"),
    "tau_clock": re.compile(r"\btau_clock\b"),
    "tau_orbital": re.compile(r"\btau_orbital\b"),
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def file_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    if path.stat().st_size > MAX_FILE_BYTES:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def all_needles_found(source_id: str) -> bool:
    text = file_text(SOURCE_FILES[source_id])
    return all(needle in text for needle in NEEDLES[source_id])


def ensure_dirs() -> None:
    for directory in [OUT, INPUT_1626, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE, DOCS]:
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
    except Exception:
        return False
    return True


def bool_str(value: Any) -> str:
    return str(value).strip().lower()


def row_has_true_claim_flag(row: dict[str, Any]) -> bool:
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]:
        if field in row and bool_str(row[field]) == "true":
            return True
    return False


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "source_path": rel(path),
            "exists": path.exists(),
            "required_needles": "; ".join(NEEDLES[source_id]),
            "needles_found": all_needles_found(source_id),
            "role": "1626 live source row validation and first prior hunt provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def csv_file_count(directory: Path) -> int:
    if not directory.exists():
        return 0
    return len([path for path in directory.glob("*.csv") if path.is_file()])


def live_intake_scan_rows() -> list[dict[str, Any]]:
    directories = [
        ("SCAN1626_0_raw", "raw", RAW, "LIVE_CANDIDATE_DIR"),
        ("SCAN1626_1_accepted", "accepted", ACCEPTED, "LIVE_ACCEPTED_DIR"),
        ("SCAN1626_2_acquisition_queue", "acquisition-queue", QUEUE, "QUEUE_NONCLAIM_NOT_ACCEPTED"),
        ("SCAN1626_3_docs", "docs", DOCS, "DOCS_TEMPLATE_NOT_LIVE"),
    ]
    rows = []
    for scan_id, label, directory, role in directories:
        csvs = sorted(path.name for path in directory.glob("*.csv")) if directory.exists() else []
        if label in {"raw", "accepted"} and not csvs:
            status = "NO_LIVE_ROWS_FOUND" if label == "raw" else "NO_ACCEPTED_ROWS_FOUND"
        elif label == "acquisition-queue":
            status = "QUEUE_ROWS_PRESENT_NONCLAIM"
        elif label == "docs":
            status = "DOCS_TEMPLATES_PRESENT_NONLIVE"
        else:
            status = "ROWS_PRESENT_REQUIRE_VALIDATION"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": label,
                "folder_path": rel(directory),
                "csv_count": len(csvs),
                "file_names": "; ".join(csvs[:20]),
                "status": status,
                "evidence_role": role,
                "accepted_live_rows": 0,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def candidate_file_type(path: Path) -> str:
    text_path = rel(path)
    if "\\raw\\" in str(path) or "/raw/" in text_path:
        return "raw_live_candidate"
    if "\\accepted\\" in str(path) or "/accepted/" in text_path:
        return "accepted_live_candidate"
    if "\\acquisition-queue\\" in str(path) or "/acquisition-queue/" in text_path:
        if "R10_alpha_lambda_bound" in path.name or "EXTERNAL_R10_BOUND" in path.name or "EXTERNAL_BOUND" in path.name:
            return "external_R10_bound_or_metadata_only"
        return "acquisition_queue_nonclaim"
    if "\\docs\\" in str(path) or "/docs/" in text_path:
        return "docs_template_not_live"
    if path.parent == ROOT and path.suffix.lower() == ".md":
        return "top_level_theory_note"
    if "\\mts_residuals\\" in str(path) or "/mts_residuals/" in text_path:
        return "historical_residual_schema_or_nonclaim"
    if "\\microscope\\" in str(path) or "/microscope/" in text_path:
        return "historical_quarantine_or_branch_copy"
    return "corpus_text_candidate"


def rejection_for_type(file_type: str, symbol: str, line: str) -> tuple[str, str]:
    if file_type in {"raw_live_candidate", "accepted_live_candidate"}:
        return "REQUIRES_ROW_VALIDATOR", "must satisfy 1625 required columns, no placeholders, local source path/anchor, units, normalization, and arena map"
    if file_type == "external_R10_bound_or_metadata_only":
        return "EXTERNAL_BOUND_ONLY_NOT_MTS_COEFFICIENT", "useful for tau_R10 comparison later, but it is not Z_R/M_R^2/J_R/B_R or an MTS projection kernel"
    if file_type == "docs_template_not_live":
        return "DOCS_TEMPLATE_NOT_LIVE_INTAKE", "docs rows are templates and remain invalid while MISSING/template markers remain"
    if file_type == "top_level_theory_note" and symbol == "J_R":
        return "THEORY_EQUATION_NOT_PARENT_SIGNED_SOURCE_ROW", "J_R equation is a strong clue, but lacks parent-signed matter descent, units, normalization, and arena projection"
    if file_type == "top_level_theory_note":
        return "THEORY_NOTE_NOT_LIVE_SOURCE_ROW", "corpus prose/equation mention is not a live coefficient row"
    if "MISSING" in line or "false" in line.lower():
        return "HISTORICAL_NONCLAIM_OR_PLACEHOLDER", "existing row advertises missing inputs or nonclaim status"
    return "UNPROMOTED_CORPUS_CANDIDATE", "symbol mention requires manual promotion into a validated live row before scoring"


def all_text_paths() -> list[Path]:
    candidate_paths: list[Path] = []
    candidate_paths.extend(ROOT.glob("*.md"))
    candidate_paths.extend(OUT.glob("*.csv"))
    for directory in [RAW, ACCEPTED, QUEUE, DOCS]:
        candidate_paths.extend(directory.glob("*.csv"))
    for directory in [
        MICROSCOPE / "branch_locked_wep" / "coefficients",
        MICROSCOPE / "branch_locked_wep" / "residuals",
    ]:
        if directory.exists():
            candidate_paths.extend(directory.glob("*.csv"))

    paths: list[Path] = []
    seen: set[Path] = set()
    for path in candidate_paths:
        if path in seen or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        seen.add(path)
        rel_path = rel(path)
        if "/1626" in rel_path or "\\1626" in str(path):
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            continue
        paths.append(path)
    return sorted(paths, key=lambda item: rel(item))


def candidate_score(path: Path, symbol: str, line: str) -> int:
    file_type = candidate_file_type(path)
    score = 0
    if file_type in {"raw_live_candidate", "accepted_live_candidate"}:
        score += 100
    if file_type == "top_level_theory_note":
        score += 70
    if file_type == "external_R10_bound_or_metadata_only" and symbol == "tau_R10":
        score += 60
    if file_type == "acquisition_queue_nonclaim":
        score += 45
    if file_type == "historical_residual_schema_or_nonclaim":
        score += 30
    if file_type == "docs_template_not_live":
        score += 10
    if "J_R = 0" in line or "J_R=0" in line:
        score += 20
    if "MISSING" in line or "TEMPLATE" in line:
        score -= 20
    if "False" in line or "false" in line:
        score -= 5
    return score


def corpus_symbol_hunt_rows() -> list[dict[str, Any]]:
    global _HUNT_CACHE
    if _HUNT_CACHE is not None:
        return _HUNT_CACHE
    text_paths = all_text_paths()
    hits_by_symbol: dict[str, list[tuple[int, Path, int, str]]] = {symbol: [] for symbol in SYMBOL_PATTERNS}
    files_by_symbol: dict[str, set[Path]] = {symbol: set() for symbol in SYMBOL_PATTERNS}
    for path in text_paths:
        text = file_text(path)
        if not text:
            continue
        present_symbols = [symbol for symbol, pattern in SYMBOL_PATTERNS.items() if pattern.search(text)]
        if not present_symbols:
            continue
        first_line_for_symbol: dict[str, tuple[int, str]] = {}
        for line_number, line in enumerate(text.splitlines(), start=1):
            for symbol in present_symbols:
                if symbol in first_line_for_symbol:
                    continue
                if SYMBOL_PATTERNS[symbol].search(line):
                    first_line_for_symbol[symbol] = (line_number, line.strip()[:260])
            if len(first_line_for_symbol) == len(present_symbols):
                break
        for symbol, (line_number, line) in first_line_for_symbol.items():
            files_by_symbol[symbol].add(path)
            hits_by_symbol[symbol].append((candidate_score(path, symbol, line), path, line_number, line))

    rows = []
    for symbol, pattern in SYMBOL_PATTERNS.items():
        hits = hits_by_symbol[symbol]
        if hits:
            hits.sort(key=lambda item: item[0], reverse=True)
            best_score, best_path, best_line, best_anchor = hits[0]
            file_type = candidate_file_type(best_path)
            status, missing = rejection_for_type(file_type, symbol, best_anchor)
            best_source_path = rel(best_path)
            best_source_anchor = best_anchor
            line_number = best_line
        else:
            best_score = 0
            file_type = "no_candidate_found"
            status = "NO_CORPUS_SYMBOL_HIT"
            missing = "need theorem-zero, numeric coefficient/prior interval, units, normalization, source path, source anchor, and arena projection"
            best_source_path = "NO_LOCAL_SOURCE_CANDIDATE"
            best_source_anchor = "NO_ANCHOR"
            line_number = 0
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "hunt_id": f"HUNT1626_{symbol.replace('^', '').replace('_', '').replace('tau', 'tau_')}",
                "target_symbol": symbol,
                "files_scanned": len(text_paths),
                "files_with_symbol_hits": len(files_by_symbol[symbol]) if hits else 0,
                "strongest_candidate_type": file_type,
                "strongest_candidate_path": best_source_path,
                "strongest_candidate_line": line_number,
                "strongest_candidate_anchor": best_source_anchor,
                "candidate_score": best_score,
                "validation_status": status,
                "missing_for_live_acceptance": missing,
                "accepted_as_live_row": False,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    _HUNT_CACHE = rows
    return rows


def read_csv_header(path: Path) -> tuple[list[str], int]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            return list(reader.fieldnames or []), len(rows)
    except Exception:
        return [], 0


def validate_file(path: Path, folder_role: str) -> dict[str, Any]:
    headers, row_count = read_csv_header(path)
    header_set = set(headers)
    missing_columns = sorted(REQUIRED_LIVE_COLUMNS - header_set)
    has_required_columns = not missing_columns
    text = file_text(path)
    contains_marker = any(marker in text for marker in MISSING_MARKERS)
    contains_true_claim = False
    contains_valid_symbol = False
    rows = []
    if headers:
        try:
            rows = read_csv(path)
        except Exception:
            rows = []
    for row in rows:
        if row.get("coefficient_symbol") in VALID_TARGET_SYMBOLS:
            contains_valid_symbol = True
        if row_has_true_claim_flag(row):
            contains_true_claim = True

    if folder_role == "docs":
        status = "REJECT_DOCS_TEMPLATE_NOT_LIVE"
        reason = "docs rows are templates and cannot be accepted as live evidence"
    elif folder_role == "acquisition-queue":
        status = "REJECT_QUEUE_ROW_NOT_ACCEPTED_LIVE_INPUT"
        reason = "queue rows are candidate/acquisition notes, not accepted live coefficient rows"
    elif not has_required_columns:
        status = "REJECT_MISSING_REQUIRED_COLUMNS"
        reason = "missing required live columns: " + ";".join(missing_columns)
    elif contains_marker:
        status = "REJECT_PLACEHOLDER_MARKER_PRESENT"
        reason = "row contains MISSING/TBD/PLACEHOLDER/TEMPLATE markers"
    elif contains_true_claim:
        status = "REJECT_CLAIM_FLAG_TRUE"
        reason = "private source rows cannot set score/claim flags true"
    elif not contains_valid_symbol:
        status = "REJECT_NO_TARGET_SYMBOL"
        reason = "row does not target Z_R, M_R^2, J_R, B_R, or tau arena symbols"
    else:
        status = "LIVE_ROW_NEEDS_SOURCE_PATH_ANCHOR_AUDIT"
        reason = "basic schema present; source path/anchor and arena map still need row-level validation"

    accepted = status == "LIVE_ROW_NEEDS_SOURCE_PATH_ANCHOR_AUDIT" and folder_role in {"raw", "accepted"}
    return {
        "same_parent_branch_id": BRANCH_ID,
        "validation_id": f"VALROW1626_{folder_role}_{path.stem[:60]}",
        "folder_role": folder_role,
        "file_path": rel(path),
        "row_count": row_count,
        "has_required_columns": has_required_columns,
        "missing_required_columns": ";".join(missing_columns),
        "contains_placeholder_marker": contains_marker,
        "contains_true_claim_flag": contains_true_claim,
        "contains_valid_target_symbol": contains_valid_symbol,
        "validation_status": status,
        "rejection_or_next_step": reason,
        "accepted_as_live_row": accepted,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def candidate_validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for folder_role, directory in [("raw", RAW), ("accepted", ACCEPTED), ("acquisition-queue", QUEUE), ("docs", DOCS)]:
        for path in sorted(directory.glob("*.csv")):
            rows.append(validate_file(path, folder_role))
    if not rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "validation_id": "VALROW1626_0_no_files",
                "folder_role": "all",
                "file_path": "NO_CSV_FILES_FOUND",
                "row_count": 0,
                "has_required_columns": False,
                "missing_required_columns": ";".join(sorted(REQUIRED_LIVE_COLUMNS)),
                "contains_placeholder_marker": False,
                "contains_true_claim_flag": False,
                "contains_valid_target_symbol": False,
                "validation_status": "NO_ROWS_TO_VALIDATE",
                "rejection_or_next_step": "place candidate rows under raw first, then promote to accepted only after validation",
                "accepted_as_live_row": False,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, Any]]:
    hunt_by_symbol = {row["target_symbol"]: row for row in corpus_symbol_hunt_rows()}
    blockers = [
        (
            "BLK1626_0_ZR",
            "Z_R",
            "kinetic residue / vertical-gradient coefficient",
            "MISSING_ZR_THEOREM_OR_COEFFICIENT",
            "need parent-signed theorem-zero or finite coefficient/prior interval with units and normalization",
            "try parent action second-variation coefficient extraction only after object-language owner is fixed",
        ),
        (
            "BLK1626_1_MR2",
            "M_R^2",
            "mass gap / screening range owner",
            "MISSING_MR2_SOURCE",
            "need Hessian/mass-gap or range scale tied to the same R_AB normalization",
            "do not invent ell_R; extract M_R^2 or write explicit range-prior assumption",
        ),
        (
            "BLK1626_2_JR",
            "J_R",
            "matter/source current coupling",
            "J_R_EQUATION_FOUND_BUT_NOT_PARENT_SIGNED",
            "top-level notes contain J_R=0/local-vacuum equations, but not parent-signed matter descent with units/arena map",
            "best next target: prove J_R=0 from matter descent or stage first finite J_R row",
        ),
        (
            "BLK1626_3_BR",
            "B_R",
            "boundary/defect/readout tail",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "need boundary no-flux theorem or finite boundary-tail coefficient with falloff convention",
            "defer until J_R and parent source-owner route is clearer",
        ),
        (
            "BLK1626_4_tau_R10",
            "tau_R10",
            "R10 alpha(lambda) projection",
            "R10_BOUND_EXISTS_BUT_MTS_PROJECTION_MISSING",
            "external alpha(lambda) bound candidates exist, but no MTS coefficient-to-alpha projection kernel is sourced",
            "after J_R/Z_R row exists, build tau_R10 kernel and compare to reviewed bound curve",
        ),
        (
            "BLK1626_5_tau_PPN",
            "tau_PPN",
            "PPN/local-GR projection",
            "MISSING_PPN_PROJECTION_KERNEL",
            "need weak-field metric response from finite R_AB residuals to gamma/beta/preferred-frame vector",
            "use only after coefficient rows are live or theorem-zero closes",
        ),
        (
            "BLK1626_6_tau_clock",
            "tau_clock",
            "clock/time-drift projection",
            "MISSING_CLOCK_PROJECTION_KERNEL",
            "need clock-readout coupling and bounds with units",
            "defer until matter/source descent identifies clock coupling owner",
        ),
        (
            "BLK1626_7_tau_orbital",
            "tau_orbital",
            "orbital/ephemeris projection",
            "MISSING_ORBITAL_PROJECTION_KERNEL",
            "need orbital response kernel and local source-support map",
            "defer until J_R/source support route is clear",
        ),
        (
            "BLK1626_8_live_intake",
            "raw/accepted",
            "live source row intake",
            "NO_RAW_OR_ACCEPTED_LIVE_ROWS",
            "raw and accepted R_AB intake folders currently contain zero live CSV rows",
            "first live row must be placed in raw and pass 1625 gates before accepted promotion",
        ),
    ]
    rows = []
    for blocker_id, symbol, role, status, missing, next_action in blockers:
        hunt = hunt_by_symbol.get(symbol, {})
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "blocker_id": blocker_id,
                "target": symbol,
                "role": role,
                "status": status,
                "strongest_candidate_path": hunt.get("strongest_candidate_path", "NOT_APPLICABLE"),
                "strongest_candidate_anchor": hunt.get("strongest_candidate_anchor", "NOT_APPLICABLE"),
                "missing_for_claim": missing,
                "next_action": next_action,
                "accepted_as_live_row": False,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1626_0_live_rows", "any finite Z_R branch live row accepted", "BLOCKED", "raw/accepted intake has no accepted live source rows"),
        ("CG1626_1_ZR_MR2_JR_BR", "coefficient set source-backed", "BLOCKED", "Z_R, M_R^2, J_R, and B_R remain missing or unpromoted"),
        ("CG1626_2_tau_R10", "R10 alpha(lambda) comparison", "BLOCKED", "external bound exists but MTS tau_R10 projection kernel is missing"),
        ("CG1626_3_PPN", "PPN/local-GR comparison", "BLOCKED", "tau_PPN projection missing"),
        ("CG1626_4_clock_orbital", "clock/orbital comparisons", "BLOCKED", "tau_clock and tau_orbital projections missing"),
        ("CG1626_5_local_GR", "derived local GR/Newton recovery", "BLOCKED", "no theorem-zero and no finite-prior arena branch has passed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "accepted_as_live_row": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1626_0_live_intake",
            "decision": "NO_LIVE_RAB_SOURCE_ROWS_ACCEPTED",
            "reason": "raw and accepted R_AB intake are empty; docs and acquisition queue remain nonclaim",
            "next_action": "do not score; build first live row only after source/theorem route is explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1626_1_bound_data",
            "decision": "R10_EXTERNAL_BOUND_MATERIAL_PRESENT_NOT_MTS_PROJECTION",
            "reason": "R10 alpha(lambda) bound candidates can support later comparison, but do not supply Z_R/J_R/B_R/tau_R10",
            "next_action": "keep external bound rows quarantined until tau_R10 kernel exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1626_2_best_prey",
            "decision": "J_R_ZERO_OR_FINITE_SOURCE_ROW_IS_BEST_NEXT_TARGET",
            "reason": "top-level theory notes already contain J_R equations and J_R=0 local-vacuum statements, so this is the closest route to closing the source coupling",
            "next_action": "try to promote J_R=0 into a parent-signed matter-descent theorem; if it fails, build first finite J_R row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1626_3_next",
            "decision": "NEXT_1627_JR_ZERO_SOURCE_THEOREM_OR_FIRST_FINITE_JR_ROW",
            "reason": "J_R is the coupling lever between local vacuum equations and real matter/source residuals",
            "next_action": "attack J_R before trying to score Z_R/tau projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md",
            "script": "scripts/Y5_R2FR_JR_zero_source_theorem_or_first_finite_JR_row.py",
            "objective": "try to derive J_R=0 from parent matter descent and local-vacuum source neutrality using the 04-07 reciprocity notes; if the theorem is not parent-signed, stage the first finite J_R source row contract with units, normalization, source path, and arena projections",
            "success_condition": "either J_R=0 becomes a parent-signed nonclaim theorem candidate with all premises listed, or a strict finite J_R row/acquisition blocker is created without scoring",
            "do_not": "do not treat local-vacuum prose as proof, do not score J_R placeholders, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        LIVE_INTAKE_SCAN,
        CORPUS_SYMBOL_HUNT,
        CANDIDATE_VALIDATION,
        BLOCKER_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source_id, source in SOURCE_FILES.items():
        if source.exists():
            target = INPUT_1626 / f"{source_id}{source.suffix}"
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    live_rows = read_csv(LIVE_INTAKE_SCAN)
    hunt_rows = read_csv(CORPUS_SYMBOL_HUNT)
    candidate_rows = read_csv(CANDIDATE_VALIDATION)
    blocker_rows_data = read_csv(BLOCKER_LEDGER)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_generated_rows: list[dict[str, Any]] = []
    for path in paths:
        all_generated_rows.extend(read_csv(path))

    raw_empty = any(row["folder_role"] == "raw" and row["csv_count"] == "0" and row["status"] == "NO_LIVE_ROWS_FOUND" for row in live_rows)
    accepted_empty = any(row["folder_role"] == "accepted" and row["csv_count"] == "0" and row["status"] == "NO_ACCEPTED_ROWS_FOUND" for row in live_rows)
    no_accepted_candidates = all(row["accepted_as_live_row"] == "False" for row in candidate_rows)
    jr_found = any(
        row["target_symbol"] == "J_R"
        and row["strongest_candidate_type"] == "top_level_theory_note"
        and row["validation_status"] == "THEORY_EQUATION_NOT_PARENT_SIGNED_SOURCE_ROW"
        for row in hunt_rows
    )
    r10_bound_rejected = any(
        row["folder_role"] == "acquisition-queue"
        and row["validation_status"] == "REJECT_QUEUE_ROW_NOT_ACCEPTED_LIVE_INPUT"
        and "R10_alpha_lambda_bound" in row["file_path"]
        for row in candidate_rows
    )
    blocker_targets = {row["target"] for row in blocker_rows_data}
    expected_blockers = {"Z_R", "M_R^2", "J_R", "B_R", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital", "raw/accepted"}
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_generated_rows)
    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1626_0_sources_exist", source_ok, "all cited 1626 local source paths exist"),
        ("VAL1626_1_needles_found", needles_ok, "all required 1626 source needles found"),
        ("VAL1626_2_raw_empty_recorded", raw_empty, "raw intake emptiness recorded"),
        ("VAL1626_3_accepted_empty_recorded", accepted_empty, "accepted intake emptiness recorded"),
        ("VAL1626_4_no_live_rows_accepted", no_accepted_candidates, "no candidate row accepted as live evidence"),
        ("VAL1626_5_jr_candidate_identified", jr_found, "J_R top-level theory-note candidate identified and rejected as not parent-signed"),
        ("VAL1626_6_r10_bound_rejected", r10_bound_rejected, "R10 bound rows rejected as queue/nonclaim rather than MTS coefficients"),
        ("VAL1626_7_blocker_coverage", blocker_targets == expected_blockers, "blocker ledger covers coefficients, arena projections, and live intake"),
        ("VAL1626_8_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1626_9_nonclaim_flags", nonclaim_ok, "all generated 1626 rows remain nonclaim/non-score-ready"),
        (
            "VAL1626_10_decision_next",
            "NEXT_1627_JR_ZERO_SOURCE_THEOREM_OR_FIRST_FINITE_JR_ROW" in decision_text,
            "decision selects J_R zero/source theorem or first finite J_R row next",
        ),
        (
            "VAL1626_11_next_target_selected",
            "1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md" in next_text,
            "next target selected",
        ),
        ("VAL1626_12_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1626_13_csv_parse", csv_ok, "all generated 1626 CSVs parse"),
        ("VAL1626_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1626_15_formalization_untouched", formalization_clean, "no 1626 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1626_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1626 finite Z_R live source row validator and first prior hunt validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    live_rows = read_csv(LIVE_INTAKE_SCAN)
    hunt_rows = read_csv(CORPUS_SYMBOL_HUNT)
    candidate_rows = read_csv(CANDIDATE_VALIDATION)
    blockers = read_csv(BLOCKER_LEDGER)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1626 — Finite `Z_R` Live Source Row Validator And First Prior Hunt

## Status

Private checkpoint. No local-GR/Newton, R10, PPN, clock, orbital, or finite-prior claim is made.

## Outcome

The live intake is empty: `source-intake/rab-sector/raw` and `source-intake/rab-sector/accepted` have no live coefficient rows. The acquisition queue contains useful R10 bound material, but it is external comparison data, not an MTS coefficient or projection kernel. The strongest internal clue is `J_R`: early local-vacuum notes contain `J_R=0` equations, but they are not parent-signed matter-descent theorems and cannot be promoted yet.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Live Intake Scan

{markdown_table(live_rows, ["scan_id", "folder_role", "csv_count", "status", "accepted_live_rows"])}

## Corpus Symbol Hunt

{markdown_table(hunt_rows, ["target_symbol", "files_with_symbol_hits", "strongest_candidate_type", "strongest_candidate_path", "strongest_candidate_line", "validation_status"])}

## Candidate Row Validation

{markdown_table(candidate_rows, ["folder_role", "file_path", "row_count", "validation_status", "accepted_as_live_row"])}

## Blocker Ledger

{markdown_table(blockers, ["blocker_id", "target", "status", "missing_for_claim", "next_action"])}

## Claim Gates

{markdown_table(claims, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        LIVE_INTAKE_SCAN: live_intake_scan_rows(),
        CORPUS_SYMBOL_HUNT: corpus_symbol_hunt_rows(),
        CANDIDATE_VALIDATION: candidate_validation_rows(),
        BLOCKER_LEDGER: blocker_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
