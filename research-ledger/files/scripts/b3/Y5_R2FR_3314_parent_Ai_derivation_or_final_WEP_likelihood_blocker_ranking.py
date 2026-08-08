from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3314-Y5-R2FR-parent-Ai-derivation-or-final-WEP-likelihood-blocker-ranking-under-AX1090.md"

SRC_3313_DOC = ROOT / "3313-Y5-R2FR-upgraded-WEP-matrix-with-material-confidence-rows-under-AX1090.md"
SRC_3313_BLOCKERS = OUT / "P8_Y5_R2FR_3313_FINAL_CLAIM_BLOCKERS.csv"
SRC_3313_SUMMARY = OUT / "P8_Y5_R2FR_3313_UPGRADED_WEP_SUMMARY.csv"
SRC_3313_RUNNER = OUT / "P8_Y5_R2FR_3313_UPGRADED_WEP_RUNNER_NONCLAIM.csv"
SRC_3313_NEXT = OUT / "P8_Y5_R2FR_3313_NEXT_TARGET.csv"
SRC_3313_VALIDATION = OUT / "P8_Y5_BRR545_3313_VALIDATION.csv"
SRC_3311_FACTOR = OUT / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv"
SRC_3303_LAW = OUT / "P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv"
SRC_3305_DERIVATION = OUT / "P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3314_SOURCE_REGISTER.csv",
    "ranking": OUT / "P8_Y5_R2FR_3314_BLOCKER_RANKING.csv",
    "Ai_derivation": OUT / "P8_Y5_R2FR_3314_PARENT_Ai_DERIVATION_ATTEMPT.csv",
    "factor_audit": OUT / "P8_Y5_R2FR_3314_Ai_FACTOR_CLAUSE_AUDIT.csv",
    "strategy": OUT / "P8_Y5_R2FR_3314_STRATEGY_COMPARISON.csv",
    "runner": OUT / "P8_Y5_R2FR_3314_BLOCKER_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3314_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3314_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3314_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3314_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

SCAN_ROOTS = [
    REPO / "core-mts-framework",
    REPO / "cosmology",
    REPO / "documents",
    REPO / "formalization-workbench",
    REPO / "mathematics",
    REPO / "orbital-dynamics",
    REPO / "quantum-particle-field",
]
TEXT_EXTENSIONS = {".md", ".txt", ".tex", ".csv", ".py", ".json", ".yaml", ".yml"}
SKIP_DIR_NAMES = {".git", "__pycache__", ".ipynb_checkpoints", "runs", "node_modules", ".venv", "venv"}
AI_PROOF_PATTERNS = [
    r"\bA_0\b",
    r"\bA_2\b",
    r"alpha0_star",
    r"alpha2_star",
    r"\bZ_0\b",
    r"\bZ_2\b",
    r"\bU_0\b",
    r"\bU_2\b",
    r"Xi_0\[Earth\]",
    r"Xi_2\[Earth\]",
    r"projector",
    r"mode\s+residue",
    r"readout",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 820) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 420)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3313_DOC, "3313 WEP matrix handoff", ["A_i", "local GR"]),
        (SRC_3313_BLOCKERS, "3313 final blockers", ["parent_Ai", "covariance"]),
        (SRC_3313_SUMMARY, "3313 WEP summary", ["A_i times source-coefficient projection"]),
        (SRC_3313_RUNNER, "3313 runner", ["REFUSE_CLAIM_PARENT_Ai"]),
        (SRC_3313_NEXT, "3313 next target", ["parent-Ai-derivation", "blocker"]),
        (SRC_3313_VALIDATION, "3313 validation", ["VAL3313_11_overall", "true"]),
        (SRC_3311_FACTOR, "3311 A_i factor law", ["AXF3311_0_scalar", "AXF3311_1_spin2"]),
        (SRC_3303_LAW, "3303 generalized alpha law", ["Z_0", "Xi_0"]),
        (SRC_3305_DERIVATION, "3305 projector derivation", ["delta S_m", "Q_0[A]"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3314_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def safe_text_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for item in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in item.parts):
            continue
        if item.is_file() and item.suffix.lower() in TEXT_EXTENSIONS:
            try:
                if item.stat().st_size <= 2_000_000:
                    files.append(item)
            except OSError:
                continue
    return files


def line_evidence(text: str, patterns: list[str], limit: int = 4) -> str:
    compiled_patterns = [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns]
    snippets: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in compiled_patterns):
            snippets.append(f"L{line_number}:{compact(line, 280)}")
        if len(snippets) >= limit:
            break
    return " | ".join(snippets) if snippets else "NO_LINE_EVIDENCE"


def parent_ai_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            matched = [pattern for pattern in AI_PROOF_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]
            if not matched:
                continue
            explicit = bool(re.search(r"(A_[02]|Z_[02]|U_[02]|Xi_[02]\[Earth\]|alpha[02]_star)\s*[:=]\s*[-+]?\d", text, flags=re.IGNORECASE))
            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(ROOT not in path.parents),
                    "patterns_hit": ";".join(matched),
                    "explicit_numeric_assignment": bool_str(explicit),
                    "candidate_status": "CANDIDATE_REVIEW_REQUIRED" if explicit else "NO_PARENT_Ai_PROMOTION",
                    "evidence_lines": line_evidence(text, AI_PROOF_PATTERNS),
                    "valid_for_claim": "false",
                }
            )
    rows.sort(key=lambda row: (row["candidate_status"] == "CANDIDATE_REVIEW_REQUIRED", row["explicit_numeric_assignment"] == "true"), reverse=True)
    if not rows:
        rows.append(
            {
                "path": "NO_PARENT_Ai_LANGUAGE_FOUND",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "patterns_hit": "",
                "explicit_numeric_assignment": "false",
                "candidate_status": "MISSING_PARENT_Ai",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def blocker_ranking_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "blocker_id": "BR3314_0_parent_Ai",
            "blocker": "parent A_i derivation",
            "why_ranked_here": "without A_i, WEP matrix bounds A_i*s_i only and cannot distinguish weak coupling from universal source safety",
            "best_next_action": "derive Z_i, U_i, Xi_i[Earth] or prove pure metric finite-mode limit",
            "current_status": "OPEN_DERIVATION_BLOCKER",
            "valid_for_claim": "false",
        },
        {
            "rank": 2,
            "blocker_id": "BR3314_1_cancellation_policy",
            "blocker": "scalar/spin2 cancellation rule",
            "why_ranked_here": "without parent relation between scalar and spin2 sectors, empirical rows must stay separate and cannot use cancellation",
            "best_next_action": "derive independent modes or explicit shared coefficient relation",
            "current_status": "OPEN_THEORY_BLOCKER",
            "valid_for_claim": "false",
        },
        {
            "rank": 3,
            "blocker_id": "BR3314_2_exact_assay",
            "blocker": "exact material assay and binding model",
            "why_ranked_here": "important for final likelihood, but not useful until theory factors A_i/s_i are interpretable",
            "best_next_action": "extract only after parent A_i route is chosen or empirical-bound route is prioritized",
            "current_status": "OPEN_DATA_BLOCKER",
            "valid_for_claim": "false",
        },
        {
            "rank": 4,
            "blocker_id": "BR3314_3_covariance",
            "blocker": "full WEP likelihood/covariance",
            "why_ranked_here": "needed for final claim, but premature while matrix still bounds composite A_i*s_i factors",
            "best_next_action": "defer until exact target parameter is fixed",
            "current_status": "OPEN_DATA_BLOCKER",
            "valid_for_claim": "false",
        },
    ]


def parent_ai_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "AID3314_0_scalar_definition",
            "statement": "A_0 = alpha0_star Xi_0[Earth] = (1/3) Z_0 U_0 Xi_0[Earth].",
            "proof_role": "separates pure metric scalar residue from MTS residue/readout/source factors",
            "status": "EXACT_FACTOR_IDENTITY_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AID3314_1_spin2_definition",
            "statement": "A_2 = alpha2_star Xi_2[Earth] = (-4/3) Z_2 U_2 Xi_2[Earth].",
            "proof_role": "separates pure metric spin-2 residue from MTS residue/readout/source factors",
            "status": "EXACT_FACTOR_IDENTITY_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AID3314_2_pure_metric_sufficient_condition",
            "statement": "If Z_0=U_0=Xi_0[Earth]=1 and Z_2=U_2=Xi_2[Earth]=1, then A_0=1/3 and A_2=-4/3.",
            "proof_role": "conditional route to import pure metric finite-mode amplitudes",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AID3314_3_source_safety_condition",
            "statement": "If parent projectors also force s_ik=0, WEP source-composition residuals vanish independent of A_i.",
            "proof_role": "shows strongest local-GR route is source-universality proof, not empirical A_i fitting",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AID3314_4_no_absorption",
            "statement": "A_i cannot be absorbed into G_cal because G_cal normalizes the massless graviton while A_i multiplies finite-range modes.",
            "proof_role": "prevents hiding finite-mode coupling in Newton calibration",
            "status": "GUARDRAIL",
            "valid_for_claim": "false",
        },
    ]


def factor_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "FAC3314_0_Z_residue",
            "factor": "Z_0,Z_2",
            "needed_proof": "linearized kinetic operator gives pure metric scalar/spin2 residues after canonical normalization",
            "current_evidence": "not parent-derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FAC3314_1_U_readout",
            "factor": "U_0,U_2",
            "needed_proof": "diagonal finite modes enter the observed public metric with pure metric readout weights",
            "current_evidence": "not parent-derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FAC3314_2_Xi_source",
            "factor": "Xi_0[Earth],Xi_2[Earth]",
            "needed_proof": "Earth/source body couples through the same Hilbert source projector as pure metric branch",
            "current_evidence": "not parent-derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FAC3314_3_sik_universality",
            "factor": "s_ik",
            "needed_proof": "no material charge direction enters finite-mode source charge",
            "current_evidence": "not parent-derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def strategy_rows() -> list[dict[str, Any]]:
    return [
        {
            "strategy_id": "STR3314_0_parent_first",
            "route": "derive parent A_i/s_ik",
            "payoff": "can close source-coupling theorem or sharply reduce WEP branch to residuals",
            "cost": "requires parent linearized kinetic/readout/source projector algebra",
            "priority": "first",
            "valid_for_claim": "false",
        },
        {
            "strategy_id": "STR3314_1_empirical_polish",
            "route": "extract exact WEP likelihood/material assay",
            "payoff": "improves final bound if source factors remain nonzero",
            "cost": "does not solve interpretation while A_i/s_i are unknown",
            "priority": "second",
            "valid_for_claim": "false",
        },
        {
            "strategy_id": "STR3314_2_conservative_public",
            "route": "present WEP matrix as internal nonclaim discipline tool",
            "payoff": "transparent and rigorous without overclaiming",
            "cost": "not a local-GR pass",
            "priority": "supporting",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in scan_rows if row["candidate_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    top_rank = blocker_ranking_rows()[0]
    all_factor_clauses_fail = all(row["passed"] == "false" for row in factor_clause_audit_rows())
    return [
        {
            "runner_id": "RUN3314_0_top_blocker",
            "test": "top blocker is parent A_i",
            "result": "PASS_NONCLAIM" if top_rank["blocker_id"] == "BR3314_0_parent_Ai" else "FAIL",
            "detail": top_rank["why_ranked_here"],
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3314_1_parent_Ai_scan",
            "test": "parent Ai candidates",
            "result": "CANDIDATE_REVIEW_REQUIRED" if candidates else "NO_PARENT_Ai_PROMOTION",
            "detail": f"candidate_count={len(candidates)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3314_2_factor_clauses",
            "test": "factor clauses block pure amplitude import",
            "result": "REFUSE_Ai_IMPORT" if all_factor_clauses_fail else "REVIEW_REQUIRED",
            "detail": ";".join(f"{row['clause_id']}={row['passed']}" for row in factor_clause_audit_rows()),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3314_3_strategy",
            "test": "parent-first strategy selected",
            "result": "PASS_NONCLAIM",
            "detail": "derive parent A_i/s_ik before further empirical polishing",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3314_0_parent_Ai",
            "claim": "A_0/A_2 are parent-derived or pure metric",
            "requirements": "Z_i, U_i, Xi_i[Earth] clauses all parent-signed",
            "current_evidence": "all factor clauses fail",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3314_1_source_coupling",
            "claim": "source-composition coupling is safe for local GR",
            "requirements": "parent A_i plus s_ik=0 theorem, or claim-ready empirical WEP route",
            "current_evidence": "neither route closed",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3314_2_more_WEP_polish",
            "claim": "more exact WEP data alone can close source coupling",
            "requirements": "not sufficient unless target parameter A_i/s_i relation is fixed",
            "current_evidence": "empirical matrix bounds composite A_i*s_i only",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3314_0",
            "question": "What is the top source-coupling blocker now?",
            "answer": "parent A_i / source-factor derivation",
            "reason": "the upgraded WEP matrix only bounds A_i*s_i projections, so data polishing cannot by itself prove universal coupling",
            "next_action": "attempt parent residue-readout-source theorem for Z_i,U_i,Xi_i and s_ik",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3314_1",
            "question": "Did 3314 prove A_i?",
            "answer": "no",
            "reason": "it derived the exact conditional factor identities but no parent clauses are signed",
            "next_action": "move to parent residue/readout/source theorem attempt",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3314_0_3315",
            "target_doc": "3315-Y5-R2FR-parent-residue-readout-source-theorem-for-Ai-and-sik-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3315_parent_residue_readout_source_theorem_for_Ai_and_sik.py",
            "objective": "attempt the parent theorem that fixes Z_i, U_i, Xi_i[Earth], and s_ik from the same public-metric Hilbert-source projector, or cleanly demote A_i/s_ik to empirical envelopes",
            "guardrails": "do not import pure metric amplitudes or set s_ik=0 unless residue, readout, and source projector clauses are all parent-signed",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    scan_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    ranking = blocker_ranking_rows()
    derivation = parent_ai_derivation_rows()
    audit = factor_clause_audit_rows()
    strategy = strategy_rows()
    runners = runner_rows(scan_rows)
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3314_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3314_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3314_2_outputs_parse",
            "all 3314 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3314_3_top_blocker_parent_Ai",
            "parent A_i is ranked as top blocker",
            ranking[0]["blocker_id"] == "BR3314_0_parent_Ai",
            "",
        ),
        (
            "VAL3314_4_derivation_has_A0_A2",
            "parent Ai derivation attempt includes A0 and A2 identities",
            any("A_0" in row["statement"] for row in derivation) and any("A_2" in row["statement"] for row in derivation),
            "",
        ),
        (
            "VAL3314_5_factor_audit_blocks_import",
            "all factor clauses remain unpassed",
            all(row["passed"] == "false" for row in audit),
            "",
        ),
        (
            "VAL3314_6_strategy_parent_first",
            "strategy comparison selects parent-first route",
            any(row["strategy_id"] == "STR3314_0_parent_first" and row["priority"] == "first" for row in strategy),
            "",
        ),
        (
            "VAL3314_7_runner_refuses_Ai_import",
            "runner refuses Ai import",
            any(row["result"] == "REFUSE_Ai_IMPORT" for row in runners),
            "",
        ),
        (
            "VAL3314_8_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3314_9_next_target_parent_theorem",
            "next target is parent residue/readout/source theorem",
            "parent-residue-readout-source-theorem" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3314_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3314_11_overall",
            "3314 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc(scan_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    ranking_table = "\n".join(
        f"- `{row['rank']}` `{row['blocker']}`: {row['why_ranked_here']}"
        for row in blocker_ranking_rows()
    )
    derivation_table = "\n".join(
        f"- `{row['derivation_id']}`: {row['statement']} Status: `{row['status']}`."
        for row in parent_ai_derivation_rows()
    )
    audit_table = "\n".join(
        f"- `{row['clause_id']}` `{row['factor']}`: passed={row['passed']}; needed={row['needed_proof']}"
        for row in factor_clause_audit_rows()
    )
    strategy_table = "\n".join(
        f"- `{row['strategy_id']}` `{row['route']}`: priority={row['priority']}; payoff={row['payoff']}"
        for row in strategy_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows(scan_rows)
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3314 - Parent Ai derivation or final WEP likelihood blocker ranking under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The blocker ranking is now explicit.

The top blocker is not more WEP data. It is parent `A_i` / source-factor derivation, because the upgraded WEP matrix bounds only

`A_i * (s_i dot Delta_q)`.

Without parent `A_i`, an empirical bound cannot tell whether the finite mode is weakly coupled, universally coupled, or absent. So the best next step is a parent residue/readout/source theorem attempt.

## Source Register

{source_table}

## Blocker Ranking

{ranking_table}

## Parent Ai Derivation Attempt

{derivation_table}

## Factor Clause Audit

{audit_table}

## Strategy Comparison

{strategy_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    scan_rows = parent_ai_scan_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["ranking"], blocker_ranking_rows())
    write_csv(OUTPUTS["Ai_derivation"], parent_ai_derivation_rows())
    write_csv(OUTPUTS["factor_audit"], factor_clause_audit_rows())
    write_csv(OUTPUTS["strategy"], strategy_rows())
    write_csv(OUTPUTS["runner"], runner_rows(scan_rows))
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(scan_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, scan_rows))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
