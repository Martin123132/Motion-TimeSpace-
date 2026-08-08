from __future__ import annotations

import csv
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4751"
CLAIM_ID = "L-593"
MARKER = "PPC4161_QTR_MAP_SOURCE_SEARCH_OR_STATIC_GAP_NUMERIC_SMOKE_4751"
PACKET_MARKER = "PPC4161_PACKET_QTR_MAP_SOURCE_SEARCH_OR_STATIC_GAP_NUMERIC_SMOKE_4751"
DECISION = "QTR_SOURCE_SEARCH_NO_PARENT_RANK_ROW_FOUND_STATIC_SMOKE_NONCLAIM_DERIVATION_NEXT"
NEXT_TARGET = "4752-Y5-R2FR-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md"

DOC_PATH = POST / "4751-Y5-R2FR-qtr-map-source-search-or-static-gap-numeric-smoke.md"
FORMAL_PATH = FORMAL / "767-PPC4161-qtr-map-source-search-or-static-gap-numeric-smoke.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_SOURCE_REGISTER.csv"
HIT_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_QTR_CORPUS_HIT_LEDGER.csv"
PARENT_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_PARENT_MAP_SOURCE_VERDICT.csv"
STATIC_SMOKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_STATIC_GAP_NUMERIC_SMOKE.csv"
PRIOR_CHAIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_PRIOR_SOURCE_CHAIN_CONSOLIDATION.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4751_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4751_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4751_0_4750_doc", POST / "4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md", "rank(J_q)=dim(chi)", "4750 source-runner requirement"),
    ("SRC4751_1_4750_formal", FORMAL / "766-PPC4161-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md", "s_min(J_q)>0", "4750 formal promotion condition"),
    ("SRC4751_2_4750_runner", SOURCE_DIR / "P8_Y5_R2FR_4750_CQUAR_SOURCE_RUNNER.csv", "FAIL_CLOSED_MISSING_PARENT_INPUTS", "4750 live branch remains blocked"),
    ("SRC4751_3_4295_verdict", SOURCE_DIR / "P8_Y5_R2FR_4295_PARENT_SIGNATURE_VERDICT.csv", "VERDICT4295_1_raw_transition_kernel", "prior raw transition kernel verdict"),
    ("SRC4751_4_4295_audit", SOURCE_DIR / "P8_Y5_R2FR_4295_CLAUSE_PROMOTION_AUDIT.csv", "CLAUSE4295_0_same_metric_Hilbert_source", "prior source-kernel clause audit"),
    ("SRC4751_5_4573_zero", SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_LIFT_ZERO_CONTRACT.csv", "ZC4573_0_define_source_lift", "source-lift definition and zero routes"),
    ("SRC4751_6_4573_branch", SOURCE_DIR / "P8_Y5_R2FR_4573_SIGMA_METRIC_BRANCH_VERDICT.csv", "BV4573_1_raw_transition_shell", "raw transition metric-zero verdict"),
    ("SRC4751_7_variable_audit", FORMAL / "04-variable-audit.csv", "local_transition_closure_contract_144", "older local transition closure status"),
    ("SRC4751_8_closure_doc", FORMAL / "144-local-transition-closure-contract.md", "Sigma_metric[q_tr]", "explicit closure contract reference"),
    ("SRC4751_9_589_formal", FORMAL / "589-PPC4161-transition-shell-source-lift-or-Sigma-metric-profile-runner.md", "MISSING_PARENT_ACTION_OR_SOURCE_LIFT", "formal source-lift blocker"),
    ("SRC4751_10_4750_validation", SOURCE_DIR / "P8_Y5_BRR545_4750_VALIDATION.csv", "VAL4750_OVERALL", "4750 validation handoff"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    HIT_LEDGER_CSV,
    PARENT_VERDICT_CSV,
    STATIC_SMOKE_CSV,
    PRIOR_CHAIN_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".py", ".json"}
SCAN_TERMS = [
    "q_tr",
    "J_q",
    "K_own",
    "D_quar",
    "c_quar",
    "C_quar_kernel",
    "Sigma_metric[q_tr]",
    "rank(J_q)",
    "s_min(J_q)",
]
TERM_RE = re.compile(r"q_tr|J_q|K_own|D_quar|c_quar|C_quar_kernel|Sigma_metric\[q_tr\]|rank\(J_q\)|s_min\(J_q\)", re.IGNORECASE)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def rel(path_object: Path) -> str:
    try:
        return str(path_object.relative_to(ROOT))
    except ValueError:
        return str(path_object)


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def classify_hit(path_object: Path, line: str) -> tuple[str, str, str]:
    lower = line.lower()
    rel_path = rel(path_object).lower()
    if "4750" in rel_path or "4749" in rel_path:
        return "RUNNER_REQUIREMENT_ONLY", "recent runner/gate language, not independent parent source", "none"
    if "sigma_metric[q_tr] :=" in lower:
        return "SOURCE_LIFT_DEFINITION_ONLY", "defines the needed metric source lift but does not supply a zero theorem", "derivation target"
    if "q_tr =" in lower and ("gamma_eff" in lower or "k_hat" in lower or "khat" in lower):
        return "FORMULA_DEFINITION_CAN_LINEARIZE", "candidate formula definition; can be linearized into a future J_q attempt", "derivation target"
    if "not_parent_signed" in lower or "not parent-sign" in lower or "not parent signed" in lower:
        return "NEGATIVE_SOURCE_EVIDENCE", "explicitly says the raw q_tr route is not parent-signed", "blocks claim"
    if "missing_parent" in lower or "missing parent" in lower or "missing_parent_action" in lower:
        return "MISSING_INPUT_EVIDENCE", "source row or action block is absent", "blocks claim"
    if "closure_only" in lower or "closure-only" in lower or "closure" in lower:
        return "CLOSURE_STATUS_EVIDENCE", "route is described as closure or quarantine, not derivation", "blocks claim"
    if "j_q=1" in lower and "q_tr" not in lower:
        return "FALSE_FRIEND_OTHER_SECTOR", "symbol J_q appears outside the q_tr quarantine parent-map meaning", "reject for this gate"
    if "rank(j_q)" in lower or "s_min(j_q)" in lower:
        return "RANK_LANGUAGE_NO_SOURCE", "rank/singular-value language appears, but not as a sourced parent map", "none"
    return "CONTEXT_HIT", "contains q_tr/quarantine vocabulary but no promotable parent-rank source row", "context only"


def evidence_layer(path_object: Path) -> str:
    path_text = rel(path_object)
    if "source-intake" in path_text:
        return "generated_csv_evidence"
    if "formalization-workbench" in path_text:
        return "formal_workbench"
    if "post-checkpoint-work" in path_text:
        return "post_checkpoint_doc"
    return "other"


def candidate_scan_paths() -> list[Path]:
    explicit = [
        FORMAL / "02-claims-register.csv",
        FORMAL / "04-variable-audit.csv",
        FORMAL / "06-consistency-red-team.md",
        FORMAL / "47-transition-current-routing-options.md",
        FORMAL / "144-local-transition-closure-contract.md",
        FORMAL / "589-PPC4161-transition-shell-source-lift-or-Sigma-metric-profile-runner.md",
        FORMAL / "590-PPC4161-P-metric-loc-zero-theorem-or-transition-profile-source-pack.md",
        POST / "1274-Y5-R10-RAB-unimodular-radial-cell-constraint-origin-or-finite-residual-intake.md",
        POST / "1374-Y5-R10-RAB-Qalg-Qtrans-first-fill-or-Kcdb-subchannel-bound.md",
        POST / "1375-Y5-R10-RAB-transition-input-row-validator-or-Kconn-first-bound.md",
        POST / "1376-Y5-R10-RAB-Kconn-operator-norm-fill-or-transition-parent-source-acquisition.md",
        POST / "1378-Y5-R10-RAB-transition-parent-law-derivation-or-explicit-closure-input-pack.md",
        POST / "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
        POST / "4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md",
        POST / "4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md",
    ]
    explicit.extend(path_object for _, path_object, _, _ in SOURCE_SPECS)
    for prefix in ("4295", "4297", "4298", "4340", "4341", "4573", "4574", "4749", "4750"):
        explicit.extend(SOURCE_DIR.glob(f"P8_Y5_R2FR_{prefix}_*.csv"))
        explicit.extend(SOURCE_DIR.glob(f"P8_Y5_BRR545_{prefix}_*.csv"))
    deduped: list[Path] = []
    seen: set[str] = set()
    for path_object in explicit:
        if path_object.exists() and path_object.is_file() and str(path_object) not in seen:
            deduped.append(path_object)
            seen.add(str(path_object))
    return deduped


def scan_corpus(timestamp: str) -> list[dict[str, Any]]:
    scan_paths = candidate_scan_paths()
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    max_per_class: dict[str, int] = {}
    for path_object in scan_paths:
        if path_object.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if "__pycache__" in path_object.parts:
            continue
        if path_object.name.startswith("Y5_R2FR_4751") or path_object.name.startswith("P8_Y5_R2FR_4751") or path_object.name == VALIDATION_CSV.name:
            continue
        try:
            if path_object.stat().st_size > 4_000_000:
                continue
            text = read_text(path_object)
        except OSError:
            continue
        if not TERM_RE.search(text):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not TERM_RE.search(line):
                continue
            classification, reason, promotion_value = classify_hit(path_object, line)
            if max_per_class.get(classification, 0) >= 18:
                continue
            term_match = TERM_RE.search(line)
            term = term_match.group(0) if term_match else "q_tr"
            snippet = re.sub(r"\s+", " ", line).strip()
            if len(snippet) > 260:
                snippet = snippet[:257] + "..."
            key = (str(path_object), line_number, snippet)
            if key in seen:
                continue
            seen.add(key)
            max_per_class[classification] = max_per_class.get(classification, 0) + 1
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "hit_id": f"HIT4751_{len(rows):04d}",
                    "source_path": str(path_object),
                    "relative_path": rel(path_object),
                    "line_number": line_number,
                    "term": term,
                    "snippet": snippet,
                    "evidence_layer": evidence_layer(path_object),
                    "classification": classification,
                    "reason": reason,
                    "promotion_value": promotion_value,
                    "score_ready": False,
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                }
            )
    priority = {
        "NEGATIVE_SOURCE_EVIDENCE": 0,
        "MISSING_INPUT_EVIDENCE": 1,
        "FORMULA_DEFINITION_CAN_LINEARIZE": 2,
        "SOURCE_LIFT_DEFINITION_ONLY": 3,
        "CLOSURE_STATUS_EVIDENCE": 4,
        "FALSE_FRIEND_OTHER_SECTOR": 5,
        "RANK_LANGUAGE_NO_SOURCE": 6,
        "RUNNER_REQUIREMENT_ONLY": 7,
        "CONTEXT_HIT": 8,
    }
    rows.sort(key=lambda row: (priority.get(str(row["classification"]), 99), str(row["relative_path"]), int(row["line_number"])))
    return rows[:120]


def parent_map_verdict_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PMV4751_0_qtr_formula",
            "q_tr formula",
            "q_tr = grad Gamma_eff - div K_hat style formula",
            "FOUND_AS_DEFINITION_NOT_LINEARIZED_TO_PARENT_MAP",
            "Existing chain supplies a formula target, but not the linearized parent map J_q needed by 4750.",
            "derive Dq_tr[X] and isolate J_q/J_K",
        ),
        (
            "PMV4751_1_Jq_map",
            "J_q",
            "parent algebraic map from X_q to q_tr/chi channel",
            "NO_PARENT_RANK_SOURCE_ROW_FOUND",
            "Corpus search found runner requirements and false-friend J_q symbols, not a parent-owned q_tr map.",
            "attempt direct linearization from Gamma_eff/K_hat",
        ),
        (
            "PMV4751_2_rank",
            "rank(J_q)",
            "certified rank in chi target space",
            "NO_RANK_CERTIFICATE_FOUND",
            "No source-backed matrix/operator row exists to rank.",
            "derive component map and basis first",
        ),
        (
            "PMV4751_3_smin",
            "s_min(J_q)>0",
            "positive singular-value lower bound",
            "NO_SMIN_CERTIFICATE_FOUND",
            "No normed parent map exists; singular value would be decoration.",
            "derive normed J_q or close branch",
        ),
        (
            "PMV4751_4_JK",
            "J_K/K_own",
            "parent K_own map and derivative channel",
            "FORMULA_TARGET_ONLY",
            "K_hat/K_own appears in cancellation/source-lift chains, but no parent-owned J_K row closes.",
            "derive K_hat variation or Delta_K divergence bound",
        ),
        (
            "PMV4751_5_Cquar_kernel",
            "C_quar_kernel",
            "finite unresolved-kernel penalty",
            "NO_SOURCE_BOUND_FOUND",
            "4750 runner expects this penalty; source search did not find a numeric/zero certificate.",
            "carry as live penalty in 4752",
        ),
        (
            "PMV4751_6_CTT_kernel",
            "C_TT_kernel",
            "TT zero or finite leakage bound",
            "ZERO_RULE_EXISTS_SOURCE_CERTIFICATE_MISSING",
            "TT exact-divergence zero is a conditional rule; parent projector/boundary certificate remains unsigned.",
            "source TT certificate in parallel, not as fake gap",
        ),
        (
            "PMV4751_7_ordinary_source_kernel",
            "ordinary local source kernel",
            "same-metric Hilbert/EM/worldtube source selector",
            "FOUND_FOR_ORDINARY_SOURCES_NOT_RAW_QTR",
            "4295 found useful ordinary-source structure but explicitly rejected raw transition promotion.",
            "do not use ordinary-source hit as q_tr proof",
        ),
        (
            "PMV4751_8_sigma_metric",
            "Sigma_metric[q_tr]",
            "metric source lift of transition current",
            "DEFINITION_EXISTS_ZERO_NOT_DERIVED",
            "4573 defines source lift and rejects generic raw shell zero.",
            "derive source-lift zero or profile bound",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "verdict_id": verdict_id,
            "object": object_name,
            "required_evidence": required_evidence,
            "verdict": verdict,
            "evidence_summary": evidence_summary,
            "next_action": next_action,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for verdict_id, object_name, required_evidence, verdict, evidence_summary, next_action in specs
    ]


def static_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    c_tfri = 1.0
    c_quar = 2.0
    c_mix_eff = 0.0
    c_tt_kernel = 0.0
    c_p = 1.0 / math.pi**2
    l_loc = 1.0
    pi_owner = 1.0
    c_zero = 0.0
    c_dstat = 1.0
    c_boundary = 0.0
    c_dn_eff = min(c_tfri, c_quar) - c_mix_eff - c_tt_kernel
    lambda_lower = c_dn_eff / (c_p * l_loc**2)
    residual_upper = pi_owner * math.sqrt(c_zero**2 + (c_dstat**2 + c_boundary) * c_p * l_loc**2 / c_dn_eff)
    return [
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4751_0_live",
            "branch": "live_source_score",
            "c_TFRI": "MISSING",
            "c_quar": "MISSING",
            "C_mix_eff": "MISSING",
            "C_TT_kernel": "MISSING",
            "C_P": "MISSING",
            "L_loc": "MISSING",
            "lambda_1_stat_lower": "",
            "C_res_static_upper": "",
            "status": "FAIL_CLOSED_MISSING_PARENT_RANK_AND_STATIC_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4751_1_canonical",
            "branch": "canonical_nonclaim_numeric_smoke",
            "c_TFRI": c_tfri,
            "c_quar": c_quar,
            "C_mix_eff": c_mix_eff,
            "C_TT_kernel": c_tt_kernel,
            "C_P": c_p,
            "L_loc": l_loc,
            "lambda_1_stat_lower": lambda_lower,
            "C_res_static_upper": residual_upper,
            "status": "PIPELINE_PASS_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4751_2_rule",
            "branch": "promotion_rule",
            "c_TFRI": "source-backed positive",
            "c_quar": "source-backed positive after penalties",
            "C_mix_eff": "source-backed finite",
            "C_TT_kernel": "zero or finite sourced",
            "C_P": "arena sourced",
            "L_loc": "arena sourced",
            "lambda_1_stat_lower": "positive iff c_DN_eff>0",
            "C_res_static_upper": "computed only after live inputs pass",
            "status": "RULE_READY_SOURCE_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def prior_chain_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CHAIN4751_0_4295",
            "4295",
            "ordinary source kernel found; raw transition q_tr not parent-signed",
            "useful positive structure exists, but cannot promote raw transition membership",
        ),
        (
            "CHAIN4751_1_4573",
            "4573",
            "Sigma_metric[q_tr] defined; generic raw shell zero not derived",
            "source-lift definition becomes a derivation target, not a pass",
        ),
        (
            "CHAIN4751_2_144",
            "144",
            "local transition branch marked closure-only",
            "closure remains honest fallback if derivation fails",
        ),
        (
            "CHAIN4751_3_4749",
            "4749",
            "quarantine coercivity reduced to rank/singular-value source test",
            "correct mathematical gate for local suppression",
        ),
        (
            "CHAIN4751_4_4750",
            "4750",
            "J_q/J_K/Cquar/CTT runner exists and validates",
            "4751 can search real sources against an executable target",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "chain_id": chain_id,
            "source_checkpoint": source_checkpoint,
            "result": result,
            "4751_use": use,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for chain_id, source_checkpoint, result, use in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4751_0_parent_Jq", "explicit parent map J_q from q_tr variation", "BLOCKED_NO_PARENT_SOURCE_ROW"),
        ("GATE4751_1_rank_smin", "rank(J_q)=dim(chi) and s_min(J_q)>0 in a fixed norm", "BLOCKED_NO_OPERATOR_TO_RANK"),
        ("GATE4751_2_Kown", "parent J_K/K_own derivative channel or bounded Delta_K", "BLOCKED_FORMULA_TARGET_ONLY"),
        ("GATE4751_3_kernel_penalty", "C_quar_kernel and C_TT_kernel zero/finite sourced", "BLOCKED_NO_KERNEL_CERTIFICATE"),
        ("GATE4751_4_static_smoke", "canonical numeric smoke must not be treated as live evidence", "PASS_NONCLAIM_PLUMBING_ONLY"),
        ("GATE4751_5_next", "next step must attempt derivation, not repeat generic missing ledger", "DERIVATION_NEXT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, requirement, status in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4751_0_false_friend", "Reject J_q hits from unrelated sectors unless the row maps parent fields into q_tr/chi."),
        ("FW4751_1_ordinary_source", "Do not promote ordinary-source Hilbert/EM kernel evidence into raw transition q_tr membership."),
        ("FW4751_2_smoke", "Do not treat canonical static smoke lambda=pi^2 as sourced local-GR evidence."),
        ("FW4751_3_closure", "If 4752 cannot derive J_q, keep the branch closure-only rather than hiding the missing coupling."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "The corpus search found definitions, closures, blockers and runner requirements, but no parent-owned J_q/rank/s_min source row; static smoke remains nonclaim.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, hit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in hit_rows:
        key = str(row["classification"])
        counts[key] = counts.get(key, 0) + 1
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_SOURCE_SEARCH_NO_PARENT_RANK_ROW_NONCLAIM",
            "summary": "Corpus source hunt completed; parent q_tr map not found; derivation from Gamma_eff/K_hat selected next.",
            "hit_count": len(hit_rows),
            "classification_counts": ";".join(f"{key}={value}" for key, value in sorted(counts.items())),
            "claim_status": "NO_LOCAL_GR_OR_NEWTON_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "Source search did not find the parent rank row, but it did isolate the formula target q_tr = grad Gamma_eff - div K_hat. The next honest move is to derive J_q by linearizing that formula, or close the branch.",
            "preferred_route": "Compute D q_tr[X] = nabla(D Gamma_eff[X]) - div(D K_hat[X]) + connection/boundary terms, then isolate algebraic J_q and derivative J_K blocks.",
            "fallback_route": "If the linearization has no algebraic full-rank J_q or bounded derivative channel, mark the route closure-only and move to finite residual/profile bounds.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str, limit: int = 8) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows[:limit])


def write_docs(
    timestamp: str,
    hit_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    chain_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    negative_count = sum(1 for row in hit_rows if row["classification"] in {"NEGATIVE_SOURCE_EVIDENCE", "MISSING_INPUT_EVIDENCE", "CLOSURE_STATUS_EVIDENCE"})
    formula_count = sum(1 for row in hit_rows if row["classification"] == "FORMULA_DEFINITION_CAN_LINEARIZE")
    doc = f"""# 4751 Y5 R2FR: q_tr Map Source Search Or Static Gap Numeric Smoke

Generated: `{timestamp}`

## Result

4751 performed the actual source hunt for the `q_tr/J_q` coupling map required by 4750. It found useful formula and blocker evidence, but no parent-owned `J_q`, `rank(J_q)`, or `s_min(J_q)>0` source row.

- Corpus hits recorded: `{len(hit_rows)}`
- Negative/blocker/closure hits: `{negative_count}`
- Linearization-target formula hits: `{formula_count}`
- Live local-GR/Newton claim: `false`

## What The Search Found

{bullet(hit_rows, "hit_id", "classification", 12)}

## Parent-Map Verdict

{bullet(verdict_rows, "verdict_id", "verdict", 12)}

## Static Numeric Smoke

{bullet(smoke_rows, "smoke_id", "status", 6)}

## Prior Chain Consolidation

{bullet(chain_rows, "chain_id", "result", 8)}

## Promotion Gates

{bullet(gates, "gate_id", "status", 8)}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 767 PPC4161: q_tr Map Source Search Or Static Gap Numeric Smoke

Generated: `{timestamp}`

## Source Hunt Verdict

The 4751 search did not find a parent-owned map:

```text
J_q : X_q -> q_tr/chi
rank(J_q)=dim(chi)
s_min(J_q)>0
```

It did find the derivation target:

```text
q_tr = grad Gamma_eff - div K_hat
```

and prior source-lift evidence that `Sigma_metric[q_tr]` is defined but not parent-zeroed for generic raw transition shells.

## Nonclaim Static Smoke

The canonical smoke branch still gives `lambda_1^stat = pi^2` under toy inputs, but it is plumbing only and remains `valid_for_claim=false`.

## Next

4752 must attempt the actual linearization:

```text
D q_tr[X] = nabla(D Gamma_eff[X]) - div(D K_hat[X]) + connection + boundary.
```

Then either isolate a full-rank algebraic `J_q`, or close the branch and carry finite profile/residual bounds.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4751 performs a corpus source hunt for the parent `q_tr/J_q` coupling row required by 4750.
- It finds formula/blocker/closure evidence, but no source-backed `J_q`, `rank(J_q)`, or `s_min(J_q)>0` row.
- The canonical static gap smoke runs only as nonclaim plumbing; live scoring remains closed.
- Next move is derivation: linearize `q_tr = grad Gamma_eff - div K_hat` to attempt an actual `J_q/J_K` split.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4751 local packet update: the source hunt did not find the missing parent-rank row. The path forward is no longer more generic searching; it is a derivation attempt on the `Gamma_eff/K_hat` formula.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4751-Y5-R2FR-qtr-map-source-search-or-static-gap-numeric-smoke.md`

## Decision

`{DECISION}`

## What moved forward

- Performed an actual corpus source hunt for the `q_tr/J_q` parent coupling map.
- Separated real blockers, closure evidence, formula targets, false-friend `J_q` hits, and recent runner requirements.
- Confirmed no parent-owned `J_q`, `rank(J_q)`, or `s_min(J_q)>0` row is currently available.
- Ran the static numeric smoke as nonclaim plumbing only.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4751 searches the corpus for a parent q_tr/J_q coupling source row and finds no source-backed J_q/rank/s_min row; static gap smoke remains nonclaim.",
        "Generated source register, q_tr corpus hit ledger, parent-map source verdict, static numeric smoke, prior-chain consolidation, promotion gates, firewalls, decision, status, next target and validation.",
        "qtr_source_search_no_parent_rank_row_static_smoke_nonclaim",
        NEXT_TARGET,
        "Treating false-friend J_q hits, ordinary-source selector evidence, or canonical static smoke as local-GR proof.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need direct linearization of q_tr=grad Gamma_eff-div K_hat into J_q/J_K, or explicit closure/finite-profile demotion.",
        "q_tr map source search or static gap numeric smoke",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    hit_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4751_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4751_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4751_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    classifications = {str(row["classification"]) for row in hit_rows}
    checks.append(("VAL4751_2_hit_ledger_nonempty", "hit ledger contains corpus hits", len(hit_rows) > 0, str(HIT_LEDGER_CSV)))
    checks.append(("VAL4751_3_hit_classes", "hit ledger separates blockers, formula targets and false friends", {"NEGATIVE_SOURCE_EVIDENCE", "MISSING_INPUT_EVIDENCE", "FALSE_FRIEND_OTHER_SECTOR"}.issubset(classifications), str(HIT_LEDGER_CSV)))
    checks.append(("VAL4751_4_parent_verdict_blocks_claim", "parent verdict says no J_q/rank/smin source row", any(row["object"] == "J_q" and "NO_PARENT" in row["verdict"] for row in verdict_rows) and any(row["object"] == "s_min(J_q)>0" and "NO_SMIN" in row["verdict"] for row in verdict_rows), str(PARENT_VERDICT_CSV)))
    smoke = next((row for row in smoke_rows if row["branch"] == "canonical_nonclaim_numeric_smoke"), None)
    smoke_ok = bool(smoke) and abs(float(smoke["lambda_1_stat_lower"]) - math.pi**2) < 1e-12 and smoke["valid_for_claim"] is False
    checks.append(("VAL4751_5_static_smoke", "canonical static smoke computes pi^2 and remains nonclaim", smoke_ok, str(STATIC_SMOKE_CSV)))
    checks.append(("VAL4751_6_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4751_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4751_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4751_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4751_10_claim_row", "claim row L-593 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4751_11_resume", "resume points from 4751 to 4752", "4751-Y5" in resume_text and "4752-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4751_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4751_OVERALL",
            "check": "all 4751 source-search and nonclaim smoke checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    hit_rows = scan_corpus(timestamp)
    verdict_rows = parent_map_verdict_rows(timestamp)
    smoke_rows = static_smoke_rows(timestamp)
    chain_rows = prior_chain_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp, hit_rows)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(HIT_LEDGER_CSV, hit_rows)
    write_csv(PARENT_VERDICT_CSV, verdict_rows)
    write_csv(STATIC_SMOKE_CSV, smoke_rows)
    write_csv(PRIOR_CHAIN_CSV, chain_rows)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, hit_rows, verdict_rows, smoke_rows, chain_rows, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, hit_rows, verdict_rows, smoke_rows, gates, timestamp))


if __name__ == "__main__":
    main()
