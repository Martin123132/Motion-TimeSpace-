from __future__ import annotations

import csv
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1982_VALIDATION.csv"

SCAN_EXTENSIONS = {".md", ".txt", ".tex", ".json", ".ipynb", ".docx"}
EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "post-checkpoint-work",
    "site-packages",
    "runs",
}
MAX_FILE_BYTES = 5_000_000
MAX_HITS = 160
CONTEXT_CHARS = 260

SOURCE_DOCS = {
    "1981_doc": {
        "path": ROOT / "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md",
        "needles": ["NEXT1981_0_primary", "WIDER_CORPUS_PARENT_ACTION_SCAN"],
    },
    "1981_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1981_VALIDATION.csv",
        "needles": ["VAL1981_OVERALL", "PASS"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_SOURCE_REGISTER.csv",
    "scan_manifest": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_SCAN_MANIFEST.csv",
    "candidate_hits": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_WIDER_CORPUS_CANDIDATE_HITS.csv",
    "classification": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_SCAN_CLASSIFICATION.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "WIDER_CORPUS_PARENT_ACTION_SCAN_1982_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1982_TOP_PARENT_ACTION_CANDIDATE_REVIEW_QUEUE.csv",
}

POSITIVE_PATTERNS = [
    ("memory_action", re.compile(r"\b(S_m|S_mem|L_m|L_mem|memory action|memory sector|scalar-memory)\b", re.I)),
    ("zm", re.compile(r"\bZ[_\s-]?m\b|Z_m|Z0|G_mm", re.I)),
    ("vr_gap", re.compile(r"V_R|partial_m\^2|V''|Hessian|mass gap|M2_min|mu_m\^2|F2", re.I)),
    ("parent_action", re.compile(r"parent action|from the action|derived from the action|action principle|Lagrangian", re.I)),
    ("sign", re.compile(r"positive|no-ghost|elliptic|coercive|stable minimum|strict minimum|convex", re.I)),
    ("source_boundary", re.compile(r"J_m|source[- ]?zero|boundary|readout|matter coupling|coupling", re.I)),
]

NEGATIVE_PATTERN = re.compile(
    r"MISSING|missing|not derived|not supplied|not signed|unsigned|candidate|closure|nonclaim|blocked|template|only|fails|fail|demote",
    re.I,
)

CLAIM_GRADE_PATTERN = re.compile(
    r"(Z_m\s*(?:=|:=)\s*[^,.;]+|V_R\s*(?:=|:=)\s*[^,.;]+|mu_m\^2\s*(?:=|:=)\s*[^,.;]+)"
    r".*(parent|action|derived|theorem|positive|strict|convex)",
    re.I,
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    base = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**base, **values}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, config in SOURCE_DOCS.items():
        path = config["path"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in config["needles"] if needle not in text]
        rows.append(
            row(
                {
                    "id": f"SRC1982_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "handoff into wider corpus parent-action signature scan",
                }
            )
        )
    return rows


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO.rglob("*"):
        if not path.is_file() or is_excluded(path):
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def read_docx(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except Exception:
        return ""
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError:
        return ""
    text_parts: list[str] = []
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for node in root.iter(f"{namespace}t"):
        if node.text:
            text_parts.append(node.text)
    return "\n".join(text_parts)


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    if suffix == ".ipynb":
        try:
            parsed = json.loads(text)
            cells = parsed.get("cells", [])
            chunks: list[str] = []
            for cell in cells:
                source = cell.get("source", [])
                if isinstance(source, list):
                    chunks.append("".join(str(part) for part in source))
                elif isinstance(source, str):
                    chunks.append(source)
            return "\n".join(chunks) if chunks else text
        except Exception:
            return text
    return text


def classify_line(line: str, matched_labels: list[str]) -> tuple[int, str]:
    score = len(matched_labels) * 2
    if "zm" in matched_labels:
        score += 4
    if "memory_action" in matched_labels:
        score += 4
    if "vr_gap" in matched_labels:
        score += 3
    if "parent_action" in matched_labels:
        score += 3
    if "sign" in matched_labels:
        score += 2
    negative = bool(NEGATIVE_PATTERN.search(line))
    claim_shaped = bool(CLAIM_GRADE_PATTERN.search(line))
    if claim_shaped and not negative:
        score += 8
        classification = "ACTION_SIGNATURE_SHAPED_NEEDS_MANUAL_REVIEW"
    elif negative:
        score -= 3
        classification = "KNOWN_BLOCKER_OR_NONCLAIM_LANGUAGE"
    elif {"memory_action", "zm"} <= set(matched_labels):
        classification = "MEMORY_ZM_ACTION_HIT_NEEDS_REVIEW"
    elif "vr_gap" in matched_labels and ("parent_action" in matched_labels or "memory_action" in matched_labels):
        classification = "GAP_OR_HESSIAN_HIT_NEEDS_REVIEW"
    else:
        classification = "LOWER_SIGNAL_CONTEXT_HIT"
    return score, classification


def scan_corpus() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    files = iter_scan_files()
    hits: list[dict[str, str]] = []
    scanned = 0
    readable = 0
    for path in files:
        scanned += 1
        text = read_text(path)
        if not text:
            continue
        readable += 1
        rel_path = str(path.relative_to(REPO))
        for line_number, line in enumerate(text.splitlines(), start=1):
            compact = " ".join(line.strip().split())
            if not compact:
                continue
            matched = [label for label, pattern in POSITIVE_PATTERNS if pattern.search(compact)]
            if len(matched) < 2:
                continue
            score, classification = classify_line(compact, matched)
            if score < 4:
                continue
            hits.append(
                {
                    "branch": BRANCH,
                    "id": f"HIT1982_{len(hits):04d}",
                    "valid_for_claim": "false",
                    "public_claim": "false",
                    "created_at_utc": CREATED_AT,
                    "relative_path": rel_path,
                    "line": str(line_number),
                    "score": str(score),
                    "matched_labels": ";".join(matched),
                    "classification": classification,
                    "excerpt": compact[:CONTEXT_CHARS],
                }
            )
    hits.sort(key=lambda item: (-int(item["score"]), item["relative_path"], int(item["line"])))
    top_hits = hits[:MAX_HITS]
    for index, hit in enumerate(top_hits):
        hit["id"] = f"HIT1982_{index:03d}"
    manifest = [
        row(
            {
                "id": "MAN1982_0_scope",
                "metric": "scan_root",
                "value": str(REPO),
                "detail": "scans wider repo excluding post-checkpoint-work and .git",
            }
        ),
        row(
            {
                "id": "MAN1982_1_files",
                "metric": "candidate_files_scanned",
                "value": scanned,
                "detail": f"extensions={','.join(sorted(SCAN_EXTENSIONS))}; max_file_bytes={MAX_FILE_BYTES}",
            }
        ),
        row(
            {
                "id": "MAN1982_2_readable",
                "metric": "readable_files",
                "value": readable,
                "detail": "docx text extracted with stdlib zip/xml where possible",
            }
        ),
        row(
            {
                "id": "MAN1982_3_hits",
                "metric": "candidate_hits_retained",
                "value": len(top_hits),
                "detail": f"top {MAX_HITS} scored hits retained from {len(hits)} raw hits",
            }
        ),
    ]
    if not top_hits:
        top_hits = [
            {
                "branch": BRANCH,
                "id": "HIT1982_NONE",
                "valid_for_claim": "false",
                "public_claim": "false",
                "created_at_utc": CREATED_AT,
                "relative_path": "NONE",
                "line": "0",
                "score": "0",
                "matched_labels": "NONE",
                "classification": "NO_HITS",
                "excerpt": "No wider-corpus candidate hits found by bounded scanner.",
            }
        ]
    return manifest, top_hits


def build_tables() -> dict[str, list[dict[str, str]]]:
    manifest, hits = scan_corpus()
    high_signal = [hit for hit in hits if hit["classification"] == "ACTION_SIGNATURE_SHAPED_NEEDS_MANUAL_REVIEW"]
    memory_zm = [hit for hit in hits if hit["classification"] == "MEMORY_ZM_ACTION_HIT_NEEDS_REVIEW"]
    blocker = [hit for hit in hits if hit["classification"] == "KNOWN_BLOCKER_OR_NONCLAIM_LANGUAGE"]
    classification = [
        row(
            {
                "id": "CLS1982_0_high_signal",
                "classification": "ACTION_SIGNATURE_SHAPED_NEEDS_MANUAL_REVIEW",
                "count": len(high_signal),
                "meaning": "looks like a parent-action/signature formula but has not been manually checked for claim-grade status",
                "claim_status": "review_only_not_claim_grade",
            }
        ),
        row(
            {
                "id": "CLS1982_1_memory_zm",
                "classification": "MEMORY_ZM_ACTION_HIT_NEEDS_REVIEW",
                "count": len(memory_zm),
                "meaning": "contains memory/Z_m action language but may be draft/candidate text",
                "claim_status": "review_only_not_claim_grade",
            }
        ),
        row(
            {
                "id": "CLS1982_2_blocker",
                "classification": "KNOWN_BLOCKER_OR_NONCLAIM_LANGUAGE",
                "count": len(blocker),
                "meaning": "scanner found explicit missing/candidate/closure language",
                "claim_status": "negative_evidence",
            }
        ),
        row(
            {
                "id": "CLS1982_3_verdict",
                "classification": "AUTO_SCAN_VERDICT",
                "count": len(hits),
                "meaning": "bounded scanner created a review queue; it does not certify any local-GR derivation",
                "claim_status": "NO_AUTO_CLAIM_GRADE_SOURCE",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1982_0_scan_not_proof",
                "gate": "wider scan proves parent signature",
                "status": "BLOCKED",
                "reason": "scanner produces candidate-review hits only; manual extraction/signature proof still required",
                "required_to_open": "manual review source row with exact equation, units, sign, and parent-branch adoption",
            }
        ),
        row(
            {
                "id": "GATE1982_1_local_GR",
                "gate": "derived local GR/Newton limit",
                "status": "BLOCKED",
                "reason": "no auto claim-grade Z_m/V_R/canonical-gap/source-boundary source was validated",
                "required_to_open": "same-parent action signature plus downstream source/boundary/Newton gates",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1982_0_scan_complete",
                "decision": "BOUNDED_WIDER_CORPUS_SCAN_COMPLETE",
                "because": "non-post-checkpoint text/docx/notebook files were scanned for parent memory action/signature language",
                "next_action": "manually review the strongest raw candidates, not the generated blocker echoes",
            }
        ),
        row(
            {
                "id": "DEC1982_1_no_auto_claim",
                "decision": "NO_AUTO_CLAIM_GRADE_SOURCE",
                "because": "automated text hits cannot establish sign, units, domain, and variation order",
                "next_action": "extract candidate equations into a strict source row only if manual review supports it",
            }
        ),
        row(
            {
                "id": "DEC1982_2_best_next",
                "decision": "TOP_CANDIDATE_MANUAL_REVIEW",
                "because": "this is the least circular path: inspect raw parent-action candidates before declaring the route permanently closure-only",
                "next_action": "1983-Y5-R2FR-top-parent-action-candidate-review.md",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1982_0_primary",
                "status": "selected",
                "target_doc": "1983-Y5-R2FR-top-parent-action-candidate-review.md",
                "target_script": "scripts/Y5_R2FR_top_parent_action_candidate_review_1983.py",
                "task": "review the highest-scored wider-corpus hits and decide whether any is a real parent action/signature source for Z_m, V_R'', canonical gap, source-zero, or boundary silence.",
                "success_condition": "promote a manually reviewed source candidate to a strict nonclaim source row, or confirm all hits are draft/candidate/blocker language",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1982_0_status",
                "area": "wider corpus scan",
                "status": "REVIEW_QUEUE_BUILT",
                "summary": "1982 broadens beyond post-checkpoint rows and creates a bounded candidate queue without modifying formalization-workbench.",
            }
        ),
        row(
            {
                "id": "SNAP1982_1_claim",
                "area": "claim status",
                "status": "NO_AUTO_CLAIM",
                "summary": "The scan is evidence-gathering only; it does not validate a parent memory signature or local-GR reduction.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1982_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_scan_index",
                "claim_safety": "all claim flags false; candidate hits require manual review",
                "use": "triage wider corpus for parent action signature candidates",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1982_0_top_hits",
                "quantity": "top wider-corpus parent action signature hits",
                "priority": "highest",
                "why": "possible raw source candidates are the only way to reopen the derivation route without closure",
                "target": "1983 manual candidate review",
            }
        )
    ]

    return {
        "source_register": source_register_rows(),
        "scan_manifest": manifest,
        "candidate_hits": hits,
        "classification": classification,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    return all(
        item.get("valid_for_claim") == "false" and item.get("public_claim") == "false"
        for rows in tables.values()
        for item in rows
    )


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def formalization_1982_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1982*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    source_ok = all(
        item["exists"] == "true" and item["needle_status"] == "PASS"
        for item in tables["source_register"]
    )
    manifest_by_id = {item["id"]: item for item in tables["scan_manifest"]}
    classification_by_id = {item["id"]: item for item in tables["classification"]}
    gates_blocked = all(item["status"] == "BLOCKED" for item in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1983-Y5-R2FR-top-parent-action-candidate-review.md"
    scanned_count = int(manifest_by_id["MAN1982_1_files"]["value"])
    hits_count = int(manifest_by_id["MAN1982_3_hits"]["value"])
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1982_artifact_count()
    specs = [
        ("VAL1982_00_sources", source_ok, "handoff sources exist and needles found"),
        ("VAL1982_01_files_scanned", scanned_count > 0, f"candidate_files_scanned={scanned_count}"),
        ("VAL1982_02_hits_written", hits_count > 0, f"candidate_hits_retained={hits_count}"),
        (
            "VAL1982_03_no_auto_claim",
            classification_by_id["CLS1982_3_verdict"]["claim_status"] == "NO_AUTO_CLAIM_GRADE_SOURCE",
            "scanner only creates review queue",
        ),
        ("VAL1982_04_claim_gates", gates_blocked, "all claim gates remain blocked"),
        (
            "VAL1982_05_decision",
            tables["decision"][-1]["decision"] == "TOP_CANDIDATE_MANUAL_REVIEW",
            "decision selects manual top-candidate review",
        ),
        ("VAL1982_06_next_target", next_selected, "1983 target selected"),
        ("VAL1982_07_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1982_08_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1982_09_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1982_10_formalization_untouched", formalization_count == 0, f"formalization_1982_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in specs
    ]
    rows.append(
        {
            "validation_id": "VAL1982_OVERALL",
            "status": "PASS" if all(item["status"] == "PASS" for item in rows) else "FAIL",
            "detail": "1982 wider corpus parent action signature scan",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], limit: int | None = None) -> str:
    selected = rows if limit is None else rows[:limit]
    headers = list(selected[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for item in selected:
        values = [item.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    if limit is not None and len(rows) > limit:
        lines.append("| " + " | ".join(["..."] * len(headers)) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"], None),
        ("Scan Manifest", tables["scan_manifest"], None),
        ("Classification", tables["classification"], None),
        ("Top Candidate Hits", tables["candidate_hits"], 35),
        ("Claim Gate", tables["claim_gate"], None),
        ("Decision Ledger", tables["decision"], None),
        ("Next Target", tables["next"], None),
        ("Project Status Snapshot", tables["snapshot"], None),
        ("Validation", validation_rows, None),
    ]
    lines = [
        "# 1982 Y5 R2FR: Wider Corpus Parent Action Signature Scan",
        "",
        "Private checkpoint. This broadens the 1981 source hunt beyond post-checkpoint rows and scans the wider Motion-TimeSpace repo for parent-action/signature language around `Z_m`, `V_R`, canonical gap, source-zero, and boundary silence.",
        "",
        "Verdict: the scanner builds a candidate-review queue only. It does not certify any source as claim-grade; every hit needs manual extraction of the exact equation, units, sign convention, parent branch, and variation order before it can reopen the local-GR derivation route.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, or public claim follows from 1982.",
        "",
    ]
    for title, rows, limit in sections:
        lines.extend([f"## {title}", "", markdown_table(rows, limit), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1982_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
