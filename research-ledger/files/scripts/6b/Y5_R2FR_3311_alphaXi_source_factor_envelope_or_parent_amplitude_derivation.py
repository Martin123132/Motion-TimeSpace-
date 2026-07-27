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

DOC = ROOT / "3311-Y5-R2FR-alphaXi-source-factor-envelope-or-parent-amplitude-derivation-under-AX1090.md"

SRC_3310_DOC = ROOT / "3310-Y5-R2FR-lambda-scan-WEP-envelope-or-parent-range-derivation-under-AX1090.md"
SRC_3310_RANGE = OUT / "P8_Y5_R2FR_3310_PARENT_RANGE_DERIVATION_AUDIT.csv"
SRC_3310_ENVELOPE = OUT / "P8_Y5_R2FR_3310_WEP_KLAMBDA_ENVELOPE.csv"
SRC_3310_SUMMARY = OUT / "P8_Y5_R2FR_3310_ENVELOPE_SUMMARY.csv"
SRC_3310_NEXT = OUT / "P8_Y5_R2FR_3310_NEXT_TARGET.csv"
SRC_3310_VALIDATION = OUT / "P8_Y5_BRR545_3310_VALIDATION.csv"
SRC_3308_MATRIX = OUT / "P8_Y5_R2FR_3308_WEP_LINEAR_CONSTRAINT_MATRIX.csv"
SRC_3303_LAW = OUT / "P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3311_SOURCE_REGISTER.csv",
    "parent_audit": OUT / "P8_Y5_R2FR_3311_PARENT_ALPHA_XI_AUDIT.csv",
    "factor_law": OUT / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv",
    "envelope": OUT / "P8_Y5_R2FR_3311_ALPHA_XI_WEP_ENVELOPE.csv",
    "summary": OUT / "P8_Y5_R2FR_3311_ALPHA_XI_ENVELOPE_SUMMARY.csv",
    "runner": OUT / "P8_Y5_R2FR_3311_ALPHA_XI_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3311_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3311_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3311_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3311_VALIDATION.csv",
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

ALPHAXI_PATTERNS = [
    r"alpha0_star",
    r"alpha2_star",
    r"alpha_0",
    r"alpha_2",
    r"Xi_0\[Earth\]",
    r"Xi_2\[Earth\]",
    r"\bZ_0\b",
    r"\bZ_2\b",
    r"\bU_0\b",
    r"\bU_2\b",
    r"source\s+factor",
    r"mode\s+residue",
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
        (SRC_3310_DOC, "3310 lambda envelope handoff", ["F(lambda", "alpha_i_star"]),
        (SRC_3310_RANGE, "3310 parent range audit", ["NO_PARENT_RANGE_PROMOTION"]),
        (SRC_3310_ENVELOPE, "3310 F(lambda) envelope", ["F_lambda", "inverse_F_lambda"]),
        (SRC_3310_SUMMARY, "3310 sensitivity summary", ["first_lambda_F_ge_0p1_m"]),
        (SRC_3310_NEXT, "3310 next target", ["alphaXi-source-factor", "parent amplitude"]),
        (SRC_3310_VALIDATION, "3310 validation", ["VAL3310_12_overall", "true"]),
        (SRC_3308_MATRIX, "3308 eta and linear forms", ["eta_sigma_proxy", "linear_form"]),
        (SRC_3303_LAW, "3303 alpha factor law", ["alpha_0", "alpha_2"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3311_{index}",
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


def parent_alpha_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            matched = [pattern for pattern in ALPHAXI_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]
            if not matched:
                continue
            parent_owned = ROOT not in path.parents
            explicit_assignment = bool(
                re.search(r"(alpha[02]_star|Xi_[02]\[Earth\]|Z_[02]|U_[02])\s*[:=]\s*[-+]?\d", text, flags=re.IGNORECASE)
            )
            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(parent_owned),
                    "patterns_hit": ";".join(matched),
                    "explicit_numeric_assignment": bool_str(explicit_assignment),
                    "promotion_status": "CANDIDATE_REVIEW_REQUIRED" if parent_owned and explicit_assignment else "NO_ALPHA_XI_PROMOTION",
                    "evidence_lines": line_evidence(text, ALPHAXI_PATTERNS),
                    "valid_for_claim": "false",
                }
            )
    rows.sort(key=lambda row: (row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED", row["explicit_numeric_assignment"] == "true"), reverse=True)
    if not rows:
        rows.append(
            {
                "path": "NO_ALPHA_XI_LANGUAGE_FOUND",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "patterns_hit": "",
                "explicit_numeric_assignment": "false",
                "promotion_status": "MISSING_ALPHA_XI_PARENT_FACTOR",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def factor_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor_id": "AXF3311_0_scalar",
            "mode": "scalar",
            "source_factor": "A_0",
            "definition": "A_0 = alpha0_star Xi_0[Earth] = (1/3) Z_0 U_0 Xi_0[Earth]",
            "pure_limit": "A_0=1/3 only if Z_0=U_0=Xi_0[Earth]=1",
            "constraint_role": "|A_0 (s_0 dot Delta_q_AB)| <= eta_bound/F(lambda,r)",
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "AXF3311_1_spin2",
            "mode": "spin2",
            "source_factor": "A_2",
            "definition": "A_2 = alpha2_star Xi_2[Earth] = (-4/3) Z_2 U_2 Xi_2[Earth]",
            "pure_limit": "A_2=-4/3 only if Z_2=U_2=Xi_2[Earth]=1",
            "constraint_role": "|A_2 (s_2 dot Delta_q_AB)| <= eta_bound/F(lambda,r)",
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "AXF3311_2_no_G_absorption",
            "mode": "both",
            "source_factor": "A_i",
            "definition": "A_i is a finite-mode relative source factor, not a calibrated Newtonian G",
            "pure_limit": "G_cal normalizes the massless graviton only",
            "constraint_role": "must remain explicit in WEP/source-composition constraints",
            "current_status": "GUARDRAIL",
            "valid_for_claim": "false",
        },
    ]


def matrix_lookup() -> dict[str, dict[str, str]]:
    return {row["constraint_id"]: row for row in read_csv(SRC_3308_MATRIX)}


def alpha_xi_envelope_rows() -> list[dict[str, Any]]:
    matrix = matrix_lookup()
    rows: list[dict[str, Any]] = []
    for row in read_csv(SRC_3310_ENVELOPE):
        constraint = matrix[row["constraint_id"]]
        mode_factor = "A_0" if row["mode"] == "scalar" else "A_2"
        try:
            eta = float(constraint["eta_sigma_proxy"])
            factor = float(row["F_lambda"])
            bound = eta / factor if factor > 0 else math.inf
            bound_text = f"{bound:.12g}" if math.isfinite(bound) else "INF_SUPPRESSED"
        except ValueError:
            bound_text = "MISSING_BOUND_PROXY"
        rows.append(
            {
                "envelope_id": f"AXENV3311_{row['envelope_id']}",
                "constraint_id": row["constraint_id"],
                "mode": row["mode"],
                "anchor_id": row["anchor_id"],
                "lambda_m": row["lambda_m"],
                "F_lambda": row["F_lambda"],
                "source_factor": mode_factor,
                "linear_form": constraint["linear_form"],
                "eta_sigma_proxy": constraint["eta_sigma_proxy"],
                "bound_on_abs_A_times_sdotq_proxy": bound_text,
                "constraint_template": f"|{mode_factor} * ({constraint['linear_form']})| <= eta_bound/F_lambda",
                "why_nonclaim": "eta_sigma is a proxy and exact material/confidence/source factors are unresolved",
                "valid_for_claim": "false",
            }
        )
    return rows


def envelope_summary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in read_csv(SRC_3310_SUMMARY):
        matching = [
            row
            for row in alpha_xi_envelope_rows()
            if row["constraint_id"] == summary["constraint_id"]
            and row["lambda_m"] == summary["first_lambda_F_ge_0p9_m"]
        ]
        rows.append(
            {
                "summary_id": f"AXSUM3311_{summary['constraint_id']}",
                "constraint_id": summary["constraint_id"],
                "mode": summary["mode"],
                "anchor_id": summary["anchor_id"],
                "lambda_F_ge_0p1_m": summary["first_lambda_F_ge_0p1_m"],
                "lambda_F_ge_0p9_m": summary["first_lambda_F_ge_0p9_m"],
                "bound_proxy_at_F_ge_0p9": matching[0]["bound_on_abs_A_times_sdotq_proxy"] if matching else "OUTSIDE_GRID",
                "interpretation": "constraint is on A_i times source-coefficient material projection, not on s_i alone",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows(audit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in audit_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    envelope = alpha_xi_envelope_rows()
    return [
        {
            "runner_id": "RUN3311_0_parent_alphaXi",
            "test": "parent alpha/Xi source-factor candidates found",
            "result": "CANDIDATE_REVIEW_REQUIRED" if candidates else "NO_ALPHA_XI_PROMOTION",
            "detail": f"candidate_count={len(candidates)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3311_1_alphaXi_envelope",
            "test": "alpha/Xi envelope exists for all lambda scan rows",
            "result": "PASS_NONCLAIM" if len(envelope) == len(read_csv(SRC_3310_ENVELOPE)) else "FAIL",
            "detail": f"rows={len(envelope)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3311_2_claim_permission",
            "test": "A_i source-factor bounds claim-ready",
            "result": "REFUSE_CLAIM_EXACT_MATERIAL_CONFIDENCE_AND_PARENT_FACTORS_MISSING",
            "detail": "A_i is explicit but not parent-derived; eta/material rows remain proxy/partial",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(audit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in audit_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "gate_id": "GATE3311_0_parent_Ai",
            "claim": "A_0 and A_2 are derived from parent mode/source data",
            "requirements": "parent-reviewed Z_i, U_i, Xi_i[Earth] or alpha_i_star values with source path and units/convention",
            "current_evidence": f"unreviewed_candidate_count={len(candidates)}",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3311_1_Ai_bound",
            "claim": "WEP data bounds A_i*s_i combinations claim-ready",
            "requirements": "exact material/confidence rows and no cancellation/source-charge loophole",
            "current_evidence": "nonclaim envelope only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3311_2_no_G_absorption",
            "claim": "finite-mode source factor can be hidden inside calibrated G",
            "requirements": "not allowed: G_cal fixes massless graviton; finite-mode A_i must remain explicit",
            "current_evidence": "guardrail active",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(audit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in audit_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "decision_id": "DEC3311_0",
            "question": "Did 3311 derive A_0/A_2 from parent data?",
            "answer": "candidate review needed" if candidates else "no",
            "reason": "no reviewed parent source-factor row has been promoted",
            "next_action": "keep A_i explicit and do not absorb it into G_cal",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3311_1",
            "question": "What changed?",
            "answer": "WEP constraints now bound |A_i(s_i dot Delta_q)| over the lambda scan",
            "reason": "alpha/source factor is separated from range factor and material projection",
            "next_action": "resolve exact material/confidence rows or derive A_i from parent projectors",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3311_0_3312",
            "target_doc": "3312-Y5-R2FR-exact-WEP-material-confidence-ledger-or-parent-Ai-proof-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3312_exact_WEP_material_confidence_ledger_or_parent_Ai_proof.py",
            "objective": "replace proxy material/confidence rows with exact WEP inputs where available, or prove A_i values from parent amplitude/source factors",
            "guardrails": "do not treat proxy material charges or eta_sigma_proxy as final bounds; do not hide A_i in G_cal",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    audit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    laws = factor_law_rows()
    envelope = alpha_xi_envelope_rows()
    summary = envelope_summary_rows()
    runners = runner_rows(audit_rows)
    gates = promotion_gate_rows(audit_rows)
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3311_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3311_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3311_2_outputs_parse",
            "all 3311 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3311_3_factor_law_complete",
            "factor law defines A_0, A_2, and no-G absorption guard",
            all(any(token in row["source_factor"] or token in row["factor_id"] for row in laws) for token in ["A_0", "A_2", "no_G"]),
            "",
        ),
        (
            "VAL3311_4_parent_audit_nonclaim",
            "parent alpha/Xi audit ran and remains nonclaim",
            bool(audit_rows) and all(row["valid_for_claim"] == "false" for row in audit_rows),
            f"rows={len(audit_rows)}",
        ),
        (
            "VAL3311_5_envelope_complete",
            "alpha/Xi envelope covers every 3310 lambda-envelope row",
            len(envelope) == len(read_csv(SRC_3310_ENVELOPE)) and all(row["valid_for_claim"] == "false" for row in envelope),
            "",
        ),
        (
            "VAL3311_6_summary_complete",
            "summary covers all 3310 constraints",
            len(summary) == len(read_csv(SRC_3310_SUMMARY)),
            "",
        ),
        (
            "VAL3311_7_runner_refuses_claim",
            "runner refuses claim until exact material/confidence and parent factors are fixed",
            any(row["result"] == "REFUSE_CLAIM_EXACT_MATERIAL_CONFIDENCE_AND_PARENT_FACTORS_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3311_8_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3311_9_next_target_exact_WEP_or_Ai",
            "next target is exact WEP material/confidence ledger or parent Ai proof",
            "exact-WEP-material-confidence" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3311_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3311_11_overall",
            "3311 validation overall",
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


def render_doc(audit_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    law_table = "\n".join(
        f"- `{row['factor_id']}` `{row['source_factor']}`: {row['definition']}."
        for row in factor_law_rows()
    )
    audit_table = "\n".join(
        f"- `{row['path']}`: status={row['promotion_status']}; hits={row['patterns_hit']}; evidence={row['evidence_lines']}"
        for row in audit_rows[:10]
    )
    summary_table = "\n".join(
        f"- `{row['constraint_id']}`: bound proxy at F>=0.9 is `{row['bound_proxy_at_F_ge_0p9']}` on |A_i(s_i dot Delta_q)|."
        for row in envelope_summary_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows(audit_rows)
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows(audit_rows)
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows(audit_rows)
    )
    next_row = next_target_rows()[0]

    return f"""# 3311 - AlphaXi source-factor envelope or parent amplitude derivation under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The remaining WEP multiplier is now explicit.

Define

`A_0 = alpha0_star Xi_0[Earth] = (1/3) Z_0 U_0 Xi_0[Earth]`

and

`A_2 = alpha2_star Xi_2[Earth] = (-4/3) Z_2 U_2 Xi_2[Earth]`.

The WEP scan therefore constrains

`|A_i (s_i dot Delta_q_AB)| <= eta_bound/F(lambda,r)`.

No `A_i` value is promoted here. The important discipline is that `A_i` is not absorbed into `G_cal`; it remains a finite-mode source/readout amplitude that must be derived or bounded.

## Source Register

{source_table}

## Factor Law

{law_table}

## Parent Alpha/Xi Audit

{audit_table}

## Envelope Summary

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
    audit_rows = parent_alpha_audit_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["parent_audit"], audit_rows)
    write_csv(OUTPUTS["factor_law"], factor_law_rows())
    write_csv(OUTPUTS["envelope"], alpha_xi_envelope_rows())
    write_csv(OUTPUTS["summary"], envelope_summary_rows())
    write_csv(OUTPUTS["runner"], runner_rows(audit_rows))
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(audit_rows))
    write_csv(OUTPUTS["decision"], decision_rows(audit_rows))
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(audit_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, audit_rows))

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
