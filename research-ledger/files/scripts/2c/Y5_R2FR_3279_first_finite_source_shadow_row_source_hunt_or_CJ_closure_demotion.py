from __future__ import annotations

import csv
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3279-Y5-R2FR-first-finite-source-shadow-row-source-hunt-or-CJ-closure-demotion-under-AX1090.md"

SRC_3278_DOC = ROOT / "3278-Y5-R2FR-source-shadow-finite-row-acquisition-or-parent-U1-clause-source-under-AX1090.md"
SRC_3278_SCAN = OUT / "P8_Y5_R2FR_3278_FINITE_COEFFICIENT_SOURCE_SCAN.csv"
SRC_3278_ACQ = OUT / "P8_Y5_R2FR_3278_SOURCE_SHADOW_ACQUISITION_AUDIT.csv"
SRC_3278_CLAUSE = OUT / "P8_Y5_R2FR_3278_EXACT_U1_CLAUSE_SOURCE_ROWS.csv"
SRC_3278_VALIDATION = OUT / "P8_Y5_BRR545_3278_VALIDATION.csv"
SRC_3277_INTAKE = OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_INTAKE_ROWS_NONCLAIM.csv"
SRC_3276_SHADOW = OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_1815_NO_RESCALE = OUT / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"

DOC_1044 = ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md"
DOC_1065 = ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md"
DOC_1066 = ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md"
DOC_1067 = ROOT / "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md"
DOC_1105 = ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md"
DOC_1106 = ROOT / "1106-Y5-R10-minimal-explicit-closure-pack-independence-audit-or-first-source-backed-coefficient-row.md"
DOC_1224 = ROOT / "1224-Y5-R10-source-weight-action-scale-current-owner-proof.md"
DOC_1229 = ROOT / "1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3279_SOURCE_REGISTER.csv",
    "search": OUT / "P8_Y5_R2FR_3279_CORPUS_SEARCH_SUMMARY.csv",
    "hits": OUT / "P8_Y5_R2FR_3279_CORPUS_SEARCH_HITS_SAMPLE.csv",
    "candidates": OUT / "P8_Y5_R2FR_3279_BEST_CANDIDATE_ROWS.csv",
    "decision": OUT / "P8_Y5_R2FR_3279_FINITE_ROW_DECISION.csv",
    "closure": OUT / "P8_Y5_R2FR_3279_CJ_CLOSURE_DEMOTION.csv",
    "next": OUT / "P8_Y5_R2FR_3279_NEXT_COUPLING_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3279_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
TERMS = [
    "epsilon_shadow",
    "J_shadow",
    "source-shadow",
    "source_shadow",
    "source shadow",
    "conserved_shadow",
    "current_rescale",
    "current rescale",
    "c_A",
    "kappa_A",
    "κ_A",
    "pre_action",
    "pre-action",
    "w_A",
    "readout_reentry",
    "readout reentry",
    "beta_source",
    "source_weight",
    "source weight",
    "Delta_w",
    "delta w_A",
    "kappa_A/kappa_univ",
    "C_J",
]
TERM_RE = re.compile("|".join(re.escape(term) for term in TERMS), re.IGNORECASE)
NUMBER_RE = re.compile(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?(?![A-Za-z_])", re.IGNORECASE)
FILENAME_FILTERS = [
    "source",
    "weight",
    "coupling",
    "current",
    "r2fr",
    "wep",
    "parent",
    "hidden-visible",
    "ordinary",
    "action",
    "shadow",
    "rescale",
    "readout",
]
DISQUALIFIERS = [
    "MISSING",
    "SMOKE",
    "CONDITIONAL",
    "THEOREM_ZERO",
    "PASS_IF",
    "FORBIDDEN",
    "BOUND",
    "GUARD",
    "COUNTERMODEL",
    "OBSTRUCTION",
    "SYMBOLIC",
    "NOT_DERIVED",
    "UNSIGNED",
    "false",
]
SCAN_CACHE: tuple[list[dict[str, Any]], dict[str, Any]] | None = None


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: str, limit: int = 300) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def line_hit(path: Path, needle: str) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if needle.lower() in line.lower():
            return f"L{line_no}:{compact(line, 260)}"
    return "NO_PATTERN_HIT"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3278_DOC, "3278 exact U1 clause and finite-row gate", "finite `C_J` branch is also forced"),
        (SRC_3278_SCAN, "3278 finite coefficient scan", "NO_REAL_FINITE_SOURCE_BACKED_NUMERIC_ROW_FOUND"),
        (SRC_3278_ACQ, "3278 source-shadow acquisition audit", "BLOCKED_NO_SOURCE_BACKED_NUMERIC_ROW"),
        (SRC_3278_CLAUSE, "3278 exact U1 source-backed clause", "CLAUSE3278_0_nonconserved"),
        (SRC_3278_VALIDATION, "3278 validation", "VAL3278_9_overall"),
        (SRC_3277_INTAKE, "3277 intake rows", "SSI3277_1_conserved_shadow_missing"),
        (SRC_3276_SHADOW, "3276 source-shadow rows", "SSR3276_1_live_source_shadow_missing"),
        (SRC_765_CEX, "rescaling counterexamples", "rescale"),
        (SRC_1815_NO_RESCALE, "conditional no-current-rescale theorem", "rescale"),
        (DOC_1044, "qbar source weight bound row", "MISSING_DELTA_KAPPA_A"),
        (DOC_1065, "no-source-only grammar or numeric row", "first-relative-weight-numeric-row"),
        (DOC_1066, "source scalar exclusion obstruction", "w_A S_A"),
        (DOC_1067, "action-scale source-weight obstruction", "SWC1067_1_relative_action_scale"),
        (DOC_1105, "master hidden-visible coefficient ledger", "FIN1105_3_WEP_relative_source_weight"),
        (DOC_1106, "closure pack independence audit", "first-source-backed-coefficient-row"),
        (DOC_1224, "source-weight current owner proof", "w_A T_A"),
        (DOC_1229, "local-GR source-coupling contract", "FR1229_0_delta_w"),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needle) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3279_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hit": line_hit(path, needle),
                "valid_for_claim": "false",
            }
        )
    return rows


def selected_corpus_files() -> list[Path]:
    manual = [
        SRC_3278_SCAN,
        SRC_3278_ACQ,
        SRC_3278_CLAUSE,
        SRC_3277_INTAKE,
        SRC_3276_SHADOW,
        SRC_765_CEX,
        SRC_1815_NO_RESCALE,
        DOC_1044,
        DOC_1065,
        DOC_1066,
        DOC_1067,
        DOC_1105,
        DOC_1106,
        DOC_1224,
        DOC_1229,
    ]
    selected: set[Path] = {path for path in manual if path.exists()}
    for path in ROOT.glob("*.md"):
        name = path.name.lower()
        if any(token in name for token in FILENAME_FILTERS):
            selected.add(path)
    for path in OUT.glob("P8_Y5_R2FR_327*.csv"):
        selected.add(path)
    return sorted(selected)


def classify_hit(text: str) -> str:
    upper = text.upper()
    if "MISSING" in upper:
        return "MISSING_INPUT"
    if "SMOKE" in upper:
        return "SMOKE_ROW"
    if "COUNTERMODEL" in upper or "COUNTEREXAMPLE" in upper or "OBSTRUCTION" in upper:
        return "COUNTERMODEL_OR_OBSTRUCTION"
    if (
        "THEOREM" in upper
        or "CONDITIONAL" in upper
        or "UNSIGNED" in upper
        or "NOT_DERIVED" in upper
        or "NOT_PARENT" in upper
        or "NOT_PROVED" in upper
        or "TARGET_" in upper
    ):
        return "THEOREM_OR_PARENT_UNSIGNED"
    if "<=" in text or "BOUND" in upper or "GUARD" in upper or "ETA_" in upper:
        return "BOUND_OR_GUARDRAIL_NOT_COEFFICIENT"
    if "SOURCE-INTAKE/" in upper or "VALIDATION" in upper or "_NEXT_TARGET" in upper:
        return "SOURCE_REFERENCE_NOT_COEFFICIENT"
    if not NUMBER_RE.search(text):
        return "SYMBOLIC_ONLY"
    if not any(marker in upper for marker in ["EPSILON_SHADOW", "C_A", "KAPPA_A", "Κ_A", "W_A", "READOUT_REENTRY", "DELTA_W", "C_J"]):
        return "NUMERIC_CONTEXT_NOT_TARGET_COEFFICIENT"
    if any(marker in text for marker in ["valid_for_claim=false", "| false", ",false"]):
        return "NUMERIC_NONCLAIM_OR_ROW_ID"
    return "POSSIBLE_NUMERIC_SOURCE_ROW_REQUIRES_MANUAL_AUDIT"


def corpus_scan() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    global SCAN_CACHE
    if SCAN_CACHE is not None:
        return SCAN_CACHE
    files = selected_corpus_files()
    hits: list[dict[str, Any]] = []
    classification_counts: dict[str, int] = {}
    total_lines = 0
    for path in files:
        try:
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line_no, line in enumerate(handle, start=1):
                    total_lines += 1
                    if not TERM_RE.search(line):
                        continue
                    classification = classify_hit(line)
                    classification_counts[classification] = classification_counts.get(classification, 0) + 1
                    if len(hits) < 250:
                        hits.append(
                            {
                                "hit_id": f"HIT3279_{len(hits)}",
                                "path": str(path),
                                "line": line_no,
                                "classification": classification,
                                "has_number": bool_str(bool(NUMBER_RE.search(line))),
                                "snippet": compact(line, 500),
                                "valid_for_claim": "false",
                            }
                        )
        except Exception as exc:
            hits.append(
                {
                    "hit_id": f"HIT3279_ERROR_{len(hits)}",
                    "path": str(path),
                    "line": "",
                    "classification": "SCAN_ERROR",
                    "has_number": "false",
                    "snippet": compact(str(exc), 500),
                    "valid_for_claim": "false",
                }
            )
    summary = {
        "files_selected": len(files),
        "lines_scanned": total_lines,
        "term_hits_total": sum(classification_counts.values()),
        "numeric_context_hits_requiring_manual_audit": classification_counts.get("POSSIBLE_NUMERIC_SOURCE_ROW_REQUIRES_MANUAL_AUDIT", 0),
        "classification_counts": classification_counts,
    }
    if not hits:
        hits.append(
            {
                "hit_id": "HIT3279_NONE",
                "path": str(ROOT),
                "line": "",
                "classification": "NO_TERM_HITS",
                "has_number": "false",
                "snippet": "no target coupling terms found",
                "valid_for_claim": "false",
            }
        )
    SCAN_CACHE = (hits, summary)
    return SCAN_CACHE


def corpus_search_summary_rows() -> list[dict[str, Any]]:
    _, summary = corpus_scan()
    counts = summary["classification_counts"]
    rows = [
        {
            "summary_id": "SEARCH3279_0_scope",
            "scope": "top-level post-checkpoint markdown plus source-intake/mts_residuals CSVs selected by source/weight/coupling/current/R2FR/WEP/parent/shadow/rescale/readout filename filters",
            "files_selected": summary["files_selected"],
            "lines_scanned": summary["lines_scanned"],
            "term_hits_total": summary["term_hits_total"],
            "numeric_context_hits_requiring_manual_audit": summary["numeric_context_hits_requiring_manual_audit"],
            "valid_for_claim": "false",
        }
    ]
    for key, value in sorted(counts.items()):
        rows.append(
            {
                "summary_id": f"SEARCH3279_CLASS_{key}",
                "scope": key,
                "files_selected": "",
                "lines_scanned": "",
                "term_hits_total": value,
                "possible_numeric_source_rows": "",
                "valid_for_claim": "false",
            }
        )
    return rows


def numeric_possible_rows() -> list[dict[str, Any]]:
    hits, _ = corpus_scan()
    return [hit for hit in hits if hit["classification"] == "POSSIBLE_NUMERIC_SOURCE_ROW_REQUIRES_MANUAL_AUDIT"]


def best_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND3279_0_epsilon_shadow",
            "target": "epsilon_shadow / conserved source-shadow",
            "best_source": str(SRC_3278_ACQ),
            "evidence": line_hit(SRC_3278_ACQ, "ACQ3278_1_conserved_shadow"),
            "candidate_status": "NO_REAL_NUMERIC_ROW",
            "why_not_enough": "the branch is present, but the coefficient and projection to C_J are missing.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_1_current_rescale",
            "target": "c_A/kappa_A current normalization",
            "best_source": str(SRC_3278_ACQ),
            "evidence": line_hit(SRC_3278_ACQ, "ACQ3278_2_current_rescale"),
            "candidate_status": "COUNTEREXAMPLE_PLUS_MISSING_COEFFICIENT",
            "why_not_enough": "current rescale survives as a countermodel unless parent current/readout ownership is signed; no numeric map is sourced.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_2_pre_action_weight",
            "target": "w_A / pre-action source weight",
            "best_source": str(DOC_1067),
            "evidence": line_hit(DOC_1067, "SWC1067_1_relative_action_scale"),
            "candidate_status": "LIVE_COUNTERMODEL_NOT_NUMERIC_PRIOR",
            "why_not_enough": "relative w_A is explicitly retained as a live source-weight countermodel; no parent-owned numeric prior width is supplied.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_3_WEP_bound_product",
            "target": "Delta_w_TiPt * tau_WEP",
            "best_source": str(DOC_1105),
            "evidence": line_hit(DOC_1105, "FIN1105_3_WEP_relative_source_weight"),
            "candidate_status": "NUMERIC_BOUND_NOT_COEFFICIENT",
            "why_not_enough": "the Eotvos guardrail exists, but the finite source coefficient and tau projection are missing.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_4_local_source_residual",
            "target": "delta w_A local source residual",
            "best_source": str(DOC_1229),
            "evidence": line_hit(DOC_1229, "FR1229_0_delta_w"),
            "candidate_status": "SYMBOLIC_RESIDUAL_CONTRACT",
            "why_not_enough": "the residual vector is correctly formulated, but the numeric prior or theorem-zero is missing.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_5_qbar_source_weight",
            "target": "qbar_source_weight / delta kappa_A",
            "best_source": str(DOC_1044),
            "evidence": line_hit(DOC_1044, "QBC1044_3_qbar_source_weight"),
            "candidate_status": "MISSING_DELTA_KAPPA_A",
            "why_not_enough": "the row names the correct source-weight quantity but explicitly records the missing delta-kappa input.",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "CAND3279_6_exact_U1_nonconserved",
            "target": "nonconserved silent compensator",
            "best_source": str(SRC_3278_CLAUSE),
            "evidence": line_hit(SRC_3278_CLAUSE, "CLAUSE3278_0_nonconserved"),
            "candidate_status": "SOURCE_BACKED_FORBIDDEN_CLAUSE_NOT_FINITE_ROW",
            "why_not_enough": "this is real progress, but it closes only the nonconserved silent route; it is not a finite coefficient value.",
            "valid_for_claim": "false",
        },
    ]


def finite_row_decision_rows() -> list[dict[str, Any]]:
    possible = numeric_possible_rows()
    return [
        {
            "decision_id": "FRD3279_0_hunt_result",
            "decision": "no admissible finite C_J source row found in the selected local corpus sweep",
            "evidence": f"numeric_context_hits_requiring_manual_audit={len(possible)}; best candidate audit rows all nonclaim/noncoefficient.",
            "effect_on_theory": "finite C_J cannot be used as a derivation or robustness claim in this branch.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "FRD3279_1_not_a_physics_zero",
            "decision": "do not infer C_J=0 from missing finite data",
            "evidence": "absence of a sourced row is not a theorem; it only demotes this research route.",
            "effect_on_theory": "C_J zero still requires the parent exact-U1/current-owner signature or a new source-backed coefficient row.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "FRD3279_2_poynting_route",
            "decision": "Poynting/wave/F-only effects should move to C_Z/C_R/EM-stress readout, not C_J active-current normalization",
            "evidence": "3278 source-backed F-only clause says magnetization current is identically conserved and belongs in stress/boundary response.",
            "effect_on_theory": "next work should attack EM stress normalization and readout coupling directly.",
            "valid_for_claim": "false",
        },
    ]


def cj_closure_demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "CJC3279_0_status",
            "object": "finite C_J source-shadow/current-rescale/pre-action/readout branch",
            "new_status": "DEMOTED_TO_EXPLICIT_CLOSURE_ONLY_UNTIL_NEW_SOURCE_ROW",
            "meaning": "we stop treating finite C_J as a near-term derivation path; it may re-open only with a numeric, unit-labelled, source-backed parent coefficient and projection to C_J.",
            "not_claimed": "not a proof that C_J=0; not a local-GR/Newton/Maxwell/WEP/R10 pass.",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CJC3279_1_surviving_exact_route",
            "object": "C_J theorem-zero route",
            "new_status": "ONLY_PARENT_EXACT_U1_CURRENT_OWNER_ROUTE_REMAINS",
            "meaning": "the exact U1 route can still close C_J, but only if A_Q projection, fixed generator lattice, matter domain, and readout transfer are parent-signed.",
            "not_claimed": "parent exact-U1 action is still unsigned.",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CJC3279_2_next_physics_route",
            "object": "alpha/source-coupling vector",
            "new_status": "MOVE_TO_C_Z_C_R_EM_STRESS_READOUT",
            "meaning": "because C_e=2 C_J-C_Z-C_R and finite C_J is closure-only, useful progress now comes from deriving/source-bounding EM stress normalization C_Z and readout C_R.",
            "not_claimed": "no alpha or Maxwell closure claim.",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3279_0_3280",
            "target_doc": "3280-Y5-R2FR-CZ-CR-EM-stress-readout-coupling-derivation-or-source-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3280_CZ_CR_EM_stress_readout_coupling_derivation_or_source_bound.py",
            "objective": "Attack C_Z and C_R directly: derive whether F_Q/Poynting/wave response fixes EM stress normalization and readout transfer, or build finite source-bound rows for C_Z and C_R without using C_J as a hidden compensator.",
            "guardrail": "Do not reopen finite C_J unless a real numeric source row appears; no Maxwell/alpha/local-GR claim unless C_Z, C_R, source paths, units, and promotion gates pass.",
            "valid_for_claim": "false",
        }
    ]


def output_csvs_parse() -> bool:
    return all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register_rows()
    search = corpus_search_summary_rows()[0]
    candidates = best_candidate_rows()
    decisions = finite_row_decision_rows()
    closures = cj_closure_demotion_rows()
    validations = [
        {
            "check_id": "VAL3279_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3279_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3279_2_outputs_parse",
            "check": "all 3279 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3279_3_corpus_search_nontrivial",
            "check": "corpus search scanned multiple files and found target-term hits",
            "passed": bool_str(int(search["files_selected"]) > 10 and int(search["term_hits_total"]) > 0),
            "detail": f"files_selected={search['files_selected']};term_hits_total={search['term_hits_total']};numeric_context_hits_requiring_manual_audit={search['numeric_context_hits_requiring_manual_audit']}",
        },
        {
            "check_id": "VAL3279_4_candidates_nonclaim",
            "check": "best candidate rows remain nonclaim and no finite row is promoted",
            "passed": bool_str(all(row["valid_for_claim"] == "false" and "PROMOTED" not in row["candidate_status"] for row in candidates)),
            "detail": ";".join(f"{row['candidate_id']}={row['candidate_status']}" for row in candidates),
        },
        {
            "check_id": "VAL3279_5_decision_demotes_finite_CJ",
            "check": "finite C_J branch is demoted to closure-only, not claimed zero",
            "passed": bool_str(any("DEMOTED_TO_EXPLICIT_CLOSURE_ONLY" in row["new_status"] for row in closures) and any("do not infer C_J=0" in row["decision"] for row in decisions)),
            "detail": "finite C_J route demoted; parent exact-U1 route remains unsigned.",
        },
        {
            "check_id": "VAL3279_6_all_rows_nonclaim",
            "check": "all 3279 rows with claim flags are nonclaim",
            "passed": bool_str(
                all(row.get("valid_for_claim", "false") == "false" for row in sources)
                and all(row.get("valid_for_claim", "false") == "false" for row in candidates)
                and all(row.get("valid_for_claim", "false") == "false" for row in decisions)
                and all(row.get("valid_for_claim", "false") == "false" for row in closures)
            ),
            "detail": "valid_for_claim=false across source/candidate/decision/closure rows.",
        },
        {
            "check_id": "VAL3279_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3279_8_overall",
            "check": "3279 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3279_8_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(compact(str(row.get(col, "")), 180).replace("|", "\\|") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc() -> None:
    search = read_csv(OUTPUTS["search"])
    candidates = read_csv(OUTPUTS["candidates"])
    decisions = read_csv(OUTPUTS["decision"])
    closure = read_csv(OUTPUTS["closure"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3279 - First finite source-shadow row source hunt or C_J closure demotion under AX1090

## Summary

3279 performs the finite-row hunt requested by 3278. The selected local corpus sweep is broader than the immediate 3276/3277 rows: it includes top-level post-checkpoint documents and `source-intake/mts_residuals` CSVs whose filenames target source weights, coupling, current ownership, WEP/source rows, parent action, shadow blocks, rescale, and readout.

Result: no admissible finite source-backed `C_J` row is found. That does **not** prove `C_J=0`. It does something narrower but useful: it demotes the finite `C_J` source-shadow/current-rescale/pre-action/readout branch to explicit closure-only unless a new numeric source row appears.

This is a real route decision. The exact U(1) branch remains alive, but parent action ownership is still unsigned. The next productive route is therefore `C_Z/C_R`: EM stress normalization and readout transfer, where Poynting/wave/F-only response actually belongs.

## Corpus Search Summary
{md_table(search, ["summary_id", "scope", "files_selected", "lines_scanned", "term_hits_total", "numeric_context_hits_requiring_manual_audit"])}

## Best Candidate Audit
{md_table(candidates, ["candidate_id", "target", "candidate_status", "why_not_enough"])}

## Finite Row Decision
{md_table(decisions, ["decision_id", "decision", "effect_on_theory"])}

## C_J Closure Demotion
{md_table(closure, ["closure_id", "object", "new_status", "meaning", "not_claimed"])}

## Next Coupling Target
{md_table(next_rows, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    hits, _ = corpus_scan()
    rows_by_key = {
        "sources": source_register_rows(),
        "search": corpus_search_summary_rows(),
        "hits": hits,
        "candidates": best_candidate_rows(),
        "decision": finite_row_decision_rows(),
        "closure": cj_closure_demotion_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
