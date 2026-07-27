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

DOC = ROOT / "3312-Y5-R2FR-exact-WEP-material-confidence-ledger-or-parent-Ai-proof-under-AX1090.md"

SRC_3311_DOC = ROOT / "3311-Y5-R2FR-alphaXi-source-factor-envelope-or-parent-amplitude-derivation-under-AX1090.md"
SRC_3311_FACTOR = OUT / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv"
SRC_3311_ENV = OUT / "P8_Y5_R2FR_3311_ALPHA_XI_WEP_ENVELOPE.csv"
SRC_3311_SUMMARY = OUT / "P8_Y5_R2FR_3311_ALPHA_XI_ENVELOPE_SUMMARY.csv"
SRC_3311_NEXT = OUT / "P8_Y5_R2FR_3311_NEXT_TARGET.csv"
SRC_3311_VALIDATION = OUT / "P8_Y5_BRR545_3311_VALIDATION.csv"

MICROSCOPE_ARXIV = "https://arxiv.org/abs/2209.15487"
MICROSCOPE_DOI = "10.1103/PhysRevLett.129.121102"
MICROSCOPE_ESA = "https://www.esa.int/Science_Exploration/Space_Science/Microscope"
EOTWASH_ARXIV = "https://arxiv.org/abs/0712.0607"
EOTWASH_DOI = "10.1103/PhysRevLett.100.041101"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3312_SOURCE_REGISTER.csv",
    "parent_Ai": OUT / "P8_Y5_R2FR_3312_PARENT_Ai_PROOF_AUDIT.csv",
    "materials": OUT / "P8_Y5_R2FR_3312_EXACT_WEP_MATERIAL_LEDGER.csv",
    "charges": OUT / "P8_Y5_R2FR_3312_UPGRADED_MATERIAL_CHARGES.csv",
    "confidence": OUT / "P8_Y5_R2FR_3312_CONFIDENCE_LEDGER.csv",
    "pair_deltas": OUT / "P8_Y5_R2FR_3312_UPGRADED_PAIR_DELTAS.csv",
    "bound_update": OUT / "P8_Y5_R2FR_3312_BOUND_INPUT_UPDATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3312_EXACT_WEP_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3312_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3312_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3312_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3312_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

ELEMENTS = {
    "Be": {"Z": 4.0, "A": 9.0122},
    "Ti": {"Z": 22.0, "A": 47.867},
    "Pt": {"Z": 78.0, "A": 195.084},
    "Rh": {"Z": 45.0, "A": 102.9055},
    "Al": {"Z": 13.0, "A": 26.9815},
    "V": {"Z": 23.0, "A": 50.9415},
}

MATERIALS = {
    "MICROSCOPE_PtRh10": {
        "experiment": "MICROSCOPE",
        "material_label": "PtRh10 alloy",
        "components": {"Pt": 0.90, "Rh": 0.10},
        "composition_source": MICROSCOPE_ESA,
        "composition_status": "source-backed mass-fraction category; isotopic assay still not extracted",
    },
    "MICROSCOPE_TA6V": {
        "experiment": "MICROSCOPE",
        "material_label": "TA6V / Ti-Al-V alloy",
        "components": {"Ti": 0.90, "Al": 0.06, "V": 0.04},
        "composition_source": MICROSCOPE_ESA,
        "composition_status": "source-backed mass-fraction category; exact alloy/isotope assay still not extracted",
    },
    "EOTWASH_Be": {
        "experiment": "Eot-Wash",
        "material_label": "Be",
        "components": {"Be": 1.0},
        "composition_source": EOTWASH_ARXIV,
        "composition_status": "source-backed test-body element; purity/isotope details not fully extracted",
        "B_over_mu": 0.99868,
    },
    "EOTWASH_Ti": {
        "experiment": "Eot-Wash",
        "material_label": "Ti",
        "components": {"Ti": 1.0},
        "composition_source": EOTWASH_ARXIV,
        "composition_status": "source-backed test-body element; purity/isotope details not fully extracted",
        "B_over_mu": 1.001077,
    },
}

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
AI_PATTERNS = [r"\bA_0\b", r"\bA_2\b", r"alpha0_star", r"alpha2_star", r"Xi_0\[Earth\]", r"Xi_2\[Earth\]", r"Z_0", r"Z_2", r"U_0", r"U_2"]


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
    local_sources = [
        (SRC_3311_DOC, "3311 alphaXi handoff", ["A_0", "A_2"]),
        (SRC_3311_FACTOR, "3311 factor law", ["AXF3311_0_scalar", "AXF3311_2_no_G"]),
        (SRC_3311_ENV, "3311 alphaXi envelope", ["bound_on_abs_A_times_sdotq_proxy"]),
        (SRC_3311_SUMMARY, "3311 summary", ["bound_proxy_at_F_ge_0p9"]),
        (SRC_3311_NEXT, "3311 next target", ["exact-WEP-material-confidence", "parent_Ai"]),
        (SRC_3311_VALIDATION, "3311 validation", ["VAL3311_11_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(local_sources):
        rows.append(
            {
                "source_id": f"SRC3312_{index}",
                "source_type": "local_path",
                "path_or_url": str(path),
                "exists_or_url_present": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    rows.extend(
        [
            {
                "source_id": "SRC3312_6",
                "source_type": "external_primary",
                "path_or_url": MICROSCOPE_ARXIV,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "MICROSCOPE eta and uncertainty source",
                "evidence_hits": "eta(Ti,Pt)=(-1.5 +/- 2.3_stat +/- 1.5_syst)e-15; DOI 10.1103/PhysRevLett.129.121102",
                "valid_for_claim": "false",
            },
            {
                "source_id": "SRC3312_7",
                "source_type": "external_primary",
                "path_or_url": MICROSCOPE_ESA,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "MICROSCOPE material category source",
                "evidence_hits": "Pt-Rh alloy and Ti-Al-V alloy mission material category; used as source-backed category, not assay table",
                "valid_for_claim": "false",
            },
            {
                "source_id": "SRC3312_8",
                "source_type": "external_primary",
                "path_or_url": EOTWASH_ARXIV,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "Eot-Wash Be/Ti eta, acceleration, and B/mu source",
                "evidence_hits": "eta_Earth(Be-Ti)=(0.3 +/- 1.8)e-13 and B/mu Be/Ti anchors",
                "valid_for_claim": "false",
            },
        ]
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


def parent_ai_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            matched = [pattern for pattern in AI_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]
            if not matched:
                continue
            explicit_assignment = bool(re.search(r"(A_[02]|alpha[02]_star|Xi_[02]\[Earth\])\s*[:=]\s*[-+]?\d", text, flags=re.IGNORECASE))
            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(ROOT not in path.parents),
                    "patterns_hit": ";".join(matched),
                    "explicit_numeric_assignment": bool_str(explicit_assignment),
                    "promotion_status": "CANDIDATE_REVIEW_REQUIRED" if explicit_assignment else "NO_PARENT_Ai_PROMOTION",
                    "evidence_lines": line_evidence(text, AI_PATTERNS),
                    "valid_for_claim": "false",
                }
            )
    rows.sort(key=lambda row: (row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED", row["explicit_numeric_assignment"] == "true"), reverse=True)
    if not rows:
        rows.append(
            {
                "path": "NO_Ai_LANGUAGE_FOUND",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "patterns_hit": "",
                "explicit_numeric_assignment": "false",
                "promotion_status": "MISSING_PARENT_Ai",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def q_values_for_element(symbol: str) -> dict[str, float]:
    z = ELEMENTS[symbol]["Z"]
    a = ELEMENTS[symbol]["A"]
    return {
        "q_B": 1.0,
        "q_p": z / a,
        "q_n": (a - z) / a,
        "q_C": z * (z - 1.0) / (a ** (4.0 / 3.0)),
        "q_D": (a - 2.0 * z) / a,
    }


def q_values_for_material(material_id: str) -> dict[str, float]:
    material = MATERIALS[material_id]
    q = {"q_B": 0.0, "q_p": 0.0, "q_n": 0.0, "q_C": 0.0, "q_D": 0.0}
    for symbol, fraction in material["components"].items():
        element_q = q_values_for_element(symbol)
        for key in q:
            q[key] += fraction * element_q[key]
    return q


def material_ledger_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for material_id, material in MATERIALS.items():
        rows.append(
            {
                "material_id": material_id,
                "experiment": material["experiment"],
                "material_label": material["material_label"],
                "mass_fraction_components": ";".join(f"{symbol}:{fraction}" for symbol, fraction in material["components"].items()),
                "composition_source": material["composition_source"],
                "B_over_mu": material.get("B_over_mu", "MISSING_NOT_REPORTED_FOR_THIS_ROW"),
                "composition_status": material["composition_status"],
                "valid_for_claim": "false",
            }
        )
    return rows


def upgraded_charge_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for material_id, material in MATERIALS.items():
        q = q_values_for_material(material_id)
        rows.append(
            {
                "material_id": material_id,
                "experiment": material["experiment"],
                "q_B": f"{q['q_B']:.12g}",
                "q_p": f"{q['q_p']:.12g}",
                "q_n": f"{q['q_n']:.12g}",
                "q_C": f"{q['q_C']:.12g}",
                "q_D": f"{q['q_D']:.12g}",
                "B_over_mu": material.get("B_over_mu", "MISSING"),
                "charge_status": "UPGRADED_PROXY_FROM_SOURCE_BACKED_MATERIAL_CATEGORY",
                "valid_for_claim": "false",
            }
        )
    return rows


def confidence_rows() -> list[dict[str, Any]]:
    microscope_sigma = math.sqrt((2.3e-15) ** 2 + (1.5e-15) ** 2)
    return [
        {
            "confidence_id": "CONF3312_0_MICROSCOPE",
            "anchor_id": "WEP3306_0_MICROSCOPE_Ti_Pt",
            "eta_central": "-1.5e-15",
            "sigma_combined_proxy": f"{microscope_sigma:.12g}",
            "two_sided_95_proxy": f"{1.96 * microscope_sigma:.12g}",
            "confidence_source": MICROSCOPE_ARXIV,
            "confidence_status": "stat/syst combined in quadrature as proxy; full covariance not applied",
            "valid_for_claim": "false",
        },
        {
            "confidence_id": "CONF3312_1_EOTWASH",
            "anchor_id": "WEP3306_1_EOTWASH_Be_Ti",
            "eta_central": "0.3e-13",
            "sigma_combined_proxy": "1.8e-13",
            "two_sided_95_proxy": f"{1.96 * 1.8e-13:.12g}",
            "confidence_source": EOTWASH_ARXIV,
            "confidence_status": "abstract eta uncertainty used as proxy; separate systematic/covariance not fully applied",
            "valid_for_claim": "false",
        },
    ]


def pair_delta_rows() -> list[dict[str, Any]]:
    charges = {row["material_id"]: row for row in upgraded_charge_rows()}
    pairs = [
        ("PAIR3312_0_MICROSCOPE_PtRh10_TA6V", "MICROSCOPE_PtRh10", "MICROSCOPE_TA6V", "WEP3306_0_MICROSCOPE_Ti_Pt"),
        ("PAIR3312_1_EOTWASH_Be_Ti", "EOTWASH_Be", "EOTWASH_Ti", "WEP3306_1_EOTWASH_Be_Ti"),
    ]
    rows: list[dict[str, Any]] = []
    for pair_id, material_a, material_b, anchor_id in pairs:
        charge_a = charges[material_a]
        charge_b = charges[material_b]
        row = {
            "pair_id": pair_id,
            "anchor_id": anchor_id,
            "material_A": material_a,
            "material_B": material_b,
        }
        for key in ["q_B", "q_p", "q_n", "q_C", "q_D"]:
            row[f"Delta_{key}"] = f"{float(charge_a[key]) - float(charge_b[key]):.12g}"
        row["Delta_B_over_mu"] = (
            f"{float(charge_a['B_over_mu']) - float(charge_b['B_over_mu']):.12g}"
            if charge_a["B_over_mu"] != "MISSING" and charge_b["B_over_mu"] != "MISSING"
            else "MISSING_FOR_PAIR"
        )
        row["pair_status"] = "UPGRADED_NONCLAIM_DELTA"
        row["valid_for_claim"] = "false"
        rows.append(row)
    return rows


def bound_update_rows() -> list[dict[str, Any]]:
    confidence = {row["anchor_id"]: row for row in confidence_rows()}
    deltas = {row["anchor_id"]: row for row in pair_delta_rows()}
    rows: list[dict[str, Any]] = []
    for anchor_id, conf in confidence.items():
        delta = deltas[anchor_id]
        rows.append(
            {
                "update_id": f"BUP3312_{anchor_id}",
                "anchor_id": anchor_id,
                "pair_id": delta["pair_id"],
                "Delta_q_vector_upgraded": f"({delta['Delta_q_B']},{delta['Delta_q_p']},{delta['Delta_q_n']},{delta['Delta_q_C']},{delta['Delta_q_D']})",
                "Delta_B_over_mu": delta["Delta_B_over_mu"],
                "eta_sigma_proxy": conf["sigma_combined_proxy"],
                "eta_95_proxy": conf["two_sided_95_proxy"],
                "bound_template": "|A_i (s_i dot Delta_q_upgraded)| <= eta_bound/F(lambda,r)",
                "status": "UPGRADED_INPUT_NONCLAIM",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows(parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in parent_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "runner_id": "RUN3312_0_parent_Ai",
            "test": "parent Ai proof candidate exists",
            "result": "CANDIDATE_REVIEW_REQUIRED" if candidates else "NO_PARENT_Ai_PROMOTION",
            "detail": f"candidate_count={len(candidates)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3312_1_material_upgrade",
            "test": "WEP materials upgraded from single-element proxies where possible",
            "result": "PASS_NONCLAIM" if len(material_ledger_rows()) == 4 and len(pair_delta_rows()) == 2 else "FAIL",
            "detail": ";".join(row["material_id"] for row in material_ledger_rows()),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3312_2_confidence_upgrade",
            "test": "confidence proxy rows exist for MICROSCOPE and Eot-Wash",
            "result": "PASS_NONCLAIM" if len(confidence_rows()) == 2 else "FAIL",
            "detail": ";".join(row["confidence_id"] for row in confidence_rows()),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3312_3_claim_permission",
            "test": "WEP exact input rows claim-ready",
            "result": "REFUSE_CLAIM_PARENT_Ai_AND_FULL_ASSAY_COVARIANCE_MISSING",
            "detail": "A_i remains parent-unproven; exact isotope/alloy assay and full covariance are not applied",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in parent_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "gate_id": "GATE3312_0_parent_Ai",
            "claim": "A_i values are parent-proven",
            "requirements": "reviewed parent amplitude/source factor derivation for A_0 and A_2",
            "current_evidence": f"unreviewed_candidate_count={len(candidates)}",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3312_1_exact_materials",
            "claim": "WEP material charges are exact experimental charges",
            "requirements": "full alloy/isotope/purity assay and nuclear/EM binding model",
            "current_evidence": "source-backed categories and proxies only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3312_2_confidence",
            "claim": "eta bounds are final confidence-ready rows",
            "requirements": "paper covariance/systematics and chosen CL convention",
            "current_evidence": "proxy sigma/95 rows only",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in parent_rows if row["promotion_status"] == "CANDIDATE_REVIEW_REQUIRED"]
    return [
        {
            "decision_id": "DEC3312_0",
            "question": "Did 3312 prove A_i from parent factors?",
            "answer": "candidate review needed" if candidates else "no",
            "reason": "no reviewed parent amplitude/source-factor derivation is promoted",
            "next_action": "keep A_i explicit and continue with nonclaim WEP input improvements",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3312_1",
            "question": "Did 3312 improve WEP data plumbing?",
            "answer": "yes",
            "reason": "MICROSCOPE material rows are upgraded to PtRh10 vs TA6V categories and confidence rows are explicit; Eot-Wash Be/Ti B/mu anchor is staged",
            "next_action": "build a final nonclaim WEP matrix using upgraded deltas, then decide whether parent Ai or exact assay/covariance is the bottleneck",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3312_0_3313",
            "target_doc": "3313-Y5-R2FR-upgraded-WEP-matrix-with-material-confidence-rows-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3313_upgraded_WEP_matrix_with_material_confidence_rows.py",
            "objective": "rebuild the WEP linear matrix using upgraded material deltas and confidence rows, while keeping A_i/lambda/source factors explicit and nonclaim",
            "guardrails": "do not claim exact WEP safety until parent A_i, exact material assays, and confidence/covariance treatment are closed",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    parent_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    local_source_paths = [Path(row["path_or_url"]) for row in source_rows if row["source_type"] == "local_path"]
    external_rows = [row for row in source_rows if row["source_type"] == "external_primary"]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    materials = material_ledger_rows()
    charges = upgraded_charge_rows()
    confidence = confidence_rows()
    pairs = pair_delta_rows()
    updates = bound_update_rows()
    runners = runner_rows(parent_rows)
    gates = promotion_gate_rows(parent_rows)
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3312_0_sources_exist",
            "local cited paths exist and external source URLs are present",
            all(path.exists() for path in local_source_paths)
            and all(row["path_or_url"].startswith("https://") for row in external_rows),
            "",
        ),
        (
            "VAL3312_1_sources_parse",
            "all local cited source paths parse",
            all(parse_ok(path) for path in local_source_paths),
            "",
        ),
        (
            "VAL3312_2_outputs_parse",
            "all 3312 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3312_3_parent_Ai_audit_nonclaim",
            "parent Ai audit ran and remains nonclaim",
            bool(parent_rows) and all(row["valid_for_claim"] == "false" for row in parent_rows),
            f"rows={len(parent_rows)}",
        ),
        (
            "VAL3312_4_materials_upgraded",
            "material ledger includes PtRh10, TA6V, Be, and Ti",
            all(any(token in row["material_id"] for row in materials) for token in ["PtRh10", "TA6V", "Be", "Ti"]),
            "",
        ),
        (
            "VAL3312_5_charge_rows_complete",
            "upgraded charge rows include q_B/q_p/q_n/q_C/q_D",
            all(all(key in row for key in ["q_B", "q_p", "q_n", "q_C", "q_D"]) for row in charges),
            "",
        ),
        (
            "VAL3312_6_confidence_rows_present",
            "confidence rows include MICROSCOPE and Eot-Wash proxy 95 rows",
            any("MICROSCOPE" in row["confidence_id"] and row["two_sided_95_proxy"] for row in confidence)
            and any("EOTWASH" in row["confidence_id"] and row["two_sided_95_proxy"] for row in confidence),
            "",
        ),
        (
            "VAL3312_7_pair_deltas_upgraded",
            "pair delta rows exist for MICROSCOPE and Eot-Wash",
            len(pairs) == 2 and all(row["valid_for_claim"] == "false" for row in pairs),
            "",
        ),
        (
            "VAL3312_8_bound_updates_nonclaim",
            "bound update rows remain nonclaim",
            len(updates) == 2 and all(row["valid_for_claim"] == "false" for row in updates),
            "",
        ),
        (
            "VAL3312_9_runner_refuses_claim",
            "runner refuses claim until parent Ai/full assay/covariance are resolved",
            any(row["result"] == "REFUSE_CLAIM_PARENT_Ai_AND_FULL_ASSAY_COVARIANCE_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3312_10_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3312_11_next_target_upgraded_matrix",
            "next target is upgraded WEP matrix",
            "upgraded-WEP-matrix" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3312_12_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3312_13_overall",
            "3312 validation overall",
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


def render_doc(parent_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}` ({row['source_type']}): `{row['path_or_url']}` — role={row['role']}"
        for row in source_register_rows()
    )
    material_table = "\n".join(
        f"- `{row['material_id']}`: {row['material_label']} components `{row['mass_fraction_components']}`; status={row['composition_status']}"
        for row in material_ledger_rows()
    )
    confidence_table = "\n".join(
        f"- `{row['confidence_id']}`: eta={row['eta_central']}, sigma_proxy={row['sigma_combined_proxy']}, 95_proxy={row['two_sided_95_proxy']}."
        for row in confidence_rows()
    )
    pair_table = "\n".join(
        f"- `{row['pair_id']}`: Delta(q_B,q_p,q_n,q_C,q_D)=({row['Delta_q_B']},{row['Delta_q_p']},{row['Delta_q_n']},{row['Delta_q_C']},{row['Delta_q_D']}), Delta_B/mu={row['Delta_B_over_mu']}."
        for row in pair_delta_rows()
    )
    audit_table = "\n".join(
        f"- `{row['path']}`: status={row['promotion_status']}; evidence={row['evidence_lines']}"
        for row in parent_rows[:8]
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows(parent_rows)
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows(parent_rows)
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows(parent_rows)
    )
    next_row = next_target_rows()[0]

    return f"""# 3312 - Exact WEP material-confidence ledger or parent Ai proof under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint upgrades the WEP input side without making a claim.

MICROSCOPE is moved from crude element proxies toward source-backed material categories: `PtRh10` versus `TA6V` (`Ti-Al-V`). Eot-Wash keeps `Be/Ti` and adds the staged `B/mu` anchor.

Confidence handling is now explicit:

- MICROSCOPE combines stat/syst in quadrature as a proxy, then records a 1.96-sigma proxy.
- Eot-Wash records the abstract eta uncertainty as a proxy, with missing full covariance/systematic treatment called out.

No local-GR/source-coupling claim is promoted because `A_i`, exact isotope/alloy assay, full confidence/covariance treatment, and parent source factors remain open.

## Source Register

{source_table}

## Parent Ai Audit

{audit_table}

## Material Ledger

{material_table}

## Confidence Ledger

{confidence_table}

## Upgraded Pair Deltas

{pair_table}

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
    parent_rows = parent_ai_audit_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["parent_Ai"], parent_rows)
    write_csv(OUTPUTS["materials"], material_ledger_rows())
    write_csv(OUTPUTS["charges"], upgraded_charge_rows())
    write_csv(OUTPUTS["confidence"], confidence_rows())
    write_csv(OUTPUTS["pair_deltas"], pair_delta_rows())
    write_csv(OUTPUTS["bound_update"], bound_update_rows())
    write_csv(OUTPUTS["runner"], runner_rows(parent_rows))
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(parent_rows))
    write_csv(OUTPUTS["decision"], decision_rows(parent_rows))
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(parent_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, parent_rows))

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
