from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3298-Y5-R2FR-Rkin-coefficient-source-sweep-and-zero-gate-under-AX1090.md"

SRC_3297_DOC = ROOT / "3297-Y5-R2FR-parent-kinetic-syntax-curvature-linear-proof-or-first-Rkin-basis-under-AX1090.md"
SRC_3297_NEXT = OUT / "P8_Y5_R2FR_3297_NEXT_TARGET.csv"
SRC_3297_BASIS = OUT / "P8_Y5_R2FR_3297_FIRST_RKIN_COEFFICIENT_BASIS.csv"
SRC_3297_INPUTS = OUT / "P8_Y5_R2FR_3297_BASIS_INPUT_REQUIREMENTS.csv"
SRC_3297_VALIDATION = OUT / "P8_Y5_BRR545_3297_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3298_SOURCE_REGISTER.csv",
    "sweep": OUT / "P8_Y5_R2FR_3298_RKIN_COEFFICIENT_SOURCE_SWEEP.csv",
    "hits": OUT / "P8_Y5_R2FR_3298_RKIN_COEFFICIENT_EVIDENCE_HITS.csv",
    "zero_gate": OUT / "P8_Y5_R2FR_3298_COEFFICIENT_ZERO_OR_SOURCE_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3298_COEFFICIENT_GATE_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3298_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3298_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3298_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3298_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
SKIP_DIRS = {".venv-score", ".git", "__pycache__", "runs", ".pytest_cache", "node_modules"}

COEFFICIENTS: dict[str, dict[str, Any]] = {
    "c_R2": {
        "basis_id": "BAS3297_0_R2_scalar",
        "patterns": ["c_R2", "BAS3297_0_R2_scalar", "R^2", "R squared", "curvature squared", "higher-curvature", "quadratic curvature", "f(R)", "scalar Yukawa"],
        "units": "length^2 or inverse mass^2 after normalization",
    },
    "c_Ric": {
        "basis_id": "BAS3297_1_Ricci2_spin2",
        "patterns": ["c_Ric", "BAS3297_1_Ricci2_spin2", "Ricci^2", "Ricci squared", "R_mu_nu R", "Riemann^2", "Weyl^2", "Weyl squared", "massive spin-2"],
        "units": "length^2 or inverse mass^2 after normalization",
    },
    "c_phi": {
        "basis_id": "BAS3297_2_scalar_tensor",
        "patterns": ["c_phi", "BAS3297_2_scalar_tensor", "scalar-tensor", "phi R", "φ R", "hidden scalar", "scalar curvature coupling", "fifth force"],
        "units": "model dependent scalar normalization",
    },
    "c_VT": {
        "basis_id": "BAS3297_3_vector_torsion_frame",
        "patterns": ["c_VT", "BAS3297_3_vector_torsion_frame", "torsion", "nonmetricity", "Einstein-aether", "preferred-frame", "frame-marker", "independent connection"],
        "units": "model dependent vector/torsion normalization",
    },
    "c_mem": {
        "basis_id": "BAS3297_4_memory_kernel",
        "patterns": ["memory kernel", "K_memory", "history-dependent", "nonlocal", "memory projection", "R_mem"],
        "units": "kernel amplitude and timescale/range",
    },
    "c_top": {
        "basis_id": "BAS3297_5_topological_boundary",
        "patterns": ["Chern-Simons", "Gauss-Bonnet", "Pontryagin", "topological", "boundary charge", "R_top"],
        "units": "coupling gradient or boundary coefficient",
    },
    "delta_A": {
        "basis_id": "BAS3297_6_Einstein_coefficient_drift",
        "patterns": ["BAS3297_6_Einstein_coefficient_drift", "Gdot", "G_eff", "delta_A", "coefficient drift", "G drift", "R_coeff", "Einstein coefficient"],
        "units": "dimensionless or time/range derivative of Einstein coefficient",
    },
}

ZERO_PATTERNS = ["theorem-zero", "theorem zero", "zero_if", "zero route", "forbid", "excluded", "silent", "q-basic constant", "constant/q-basic"]
SOURCE_PATTERNS = ["source-backed", "numeric", "units", "bound", "lambda", "alpha", "coefficient"]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 500) -> str:
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
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 320)}")
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


def iter_corpus_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".csv", ".txt"}:
            files.append(path)
    return files


def scan_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    files = iter_corpus_files()
    sweep_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []

    file_text_cache: dict[Path, list[str]] = {}
    for path in files:
        try:
            file_text_cache[path] = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            file_text_cache[path] = []

    for coeff, meta in COEFFICIENTS.items():
        patterns = [pattern.lower() for pattern in meta["patterns"]]
        zero_hits = 0
        source_hits = 0
        total_hits = 0
        first_paths: list[str] = []
        examples: list[str] = []
        for path, lines in file_text_cache.items():
            path_hits_for_coeff = 0
            for line_no, line in enumerate(lines, start=1):
                lower = line.lower()
                if any(pattern.lower() in lower for pattern in patterns):
                    total_hits += 1
                    path_hits_for_coeff += 1
                    if any(zero_pattern in lower for zero_pattern in ZERO_PATTERNS):
                        zero_hits += 1
                    if any(source_pattern in lower for source_pattern in SOURCE_PATTERNS):
                        source_hits += 1
                    if len(examples) < 8:
                        rel = str(path.relative_to(ROOT))
                        examples.append(f"{rel}:L{line_no}:{compact(line, 220)}")
                        hit_rows.append(
                            {
                                "coefficient": coeff,
                                "basis_id": meta["basis_id"],
                                "path": str(path),
                                "line": line_no,
                                "matched_text": compact(line, 420),
                                "valid_for_claim": "false",
                            }
                        )
            if path_hits_for_coeff and len(first_paths) < 6:
                first_paths.append(str(path))

        if total_hits == 0:
            status = "MISSING_NO_CORPUS_HIT"
        elif zero_hits > 0 and source_hits > 0:
            status = "HAS_ZERO_AND_SOURCE_LANGUAGE_BUT_NOT_PROMOTED"
        elif zero_hits > 0:
            status = "HAS_ZERO_LANGUAGE_NOT_PARENT_SIGNED"
        elif source_hits > 0:
            status = "HAS_SOURCE_LANGUAGE_NOT_NUMERIC_GATE"
        else:
            status = "MENTIONED_ONLY_NOT_SOURCEABLE"

        sweep_rows.append(
            {
                "coefficient": coeff,
                "basis_id": meta["basis_id"],
                "patterns": ";".join(meta["patterns"]),
                "expected_units": meta["units"],
                "total_pattern_hits": total_hits,
                "zero_language_hits": zero_hits,
                "source_language_hits": source_hits,
                "first_paths": " | ".join(first_paths),
                "example_hits": " || ".join(examples),
                "status": status,
                "valid_for_claim": "false",
            }
        )

    if not hit_rows:
        hit_rows.append(
            {
                "coefficient": "NO_HITS",
                "basis_id": "NO_HITS",
                "path": "",
                "line": "",
                "matched_text": "No coefficient evidence hits found.",
                "valid_for_claim": "false",
            }
        )
    return sweep_rows, hit_rows


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3297_DOC, "3297 coefficient basis handoff", ["c_R2", "delta_A"]),
        (SRC_3297_NEXT, "3297 next target", ["Rkin-coefficient-source-sweep", "zero gate"]),
        (SRC_3297_BASIS, "R_kin coefficient basis", ["BAS3297_0_R2_scalar", "BAS3297_6_Einstein_coefficient_drift"]),
        (SRC_3297_INPUTS, "basis input requirements", ["REQ3297_1_coefficients", "MISSING"]),
        (SRC_3297_VALIDATION, "3297 validation", ["VAL3297_13_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3298_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_gate_rows(sweep_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in sweep_rows:
        coeff = row["coefficient"]
        status = row["status"]
        if status == "MISSING_NO_CORPUS_HIT":
            gate_status = "BLOCKED_MISSING_COEFFICIENT_EVIDENCE"
            next_action = "search parent action/corpus manually or keep coefficient as explicit zero-required unknown"
        elif status == "HAS_ZERO_LANGUAGE_NOT_PARENT_SIGNED":
            gate_status = "BLOCKED_ZERO_LANGUAGE_UNSIGNED"
            next_action = "trace zero language to parent theorem and validate assumptions"
        elif status == "HAS_SOURCE_LANGUAGE_NOT_NUMERIC_GATE":
            gate_status = "BLOCKED_SOURCE_LANGUAGE_NO_NUMERIC_UNITS"
            next_action = "extract coefficient value/units/source path or demote to symbolic residual"
        elif status == "HAS_ZERO_AND_SOURCE_LANGUAGE_BUT_NOT_PROMOTED":
            gate_status = "BLOCKED_MIXED_LANGUAGE_NEEDS_ADJUDICATION"
            next_action = "separate theorem-zero branch from finite coefficient branch"
        else:
            gate_status = "BLOCKED_MENTION_ONLY"
            next_action = "turn mention into theorem-zero proof or sourced finite coefficient"
        rows.append(
            {
                "coefficient": coeff,
                "basis_id": row["basis_id"],
                "sweep_status": status,
                "gate_status": gate_status,
                "claim_allowed": "false",
                "next_action": next_action,
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows(zero_gate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_blocked = all(row["claim_allowed"] == "false" and row["gate_status"].startswith("BLOCKED") for row in zero_gate)
    return [
        {
            "run_id": "RUN3298_0_coefficients_scanned",
            "check": "all seven R_kin coefficients have sweep rows",
            "observed_status": "PASS_NONCLAIM" if len(zero_gate) == len(COEFFICIENTS) else "FAIL_SCHEMA",
            "expectation_match": bool_str(len(zero_gate) == len(COEFFICIENTS)),
            "claim_allowed": "false",
        },
        {
            "run_id": "RUN3298_1_gate_blocks_claims",
            "check": "zero/source gate blocks all unsourced coefficients",
            "observed_status": "REFUSE_CLAIM_NONCLAIM" if all_blocked else "FAIL_GATE",
            "expectation_match": bool_str(all_blocked),
            "claim_allowed": "false",
        },
        {
            "run_id": "RUN3298_2_next_work_defined",
            "check": "next action defined per coefficient",
            "observed_status": "PASS_NONCLAIM" if all(row["next_action"] for row in zero_gate) else "FAIL_NEXT_ACTION",
            "expectation_match": bool_str(all(row["next_action"] for row in zero_gate)),
            "claim_allowed": "false",
        },
    ]


def promotion_rows(zero_gate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    any_promoted = any(row["claim_allowed"] == "true" for row in zero_gate)
    return [
        {
            "gate_id": "GATE3298_0_sweep_complete",
            "gate": "all R_kin coefficients swept",
            "passed": bool_str(len(zero_gate) == len(COEFFICIENTS)),
            "claim_allowed": "false",
            "detail": f"swept={len(zero_gate)} expected={len(COEFFICIENTS)}",
        },
        {
            "gate_id": "GATE3298_1_any_coefficient_promoted",
            "gate": "any coefficient theorem-zero or finite sourced enough for claim",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "promotion requires parent theorem or numeric units/source/bounds; sweep language alone is insufficient.",
        },
        {
            "gate_id": "GATE3298_2_no_false_zero",
            "gate": "no coefficient set to zero by taste",
            "passed": bool_str(not any_promoted),
            "claim_allowed": "false",
            "detail": "all rows remain nonclaim.",
        },
    ]


def decision_rows(sweep_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["coefficient"] for row in sweep_rows if row["status"] == "MISSING_NO_CORPUS_HIT"]
    discussed = [row["coefficient"] for row in sweep_rows if row["status"] != "MISSING_NO_CORPUS_HIT"]
    return [
        {
            "decision_id": "DEC3298_0_sweep_result",
            "finding": f"Corpus sweep found discussed coefficient language for {','.join(discussed) if discussed else 'none'} and no direct hits for {','.join(missing) if missing else 'none'}.",
            "consequence": "discussion is not proof; each coefficient still needs theorem-zero or sourced finite units.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3298_1_no_promotion",
            "finding": "No R_kin coefficient is promoted to zero or numeric finite evidence by this sweep.",
            "consequence": "local-GR kinetic claim remains blocked, but the coefficient debt is now auditable row-by-row.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3298_2_best_next",
            "finding": "The best next move is to convert the basis into a small coefficient ledger with zero-proof and finite-source columns, then attack the biggest coefficient first.",
            "consequence": "the project moves toward testable R_kin bounds rather than repeating Lovelock prose.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3298_0_3299",
            "target_doc": "3299-Y5-R2FR-Rkin-coefficient-ledger-zero-proof-priority-order-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3299_Rkin_coefficient_ledger_zero_proof_priority_order.py",
            "objective": "turn the 3298 sweep into a priority ledger: for each R_kin coefficient, decide zero-proof route, finite-source route, first bound arena, and exact missing parent input.",
            "guardrails": "do not promote mentions; do not treat zero-language as proof; do not run numeric tests until coefficient units and source-backed bounds exist.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    sweep: list[dict[str, Any]],
    hits: list[dict[str, Any]],
    zero_gate: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3298_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3298_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3298_2_outputs_parse", "all 3298 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    coeffs = {row["coefficient"] for row in sweep}
    add("VAL3298_3_all_coefficients_swept", "all seven coefficients swept", set(COEFFICIENTS).issubset(coeffs) and len(sweep) == len(COEFFICIENTS))
    add("VAL3298_4_hits_table_parseable", "evidence hits table exists and parses", len(hits) >= 1 and all("valid_for_claim" in row for row in hits))
    add(
        "VAL3298_5_zero_gate_blocks_all",
        "zero/source gate blocks all coefficients from claim",
        len(zero_gate) == len(COEFFICIENTS) and all(row["claim_allowed"] == "false" and row["gate_status"].startswith("BLOCKED") for row in zero_gate),
    )
    add("VAL3298_6_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3298_7_claim_gates_false", "no 3298 gate allows local GR/R_kin claim", all(row["claim_allowed"] == "false" for row in promotion))
    add(
        "VAL3298_8_decision_records_no_promotion",
        "decision ledger records no coefficient promotion",
        any("No R_kin coefficient is promoted" in row["finding"] for row in decisions),
    )
    add(
        "VAL3298_9_next_target_focused",
        "next target focuses coefficient ledger and priority order",
        len(next_target) == 1 and "Rkin-coefficient-ledger" in next_target[0]["target_doc"],
    )
    add(
        "VAL3298_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3298_11_overall", "3298 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    sweep: list[dict[str, Any]],
    hits: list[dict[str, Any]],
    zero_gate: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3298 - R_kin coefficient source sweep and zero gate under AX1090

**Run UTC:** {RUN_UTC}

3298 performs the first automated source sweep for the explicit `R_kin` coefficient basis from 3297. This does not promote any coefficient. It creates a harder gate:

Each coefficient must be either:

1. theorem-zero with parent assumptions cited,
2. finite with sourced value/units and a bound arena,
3. or retained as a missing residual.

Mentioned language is not proof. Zero-language is not proof. Source-looking language without units is not a numeric input.

## Source Register

{md_table(sources)}

## R_kin Coefficient Source Sweep

{md_table(sweep)}

## Evidence Hits

{md_table(hits[:24])}

## Coefficient Zero Or Source Gate

{md_table(zero_gate)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    sweep, hits = scan_corpus()
    zero_gate = zero_gate_rows(sweep)
    runner = runner_rows(zero_gate)
    promotion = promotion_rows(zero_gate)
    decisions = decision_rows(sweep)
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["sweep"], sweep)
    write_csv(OUTPUTS["hits"], hits)
    write_csv(OUTPUTS["zero_gate"], zero_gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, sweep, hits, zero_gate, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, sweep, hits, zero_gate, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
