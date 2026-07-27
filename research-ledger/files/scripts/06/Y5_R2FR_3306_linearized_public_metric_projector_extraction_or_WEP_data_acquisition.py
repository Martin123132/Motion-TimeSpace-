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

DOC = ROOT / "3306-Y5-R2FR-linearized-public-metric-projector-extraction-or-WEP-data-acquisition-under-AX1090.md"

SRC_3305_DOC = ROOT / "3305-Y5-R2FR-parent-projector-proof-for-Xi-universality-or-WEP-bound-pack-under-AX1090.md"
SRC_3305_DERIVATION = OUT / "P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv"
SRC_3305_AUDIT = OUT / "P8_Y5_R2FR_3305_PROJECTOR_PROOF_CLAUSE_AUDIT.csv"
SRC_3305_WEP = OUT / "P8_Y5_R2FR_3305_WEP_BOUND_PACK_SCHEMA.csv"
SRC_3305_NEXT = OUT / "P8_Y5_R2FR_3305_NEXT_TARGET.csv"
SRC_3305_VALIDATION = OUT / "P8_Y5_BRR545_3305_VALIDATION.csv"

MICROSCOPE_URL = "https://arxiv.org/abs/2209.15487"
MICROSCOPE_DOI = "10.1103/PhysRevLett.129.121102"
EOTWASH_URL = "https://arxiv.org/abs/0712.0607"
EOTWASH_DOI = "10.1103/PhysRevLett.100.041101"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3306_SOURCE_REGISTER.csv",
    "scan": OUT / "P8_Y5_R2FR_3306_PARENT_PROJECTOR_SCAN.csv",
    "projector_contract": OUT / "P8_Y5_R2FR_3306_PROJECTOR_EXTRACTION_CONTRACT.csv",
    "wep_sources": OUT / "P8_Y5_R2FR_3306_WEP_SOURCE_ANCHORS.csv",
    "wep_mapping": OUT / "P8_Y5_R2FR_3306_WEP_TO_DELTA_XI_MAPPING.csv",
    "runner": OUT / "P8_Y5_R2FR_3306_PROJECTOR_OR_WEP_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3306_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3306_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3306_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3306_VALIDATION.csv",
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

PROJECTOR_PATTERNS = {
    "public_metric_linearization": [
        r"delta\s+g",
        r"\bh_mu_nu\b",
        r"linearized\s+metric",
        r"metric\s+perturbation",
        r"public\s+metric",
        r"g_pub",
    ],
    "scalar_projector": [
        r"e\^\(0\)",
        r"scalar\s+projector",
        r"trace\s+projector",
        r"spin[-\s]?0",
        r"phi_0",
        r"lambda_0",
    ],
    "spin2_projector": [
        r"e\^\(2\)",
        r"spin[-\s]?2",
        r"massive\s+spin",
        r"transverse[-\s]?traceless",
        r"TT\s+projector",
        r"lambda_2",
    ],
    "matter_projection": [
        r"T_H",
        r"Hilbert\s+stress",
        r"delta\s+S_m",
        r"source\s+projection",
        r"mode\s+charge",
        r"Xi_0",
        r"Xi_2",
    ],
}


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
        (SRC_3305_DOC, "3305 projector proof handoff", ["delta S_m", "Q_0[A]", "WEP"]),
        (SRC_3305_DERIVATION, "3305 conditional projector derivation", ["PIP3305_1_matter_variation", "PIP3305_2_mode_charges"]),
        (SRC_3305_AUDIT, "3305 projector audit", ["PCA3305_2_linearized_projectors", "false"]),
        (SRC_3305_WEP, "3305 WEP pack schema", ["eta_bound", "Delta_Xi"]),
        (SRC_3305_NEXT, "3305 next target", ["linearized-public-metric-projector", "WEP-data-acquisition"]),
        (SRC_3305_VALIDATION, "3305 validation", ["VAL3305_10_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(local_sources):
        rows.append(
            {
                "source_id": f"SRC3306_{index}",
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
                "source_id": "SRC3306_6",
                "source_type": "external_primary",
                "path_or_url": MICROSCOPE_URL,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "MICROSCOPE final WEP Ti/Pt bound anchor",
                "evidence_hits": "arXiv abstract reports no violation and Eotvos parameter eta(Ti,Pt)=(-1.5 +/- 2.3(stat) +/- 1.5(syst))*10^-15; DOI 10.1103/PhysRevLett.129.121102",
                "valid_for_claim": "false",
            },
            {
                "source_id": "SRC3306_7",
                "source_type": "external_primary",
                "path_or_url": EOTWASH_URL,
                "exists_or_url_present": "true",
                "parse_ok": "true",
                "role": "Eot-Wash Be/Ti rotating torsion balance WEP anchor",
                "evidence_hits": "arXiv abstract reports differential acceleration of Be and Ti toward Earth eta_Earth(Be-Ti)=(0.3 +/- 1.8)*10^-13; DOI 10.1103/PhysRevLett.100.041101",
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


def line_evidence(text: str, patterns: list[str], limit: int = 5) -> str:
    compiled_patterns = [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns]
    snippets: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in compiled_patterns):
            snippets.append(f"L{line_number}:{compact(line, 300)}")
        if len(snippets) >= limit:
            break
    return " | ".join(snippets) if snippets else "NO_LINE_EVIDENCE"


def projector_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    all_patterns = [pattern for patterns in PROJECTOR_PATTERNS.values() for pattern in patterns]
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            hits: dict[str, list[str]] = {}
            for clause, patterns in PROJECTOR_PATTERNS.items():
                matched = [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]
                if matched:
                    hits[clause] = matched
            if not hits:
                continue
            clause_count = len(hits)
            has_all_projector_pieces = all(
                clause in hits
                for clause in ["public_metric_linearization", "scalar_projector", "spin2_projector", "matter_projection"]
            )
            parent_owned = ROOT not in path.parents
            rows.append(
                {
                    "path": str(path),
                    "scan_root": str(root),
                    "parent_owned": bool_str(parent_owned),
                    "clause_count": clause_count,
                    "clauses_hit": ";".join(hits.keys()),
                    "patterns_hit": ";".join(pattern for patterns in hits.values() for pattern in patterns),
                    "candidate_status": "PROJECTOR_CANDIDATE_NEEDS_REVIEW" if has_all_projector_pieces and parent_owned else "PARTIAL_OR_GENERATED_LANGUAGE",
                    "promotes_Xi_universality": "false",
                    "evidence_lines": line_evidence(text, all_patterns),
                    "valid_for_claim": "false",
                }
            )
    rows.sort(key=lambda row: (row["candidate_status"] == "PROJECTOR_CANDIDATE_NEEDS_REVIEW", int(row["clause_count"])), reverse=True)
    if not rows:
        rows.append(
            {
                "path": "NO_PROJECTOR_LANGUAGE_FOUND",
                "scan_root": ";".join(str(root) for root in SCAN_ROOTS),
                "parent_owned": "false",
                "clause_count": 0,
                "clauses_hit": "",
                "patterns_hit": "",
                "candidate_status": "MISSING_PARENT_PROJECTOR",
                "promotes_Xi_universality": "false",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "valid_for_claim": "false",
            }
        )
    return rows[:80]


def projector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PEC3306_0_linearized_metric",
            "required_object": "delta g_pub_mu_nu = e^(m)_mu_nu h_m + e^(0)_mu_nu phi_0 + e^(2)_mu_nu H_2 + residuals",
            "must_show": "public metric readout decomposes into massless, scalar, and spin-2 local modes with no hidden matter-only metric",
            "current_status": "NOT_EXTRACTED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PEC3306_1_scalar_projector",
            "required_object": "e^(0)_mu_nu",
            "must_show": "scalar projector equals pure metric trace projector in the local nonrelativistic limit or derive its replacement",
            "current_status": "NOT_EXTRACTED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PEC3306_2_spin2_projector",
            "required_object": "e^(2)_mu_nu",
            "must_show": "massive spin-2 projector equals pure metric spin-2 projector in the local nonrelativistic limit or derive its replacement",
            "current_status": "NOT_EXTRACTED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PEC3306_3_source_projection",
            "required_object": "Q_i[A] = (1/2) integral_A sqrt(-g) T_H^mu_nu e^(i)_mu_nu",
            "must_show": "matter sees finite modes only through the same public metric variation",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PEC3306_4_universality_acceptance",
            "required_object": "Xi_i[A]=1 for all A",
            "must_show": "projector/source/readout combination is body independent after EM/Poynting/binding-energy accounting",
            "current_status": "NOT_PROVEN",
            "valid_for_claim": "false",
        },
    ]


def wep_source_anchor_rows() -> list[dict[str, Any]]:
    return [
        {
            "anchor_id": "WEP3306_0_MICROSCOPE_Ti_Pt",
            "experiment": "MICROSCOPE final result",
            "source_url": MICROSCOPE_URL,
            "doi": MICROSCOPE_DOI,
            "year": 2022,
            "test_body_pair": "Ti/Pt alloys",
            "attractor_source": "Earth",
            "eta_central": "-1.5e-15",
            "eta_stat_uncertainty": "2.3e-15",
            "eta_syst_uncertainty": "1.5e-15",
            "eta_bound_interpretation": "measurement anchor; convert to chosen confidence bound before claim use",
            "range_regime": "Earth-satellite orbital scale; not a direct short-range Yukawa alpha(lambda) curve",
            "confidence_level": "reported statistical and systematic uncertainties; claim use requires explicit CL convention",
            "extraction_method": "source-backed abstract/manual anchor, not digitized curve",
            "current_status": "SOURCE_BACKED_NONCLAIM_ANCHOR",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "WEP3306_1_EOTWASH_Be_Ti",
            "experiment": "Eot-Wash rotating torsion balance",
            "source_url": EOTWASH_URL,
            "doi": EOTWASH_DOI,
            "year": 2008,
            "test_body_pair": "Be/Ti",
            "attractor_source": "Earth",
            "eta_central": "0.3e-13",
            "eta_stat_uncertainty": "1.8e-13",
            "eta_syst_uncertainty": "MISSING_SEPARATE_SYSTEMATIC",
            "eta_bound_interpretation": "measurement anchor; use paper covariance/systematics before claim use",
            "range_regime": "laboratory/Earth-source WEP; not a full lambda-dependent bound curve",
            "confidence_level": "reported one-sigma-style uncertainty in abstract; claim use requires full paper convention",
            "extraction_method": "source-backed abstract/manual anchor, not digitized curve",
            "current_status": "SOURCE_BACKED_NONCLAIM_ANCHOR",
            "valid_for_claim": "false",
        },
    ]


def wep_mapping_rows() -> list[dict[str, Any]]:
    return [
        {
            "mapping_id": "WMAP3306_0_scalar",
            "uses_anchor": "WEP3306_0_MICROSCOPE_Ti_Pt;WEP3306_1_EOTWASH_Be_Ti",
            "residual_quantity": "Delta_Xi_0[A,B]",
            "acceptance_template": "|alpha0_star Xi_0[E] Delta_Xi_0[A,B] (1+r/lambda_0) exp(-r/lambda_0)| <= eta_bound(A,B,E,lambda_0)",
            "missing_before_claim": "alpha0_star; lambda_0; Xi_0[E]; material source charges; confidence convention; range transfer",
            "current_status": "BOUND_SCHEMA_ONLY",
            "valid_for_claim": "false",
        },
        {
            "mapping_id": "WMAP3306_1_spin2",
            "uses_anchor": "WEP3306_0_MICROSCOPE_Ti_Pt;WEP3306_1_EOTWASH_Be_Ti",
            "residual_quantity": "Delta_Xi_2[A,B]",
            "acceptance_template": "|alpha2_star Xi_2[E] Delta_Xi_2[A,B] (1+r/lambda_2) exp(-r/lambda_2)| <= eta_bound(A,B,E,lambda_2)",
            "missing_before_claim": "alpha2_star; lambda_2; Xi_2[E]; material source charges; confidence convention; range transfer",
            "current_status": "BOUND_SCHEMA_ONLY",
            "valid_for_claim": "false",
        },
        {
            "mapping_id": "WMAP3306_2_combined",
            "uses_anchor": "WEP3306_0_MICROSCOPE_Ti_Pt;WEP3306_1_EOTWASH_Be_Ti",
            "residual_quantity": "eta_AB,E",
            "acceptance_template": "|sum_i alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i)| <= eta_bound",
            "missing_before_claim": "all scalar and spin-2 quantities plus treatment of cancellations/correlations",
            "current_status": "BOUND_SCHEMA_ONLY",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projector_candidates = [row for row in scan_rows if row["candidate_status"] == "PROJECTOR_CANDIDATE_NEEDS_REVIEW"]
    wep_anchors = wep_source_anchor_rows()
    source_backed_anchors = [
        row
        for row in wep_anchors
        if row["source_url"].startswith("https://")
        and row["eta_central"] != ""
        and row["test_body_pair"]
        and row["attractor_source"]
    ]
    return [
        {
            "runner_id": "RUN3306_0_projector_scan",
            "test": "parent projector candidates found",
            "result": "CANDIDATES_NEED_REVIEW" if projector_candidates else "NO_PARENT_PROJECTOR_PROMOTION",
            "detail": f"candidate_count={len(projector_candidates)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3306_1_WEP_source_anchors",
            "test": "source-backed WEP anchors present",
            "result": "PASS_NONCLAIM" if len(source_backed_anchors) >= 2 else "FAIL",
            "detail": ";".join(row["anchor_id"] for row in source_backed_anchors),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3306_2_WEP_claim_permission",
            "test": "WEP rows can be used as claim bounds",
            "result": "REFUSE_CLAIM_RANGE_AND_COUPLINGS_MISSING",
            "detail": "lambda_i, alpha_i_star, Xi_i[E], material charge model, and confidence convention are not filled",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projector_candidates = [row for row in scan_rows if row["candidate_status"] == "PROJECTOR_CANDIDATE_NEEDS_REVIEW"]
    return [
        {
            "gate_id": "GATE3306_0_projector_promote",
            "claim": "parent public-metric projectors e^(0), e^(2) are extracted and prove Xi universality",
            "requirements": "reviewed parent candidate with metric linearization, scalar projector, spin-2 projector, and matter projection all in one source",
            "current_evidence": f"unreviewed_candidate_count={len(projector_candidates)}",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3306_1_WEP_bound_use",
            "claim": "WEP anchors bound Delta_Xi residuals",
            "requirements": "sourced eta bound, material/source model, lambda range mapping, alpha_star values, confidence convention",
            "current_evidence": "source anchors staged only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3306_2_local_GR_source_gate",
            "claim": "source-projection gate is closed for local GR",
            "requirements": "GATE3306_0 true or GATE3306_1 true",
            "current_evidence": "neither proof nor bound claim is closed",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projector_candidates = [row for row in scan_rows if row["candidate_status"] == "PROJECTOR_CANDIDATE_NEEDS_REVIEW"]
    if projector_candidates:
        answer = "candidate evidence found but not promoted"
        next_action = "manually audit the top projector candidates before WEP scoring"
    else:
        answer = "no parent projector candidate found strong enough to review"
        next_action = "continue finite branch using WEP anchors as nonclaim data plumbing while deriving projectors"
    return [
        {
            "decision_id": "DEC3306_0",
            "question": "Did 3306 extract parent public-metric projectors e^(0), e^(2)?",
            "answer": answer,
            "candidate_count": len(projector_candidates),
            "reason": "keyword scan cannot promote projector theorem; explicit reviewed projector algebra is required",
            "next_action": next_action,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3306_1",
            "question": "Did 3306 improve the bound route?",
            "answer": "yes, it added source-backed MICROSCOPE and Eot-Wash WEP anchors as nonclaim rows",
            "candidate_count": len(projector_candidates),
            "reason": "Delta_Xi residuals now have real experiment anchors, but no range/coupling/material charge map yet",
            "next_action": "derive material charge model or acquire full WEP bound tables before scoring",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projector_candidates = [row for row in scan_rows if row["candidate_status"] == "PROJECTOR_CANDIDATE_NEEDS_REVIEW"]
    if projector_candidates:
        objective = "manually adjudicate the parent projector candidate rows and either promote a real e^(0)/e^(2) projector theorem or reject them into the WEP bound branch"
    else:
        objective = "build the material/source charge model that maps Delta_Xi_0 and Delta_Xi_2 onto MICROSCOPE/Eot-Wash WEP anchors without assuming universal composition independence"
    return [
        {
            "next_id": "NEXT3306_0_3307",
            "target_doc": "3307-Y5-R2FR-material-source-charge-model-for-DeltaXi-WEP-bounds-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3307_material_source_charge_model_for_DeltaXi_WEP_bounds.py",
            "objective": objective,
            "guardrails": "do not score WEP anchors as claims until lambda_i, alpha_i_star, Xi_i[E], material charge differences, and confidence convention are explicit",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    scan_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    local_source_paths = [Path(row["path_or_url"]) for row in source_rows if row["source_type"] == "local_path"]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    projector_contract = projector_contract_rows()
    wep_anchors = wep_source_anchor_rows()
    wep_mapping = wep_mapping_rows()
    runners = runner_rows(scan_rows)
    gates = promotion_gate_rows(scan_rows)
    next_rows = next_target_rows(scan_rows)

    checks = [
        (
            "VAL3306_0_sources_exist",
            "all local cited source paths exist and external URLs are present",
            all(path.exists() for path in local_source_paths)
            and all(row["path_or_url"].startswith("https://") for row in source_rows if row["source_type"] == "external_primary"),
            "",
        ),
        (
            "VAL3306_1_sources_parse",
            "all local cited source paths parse",
            all(parse_ok(path) for path in local_source_paths),
            "",
        ),
        (
            "VAL3306_2_outputs_parse",
            "all 3306 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3306_3_scan_ran",
            "projector scan produced rows",
            bool(scan_rows),
            f"rows={len(scan_rows)}",
        ),
        (
            "VAL3306_4_projector_contract_complete",
            "projector extraction contract includes metric, scalar, spin2, source, and universality objects",
            all(
                any(token in row["required_object"] for row in projector_contract)
                for token in ["delta g_pub", "e^(0)", "e^(2)", "Q_i[A]", "Xi_i[A]"]
            ),
            "",
        ),
        (
            "VAL3306_5_WEP_anchor_sources_complete",
            "WEP anchors include source URLs, material pairs, attractors, and eta values",
            all(
                row["source_url"].startswith("https://")
                and row["test_body_pair"]
                and row["attractor_source"]
                and "e-" in row["eta_central"]
                for row in wep_anchors
            ),
            "",
        ),
        (
            "VAL3306_6_WEP_anchors_nonclaim",
            "WEP anchors remain non-claim until range/coupling/material mapping is filled",
            all(row["valid_for_claim"] == "false" for row in wep_anchors)
            and any("REFUSE_CLAIM" in row["result"] for row in runners),
            "",
        ),
        (
            "VAL3306_7_mapping_covers_scalar_spin2_combined",
            "WEP mapping covers scalar, spin2, and combined residuals",
            all(
                any(token in row["residual_quantity"] for row in wep_mapping)
                for token in ["Delta_Xi_0", "Delta_Xi_2", "eta_AB"]
            ),
            "",
        ),
        (
            "VAL3306_8_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3306_9_next_target_material_charge",
            "next target is material/source charge model for DeltaXi WEP bounds",
            "material-source-charge-model" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3306_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3306_11_overall",
            "3306 validation overall",
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
        f"- `{row['source_id']}` ({row['source_type']}): `{row['path_or_url']}` — role={row['role']}"
        for row in source_register_rows()
    )
    scan_table = "\n".join(
        f"- `{row['path']}`: clauses={row['clauses_hit'] or 'none'}; status={row['candidate_status']}; evidence={row['evidence_lines']}"
        for row in scan_rows[:10]
    )
    contract_table = "\n".join(
        f"- `{row['contract_id']}` `{row['required_object']}`: {row['must_show']} Status: `{row['current_status']}`."
        for row in projector_contract_rows()
    )
    anchor_table = "\n".join(
        f"- `{row['anchor_id']}`: {row['experiment']} `{row['test_body_pair']}` toward `{row['attractor_source']}`, eta={row['eta_central']} stat={row['eta_stat_uncertainty']} syst={row['eta_syst_uncertainty']}, source={row['source_url']}"
        for row in wep_source_anchor_rows()
    )
    mapping_table = "\n".join(
        f"- `{row['mapping_id']}` `{row['residual_quantity']}`: `{row['acceptance_template']}` Missing: {row['missing_before_claim']}."
        for row in wep_mapping_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows(scan_rows)
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows(scan_rows)
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows(scan_rows)
    )
    next_row = next_target_rows(scan_rows)[0]

    return f"""# 3306 - Linearized public-metric projector extraction or WEP data acquisition under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint searched for parent-owned linearized public-metric projectors and staged real WEP anchors for the fallback route.

No `Xi_i[A]=1` theorem is promoted. Keyword/projector candidates, if any, require manual algebraic review; the scan alone cannot prove `e^(0)_mu_nu` or `e^(2)_mu_nu`.

The WEP/source-composition branch now has source-backed nonclaim anchors:

- MICROSCOPE final Ti/Pt result: `eta(Ti,Pt)=(-1.5 +/- 2.3_stat +/- 1.5_syst) x 10^-15`.
- Eot-Wash Be/Ti result: `eta_Earth(Be-Ti)=(0.3 +/- 1.8) x 10^-13`.

They are not claim bounds yet because `lambda_i`, `alpha_i_star`, material source charges, source-body charges, and confidence conventions are still missing.

## Source Register

{source_table}

## Projector Scan

{scan_table}

## Projector Extraction Contract

{contract_table}

## WEP Source Anchors

{anchor_table}

## WEP-to-DeltaXi Mapping

{mapping_table}

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
    scan_rows = projector_scan_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["scan"], scan_rows)
    write_csv(OUTPUTS["projector_contract"], projector_contract_rows())
    write_csv(OUTPUTS["wep_sources"], wep_source_anchor_rows())
    write_csv(OUTPUTS["wep_mapping"], wep_mapping_rows())
    write_csv(OUTPUTS["runner"], runner_rows(scan_rows))
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(scan_rows))
    write_csv(OUTPUTS["decision"], decision_rows(scan_rows))
    write_csv(OUTPUTS["next"], next_target_rows(scan_rows))

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
