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

DOC = ROOT / "3301-Y5-R2FR-parent-curvature-linear-signature-hunt-or-quadratic-bound-fill-under-AX1090.md"

SRC_3300_DOC = ROOT / "3300-Y5-R2FR-curvature-squared-zero-proof-or-Yukawa-basis-fill-under-AX1090.md"
SRC_3300_ZERO = OUT / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_CONDITIONAL_ZERO_PROOF.csv"
SRC_3300_VARIATION = OUT / "P8_Y5_R2FR_3300_R2_RICCI2_VARIATION_AUDIT.csv"
SRC_3300_YUKAWA = OUT / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_YUKAWA_BASIS.csv"
SRC_3300_NEXT = OUT / "P8_Y5_R2FR_3300_NEXT_TARGET.csv"
SRC_3300_VALIDATION = OUT / "P8_Y5_BRR545_3300_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3301_SOURCE_REGISTER.csv",
    "scan": OUT / "P8_Y5_R2FR_3301_PARENT_SIGNATURE_SCAN.csv",
    "clause_score": OUT / "P8_Y5_R2FR_3301_PARENT_SIGNATURE_CLAUSE_SCORE.csv",
    "decision": OUT / "P8_Y5_R2FR_3301_SIGNATURE_DECISION.csv",
    "finite_schema": OUT / "P8_Y5_R2FR_3301_QUADRATIC_BOUND_FILL_SCHEMA.csv",
    "promotion": OUT / "P8_Y5_R2FR_3301_PROMOTION_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3301_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3301_VALIDATION.csv",
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

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".tex",
    ".csv",
    ".py",
    ".json",
    ".yaml",
    ".yml",
}

SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
    "runs",
    "node_modules",
    ".venv",
    "venv",
}

CLAUSE_PATTERNS = {
    "action_or_variation": [
        r"\baction\b",
        r"\bvariation\b",
        r"\bLagrangian\b",
        r"S[_\-\s]?kin",
        r"Einstein[-\s]?Hilbert",
        r"sqrt\(-g\)",
    ],
    "curvature_linear": [
        r"curvature[-\s]?linear",
        r"linear in curvature",
        r"\bA\s*R\b",
        r"\bR\s*-\s*2\s*Lambda\b",
        r"Einstein[-\s]?Hilbert",
        r"\bLovelock\b",
    ],
    "second_order": [
        r"second[-\s]?order",
        r"two derivatives",
        r"no higher[-\s]?derivative",
        r"principal symbol",
        r"field equations are second",
    ],
    "single_metric": [
        r"single metric",
        r"public metric",
        r"Levi[-\s]?Civita",
        r"metric compatible",
        r"torsion[-\s]?free",
    ],
    "no_extra_modes": [
        r"no extra local",
        r"no extra field",
        r"auxiliary",
        r"constraint",
        r"decoupled",
        r"gauge",
        r"silent",
    ],
    "quadratic_guard": [
        r"\bR\^2\b",
        r"R\^{2}",
        r"Ricci\^2",
        r"Ricci squared",
        r"Weyl\^2",
        r"Weyl squared",
        r"quadratic curvature",
        r"higher curvature",
        r"\bf\(R\)",
        r"Gauss[-\s]?Bonnet",
    ],
}

EXCLUSION_PATTERNS = [
    r"not parent signed",
    r"conditional theorem",
    r"valid_for_claim",
    r"checkpoint",
    r"nonclaim",
    r"not promoted",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 720) -> str:
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
            hits.append(f"L{line_number}:{compact(line, 380)}")
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
        (SRC_3300_DOC, "3300 conditional theorem handoff", ["curvature-squared", "c_R2", "c_Ric"]),
        (SRC_3300_ZERO, "3300 zero proof ledger", ["CZ3300_2_c_R2_zero", "CZ3300_3_c_Ric_zero"]),
        (SRC_3300_VARIATION, "3300 operator variation audit", ["VAR3300_2_R_squared", "VAR3300_5_Gauss_Bonnet"]),
        (SRC_3300_YUKAWA, "3300 finite Yukawa basis", ["alpha_0", "alpha_2"]),
        (SRC_3300_NEXT, "3300 next target", ["parent-curvature-linear-signature", "quadratic-bound"]),
        (SRC_3300_VALIDATION, "3300 validation", ["VAL3300_10_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3301_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    for index, root in enumerate(SCAN_ROOTS, start=len(rows)):
        rows.append(
            {
                "source_id": f"SRC3301_{index}",
                "path": str(root),
                "exists": bool_str(root.exists()),
                "parse_ok": bool_str(root.exists() and root.is_dir()),
                "role": "scan root for parent-owned curvature-linear signature",
                "evidence_hits": "DIRECTORY_SCAN_ROOT",
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


def regex_hits(text: str, patterns: list[str]) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def line_evidence(text: str, patterns: list[str], limit: int = 4) -> str:
    compiled = [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns]
    snippets: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in compiled):
            snippets.append(f"L{line_number}:{compact(line, 260)}")
        if len(snippets) >= limit:
            break
    return " | ".join(snippets) if snippets else "NO_LINE_EVIDENCE"


def scan_parent_corpus() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            clause_hits = {
                clause: regex_hits(text, patterns)
                for clause, patterns in CLAUSE_PATTERNS.items()
            }
            support_clauses = [
                clause
                for clause in ["action_or_variation", "curvature_linear", "second_order", "single_metric", "no_extra_modes"]
                if clause_hits[clause]
            ]
            guard_hits = clause_hits["quadratic_guard"]
            exclusion_hits = regex_hits(text, EXCLUSION_PATTERNS)
            if not support_clauses and not guard_hits:
                continue

            parent_owned = ROOT not in path.parents
            all_zero_clauses = all(
                clause in support_clauses
                for clause in ["action_or_variation", "curvature_linear", "second_order", "single_metric", "no_extra_modes"]
            )
            has_guard_or_no_quadratic_language = bool(guard_hits) or "quadratic" not in text.lower()
            promotes_zero = parent_owned and all_zero_clauses and not exclusion_hits and has_guard_or_no_quadratic_language
            score = len(support_clauses) * 10 + len(guard_hits) - len(exclusion_hits) * 8

            evidence_patterns: list[str] = []
            for clause in ["action_or_variation", "curvature_linear", "second_order", "single_metric", "no_extra_modes", "quadratic_guard"]:
                evidence_patterns.extend(CLAUSE_PATTERNS[clause])

            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(parent_owned),
                    "support_clause_count": len(support_clauses),
                    "support_clauses": ";".join(support_clauses),
                    "quadratic_guard_hit_count": len(guard_hits),
                    "quadratic_guard_patterns": ";".join(guard_hits),
                    "exclusion_hit_count": len(exclusion_hits),
                    "exclusion_patterns": ";".join(exclusion_hits),
                    "score": score,
                    "promotes_curvature_squared_zero": bool_str(promotes_zero),
                    "evidence_lines": line_evidence(text, evidence_patterns),
                    "valid_for_claim": "false",
                }
            )

    rows.sort(
        key=lambda row: (
            row["promotes_curvature_squared_zero"] == "true",
            int(row["support_clause_count"]),
            int(row["score"]),
        ),
        reverse=True,
    )
    if not rows:
        rows.append(
            {
                "path": "NO_PARENT_TEXT_CANDIDATE",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "support_clause_count": 0,
                "support_clauses": "",
                "quadratic_guard_hit_count": 0,
                "quadratic_guard_patterns": "",
                "exclusion_hit_count": 0,
                "exclusion_patterns": "",
                "score": 0,
                "promotes_curvature_squared_zero": "false",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def clause_score_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required_clauses = ["action_or_variation", "curvature_linear", "second_order", "single_metric", "no_extra_modes"]
    parent_rows = [row for row in scan_rows if row["parent_owned"] == "true"]
    rows: list[dict[str, Any]] = []
    for clause in required_clauses:
        rows_with_clause = [row for row in parent_rows if clause in row["support_clauses"].split(";")]
        best = rows_with_clause[0] if rows_with_clause else None
        rows.append(
            {
                "clause": clause,
                "parent_candidate_count": len(rows_with_clause),
                "best_path": best["path"] if best else "MISSING_PARENT_CLAUSE",
                "best_evidence": best["evidence_lines"] if best else "MISSING_PARENT_CLAUSE",
                "passed": bool_str(bool(rows_with_clause)),
                "valid_for_claim": "false",
            }
        )
    zero_promoters = [row for row in parent_rows if row["promotes_curvature_squared_zero"] == "true"]
    rows.append(
        {
            "clause": "all_clauses_same_parent_signature",
            "parent_candidate_count": len(zero_promoters),
            "best_path": zero_promoters[0]["path"] if zero_promoters else "MISSING_SINGLE_PARENT_SIGNATURE",
            "best_evidence": zero_promoters[0]["evidence_lines"] if zero_promoters else "NO_SINGLE_PARENT_FILE_SIGNS_ALL_CLAUSES",
            "passed": bool_str(bool(zero_promoters)),
            "valid_for_claim": "false",
        }
    )
    return rows


def signature_decision_rows(scan_rows: list[dict[str, Any]], clause_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    zero_promoters = [row for row in scan_rows if row["promotes_curvature_squared_zero"] == "true"]
    all_clauses = next(row for row in clause_rows if row["clause"] == "all_clauses_same_parent_signature")
    top_candidate = scan_rows[0]
    zero_claim = bool(zero_promoters)
    return [
        {
            "decision_id": "DEC3301_0_parent_signature",
            "question": "Does the parent text corpus currently sign the curvature-linear/second-order/no-extra-mode contract strongly enough to set c_R2=c_Ric=0?",
            "answer": "yes" if zero_claim else "no",
            "top_candidate_path": top_candidate["path"],
            "all_clauses_same_parent_signature": all_clauses["passed"],
            "reason": "single parent-owned signature found" if zero_claim else "scan found supporting language but not a single parent-owned all-clause signature suitable for a zero claim",
            "next_action": "promote zero route only after human/theory review" if zero_claim else "fill finite alpha/lambda rows and continue parent syntax hunt",
            "valid_for_claim": "false",
        }
    ]


def finite_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QBF3301_0_c_R2_scalar",
            "coefficient": "c_R2",
            "mode": "scalar_curvature_Yukawa",
            "needed_parent_quantity": "c_R2 with units or parent theorem c_R2=0",
            "projection_quantities": "m_0, lambda_0=1/m_0, alpha_0, gamma(r)-1, beta(r)-1",
            "bound_inputs_needed": "R10 alpha(lambda) bound curve; PPN gamma/beta bounds; orbital residual limits if lambda_0 solar-system scale",
            "source_status": "MISSING_PARENT_COEFFICIENT_OR_ZERO_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "QBF3301_1_c_Ric_spin2",
            "coefficient": "c_Ric",
            "mode": "massive_spin2_or_Weyl_Bach_Yukawa",
            "needed_parent_quantity": "c_Ric/c_W with units or parent theorem c_Ric=c_W=0",
            "projection_quantities": "m_2, lambda_2=1/m_2, alpha_2, light_bending_shift, perihelion/precession residual",
            "bound_inputs_needed": "PPN light-bending/gamma bounds; orbital precession bounds; R10 alpha(lambda) only if finite short range",
            "source_status": "MISSING_PARENT_COEFFICIENT_OR_ZERO_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "QBF3301_2_combined_gate",
            "coefficient": "c_R2+c_Ric",
            "mode": "multi_mode_local_residual",
            "needed_parent_quantity": "both zero signatures or both finite source projections",
            "projection_quantities": "alpha_eff(lambda) is not enough; must keep mode identity and arena identity",
            "bound_inputs_needed": "joint R10/PPN/orbital consistency table with no cherry-picking",
            "source_status": "MISSING_JOINT_PARENT_SIGNATURE",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    zero_promoters = [row for row in scan_rows if row["promotes_curvature_squared_zero"] == "true"]
    zero_pass = bool(zero_promoters)
    return [
        {
            "gate_id": "GATE3301_0_parent_zero",
            "claim": "set c_R2=c_Ric=0 from parent-owned local kinetic grammar",
            "requirements": "a parent-owned source must sign action/variation, curvature-linearity, second-order equations, single metric/Levi-Civita branch, no extra local modes, and no generic quadratic-curvature loophole",
            "current_evidence": zero_promoters[0]["path"] if zero_pass else "MISSING_SINGLE_PARENT_SIGNATURE",
            "passed": bool_str(zero_pass),
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3301_1_finite_fill",
            "claim": "use finite c_R2/c_Ric rows as predictions",
            "requirements": "numeric or algebraic coefficient source, units, projection derivation, sign convention, and bound source rows",
            "current_evidence": "schema staged only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3301_2_local_GR_curvature_squared",
            "claim": "curvature-squared local-GR gate is closed",
            "requirements": "GATE3301_0 true after review, or GATE3301_1 true with residuals below all relevant bounds",
            "current_evidence": "not claim-ready",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    zero_promoters = [row for row in scan_rows if row["promotes_curvature_squared_zero"] == "true"]
    if zero_promoters:
        objective = "review the parent-owned signature candidate manually, then either promote the curvature-squared zero theorem or demote it after clause audit"
        guardrails = "do not auto-promote from keyword scan; require clause-by-clause human/theory review"
    else:
        objective = "construct the finite c_R2/c_Ric coefficient extraction table and connect it to real R10/PPN/orbital bound inputs without scoring placeholders as predictions"
        guardrails = "do not treat missing parent coefficients as zero; do not collapse scalar and spin-2 modes into one alpha unless projection derives it"
    return [
        {
            "next_id": "NEXT3301_0_3302",
            "target_doc": "3302-Y5-R2FR-quadratic-curvature-finite-coefficient-extraction-and-bound-map-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3302_quadratic_curvature_finite_coefficient_extraction_and_bound_map.py",
            "objective": objective,
            "guardrails": guardrails,
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    scan_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows if row["role"] != "scan root for parent-owned curvature-linear signature"]
    scan_roots = [Path(row["path"]) for row in source_rows if row["role"] == "scan root for parent-owned curvature-linear signature"]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    finite_schema = finite_schema_rows()
    gates = promotion_gate_rows(scan_rows)
    next_rows = next_target_rows(scan_rows)
    top_scan_exists = bool(scan_rows) and scan_rows[0]["path"] != "NO_PARENT_TEXT_CANDIDATE"
    all_clause_row = next(row for row in clause_rows if row["clause"] == "all_clauses_same_parent_signature")

    checks = [
        (
            "VAL3301_0_sources_exist",
            "all cited checkpoint source paths and scan roots exist",
            all(path.exists() for path in source_paths) and all(path.exists() for path in scan_roots),
            "",
        ),
        (
            "VAL3301_1_sources_parse",
            "all cited checkpoint source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3301_2_outputs_parse",
            "all 3301 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3301_3_scan_has_evidence_or_placeholder",
            "parent signature scan produced evidence rows or an explicit placeholder",
            bool(scan_rows),
            f"top_scan_exists={bool_str(top_scan_exists)}; rows={len(scan_rows)}",
        ),
        (
            "VAL3301_4_clause_score_complete",
            "clause score covers required parent-signature clauses",
            all(
                any(row["clause"] == clause for row in clause_rows)
                for clause in [
                    "action_or_variation",
                    "curvature_linear",
                    "second_order",
                    "single_metric",
                    "no_extra_modes",
                    "all_clauses_same_parent_signature",
                ]
            ),
            "",
        ),
        (
            "VAL3301_5_zero_not_claimed_by_default",
            "zero route is not claim-promoted unless a single parent-owned signature satisfies all clauses",
            (all_clause_row["passed"] == "true")
            == any(row["promotes_curvature_squared_zero"] == "true" for row in scan_rows),
            f"single_signature={all_clause_row['passed']}",
        ),
        (
            "VAL3301_6_finite_schema_complete",
            "finite schema covers c_R2, c_Ric, and combined gate",
            all(any(row["coefficient"] == coeff for row in finite_schema) for coeff in ["c_R2", "c_Ric", "c_R2+c_Ric"]),
            "",
        ),
        (
            "VAL3301_7_claim_gates_safe",
            "no finite/local-GR claim is allowed from schema rows",
            all(row["valid_for_claim"] == "false" for row in gates)
            and all(row["passed"] == "false" for row in gates if row["gate_id"] != "GATE3301_0_parent_zero"),
            "",
        ),
        (
            "VAL3301_8_next_target_finite_bound_map",
            "next target is finite coefficient extraction and bound map",
            "finite-coefficient-extraction" in next_rows[0]["target_doc"]
            and "bound-map" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3301_9_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3301_10_overall",
            "3301 validation overall",
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


def render_doc(scan_rows: list[dict[str, Any]], clause_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    top_scan_table = "\n".join(
        f"- `{row['path']}`: parent_owned={row['parent_owned']}; clauses={row['support_clauses'] or 'none'}; promotes_zero={row['promotes_curvature_squared_zero']}; evidence={row['evidence_lines']}"
        for row in scan_rows[:10]
    )
    clause_table = "\n".join(
        f"- `{row['clause']}`: passed={row['passed']}; best=`{row['best_path']}`"
        for row in clause_rows
    )
    finite_table = "\n".join(
        f"- `{row['row_id']}` `{row['coefficient']}`: {row['projection_quantities']}; status={row['source_status']}"
        for row in finite_schema_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; evidence={row['current_evidence']}"
        for row in promotion_gate_rows(scan_rows)
    )
    decision = signature_decision_rows(scan_rows, clause_rows)[0]
    next_row = next_target_rows(scan_rows)[0]

    return f"""# 3301 - Parent curvature-linear signature hunt or quadratic bound fill under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint performs the actual source hunt requested by `3300`.

Decision: `{decision['answer']}` to parent-signed curvature-squared zero promotion.

Reason: {decision['reason']}.

The work therefore stays non-claim unless a parent-owned all-clause signature is reviewed and promoted. The fallback route is now finite coefficient extraction: `c_R2 -> alpha_0/lambda_0` and `c_Ric/c_W -> alpha_2/lambda_2`, with PPN/orbital duties kept separate.

## Scan Roots

{source_table}

## Top Parent-Side Signature Hits

{top_scan_table}

## Clause Score

{clause_table}

## Finite Coefficient/Bound Fill Schema

{finite_table}

## Promotion Gates

{gate_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    scan_rows = scan_parent_corpus()
    clause_rows = clause_score_rows(scan_rows)

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["scan"], scan_rows)
    write_csv(OUTPUTS["clause_score"], clause_rows)
    write_csv(OUTPUTS["decision"], signature_decision_rows(scan_rows, clause_rows))
    write_csv(OUTPUTS["finite_schema"], finite_schema_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(scan_rows))
    write_csv(OUTPUTS["next"], next_target_rows(scan_rows))

    DOC.write_text(render_doc(scan_rows, clause_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, scan_rows, clause_rows))

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
