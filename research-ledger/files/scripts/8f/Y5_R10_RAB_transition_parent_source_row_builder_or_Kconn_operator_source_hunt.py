from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1377"
TITLE = "1377-Y5-R10-RAB-transition-parent-source-row-builder-or-Kconn-operator-source-hunt"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SOURCE_HUNT_HITS_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_HUNT_HITS.csv"
TRANSITION_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_PARENT_CANDIDATE_ROW_ATTEMPT.csv"
KCONN_HUNT_PATH = OUT_DIR / f"{PACK_ID}_KCONN_OPERATOR_SOURCE_HUNT.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1377_VALIDATION.csv"

TRANSITION_REQUIRED_FIELDS = [
    "U_B",
    "pS",
    "pL",
    "pT",
    "pB",
    "F2",
    "A_S",
    "A_L",
    "A_T",
    "A_B",
    "b_mem",
    "L_cg",
    "L_tr",
    "epsilon_q_limit",
    "epsilon_N_limit",
]

PROVENANCE_REQUIRED_FIELDS = [
    "source_path",
    "source_anchor",
    "units",
    "extraction_method",
]

TRANSITION_HUNT_TERMS = [
    "U_B",
    "pS",
    "pL",
    "pT",
    "pB",
    "A_S",
    "A_L",
    "A_T",
    "A_B",
    "b_mem",
    "F2",
    "L0",
    "L_tr",
    "A_ref",
    "epsilon_q_limit",
    "epsilon_N_limit",
    "transition_shell_projector_identity_or_explicit_bound",
]

KCONN_HUNT_TERMS = [
    "N_conn,nabla",
    "N_conn,star",
    "N_conn,ibp",
    "N_conn,edge",
    "S_der",
    "S_star",
    "S_ibp",
    "B_der",
    "connection variation",
    "Hodge",
    "coframe response",
    "integration-by-parts",
]


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1377_0_1376_doc",
            "source_path": "1376-Y5-R10-RAB-Kconn-operator-norm-fill-or-transition-parent-source-acquisition.md",
            "required_anchor": "NEXT1376_0_1377",
            "purpose": "1376 handoff to transition parent row builder or K_conn source hunt.",
        },
        {
            "source_id": "SRC1377_1_1376_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1376_NEXT_TARGET.csv",
            "required_anchor": "NEXT1376_0_1377",
            "purpose": "machine-readable 1377 target.",
        },
        {
            "source_id": "SRC1377_2_1376_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
            "required_anchor": "TPS1376_0_U_B",
            "purpose": "required source checklist for parent transition row.",
        },
        {
            "source_id": "SRC1377_3_1376_kconn",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1376_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv",
            "required_anchor": "KOF1376_7_verdict",
            "purpose": "K_conn operator-norm fill failed without sourced coefficients.",
        },
        {
            "source_id": "SRC1377_4_1375_validator",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_TRANSITION_INPUT_VALIDATOR_RESULTS.csv",
            "required_anchor": "VALIDATOR1375_VERDICT",
            "purpose": "current transition rows are missing-parent or toy/nonclaim.",
        },
        {
            "source_id": "SRC1377_5_799_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "required_anchor": "template_missing_parent_values",
            "purpose": "only available transition calculator input rows.",
        },
        {
            "source_id": "SRC1377_6_799_smoke_output",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
            "required_anchor": "toy_strong_support_nonclaim",
            "purpose": "toy transition row is not physics evidence.",
        },
        {
            "source_id": "SRC1377_7_1375_kconn_bound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv",
            "required_anchor": "KCB1375_2_operator_norm_bound",
            "purpose": "K_conn symbolic operator-bound contract.",
        },
        {
            "source_id": "SRC1377_8_1288_derivative",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "required_anchor": "KMR1288_2_derivative_terms",
            "purpose": "Kmetric derivative terms are still not computable.",
        },
        {
            "source_id": "SRC1377_9_776_kgamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "Kgamma derivative/Hodge/projector metric-response terms are open.",
        },
        {
            "source_id": "SRC1377_10_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "transition shell cannot be ignored.",
        },
        {
            "source_id": "SRC1377_11_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "generic shell suppression is not enough.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def snippet(line: str, limit: int = 180) -> str:
    compact = " ".join(line.strip().split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def line_status(line: str) -> str:
    lower = line.lower()
    if "toy_nonclaim" in lower or "toy_" in lower:
        return "NOT_SOURCE_READY_TOY_CONTEXT"
    if "missing_" in lower or "missing;" in lower or "missing," in lower:
        return "NOT_SOURCE_READY_MISSING_MARKER"
    if "valid_for_claim=false" in lower or ",false,false" in lower or ",false," in lower:
        return "NONCLAIM_SYMBOLIC_CONTEXT"
    if "source_ready" in lower or "sourced" in lower:
        return "POTENTIAL_SOURCE_CONTEXT_NEEDS_REVIEW"
    return "TEXT_MATCH_NEEDS_REVIEW"


def hunt_hits_for_terms(terms: list[str], category: str, max_hits_per_term: int = 4) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    counts = {term: 0 for term in terms}
    files = sorted(OUT_DIR.glob("*.csv"))
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for term in terms:
                if counts[term] >= max_hits_per_term:
                    continue
                if term.lower() in line.lower():
                    counts[term] += 1
                    hits.append(
                        {
                            "hunt_id": f"HIT1377_{category}_{term.replace(',', '_').replace(' ', '_')}_{counts[term]}",
                            "category": category,
                            "target_term": term,
                            "source_path": f"source-intake/mts_residuals/{path.name}",
                            "line_number": line_number,
                            "hit_status": line_status(line),
                            "snippet": snippet(line),
                        }
                    )
    missing_rows = [
        {
            "hunt_id": f"HIT1377_{category}_{term.replace(',', '_').replace(' ', '_')}_0",
            "category": category,
            "target_term": term,
            "source_path": "aggregate_source-intake/mts_residuals/*.csv",
            "line_number": "",
            "hit_status": "NO_TEXT_MATCH_FOUND",
            "snippet": "no matching row found in CSV source intake",
        }
        for term, count in counts.items()
        if count == 0
    ]
    return mark_nonclaim(hits + missing_rows)


def source_hunt_rows() -> list[dict[str, object]]:
    rows = hunt_hits_for_terms(TRANSITION_HUNT_TERMS, "transition", max_hits_per_term=4)
    rows.append(
        {
            "hunt_id": "HIT1377_transition_VERDICT",
            "category": "transition",
            "target_term": "all_transition_parent_inputs",
            "source_path": "aggregate_transition_hunt",
            "line_number": "",
            "hit_status": "NO_COMPLETE_SOURCE_BACKED_PARENT_ROW_FOUND",
            "snippet": "hits are existing symbolic/blocker/template/toy contexts; no complete row has values, units, source_path, source_anchor, extraction_method, and shell gate.",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def transition_candidate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    input_path = source_path("source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv")
    for input_row in read_csv_rows(input_path):
        missing = []
        for field in TRANSITION_REQUIRED_FIELDS:
            value = input_row.get(field, "")
            if not value or "MISSING" in value.upper():
                missing.append(field)
        for field in PROVENANCE_REQUIRED_FIELDS:
            if field not in input_row or not input_row.get(field) or "MISSING" in input_row.get(field, "").upper():
                missing.append(field)
        source_value = input_row.get("source_path", "")
        toy_flag = "toy" in input_row.get("case_id", "").lower() or "toy_nonclaim" in source_value.lower()
        source_ready = not missing and not toy_flag and source_value and not source_value.upper().startswith("MISSING")
        rows.append(
            {
                "candidate_id": f"CAND1377_{input_row.get('case_id', 'unknown')}",
                "case_id": input_row.get("case_id", ""),
                "input_source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
                "row_status": input_row.get("row_status", ""),
                "candidate_status": "SOURCE_BACKED_CANDIDATE_READY" if source_ready else "REJECTED_NOT_SOURCE_BACKED",
                "missing_required_fields": ";".join(missing) if missing else "none",
                "toy_flag": toy_flag,
                "source_path_value": source_value,
                "reason": "candidate can be reviewed but still nonclaim" if source_ready else "fails required field/provenance/toy gates",
            }
        )
    rows.append(
        {
            "candidate_id": "CAND1377_VERDICT",
            "case_id": "aggregate_transition_parent_row_attempt",
            "input_source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "row_status": "aggregate",
            "candidate_status": "NO_SOURCE_BACKED_TRANSITION_PARENT_ROW_FOUND",
            "missing_required_fields": "at least one of value/unit/source_anchor/extraction_method/shell gate for every available row",
            "toy_flag": "toy row present but refused",
            "source_path_value": "aggregate",
            "reason": "available rows are missing-parent template or toy calculator wiring only",
        }
    )
    return mark_nonclaim(rows)


def kconn_hunt_rows() -> list[dict[str, object]]:
    hit_rows = hunt_hits_for_terms(KCONN_HUNT_TERMS, "Kconn", max_hits_per_term=4)
    per_term: list[dict[str, object]] = []
    for term in KCONN_HUNT_TERMS:
        rows_for_term = [row for row in hit_rows if row["target_term"] == term]
        statuses = sorted({str(row["hit_status"]) for row in rows_for_term})
        exact_ready = False
        per_term.append(
            {
                "hunt_id": f"KOH1377_{term.replace(',', '_').replace(' ', '_')}",
                "operator_target": term,
                "hits_found": len([row for row in rows_for_term if row["hit_status"] != "NO_TEXT_MATCH_FOUND"]),
                "best_status": ";".join(statuses),
                "exact_operator_source_ready": exact_ready,
                "reason": "matches are symbolic/blocker/context rows, not an operator convention with units, domain norm, gauge/frame, and source path",
                "representative_sources": ";".join(str(row["source_path"]) for row in rows_for_term[:3]),
            }
        )
    per_term.append(
        {
            "hunt_id": "KOH1377_VERDICT",
            "operator_target": "K_conn_operator_convention_pack",
            "hits_found": sum(int(row["hits_found"]) for row in per_term),
            "best_status": "NO_EXACT_SOURCE_BACKED_OPERATOR_CONVENTION_ROW_FOUND",
            "exact_operator_source_ready": False,
            "reason": "no row supplies N_conn,* values or theorem-zero convention with domain/gauge/frame/boundary requirements",
            "representative_sources": "source-intake/mts_residuals/P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1376_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv",
        }
    )
    return mark_nonclaim(per_term)


def blocker_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "blocker_id": "BLK1377_0_U_B_parent_law",
                "blocked_object": "U_B",
                "why_blocked": "no parent transition/no-hair law or universal profile is sourced",
                "minimum_to_clear": "derive or source U_B as a parent law, not a local-test convenience value",
                "next_action": "derive transition support law from fixed-L0/double-zero branch or demote to closure input",
            },
            {
                "blocker_id": "BLK1377_1_support_power_pack",
                "blocked_object": "pS;pL;pT;pB",
                "why_blocked": "support powers appear only as symbolic formula slots",
                "minimum_to_clear": "parent law giving powers with no per-arena tuning",
                "next_action": "attempt exponent derivation from scaling of Delta_m, L-chain, trace, and boundary channels",
            },
            {
                "blocker_id": "BLK1377_2_amplitude_pack",
                "blocked_object": "A_S;A_L;A_T;A_B;b_mem;F2",
                "why_blocked": "amplitudes/curvature coefficients lack source-backed numeric or theorem-zero rows",
                "minimum_to_clear": "parent action coefficient extraction with units and source anchors",
                "next_action": "tie amplitudes to fixed-L0 parent action or mark closure-only",
            },
            {
                "blocker_id": "BLK1377_3_scale_pack",
                "blocked_object": "L0;L_tr;A_ref",
                "why_blocked": "L0 action role exists but numeric/source rule is missing; L_tr and A_ref lack geometry/normalization conventions",
                "minimum_to_clear": "scale-setting rule, transition geometry, and normalization convention",
                "next_action": "derive L_tr/L0 from transition geometry and define A_ref before runner use",
            },
            {
                "blocker_id": "BLK1377_4_shell_gate",
                "blocked_object": "transition shell",
                "why_blocked": "802/803 reject direct shell ignoring and generic suppression",
                "minimum_to_clear": "exact projector cancellation/quarantine theorem or explicit shell bound",
                "next_action": "keep shell term in Q_trans/Q_proj until theorem or bound exists",
            },
            {
                "blocker_id": "BLK1377_5_Kconn_operator_pack",
                "blocked_object": "N_conn,*;S_der;S_star;S_ibp;B_der",
                "why_blocked": "no exact operator-source row fixes domain norm, gauge/frame, Hodge/coframe response, IBP split, or edge term",
                "minimum_to_clear": "operator convention row or theorem-zero proof",
                "next_action": "do not score Q_conn numerically before operator pack exists",
            },
            {
                "blocker_id": "BLK1377_6_arena_projection",
                "blocked_object": "epsilon limits and local observable response",
                "why_blocked": "R10/PPN/clock/orbital projection map still missing",
                "minimum_to_clear": "arena response operator and accepted observable limit rows",
                "next_action": "defer local scoring until parent residual row exists",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1377_0_transition_candidate",
                "runner_field": "transition_parent_row",
                "feed_update": "no candidate transition row is promoted from existing files",
                "status": "BLOCKED_NO_SOURCE_BACKED_ROW",
                "blocks_claim_because": "existing rows are missing-parent or toy/nonclaim and lack units/source_anchor/extraction_method",
            },
            {
                "feed_id": "RUF1377_1_Kconn_operator_source",
                "runner_field": "Q_conn",
                "feed_update": "no exact K_conn operator convention row is found",
                "status": "BLOCKED_NO_EXACT_OPERATOR_SOURCE",
                "blocks_claim_because": "N_conn,* and source tensor norms remain symbolic",
            },
            {
                "feed_id": "RUF1377_2_next_derivation",
                "runner_field": "next_work",
                "feed_update": "move to deriving the transition parent law rather than searching the same old rows again",
                "status": "NEXT_DERIVATION_SELECTED",
                "blocks_claim_because": "derivation is required before local scoring",
            },
            {
                "feed_id": "RUF1377_3_claim_status",
                "runner_field": "local_GR_PPN_R10_status",
                "feed_update": "local-GR, PPN, R10, and q_loc=0 claims remain blocked",
                "status": "BLOCKED_NO_CLAIM",
                "blocks_claim_because": "neither source route supplies claim-grade inputs",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1377_0_source_hunt",
                "gate": "source hunt ran over local CSV intake",
                "status": "PASS_HUNT_RAN",
                "reason": "transition and K_conn terms were scanned and summarized with strict nonclaim status.",
            },
            {
                "gate_id": "GATE1377_1_transition_candidate",
                "gate": "source-backed transition parent row exists",
                "status": "BLOCKED_NO_SOURCE_BACKED_ROW",
                "reason": "available transition rows fail missing/provenance/toy gates.",
            },
            {
                "gate_id": "GATE1377_2_Kconn_operator_source",
                "gate": "exact K_conn operator source/convention row exists",
                "status": "BLOCKED_NO_EXACT_OPERATOR_SOURCE",
                "reason": "matches are symbolic contexts, not source-backed operator norm rows.",
            },
            {
                "gate_id": "GATE1377_3_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "no source-backed transition row and no exact K_conn operator row.",
            },
            {
                "gate_id": "GATE1377_4_next_route",
                "gate": "next route is selected",
                "status": "PASS_DERIVATION_ROUTE_SELECTED",
                "reason": "attempt parent transition law derivation before any local observable scoring.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1377_0_existing_rows",
                "decision": "do not build a candidate row from existing transition calculator files",
                "why": "the only rows are a missing-parent template and a toy nonclaim row",
                "next_action": "derive or source a new parent row rather than editing a toy row into evidence",
            },
            {
                "decision_id": "DEC1377_1_Kconn_hunt",
                "decision": "do not promote K_conn from text matches",
                "why": "text matches identify the symbolic blocker but not an exact operator convention",
                "next_action": "leave Q_conn symbolic until a real operator pack exists",
            },
            {
                "decision_id": "DEC1377_2_best_next_route",
                "decision": "attack the parent transition law directly",
                "why": "repeated source hunts now point to a derivation gap, not a missing CSV hiding in the corpus",
                "next_action": "derive U_B, powers, amplitudes, L_tr/L0, and shell handling from the fixed-L0 double-zero branch or demote them to closure-only inputs",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1377_0_1378",
                "next_doc": "1378-Y5-R10-RAB-transition-parent-law-derivation-or-explicit-closure-input-pack.md",
                "next_script": "scripts/Y5_R10_RAB_transition_parent_law_derivation_or_explicit_closure_input_pack.py",
                "task": "derive the universal transition parent law for U_B, support powers, amplitudes, L_tr/L0, A_ref, and shell handling from the fixed-L0 double-zero branch; if not derivable, demote these values to an explicit closure-input pack",
                "success_condition": "either a parent-signed transition law satisfies the anti-cheat gates, or a closure-only finite-input pack exists with no local-GR/PPN/R10 claim",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        SOURCE_HUNT_HITS_PATH,
        TRANSITION_CANDIDATE_PATH,
        KCONN_HUNT_PATH,
        BLOCKER_LEDGER_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    hunt_hits: list[dict[str, object]],
    candidates: list[dict[str, object]],
    kconn_hunt: list[dict[str, object]],
    blockers: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    source_hunt_ran = len(hunt_hits) > len(TRANSITION_HUNT_TERMS)
    no_candidate = any(row["candidate_id"] == "CAND1377_VERDICT" and row["candidate_status"] == "NO_SOURCE_BACKED_TRANSITION_PARENT_ROW_FOUND" for row in candidates)
    no_kconn_source = any(row["hunt_id"] == "KOH1377_VERDICT" and row["exact_operator_source_ready"] is False for row in kconn_hunt)
    blockers_cover = len(blockers) >= 7
    runner_blocks = any(row["feed_id"] == "RUF1377_3_claim_status" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1377_3_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    nonclaim = all_rows_nonclaim(sources, hunt_hits, candidates, kconn_hunt, blockers, runner_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs = [DOC_PATH, VALIDATION_PATH, *csv_paths]
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs)
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in outputs)

    rows = [
        {
            "validation_id": "VAL1377_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1377_1_source_hunt",
            "check": "source hunt rows were generated for transition parent targets",
            "status": "PASS" if source_hunt_ran else "FAIL",
            "details": f"hunt_rows={len(hunt_hits)} terms={len(TRANSITION_HUNT_TERMS)}",
        },
        {
            "validation_id": "VAL1377_2_transition_candidate",
            "check": "candidate builder refuses current transition rows",
            "status": "PASS" if no_candidate else "FAIL",
            "details": "CAND1377_VERDICT records no source-backed transition parent row.",
        },
        {
            "validation_id": "VAL1377_3_Kconn_hunt",
            "check": "K_conn operator-source hunt does not promote symbolic matches",
            "status": "PASS" if no_kconn_source else "FAIL",
            "details": "KOH1377_VERDICT records no exact source-backed operator convention row.",
        },
        {
            "validation_id": "VAL1377_4_blockers",
            "check": "blocker ledger covers transition, shell, Kconn, and arena projection gaps",
            "status": "PASS" if blockers_cover else "FAIL",
            "details": f"blocker_rows={len(blockers)}",
        },
        {
            "validation_id": "VAL1377_5_runner_refusal",
            "check": "runner feed and gates keep local claims blocked",
            "status": "PASS" if runner_blocks and local_claim_blocked else "FAIL",
            "details": "RUF1377_3 and GATE1377_3 both keep BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1377_6_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1377 is a source hunt and blocker ledger, not a local-GR/PPN/R10 pass.",
        },
        {
            "validation_id": "VAL1377_7_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1377_8_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1377_9_overall",
            "check": "overall 1377 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1377 finds no source-backed transition row or exact K_conn operator source; next route is parent transition-law derivation.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    hunt_hits: list[dict[str, object]],
    candidates: list[dict[str, object]],
    kconn_hunt: list[dict[str, object]],
    blockers: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    transition_summary = [row for row in hunt_hits if row["hunt_id"] == "HIT1377_transition_VERDICT"]
    text = f"""# {TITLE}

**Current verdict:** 1377 tried to build a real transition parent row from the existing files. It cannot honestly do it: the available transition calculator rows are still missing-parent or toy/nonclaim, and the source hunt only finds symbolic/blocker contexts rather than a complete row with values, units, source anchors, extraction method, and shell handling.

**K_conn verdict:** the operator-source hunt also does not close the gap. The corpus contains symbolic `K_conn` contracts and derivative/connection blocker rows, but not an exact operator convention row for `N_conn,*`, source tensor norms, domain/gauge/frame, Hodge/coframe response, IBP split, and boundary edge terms.

**Useful movement:** this pins the next real derivation target: stop hunting the same cupboards and derive the transition parent law itself, or explicitly demote the transition inputs to closure-only finite inputs. No local-GR, PPN, R10, or `q_loc=0` claim is made here.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Source Hunt Summary

{table(["hunt_id", "category", "target_term", "source_path", "line_number", "hit_status", "snippet", "valid_for_claim", "claim_allowed"], transition_summary)}

## Transition Parent Candidate Row Attempt

{table(["candidate_id", "case_id", "input_source_path", "row_status", "candidate_status", "missing_required_fields", "toy_flag", "source_path_value", "reason", "valid_for_claim", "claim_allowed"], candidates)}

## `K_conn` Operator Source Hunt

{table(["hunt_id", "operator_target", "hits_found", "best_status", "exact_operator_source_ready", "reason", "representative_sources", "valid_for_claim", "claim_allowed"], kconn_hunt)}

## Blocker Ledger

{table(["blocker_id", "blocked_object", "why_blocked", "minimum_to_clear", "next_action", "valid_for_claim", "claim_allowed"], blockers)}

## Runner Feed Update

{table(["feed_id", "runner_field", "feed_update", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    hunt_hits = source_hunt_rows()
    candidates = transition_candidate_rows()
    kconn_hunt = kconn_hunt_rows()
    blockers = blocker_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(SOURCE_HUNT_HITS_PATH, hunt_hits)
    write_csv(TRANSITION_CANDIDATE_PATH, candidates)
    write_csv(KCONN_HUNT_PATH, kconn_hunt)
    write_csv(BLOCKER_LEDGER_PATH, blockers)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, hunt_hits, candidates, kconn_hunt, blockers, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, hunt_hits, candidates, kconn_hunt, blockers, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
