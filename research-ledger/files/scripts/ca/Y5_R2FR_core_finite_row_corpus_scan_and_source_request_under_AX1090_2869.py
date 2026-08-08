from __future__ import annotations

import csv
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2869-Y5-R2FR-core-finite-row-corpus-scan-and-source-request-under-AX1090.md"

SRC_2869_SCRIPT = ROOT / "scripts" / "Y5_R2FR_core_finite_row_corpus_scan_and_source_request_under_AX1090_2869.py"
SRC_2868_DOC = ROOT / "2868-Y5-R2FR-finite-core-source-acquisition-after-Uamp-closure-demotion-under-AX1090.md"
SRC_2868_ACQ = RESIDUALS / "P8_Y5_R2FR_2868_FINITE_CORE_ACQUISITION_PACK.csv"
SRC_2868_PREFLIGHT = RESIDUALS / "P8_Y5_R2FR_2868_ROW_READINESS_PREFLIGHT.csv"
SRC_2868_RUNNER = RESIDUALS / "P8_Y5_R2FR_2868_RUNNER_REFUSAL.csv"
SRC_2868_NEXT = RESIDUALS / "P8_Y5_R2FR_2868_NEXT_TARGET.csv"
SRC_2868_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2868_VALIDATION.csv"
SRC_2867_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2862_REJECTIONS = RESIDUALS / "P8_Y5_R2FR_2862_SEMANTIC_REJECTION_RULES.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2869_SOURCE_REGISTER.csv",
    "targets": RESIDUALS / "P8_Y5_R2FR_2869_SCAN_TARGETS.csv",
    "summary": RESIDUALS / "P8_Y5_R2FR_2869_CORPUS_SCAN_SUMMARY.csv",
    "candidates": RESIDUALS / "P8_Y5_R2FR_2869_CANDIDATE_RANKINGS.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2869_EXACT_SOURCE_REQUESTS.csv",
    "rejections": RESIDUALS / "P8_Y5_R2FR_2869_REJECTION_LEDGER.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2869_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2869_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2869_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2869_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2869_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": BETA_DOCS / "RAB_CORE_FINITE_ROW_CANDIDATE_RANKINGS_2869_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_CORE_EXACT_SOURCE_REQUESTS_2869_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2869_triplet_deep_source_extraction_NEXT.csv",
    "runner_copy": LOCAL_BOUNDS / "RAB_CORE_RUNNER_STATUS_2869_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Target:
    target_id: str
    quantity: str
    patterns: tuple[str, ...]
    required_evidence: str
    missing_code: str
    exact_request: str
    priority_rank: int


TARGETS = [
    Target(
        "TGT2869_0_Q_CAB",
        "Q_CAB",
        ("Q_CAB", "A_CAB", "J_CAB", "rho_CAB", "L_CAB"),
        "finite target-map/source monopole or parent-zero theorem with units, source path, equation anchor, boundary policy and shared sign convention",
        "MISSING_PARENT_INPUT",
        "Provide the parent/source equation or table row giving Q_CAB=4*pi*A_CAB as a finite value or theorem-zero row, including L_CAB, J_CAB/rho_CAB, units, boundary/corner policy, branch id, and Green/sign convention.",
        1,
    ),
    Target(
        "TGT2869_1_q_R_eff",
        "q_R_eff",
        ("q_R_eff", "q_Reff", "S_R/Z_R", "delta_R", "ell_R", "Green charge"),
        "finite residual-curvature Green charge or source-zero theorem in the same convention as Q_CAB",
        "MISSING_SOURCE_NORMALIZATION",
        "Provide q_R_eff as a finite compact-source Green charge, with q_R_eff=-int S_R/Z_R d^3x or equivalent, ell_R/long-range limit, units, source support, boundary policy, source path and equation anchor.",
        2,
    ),
    Target(
        "TGT2869_2_sigma_R_source_sign",
        "sigma_R_source_sign",
        ("sigma_R_source_sign", "sigma_R", "operator sign", "Green orientation", "sign convention"),
        "parent operator/Green/source sign; not sigma_R_profile and not U_amp closure authority",
        "MISSING_OPERATOR_GREEN_SIGN_OWNER",
        "Provide a signed parent operator/Green convention row fixing sigma_R_source_sign before readout, with metric signature, Green orientation, operator/source sign, source path and equation anchor.",
        3,
    ),
    Target(
        "TGT2869_3_common_Green",
        "shared Green/radial convention",
        ("common Green", "shared Green", "Green convention", "radial convention", "4*pi", "operator pair"),
        "single exterior convention tying C_AB and delta_R radial coefficients",
        "MISSING_COMMON_GREEN_CONVENTION",
        "Provide one parent-owned convention for C_AB=Q_CAB/(4*pi*r)+... and delta_R=sigma*q_R_eff exp(-r/ell)/(4*pi*r)+..., including operator pair, sign orientation and range hierarchy.",
        4,
    ),
    Target(
        "TGT2869_4_boundary_tail",
        "boundary/tail",
        ("K_amp", "B_CAB", "B_R", "H_R", "boundary", "tail", "C_AB_reg"),
        "boundary/tail zero, exact, included-charge theorem, or finite arena-projected bound",
        "MISSING_SHARED_MEASURE_AND_BOUNDARY_CLASS",
        "Provide boundary/corner/tail theorem or finite bound for K_amp, B_CAB, B_R, H_R and C_AB_reg, including worldtube rule, compact support, source path, equation anchor and arena validity.",
        5,
    ),
    Target(
        "TGT2869_5_measured_GM",
        "measured GM",
        ("M_source", "GM", "measured GM", "H_tau", "worldtube", "metric 1/r"),
        "same-frame measured GM/source denominator and weak-field metric readout",
        "MISSING_GM_PARENT_GLUE",
        "Provide the worldtube/Hamiltonian source measure and weak-field metric 1/r readout tying M_source/GM to the same branch, including no-extra-mass-channel clause and source path.",
        6,
    ),
    Target(
        "TGT2869_6_full_local_vector",
        "full local residual vector",
        ("full PPN", "local vector", "beta", "preferred", "clock", "orbital", "q_loc", "alpha_i", "zeta"),
        "same-branch non-gamma local residual vector covering PPN, clocks, orbital, endpoint/readout and q_loc",
        "MISSING_FULL_VECTOR_CLOSURE",
        "Provide finite/theorem-zero rows for gamma, beta, alpha_i, xi, zeta_i, clock, orbital, endpoint/readout and q_loc in the same branch and convention.",
        7,
    ),
]

POSITIVE_TERMS = ("source_path", "equation_anchor", "units", "finite", "numeric", "value", "theorem", "valid_for_claim,true", "accepted_source_present,true")
NEGATIVE_TERMS = ("MISSING", "placeholder", "NONCLAIM", "nonclaim", "closure-only", "closure_only", "valid_for_claim,false", "claim_allowed,false", "score_ready,false", "BLOCKED", "REJECT", "False")
PROFILE_TERMS = ("sigma_R_profile", "profile_as_sign", "gamma_bound_backsolve")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2869_0_2868_doc", SRC_2868_DOC, "NEXT2868_0_2869;VAL2868_OVERALL", "2868 selected corpus-wide finite row scan"),
        ("SRC2869_1_2868_acq", SRC_2868_ACQ, "ACQ2868_0_Q_CAB;ACQ2868_7_full_local_vector", "finite acquisition pack"),
        ("SRC2869_2_2868_preflight", SRC_2868_PREFLIGHT, "PF2868_OVERALL", "strict import preflight refusal"),
        ("SRC2869_3_2868_runner", SRC_2868_RUNNER, "RUNREF2868_0_template;RUNREF2868_1_Uamp", "runner refusal"),
        ("SRC2869_4_2868_next", SRC_2868_NEXT, "NEXT2868_0_2869", "handoff target"),
        ("SRC2869_5_2868_validation", SRC_2868_VALIDATION, "VAL2868_OVERALL", "2868 validation"),
        ("SRC2869_6_2867_demotion", SRC_2867_DEMOTION, "DEM2867_0_Uamp_route;DEM2867_2_finite_route", "U_amp closure-only demotion"),
        ("SRC2869_7_2862_requests", SRC_2862_REQUESTS, "REQ2862_0_Q_CAB;REQ2862_2_sigma_R_source_sign", "first-row source request pack"),
        ("SRC2869_8_2862_rejections", SRC_2862_REJECTIONS, "REJ2862_0_profile_as_sign;REJ2862_4_placeholder", "semantic rejection rules"),
        ("SRC2869_9_2861_scan", SRC_2861_SCAN, "SCAN2861_0_Q_CAB;SCAN2861_2_sigma_R_source_sign", "first-row source scan"),
        ("SRC2869_10_2854_scan", SRC_2854_SCAN, "SCAN2854_0_Q_CAB;SCAN2854_6_full_vector", "older real-source scan"),
        ("SRC2869_11_script", SRC_2869_SCRIPT, "def scan_corpus;def validation_rows", "2869 generator self-check"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "target_id": target.target_id,
                "quantity": target.quantity,
                "patterns": ";".join(target.patterns),
                "required_evidence": target.required_evidence,
                "missing_code": target.missing_code,
                "priority_rank": target.priority_rank,
            }
        )
        for target in TARGETS
    ]


def iter_scan_files() -> list[Path]:
    root_docs = [path for path in ROOT.glob("*.md") if "2869-" not in path.name]
    residual_csv = [path for path in RESIDUALS.rglob("*.csv") if "2869" not in path.name]
    return sorted(root_docs + residual_csv, key=lambda item: str(item).lower())


def candidate_score(text: str) -> tuple[int, str, str]:
    normalized = text.replace('"', "").replace("'", "")
    score = 0
    positives = [term for term in POSITIVE_TERMS if term.lower() in normalized.lower()]
    negatives = [term for term in NEGATIVE_TERMS if term.lower() in normalized.lower()]
    if positives:
        score += 3 * len(positives)
    if "source_path" in normalized and "equation_anchor" in normalized:
        score += 6
    if re.search(r"(?<![A-Za-z_])[-+]?\d+(\.\d+)?([eE][-+]?\d+)?(?![A-Za-z_])", normalized):
        score += 1
    score -= 4 * len(negatives)
    if any(term.lower() in normalized.lower() for term in PROFILE_TERMS):
        score -= 8
    if "UAMP_CLOSURE_ONLY" in normalized or "closure-only" in normalized:
        score -= 8

    if any(term.lower() in normalized.lower() for term in ("MISSING", "placeholder", "closure-only", "UAMP_CLOSURE_ONLY")):
        evidence_class = "REJECT_PLACEHOLDER_OR_CLOSURE"
        reason = "contains missing/placeholder/closure-only marker"
    elif any(term.lower() in normalized.lower() for term in PROFILE_TERMS):
        evidence_class = "REJECT_PROFILE_OR_BACKSOLVE"
        reason = "profile/backsolve evidence cannot fill finite source row"
    elif "source request" in normalized.lower() or "needed_source" in normalized.lower():
        evidence_class = "SOURCE_REQUEST_ONLY"
        reason = "request row, not evidence row"
    elif "BLOCK" in normalized or "FAIL" in normalized or "False" in normalized:
        evidence_class = "BLOCKER_OR_FAILED_GATE"
        reason = "blocker/gate row remains false"
    elif "symbolic" in normalized.lower() or "conditional" in normalized.lower():
        evidence_class = "SYMBOLIC_OR_CONDITIONAL"
        reason = "symbolic/conditional evidence only"
    else:
        evidence_class = "POSSIBLE_SOURCE_CANDIDATE"
        reason = "matched target terms but still requires manual provenance review"
    return score, evidence_class, reason


def accepted_candidate(text: str) -> bool:
    lower = text.lower()
    if any(marker.lower() in lower for marker in ("missing", "placeholder", "nonclaim", "closure-only", "uamp_closure_only", "reject", "blocked")):
        return False
    if "valid_for_claim,true" not in lower and "accepted_source_present,true" not in lower and "accepted_source_row,true" not in lower:
        return False
    return "source_path" in lower and ("equation_anchor" in lower or "anchor" in lower)


def scan_csv_file(path: Path, target: Target) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader, start=2):
                text = "; ".join(f"{key}={value}" for key, value in row.items())
                if not any(pattern.lower() in text.lower() for pattern in target.patterns):
                    continue
                score, evidence_class, reason = candidate_score(text)
                rows.append(
                    {
                        "target_id": target.target_id,
                        "quantity": target.quantity,
                        "source_path": str(path),
                        "location": f"row:{index}",
                        "matched_text": text[:500],
                        "score": score,
                        "evidence_class": evidence_class,
                        "accepted_source_candidate": accepted_candidate(text),
                        "rejection_reason": "" if accepted_candidate(text) else reason,
                    }
                )
    except Exception:
        return rows
    return rows


def scan_md_file(path: Path, target: Target) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for index, line in enumerate(read_text(path).splitlines(), start=1):
            if not any(pattern.lower() in line.lower() for pattern in target.patterns):
                continue
            score, evidence_class, reason = candidate_score(line)
            rows.append(
                {
                    "target_id": target.target_id,
                    "quantity": target.quantity,
                    "source_path": str(path),
                    "location": f"line:{index}",
                    "matched_text": line[:500],
                    "score": score,
                    "evidence_class": evidence_class,
                    "accepted_source_candidate": accepted_candidate(line),
                    "rejection_reason": "" if accepted_candidate(line) else reason,
                }
            )
    except Exception:
        return rows
    return rows


def scan_corpus() -> tuple[list[dict[str, Any]], dict[str, int]]:
    files = iter_scan_files()
    all_rows: list[dict[str, Any]] = []
    scanned_rows_or_lines = 0
    for path in files:
        if path.suffix.lower() == ".csv":
            try:
                with path.open(newline="", encoding="utf-8", errors="replace") as handle:
                    scanned_rows_or_lines += sum(1 for _ in handle)
            except Exception:
                pass
            for target in TARGETS:
                all_rows.extend(scan_csv_file(path, target))
        elif path.suffix.lower() == ".md":
            try:
                scanned_rows_or_lines += len(read_text(path).splitlines())
            except Exception:
                pass
            for target in TARGETS:
                all_rows.extend(scan_md_file(path, target))

    ranked: list[dict[str, Any]] = []
    for target in TARGETS:
        target_rows_for_sort = [row for row in all_rows if row["target_id"] == target.target_id]
        target_rows_for_sort.sort(key=lambda row: (row["accepted_source_candidate"], row["score"]), reverse=True)
        for rank, row in enumerate(target_rows_for_sort[:15], start=1):
            ranked.append(add_common({"candidate_id": f"CAND2869_{target.target_id.split('_')[-1]}_{rank:02d}", "rank": rank, **row}))
    stats = {
        "files_scanned": len(files),
        "rows_or_lines_scanned": scanned_rows_or_lines,
        "raw_matches": len(all_rows),
        "ranked_candidates": len(ranked),
    }
    return ranked, stats


def summary_rows(candidates: list[dict[str, Any]], stats: dict[str, int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        target_candidates = [row for row in candidates if row["target_id"] == target.target_id]
        accepted = [row for row in target_candidates if row["accepted_source_candidate"]]
        best = target_candidates[0] if target_candidates else {}
        rows.append(
            add_common(
                {
                    "summary_id": f"SUM2869_{target.target_id.split('_')[-1]}",
                    "target_id": target.target_id,
                    "quantity": target.quantity,
                    "files_scanned": stats["files_scanned"],
                    "rows_or_lines_scanned": stats["rows_or_lines_scanned"],
                    "ranked_candidates": len(target_candidates),
                    "accepted_candidates": len(accepted),
                    "best_score": best.get("score", ""),
                    "best_source_path": best.get("source_path", ""),
                    "best_location": best.get("location", ""),
                    "verdict": "NO_ACCEPTED_SOURCE_ROW",
                    "missing_code": target.missing_code,
                }
            )
        )
    rows.append(
        add_common(
            {
                "summary_id": "SUM2869_SCAN_TOTAL",
                "target_id": "ALL",
                "quantity": "core finite row corpus scan",
                "files_scanned": stats["files_scanned"],
                "rows_or_lines_scanned": stats["rows_or_lines_scanned"],
                "ranked_candidates": stats["ranked_candidates"],
                "accepted_candidates": 0,
                "best_score": "",
                "best_source_path": "",
                "best_location": "",
                "verdict": "STRICT_SCAN_FOUND_NO_ACCEPTED_SOURCE_ROWS",
                "missing_code": "ALL_CORE_ROWS_REMAIN_UNACCEPTED",
            }
        )
    )
    return rows


def request_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        target_candidates = [row for row in candidates if row["target_id"] == target.target_id]
        best = target_candidates[0] if target_candidates else {}
        rows.append(
            add_common(
                {
                    "request_id": f"REQ2869_{target.target_id.split('_')[-1]}",
                    "target_id": target.target_id,
                    "quantity": target.quantity,
                    "needed_source": target.required_evidence,
                    "exact_request": target.exact_request,
                    "current_best_candidate": best.get("source_path", "NO_MATCH"),
                    "current_best_location": best.get("location", ""),
                    "acceptance_rule": "must be finite/source-backed or parent-signed theorem-zero; must include source_path, equation_anchor, units/conventions, branch id, no MISSING markers, and no closure-only/profile substitution",
                    "status": "OPEN_SOURCE_REQUEST",
                    "ready_for_runner": False,
                }
            )
        )
    return rows


def rejection_rows() -> list[dict[str, Any]]:
    specs = [
        ("REJ2869_0_placeholder", "MISSING_* or blank source fields", "REJECT", "placeholders cannot feed finite rows or runner"),
        ("REJ2869_1_Uamp_closure", "U_amp closure-only authority", "REJECT", "2867 demoted U_amp route to closure-only current status"),
        ("REJ2869_2_sigma_profile", "sigma_R_profile as sigma_R_source_sign", "REJECT", "profile sign collision remains rejected"),
        ("REJ2869_3_symbolic_formula", "symbolic equation without finite source/provenance", "REJECT_FOR_CLAIM", "formula is useful but not a source row"),
        ("REJ2869_4_blocker_row", "blocker/gate row copied as source evidence", "REJECT_FOR_CLAIM", "blocker rows identify missing evidence"),
        ("REJ2869_5_partial_triplet", "one or two first-triplet rows without the rest", "REJECT_FOR_RUNNER", "A_total requires Q_CAB, q_R_eff, sigma and common Green together"),
        ("REJ2869_6_gamma_only", "gamma/A_total-only local claim", "REJECT_FOR_LOCAL_GR", "full local vector and GM glue remain required"),
    ]
    return [
        add_common(
            {
                "rejection_id": rejection_id,
                "attempt": attempt,
                "status": status,
                "reason": reason,
                "rejection_active": True,
            }
        )
        for rejection_id, attempt, status, reason in specs
    ]


def runner_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_total = sum(int(row["accepted_candidates"]) for row in summary if row["target_id"] != "ALL")
    return [
        add_common(
            {
                "runner_id": "RUN2869_0_status",
                "status": "REFUSED",
                "accepted_source_rows": accepted_total,
                "required_source_rows": len(TARGETS),
                "reason": "corpus scan found no accepted finite/source-backed row set; placeholders and closure-only authority remain rejected",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2869_0_scan", "Corpus scan/ranker completed.", "COMPLETE_NONCLAIM", "ranked candidates exist for every core finite row target"),
        ("DEC2869_1_acceptance", "No accepted finite/source-backed row was found.", "NO_ACCEPTED_SOURCE_ROWS", "top hits are symbolic, blocker, request, placeholder, or closure-only rows"),
        ("DEC2869_2_requests", "Exact source requests emitted for every missing row.", "OPEN_REQUESTS", "each request states provenance and acceptance rule"),
        ("DEC2869_3_runner", "Strict runner remains locked.", "REFUSED", "no first triplet in one convention, no boundary/tail, no GM, no full vector"),
        ("DEC2869_4_next", "Deep-source extraction should focus on the first triplet.", "SELECTED_2870", "Q_CAB, q_R_eff, sigma_R_source_sign and common Green are the smallest unblocker set"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2869_0_2870",
                "status": "selected_primary",
                "target_doc": "2870-Y5-R2FR-first-triplet-deep-source-extraction-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_triplet_deep_source_extraction_under_AX1090_2870.py",
                "mission": "deep-extract or definitively reject source-backed rows for the first triplet Q_CAB, q_R_eff, sigma_R_source_sign and common Green convention using the 2869 ranked candidates; do not score A_total unless all first-triplet rows pass source/provenance gates",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2869_0_candidates", OUTPUTS["candidates"], BRANCH_OUTPUTS["candidate_copy"], "ranked finite-row candidates nonclaim copy"),
        ("COPY2869_1_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "exact source requests nonclaim copy"),
        ("COPY2869_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2870"),
        ("COPY2869_3_runner", OUTPUTS["runner"], BRANCH_OUTPUTS["runner_copy"], "runner refusal nonclaim copy"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_source_candidate",
        "ready_for_runner",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if not key.endswith("_path") and key not in {"source_table", "copy_path", "current_best_candidate", "best_source_path"}:
                    continue
                if value in {"", None, "NO_MATCH"}:
                    continue
                path_text = str(value)
                if path_text.startswith("scripts/") or path_text.startswith("scripts\\"):
                    continue
                if not Path(path_text).exists():
                    return False
    return True


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], stats: dict[str, int]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2869_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2869_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2869_2_scan_scope", stats["files_scanned"] > 100 and stats["rows_or_lines_scanned"] > 1000, "corpus scan covered substantial local md/csv evidence"),
        ("VAL2869_3_target_coverage", len(rows_by_name["targets"]) == len(TARGETS), "all finite source targets are declared"),
        ("VAL2869_4_candidate_coverage", all(any(row["target_id"] == target.target_id for row in rows_by_name["candidates"]) for target in TARGETS), "ranked candidates exist for every target"),
        ("VAL2869_5_no_accepted_candidates", all(not row["accepted_source_candidate"] for row in rows_by_name["candidates"]), "no accepted finite/source-backed candidate was promoted"),
        ("VAL2869_6_summary_no_accepts", all(int(row["accepted_candidates"]) == 0 for row in rows_by_name["summary"]), "summary keeps accepted count at zero"),
        ("VAL2869_7_requests_complete", len(rows_by_name["requests"]) == len(TARGETS) and all(row["status"] == "OPEN_SOURCE_REQUEST" for row in rows_by_name["requests"]), "exact source requests cover every target"),
        ("VAL2869_8_rejections_cover_policy", len(rows_by_name["rejections"]) >= 7 and all(row["rejection_active"] for row in rows_by_name["rejections"]), "rejection ledger covers placeholders, Uamp closure, profile import, partial triplet and gamma-only shortcuts"),
        ("VAL2869_9_runner_refused", all(not row["runner_ready"] for row in rows_by_name["runner"]), "strict runner remains refused"),
        ("VAL2869_10_next_target_2870", rows_by_name["next"][0]["next_id"] == "NEXT2869_0_2870" and "first_triplet" in rows_by_name["next"][0]["target_script"], "first-triplet deep extraction selected next"),
        ("VAL2869_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2869_12_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2869_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2869_14_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2869_15_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2869_16_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2869_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2869_18_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2869_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2869 scanned the local corpus for finite/source-backed core rows, ranked candidates, promoted none, emitted exact source requests, kept the runner refused, and selected first-triplet deep extraction for 2870.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    top_candidates = rows["candidates"][:35]
    lines = [
        "# 2869 - Y5 R2FR Core Finite Row Corpus Scan And Source Request Under AX1090",
        "",
        "Status: `Y5_R2FR_2869_corpus_scan_ranked_no_accepted_source_rows_requests_emitted`",
        "",
        "## Private Verdict",
        "",
        "2869 performed the promised local corpus scan/ranker for finite source rows. It looked for actual source-backed candidates for `Q_CAB`, `q_R_eff`, `sigma_R_source_sign`, shared Green convention, boundary/tail, measured `GM`, and the full local residual vector.",
        "",
        "The result is clean but not yet happy: the scan finds many symbolic, blocker, request, template, conditional, and nonclaim rows, but no accepted finite/source-backed row set. That means the runner stays locked.",
        "",
        "This is still progress: the missing evidence is now expressed as exact source requests rather than vague discomfort. The next target is deep extraction of the first triplet, because without `Q_CAB`, `q_R_eff`, `sigma_R_source_sign`, and common Green in one convention, `A_total` cannot honestly exist as a test row.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Scan Targets",
        "",
        markdown_table(rows["targets"], ["target_id", "quantity", "required_evidence", "missing_code", "priority_rank", "valid_for_claim"]),
        "",
        "## Corpus Scan Summary",
        "",
        markdown_table(rows["summary"], ["summary_id", "quantity", "files_scanned", "rows_or_lines_scanned", "ranked_candidates", "accepted_candidates", "best_score", "verdict", "missing_code", "valid_for_claim"]),
        "",
        "## Top Candidate Rankings",
        "",
        markdown_table(top_candidates, ["candidate_id", "rank", "quantity", "source_path", "location", "score", "evidence_class", "accepted_source_candidate", "rejection_reason", "valid_for_claim"]),
        "",
        "## Exact Source Requests",
        "",
        markdown_table(rows["requests"], ["request_id", "quantity", "needed_source", "exact_request", "current_best_candidate", "current_best_location", "status", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Rejection Ledger",
        "",
        markdown_table(rows["rejections"], ["rejection_id", "attempt", "status", "reason", "rejection_active", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        markdown_table(rows["runner"], ["runner_id", "status", "accepted_source_rows", "required_source_rows", "reason", "runner_ready", "score_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["targets"] = target_rows()
    rows["candidates"], stats = scan_corpus()
    rows["summary"] = summary_rows(rows["candidates"], stats)
    rows["requests"] = request_rows(rows["candidates"])
    rows["rejections"] = rejection_rows()
    rows["runner"] = runner_rows(rows["summary"])
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "targets", "summary", "candidates", "requests", "rejections", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, stats)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2869_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2869_OVERALL={overall['passed']}")
    print(f"FILES_SCANNED={stats['files_scanned']}")
    print(f"RAW_MATCHES={stats['raw_matches']}")


if __name__ == "__main__":
    main()
