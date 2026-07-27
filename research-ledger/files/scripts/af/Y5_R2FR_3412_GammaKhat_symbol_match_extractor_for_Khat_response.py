from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3412-Y5-R2FR-GammaKhat-symbol-match-extractor-for-Khat-response-under-AX1090.md"

SOURCES = {
    "doc_3411": ROOT / "3411-Y5-R2FR-Khat-metric-response-identity-for-q_loc-Ward-zero-under-AX1090.md",
    "next_3411": OUT / "P8_Y5_R2FR_3411_NEXT_TARGET.csv",
    "symbol_audit_3411": OUT / "P8_Y5_R2FR_3411_CURRENT_SYMBOL_MATCH_AUDIT.csv",
    "contract_3411": OUT / "P8_Y5_R2FR_3411_KHAT_METRIC_RESPONSE_CONTRACT.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "residual_3411": OUT / "P8_Y5_R2FR_3411_RESIDUAL_IF_IDENTITY_FAILS.csv",
    "doc_515": ROOT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
    "doc_516": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
    "doc_597": ROOT / "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md",
    "doc_3008": ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md",
    "doc_3064": ROOT / "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md",
    "stress_rewrite_513": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "match_audit_2409": OUT / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "gamma_owner_2976": OUT / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "proof_gate_3064": OUT / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
    "residual_3064": OUT / "P8_Y5_R2FR_3064_QLOC_RESIDUAL_INTERFACE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3412_SOURCE_REGISTER.csv",
    "scan_summary": OUT / "P8_Y5_R2FR_3412_SCAN_SUMMARY.csv",
    "term_hits": OUT / "P8_Y5_R2FR_3412_TERM_HITS.csv",
    "candidate_symbol_extracts": OUT / "P8_Y5_R2FR_3412_CANDIDATE_SYMBOL_EXTRACTS.csv",
    "response_pair_test_matrix": OUT / "P8_Y5_R2FR_3412_RESPONSE_PAIR_TEST_MATRIX.csv",
    "construction_candidate_ranking": OUT / "P8_Y5_R2FR_3412_CONSTRUCTION_CANDIDATE_RANKING.csv",
    "symbol_match_verdict": OUT / "P8_Y5_R2FR_3412_SYMBOL_MATCH_VERDICT.csv",
    "next_target": OUT / "P8_Y5_R2FR_3412_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3412_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3412_VALIDATION.csv",
}

SCAN_EXTENSIONS = {".md", ".csv"}
EXCLUDED_PARTS = {"runs", ".venv-score", "__pycache__", "scripts"}
SELF_PATTERNS = {"3412-Y5-R2FR-GammaKhat", "P8_Y5_R2FR_3412", "Y5_R2FR_3412"}
MAX_FILE_BYTES = 2_500_000
MAX_HITS = 120
MAX_SCAN_FILES = 650
NAME_SCAN_PATTERN = re.compile(
    r"Gamma|Khat|QLOC|q_loc|GK|metric[-_ ]?response|Ward|Helmholtz|source[-_ ]?current",
    re.IGNORECASE,
)

TERM_PATTERNS = {
    "Gamma_eff": re.compile(r"Gamma[_ -]?eff|Γ_eff|Gamma0", re.IGNORECASE),
    "K_hat": re.compile(r"K[_ -]?hat|Khat|K_metric|K_gamma", re.IGNORECASE),
    "metric_response": re.compile(r"metric response|metric variation|delta\[sqrt\(-g\)|δ\[sqrt\(-g\)|functional metric", re.IGNORECASE),
    "S_GK": re.compile(r"S_GK|T_GK|Hilbert stress|Ward", re.IGNORECASE),
    "q_loc": re.compile(r"q_loc|P_loc", re.IGNORECASE),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in SCAN_EXTENSIONS:
        return False
    path_text = str(path)
    if any(part in path.parts for part in EXCLUDED_PARTS):
        return False
    if any(pattern in path_text for pattern in SELF_PATTERNS):
        return False
    try:
        return path.stat().st_size <= MAX_FILE_BYTES
    except OSError:
        return False


def classify_hit(line: str) -> str:
    lower = line.lower()
    if "not matched" in lower or "fail_for_current_claim" in lower or "no explicit" in lower:
        return "current_match_failure"
    if "2/sqrt" in lower and "gamma_eff" in lower and ("delta" in lower or "variation" in lower):
        return "metric_response_identity_contract"
    if "t_gk" in lower and "gamma" in lower and "k_hat" in lower:
        return "stress_rewrite_identity"
    if "gamma_eff =" in lower or "gamma_eff=" in lower or "gamma0" in lower:
        return "candidate_gamma_density"
    if "s_gk" in lower and ("int" in lower or "action" in lower or "density" in lower):
        return "candidate_action_density"
    if "k_hat" in lower or "khat" in lower or "k_metric" in lower:
        return "candidate_khat_symbol"
    return "context_hit"


def score_hit(line: str, flags: list[str], candidate_type: str) -> int:
    score = len(flags)
    if "Gamma_eff" in flags and "K_hat" in flags:
        score += 4
    if "metric_response" in flags:
        score += 3
    if candidate_type in {"candidate_gamma_density", "candidate_action_density", "metric_response_identity_contract"}:
        score += 3
    if candidate_type == "current_match_failure":
        score += 2
    return score


def scan_paths() -> tuple[list[Path], int]:
    paths: dict[str, Path] = {}
    for path in SOURCES.values():
        if path.exists() and should_scan(path):
            paths[str(path)] = path
    skipped_name = 0
    candidates: list[Path] = []
    for base in (ROOT, OUT):
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SCAN_EXTENSIONS:
                continue
            if not NAME_SCAN_PATTERN.search(path.name):
                skipped_name += 1
                continue
            if should_scan(path):
                candidates.append(path)
    for path in sorted(set(candidates), key=lambda item: str(item).lower()):
        if len(paths) >= MAX_SCAN_FILES:
            break
        paths[str(path)] = path
    ordered = sorted(paths.values(), key=lambda item: str(item).lower())
    return ordered, skipped_name


def scan_corpus() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    scanned_files = 0
    skipped_large = 0
    paths, skipped_name = scan_paths()
    for path in paths:
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                skipped_large += 1
                continue
        except OSError:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            continue
        scanned_files += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            flags = [term for term, pattern in TERM_PATTERNS.items() if pattern.search(line)]
            if not flags:
                continue
            candidate_type = classify_hit(line)
            score = score_hit(line, flags, candidate_type)
            excerpt = re.sub(r"\s+", " ", line.strip())
            if len(excerpt) > 280:
                excerpt = excerpt[:277] + "..."
            hits.append(
                {
                    "hit_id": f"HIT3412_{len(hits):04d}",
                    "source_path": str(path),
                    "line_number": line_number,
                    "candidate_type": candidate_type,
                    "term_flags": ";".join(flags),
                    "relevance_score": score,
                    "usable_as_current_definition": candidate_type in {"candidate_gamma_density", "candidate_action_density", "candidate_khat_symbol"},
                    "excerpt": excerpt,
                    "valid_for_claim": False,
                }
            )
    hits.sort(key=lambda row: (-int(row["relevance_score"]), row["source_path"], int(row["line_number"])))
    compact_hits = hits[:MAX_HITS]
    summary = {
        "scanned_files": scanned_files,
        "candidate_files": len(paths),
        "skipped_name_filter": skipped_name,
        "skipped_large_files": skipped_large,
        "total_hits": len(hits),
        "reported_hits": len(compact_hits),
        "gamma_hits": sum("Gamma_eff" in row["term_flags"].split(";") for row in hits),
        "khat_hits": sum("K_hat" in row["term_flags"].split(";") for row in hits),
        "metric_response_hits": sum("metric_response" in row["term_flags"].split(";") for row in hits),
    }
    return compact_hits, summary


SCAN_HITS, SCAN_SUMMARY = scan_corpus()


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3411": "conditional Ward route and current symbol-match failure",
        "next_3411": "declared 3412 extractor target",
        "symbol_audit_3411": "current Gamma_eff/Khat symbol-match audit",
        "contract_3411": "metric-response identity acceptance contract",
        "ward_3411": "conditional q_loc Ward-zero theorem",
        "residual_3411": "residual components if identity fails",
        "doc_515": "prior Gamma_eff/Khat match audit",
        "doc_516": "Gamma_eff owner candidates including response doublet",
        "doc_597": "reduced GK action owner route and current symbol-match failure",
        "doc_3008": "Gamma-Khat q_loc action existence route",
        "doc_3064": "GammaKhat q_loc proof gate and Khat identity bottleneck",
        "stress_rewrite_513": "algebraic stress divergence identity",
        "match_audit_2409": "current Khat metric-response match audit",
        "gamma_owner_2976": "Gamma_eff scalar-density owner audit",
        "proof_gate_3064": "action/Khat/Helmholtz/Euler/boundary gates",
        "residual_3064": "retained q_loc residual interface",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def scan_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "SS3412_0_corpus_scan",
            "scan_root": str(ROOT),
            "candidate_files": SCAN_SUMMARY["candidate_files"],
            "scanned_files": SCAN_SUMMARY["scanned_files"],
            "skipped_large_files": SCAN_SUMMARY["skipped_large_files"],
            "total_hits": SCAN_SUMMARY["total_hits"],
            "reported_hits": SCAN_SUMMARY["reported_hits"],
            "gamma_hits": SCAN_SUMMARY["gamma_hits"],
            "khat_hits": SCAN_SUMMARY["khat_hits"],
            "metric_response_hits": SCAN_SUMMARY["metric_response_hits"],
            "valid_for_claim": False,
        }
    ]


def term_hits() -> list[dict[str, Any]]:
    return SCAN_HITS or [
        {
            "hit_id": "HIT3412_NONE",
            "source_path": str(ROOT),
            "line_number": "",
            "candidate_type": "no_hits",
            "term_flags": "",
            "relevance_score": 0,
            "usable_as_current_definition": False,
            "excerpt": "No Gamma_eff/K_hat hits found by scanner.",
            "valid_for_claim": False,
        }
    ]


def candidate_symbol_extracts() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CSE3412_0_stress_rewrite",
            "candidate_type": "exact_algebraic_rewrite",
            "Gamma_eff_candidate": "Gamma_eff appears in T_GK^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "K_hat_candidate": "K_hat appears as the tensor subtracted from Gamma_eff g",
            "source_path": str(SOURCES["stress_rewrite_513"]),
            "metric_response_status": "ALgebraic_q_loc_rewrite_only_not_metric_response_proof",
            "current_definition_grade": "identity_context_not_action_owner",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CSE3412_1_response_doublet",
            "candidate_type": "constructive_Gamma_density_candidate",
            "Gamma_eff_candidate": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "K_hat_candidate": "K_hat would be defined as metric response of this density",
            "source_path": str(SOURCES["doc_516"]),
            "metric_response_status": "VIABLE_CONSTRUCTION_TEMPLATE_NOT_CURRENT_SYMBOL_MATCH",
            "current_definition_grade": "candidate_new_parent_clause",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CSE3412_2_reduced_observed_action",
            "candidate_type": "reduced_action_candidate",
            "Gamma_eff_candidate": "S_GK^red[Q_obs] with Gamma_eff=gamma(g_obs,Phi_red,D Phi_red,topological data)",
            "K_hat_candidate": "K_hat:=K_gamma under the reduced metric-response convention",
            "source_path": str(SOURCES["doc_597"]),
            "metric_response_status": "DEFINITION_POSSIBLE_EXISTING_MATCH_FAILED",
            "current_definition_grade": "candidate_if_adopted",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CSE3412_3_positive_auxiliary",
            "candidate_type": "positive_auxiliary_density_candidate",
            "Gamma_eff_candidate": "Gamma_eff=V(Phi)+1/2 G_AB(Phi) nabla Phi^A nabla Phi^B",
            "K_hat_candidate": "K_hat would be kinetic/elastic metric response",
            "source_path": str(SOURCES["doc_516"]),
            "metric_response_status": "VIABLE_TEMPLATE_BUT_SOURCE_CURRENT_ZERO_NOT_DERIVED",
            "current_definition_grade": "candidate_new_field_route",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CSE3412_4_topological_improvement",
            "candidate_type": "topological_boundary_density_candidate",
            "Gamma_eff_candidate": "Gamma_eff from normalized boundary/topological density or exact form",
            "K_hat_candidate": "K_hat would be boundary/improvement stress response",
            "source_path": str(SOURCES["doc_516"]),
            "metric_response_status": "BULK_PROMISING_BOUNDARY_FLUX_OPEN",
            "current_definition_grade": "candidate_boundary_route",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CSE3412_5_current_symbol_match",
            "candidate_type": "current_corpus_match_attempt",
            "Gamma_eff_candidate": "no explicit source-backed scalar density owner found for current symbols",
            "K_hat_candidate": "no explicit K_hat metric-response derivation found for current symbols",
            "source_path": str(SOURCES["doc_515"]),
            "metric_response_status": "FAIL_CURRENT_SYMBOL_MATCH",
            "current_definition_grade": "not_claim_ready",
            "valid_for_claim": False,
        },
    ]


def response_pair_test_matrix() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "RPT3412_0_explicit_Gamma_density",
            "test": "A concrete scalar density sqrt(-g) Gamma_eff[g,Phi,nablaPhi,D,...] is present for current MTS.",
            "evidence": "scanner finds contracts/candidates, but the current-symbol audit says formal candidate only",
            "result": "FAIL_CURRENT",
            "repair": "extract or declare the actual parent density terms with units and branch domain",
            "valid_for_claim": False,
        },
        {
            "test_id": "RPT3412_1_explicit_Khat_formula",
            "test": "Current K_hat expression is explicit enough to compare tensor terms.",
            "evidence": "scanner finds K_hat in identities and contracts, not a sourced full tensor definition",
            "result": "FAIL_CURRENT",
            "repair": "extract K_hat components and boundary terms from original parent equations",
            "valid_for_claim": False,
        },
        {
            "test_id": "RPT3412_2_metric_variation",
            "test": "K_hat equals 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} in one sign convention.",
            "evidence": "2409/3064/3411 all retain Delta_K=K_hat-K_metric[Gamma_eff]",
            "result": "FAIL_CURRENT_SYMBOL_MATCH",
            "repair": "compute K_metric from a selected candidate density and compare symbol-by-symbol",
            "valid_for_claim": False,
        },
        {
            "test_id": "RPT3412_3_Helmholtz",
            "test": "T_GK passes second-variation symmetry as a real Hilbert stress.",
            "evidence": "Helmholtz is not checked for current symbols",
            "result": "UNSIGNED",
            "repair": "run Helmholtz symmetry on any extracted candidate pair",
            "valid_for_claim": False,
        },
        {
            "test_id": "RPT3412_4_Ward_zero",
            "test": "q_loc can be killed by Ward/Euler/boundary closure.",
            "evidence": "3411 derives this conditionally, but symbol match and boundary/projector gates fail",
            "result": "BLOCKED",
            "repair": "pass RPT3412_0 through RPT3412_3 plus projector/boundary gates",
            "valid_for_claim": False,
        },
        {
            "test_id": "RPT3412_5_construction_route",
            "test": "A construction route exists if current symbols fail.",
            "evidence": "response-doublet and reduced-action candidates exist in 516/597",
            "result": "PASS_CONDITIONAL_CONSTRUCTION_TARGET",
            "repair": "attempt response-doublet parent-density construction before residual demotion",
            "valid_for_claim": False,
        },
    ]


def construction_candidate_ranking() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "candidate": "response_doublet_quadratic_density",
            "route": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), K_hat:=metric response",
            "why_ranked_here": "best chance to derive double-zero and kill q_loc without tuning alpha3",
            "main_risk": "Z^A must be the actual physical q_loc residual basis and Y5/Y6 source/stress rows must be covered",
            "next_action": "construct the density and compute K_metric symbolically enough to compare to K_hat",
            "valid_for_claim": False,
        },
        {
            "rank": 2,
            "candidate": "reduced_observed_action",
            "route": "S_GK^red[Q_obs] with Gamma_eff=gamma and K_hat=K_gamma",
            "why_ranked_here": "clean Ward theorem if adopted; keeps variables in observed quotient",
            "main_risk": "may be a new closure/adoption rather than derivation from original MTS",
            "next_action": "test whether existing symbols factor through Q_obs rather than redefining them",
            "valid_for_claim": False,
        },
        {
            "rank": 3,
            "candidate": "positive_auxiliary_energy_density",
            "route": "Gamma_eff=V(Phi)+1/2 G_AB nabla Phi^A nabla Phi^B",
            "why_ranked_here": "positive operator/no-hair could silence local residuals",
            "main_risk": "adds a fifth-force carrier unless source-free and boundary no-hair are proved",
            "next_action": "use only if response doublet cannot cover source/stress rows",
            "valid_for_claim": False,
        },
        {
            "rank": 4,
            "candidate": "topological_improvement_density",
            "route": "T_GK exact/improvement stress with zero compact local flux",
            "why_ranked_here": "could kill bulk q_loc elegantly",
            "main_risk": "boundary/source-measure flux is exactly where local GR can leak",
            "next_action": "defer until boundary flux owner is stronger",
            "valid_for_claim": False,
        },
        {
            "rank": 5,
            "candidate": "explicit_residual_bound_branch",
            "route": "retain Delta_K, H_GK, J_GK, B_GK, P_loc_commutator and bound them",
            "why_ranked_here": "honest fallback if no derivation route closes",
            "main_risk": "becomes a bounded modified-gravity closure rather than derived local GR",
            "next_action": "use only after construction attempt fails",
            "valid_for_claim": False,
        },
    ]


def symbol_match_verdict() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "SMV3412_0_current_match",
            "question": "Does the current corpus already provide a claim-grade Gamma_eff/K_hat metric-response pair?",
            "answer": "NO",
            "evidence": "contracts and candidates exist; current-symbol audits still fail Gamma owner and Khat metric-response match",
            "claim_effect": "q_loc Ward zero cannot be claimed",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "SMV3412_1_derivation_route",
            "question": "Is there still a non-stupid derivation route worth pursuing?",
            "answer": "YES_RESPONSE_DOUBLET_OR_REDUCED_ACTION_CANDIDATE",
            "evidence": "516 and 597 supply coherent construction templates that would define K_hat by metric response rather than fit it",
            "claim_effect": "attempt construction next before demoting q_loc to pure residual bound",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "SMV3412_2_no_closure_assumption",
            "question": "Can we just adopt K_hat:=K_metric and claim the route?",
            "answer": "NO",
            "evidence": "that would be a new parent action clause unless it is shown to reproduce the current MTS K_hat symbols and source/readout gates",
            "claim_effect": "construction must be tested, not declared",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3413-Y5-R2FR-response-doublet-Gamma-density-construction-test-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3413_response_doublet_Gamma_density_construction_test.py",
            "objective": "construct the response-doublet Gamma_eff density candidate, compute its metric-response K_metric template, and test whether it can cover the retained q_loc/Y5/Y6 residual basis without smuggling source couplings",
            "why_next": "3412 found no current claim-grade symbol match, but the response-doublet route is the best derivation-first repair before demoting q_loc",
            "valid_for_claim": False,
        },
        {
            "target_id": "3414-Y5-R2FR-q_loc-residual-bound-demotion-if-construction-fails-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3414_q_loc_residual_bound_demotion_if_construction_fails.py",
            "objective": "if the response-doublet construction fails, demote q_loc to explicit residual components Delta_K, H_GK, J_GK, B_GK and P_loc_commutator with empirical bound rows",
            "why_next": "this keeps the work testable and prevents the Ward route from becoming a closure assumption",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3412_0",
            "script": str(Path(__file__).resolve()),
            "scan_root": str(ROOT),
            "scanned_files": SCAN_SUMMARY["scanned_files"],
            "reported_hits": SCAN_SUMMARY["reported_hits"],
            "claim_status": "SYMBOL_EXTRACTION_AND_MATCH_AUDIT_ONLY",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    test_rows = generated["response_pair_test_matrix"]
    verdict_rows = generated["symbol_match_verdict"]
    ranking_rows = generated["construction_candidate_ranking"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    hits_present = SCAN_SUMMARY["gamma_hits"] > 0 and SCAN_SUMMARY["khat_hits"] > 0
    current_match_failed = any(row.get("result") == "FAIL_CURRENT_SYMBOL_MATCH" for row in test_rows)
    construction_present = any(row.get("result") == "PASS_CONDITIONAL_CONSTRUCTION_TARGET" for row in test_rows)
    verdict_no = any(row.get("verdict_id") == "SMV3412_0_current_match" and row.get("answer") == "NO" for row in verdict_rows)
    response_doublet_ranked = any(row.get("rank") == 1 and "response_doublet" in row.get("candidate", "") for row in ranking_rows)
    next_construct = "response-doublet" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3412_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3412_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3412_2_scan_hits",
            "check": "scan found both Gamma_eff and K_hat evidence",
            "passed": hits_present,
            "detail": f"gamma_hits={SCAN_SUMMARY['gamma_hits']}; khat_hits={SCAN_SUMMARY['khat_hits']}",
        },
        {
            "check_id": "VAL3412_3_no_overclaim",
            "check": "all generated rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "extractor does not claim q_loc zero or local GR",
        },
        {
            "check_id": "VAL3412_4_current_match_failed",
            "check": "current metric-response symbol match remains failed",
            "passed": current_match_failed and verdict_no,
            "detail": "SMV3412_0 says no current claim-grade pair",
        },
        {
            "check_id": "VAL3412_5_construction_route",
            "check": "construction route is retained rather than immediate closure-only demotion",
            "passed": construction_present and response_doublet_ranked,
            "detail": "response-doublet construction ranked first",
        },
        {
            "check_id": "VAL3412_6_next_target",
            "check": "next target attempts response-doublet construction",
            "passed": next_construct,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3412_7_overall",
            "check": "3412 symbol extractor is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3412 - GammaKhat Symbol Match Extractor For Khat Response",
            "## Summary\n"
            "- This checkpoint scans the current `post-checkpoint-work` corpus for `Gamma_eff`, `K_hat`, metric-response, `S_GK/T_GK`, and `q_loc` evidence.\n"
            "- It finds contracts and construction candidates, but no claim-grade current-symbol match where `K_hat` is already proven to be the metric response of `sqrt(-g) Gamma_eff`.\n"
            "- That means the Ward-zero route remains alive but unpromoted.\n"
            "- The best derivation-first next move is to test the response-doublet Gamma-density construction before demoting q_loc to a pure bound residual.",
            "## Scan Summary\n" + md_table(generated["scan_summary"]),
            "## Candidate Symbol Extracts\n" + md_table(generated["candidate_symbol_extracts"]),
            "## Response Pair Test Matrix\n" + md_table(generated["response_pair_test_matrix"]),
            "## Construction Candidate Ranking\n" + md_table(generated["construction_candidate_ranking"]),
            "## Symbol Match Verdict\n" + md_table(generated["symbol_match_verdict"]),
            "## Top Term Hits\n" + md_table(generated["term_hits"][:25]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "No current-symbol `Gamma_eff/K_hat` match was found. That is not the end of the derivation route: the response-doublet density is a real constructive target, "
            "but it must now be built and tested against q_loc/Y5/Y6 source and stress rows. If it cannot cover those, q_loc must be explicitly bounded.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "scan_summary": scan_summary(),
        "term_hits": term_hits(),
        "candidate_symbol_extracts": candidate_symbol_extracts(),
        "response_pair_test_matrix": response_pair_test_matrix(),
        "construction_candidate_ranking": construction_candidate_ranking(),
        "symbol_match_verdict": symbol_match_verdict(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3412 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
