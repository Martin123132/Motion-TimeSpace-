from __future__ import annotations

import csv
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3310-Y5-R2FR-lambda-scan-WEP-envelope-or-parent-range-derivation-under-AX1090.md"

SRC_3309_DOC = ROOT / "3309-Y5-R2FR-mode-factor-Klambda-and-exact-WEP-inputs-under-AX1090.md"
SRC_3309_DERIVATION = OUT / "P8_Y5_R2FR_3309_KLAMBDA_DERIVATION.csv"
SRC_3309_INPUTS = OUT / "P8_Y5_R2FR_3309_EXACT_WEP_INPUT_LEDGER.csv"
SRC_3309_CONSTRAINTS = OUT / "P8_Y5_R2FR_3309_KLAMBDA_CONSTRAINT_UPDATE.csv"
SRC_3309_BLOCKERS = OUT / "P8_Y5_R2FR_3309_WEP_CLAIM_BLOCKERS.csv"
SRC_3309_NEXT = OUT / "P8_Y5_R2FR_3309_NEXT_TARGET.csv"
SRC_3309_VALIDATION = OUT / "P8_Y5_BRR545_3309_VALIDATION.csv"
SRC_3302_COEFF_SCAN = OUT / "P8_Y5_R2FR_3302_PARENT_COEFFICIENT_EXTRACTION_SCAN.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3310_SOURCE_REGISTER.csv",
    "parent_range": OUT / "P8_Y5_R2FR_3310_PARENT_RANGE_DERIVATION_AUDIT.csv",
    "lambda_grid": OUT / "P8_Y5_R2FR_3310_LAMBDA_GRID.csv",
    "envelope": OUT / "P8_Y5_R2FR_3310_WEP_KLAMBDA_ENVELOPE.csv",
    "summary": OUT / "P8_Y5_R2FR_3310_ENVELOPE_SUMMARY.csv",
    "runner": OUT / "P8_Y5_R2FR_3310_LAMBDA_SCAN_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3310_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3310_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3310_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3310_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
LAMBDA_GRID_M = [10.0**exp for exp in range(3, 14)]

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

RANGE_PATTERNS = [
    r"\blambda_0\b",
    r"\blambda_2\b",
    r"\bm_0\b",
    r"\bm_2\b",
    r"\ba_R2\b",
    r"\bb_Ric\b",
    r"\bc_R2\b",
    r"\bc_Ric\b",
    r"Weyl",
    r"Ricci\^2",
    r"R\^2",
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
        (SRC_3309_DOC, "3309 K(lambda) handoff", ["K_i(lambda_i", "lambda_i"]),
        (SRC_3309_DERIVATION, "3309 K(lambda) derivation", ["KDER3309_3_mode_factor", "limits"]),
        (SRC_3309_INPUTS, "3309 upgraded WEP inputs", ["MICROSCOPE_eta", "EOTWASH_eta"]),
        (SRC_3309_CONSTRAINTS, "3309 K(lambda) constraints", ["r_MICROSCOPE_Earth_proxy", "K_0"]),
        (SRC_3309_BLOCKERS, "3309 claim blockers", ["lambda_0", "lambda_2"]),
        (SRC_3309_NEXT, "3309 next target", ["lambda-scan", "parent range"]),
        (SRC_3309_VALIDATION, "3309 validation", ["VAL3309_12_overall", "true"]),
        (SRC_3302_COEFF_SCAN, "3302 parent coefficient scan", ["NO_PARENT_COEFFICIENT_CANDIDATE", "MISSING_PARENT_COEFFICIENT"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3310_{index}",
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


def parent_range_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            matched = [pattern for pattern in RANGE_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]
            if not matched:
                continue
            has_numeric = bool(re.search(r"[-+]?\d+(\.\d+)?([eE][-+]?\d+)?", text))
            parent_owned = ROOT not in path.parents
            exact_range = bool(re.search(r"lambda_[02]\s*[:=]\s*[-+]?\d", text, flags=re.IGNORECASE))
            exact_mass = bool(re.search(r"m_[02]\s*[:=]\s*[-+]?\d", text, flags=re.IGNORECASE))
            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(parent_owned),
                    "patterns_hit": ";".join(matched),
                    "numeric_language_present": bool_str(has_numeric),
                    "exact_lambda_assignment": bool_str(exact_range),
                    "exact_mass_assignment": bool_str(exact_mass),
                    "promotion_status": "CANDIDATE_REVIEW_REQUIRED" if parent_owned and (exact_range or exact_mass) else "NO_PARENT_RANGE_PROMOTION",
                    "evidence_lines": line_evidence(text, RANGE_PATTERNS),
                    "valid_for_claim": "false",
                }
            )
    rows.sort(
        key=lambda row: (
            row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED",
            row["exact_lambda_assignment"] == "true",
            row["exact_mass_assignment"] == "true",
            row["numeric_language_present"] == "true",
        ),
        reverse=True,
    )
    if not rows:
        rows.append(
            {
                "path": "NO_RANGE_LANGUAGE_FOUND",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "patterns_hit": "",
                "numeric_language_present": "false",
                "exact_lambda_assignment": "false",
                "exact_mass_assignment": "false",
                "promotion_status": "MISSING_PARENT_RANGE",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def lambda_grid_rows() -> list[dict[str, Any]]:
    return [
        {
            "grid_id": f"LGRID3310_{index}",
            "lambda_m": f"{value:.12g}",
            "lambda_description": "log10 meter grid from laboratory/geophysical to astronomical range",
            "valid_for_claim": "false",
        }
        for index, value in enumerate(LAMBDA_GRID_M)
    ]


def yukawa_range_factor(range_m: float, lambda_m: float) -> float:
    return (1.0 + range_m / lambda_m) * math.exp(-range_m / lambda_m)


def get_constraints() -> list[dict[str, str]]:
    return read_csv(SRC_3309_CONSTRAINTS)


def envelope_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for constraint in get_constraints():
        range_m = float(constraint["range_value_m_proxy"])
        for lambda_m in LAMBDA_GRID_M:
            range_factor = yukawa_range_factor(range_m, lambda_m)
            try:
                # eta is not stored here; map back via 3308 matrix row would be heavier.
                # Use symbolic sensitivity only and keep nonclaim.
                inverse_factor = 1.0 / range_factor if range_factor > 0 else math.inf
                inverse_text = f"{inverse_factor:.12g}" if math.isfinite(inverse_factor) else "INF_SUPPRESSED"
            except OverflowError:
                inverse_text = "INF_SUPPRESSED"
            rows.append(
                {
                    "envelope_id": f"ENV3310_{constraint['constraint_id']}_L{lambda_m:.0e}",
                    "constraint_id": constraint["constraint_id"],
                    "mode": constraint["mode"],
                    "anchor_id": constraint["anchor_id"],
                    "range_symbol": constraint["range_symbol"],
                    "range_value_m_proxy": constraint["range_value_m_proxy"],
                    "lambda_m": f"{lambda_m:.12g}",
                    "range_over_lambda": f"{range_m / lambda_m:.12g}",
                    "F_lambda": f"{range_factor:.12g}",
                    "inverse_F_lambda": inverse_text,
                    "bounded_combination": "|alpha_i_star Xi_i[Earth] (s_i dot Delta_q_AB)| <= eta_bound / F_lambda",
                    "interpretation": "nonclaim range envelope; F near 1 means WEP anchor is range-sensitive, F near 0 means suppressed",
                    "valid_for_claim": "false",
                }
            )
    return rows


def envelope_summary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for constraint in get_constraints():
        matching = [row for row in envelope_rows() if row["constraint_id"] == constraint["constraint_id"]]
        sensitive = [row for row in matching if float(row["F_lambda"]) >= 0.1]
        strong = [row for row in matching if float(row["F_lambda"]) >= 0.9]
        rows.append(
            {
                "summary_id": f"SUM3310_{constraint['constraint_id']}",
                "constraint_id": constraint["constraint_id"],
                "mode": constraint["mode"],
                "anchor_id": constraint["anchor_id"],
                "range_value_m_proxy": constraint["range_value_m_proxy"],
                "first_lambda_F_ge_0p1_m": sensitive[0]["lambda_m"] if sensitive else "OUTSIDE_GRID",
                "first_lambda_F_ge_0p9_m": strong[0]["lambda_m"] if strong else "OUTSIDE_GRID",
                "physics_read": "Earth-source WEP anchors mainly constrain modes with lambda comparable to or larger than Earth-radius scale",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows(range_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_promotions = [row for row in range_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    envelopes = envelope_rows()
    summaries = envelope_summary_rows()
    return [
        {
            "runner_id": "RUN3310_0_parent_range",
            "test": "parent lambda/mass candidate rows found",
            "result": "CANDIDATE_REVIEW_REQUIRED" if parent_promotions else "NO_PARENT_RANGE_PROMOTION",
            "detail": f"candidate_count={len(parent_promotions)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3310_1_lambda_envelope",
            "test": "lambda scan envelope generated for all constraints",
            "result": "PASS_NONCLAIM" if len(envelopes) == len(get_constraints()) * len(LAMBDA_GRID_M) else "FAIL",
            "detail": f"rows={len(envelopes)}; constraints={len(get_constraints())}; grid={len(LAMBDA_GRID_M)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3310_2_sensitivity_summary",
            "test": "sensitivity summary exists for all constraints",
            "result": "PASS_NONCLAIM" if len(summaries) == len(get_constraints()) else "FAIL",
            "detail": ";".join(f"{row['constraint_id']}:{row['first_lambda_F_ge_0p1_m']}" for row in summaries),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3310_3_claim_permission",
            "test": "lambda envelope claim-ready",
            "result": "REFUSE_CLAIM_ALPHA_XI_MATERIAL_CONFIDENCE_MISSING",
            "detail": "range envelope is numeric in F(lambda) only; amplitude/source/material/confidence blockers remain",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(range_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_promotions = [row for row in range_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "gate_id": "GATE3310_0_parent_lambda",
            "claim": "lambda_0/lambda_2 are derived from parent coefficients",
            "requirements": "reviewed parent action coefficients a_R2/b_Ric/b_W or masses m_0/m_2 with units and convention",
            "current_evidence": f"unreviewed_candidate_count={len(parent_promotions)}",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3310_1_lambda_scan_bound",
            "claim": "WEP lambda scan bounds s_ik combinations",
            "requirements": "claim-ready alpha_i_star, Xi_i[Earth], exact materials, eta confidence, and lambda scan policy",
            "current_evidence": "F(lambda) envelope only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3310_2_local_source_range_gate",
            "claim": "local source-coupling range gate is closed",
            "requirements": "GATE3310_0 or GATE3310_1 true",
            "current_evidence": "neither route closed",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(range_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_promotions = [row for row in range_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "decision_id": "DEC3310_0",
            "question": "Did 3310 derive lambda_0/lambda_2 from parent coefficients?",
            "answer": "candidate review needed" if parent_promotions else "no",
            "reason": "no reviewed parent coefficient/mass row with units has been promoted",
            "next_action": "review candidates if any; otherwise keep lambda as scan parameter",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3310_1",
            "question": "What did the lambda scan add?",
            "answer": "range-aware F(lambda) envelopes for every MICROSCOPE/Eot-Wash scalar/spin2 constraint",
            "reason": "the WEP bound now knows when finite modes are exponentially suppressed or long-range sensitive",
            "next_action": "combine F(lambda) with exact material/confidence rows and alpha/Xi source factors",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3310_0_3311",
            "target_doc": "3311-Y5-R2FR-alphaXi-source-factor-envelope-or-parent-amplitude-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3311_alphaXi_source_factor_envelope_or_parent_amplitude_derivation.py",
            "objective": "derive alpha_i_star and Xi_i[Earth] from parent mode/source data if possible; otherwise keep them as an explicit envelope factor multiplying the lambda-scan WEP constraints",
            "guardrails": "do not absorb alpha_i_star or Xi_i[Earth] into G_cal; do not score exact WEP claims until exact material and confidence rows are resolved",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    range_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    lambda_rows = lambda_grid_rows()
    envelopes = envelope_rows()
    summaries = envelope_summary_rows()
    runners = runner_rows(range_rows)
    gates = promotion_gate_rows(range_rows)
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3310_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3310_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3310_2_outputs_parse",
            "all 3310 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3310_3_parent_range_audit_ran",
            "parent range audit produced rows and no promoted claim",
            bool(range_rows) and all(row["valid_for_claim"] == "false" for row in range_rows),
            f"rows={len(range_rows)}",
        ),
        (
            "VAL3310_4_lambda_grid_complete",
            "lambda grid spans 1e3 through 1e13 meters",
            len(lambda_rows) == len(LAMBDA_GRID_M)
            and float(lambda_rows[0]["lambda_m"]) == 1.0e3
            and float(lambda_rows[-1]["lambda_m"]) == 1.0e13,
            "",
        ),
        (
            "VAL3310_5_envelope_complete",
            "lambda envelope covers every 3309 constraint and lambda grid row",
            len(envelopes) == len(get_constraints()) * len(LAMBDA_GRID_M)
            and all(row["valid_for_claim"] == "false" for row in envelopes),
            "",
        ),
        (
            "VAL3310_6_envelope_has_F",
            "envelope rows include F(lambda) and inverse F(lambda)",
            all("F_lambda" in row and "inverse_F_lambda" in row for row in envelopes),
            "",
        ),
        (
            "VAL3310_7_summary_complete",
            "sensitivity summary covers all constraints",
            len(summaries) == len(get_constraints()),
            "",
        ),
        (
            "VAL3310_8_runner_refuses_claim",
            "runner refuses claim while blockers remain",
            any(row["result"] == "REFUSE_CLAIM_ALPHA_XI_MATERIAL_CONFIDENCE_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3310_9_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3310_10_next_target_alphaXi",
            "next target is alpha/Xi source factor envelope or amplitude derivation",
            "alphaXi-source-factor" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3310_11_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3310_12_overall",
            "3310 validation overall",
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


def render_doc(range_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    parent_table = "\n".join(
        f"- `{row['path']}`: status={row['promotion_status']}; hits={row['patterns_hit']}; evidence={row['evidence_lines']}"
        for row in range_rows[:10]
    )
    summary_table = "\n".join(
        f"- `{row['constraint_id']}`: F>=0.1 at lambda={row['first_lambda_F_ge_0p1_m']} m; F>=0.9 at lambda={row['first_lambda_F_ge_0p9_m']} m."
        for row in envelope_summary_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows(range_rows)
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows(range_rows)
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows(range_rows)
    )
    next_row = next_target_rows()[0]

    return f"""# 3310 - Lambda-scan WEP envelope or parent range derivation under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint tries the parent range route first, then builds the nonclaim lambda envelope.

The parent route is not promoted unless a reviewed parent coefficient/mass row supplies `lambda_0` or `lambda_2` with units and convention.

The scan route uses

`F(lambda,r) = (1+r/lambda) exp(-r/lambda)`

so each WEP constraint becomes

`|alpha_i_star Xi_i[Earth] (s_i dot Delta_q_AB)| <= eta_bound / F(lambda,r)`.

This is range-aware but still nonclaim because `alpha_i_star`, `Xi_i[Earth]`, exact materials, and confidence conventions remain open.

## Source Register

{source_table}

## Parent Range Audit

{parent_table}

## Lambda Sensitivity Summary

{summary_table}

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
    range_rows = parent_range_audit_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["parent_range"], range_rows)
    write_csv(OUTPUTS["lambda_grid"], lambda_grid_rows())
    write_csv(OUTPUTS["envelope"], envelope_rows())
    write_csv(OUTPUTS["summary"], envelope_summary_rows())
    write_csv(OUTPUTS["runner"], runner_rows(range_rows))
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(range_rows))
    write_csv(OUTPUTS["decision"], decision_rows(range_rows))
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(range_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, range_rows))

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
