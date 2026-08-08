from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md"

SRC_2858_DOC = ROOT / "2858-Y5-R2FR-minimal-amplitude-doublet-action-consistency-gate-or-reject-under-AX1090.md"
SRC_2858_NEXT = RESIDUALS / "P8_Y5_R2FR_2858_NEXT_TARGET.csv"
SRC_2858_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2858_VALIDATION.csv"
SRC_2858_CONSISTENCY = RESIDUALS / "P8_Y5_R2FR_2858_CONSISTENCY_GATE_MATRIX.csv"
SRC_2858_NONTUNING = RESIDUALS / "P8_Y5_R2FR_2858_NON_TUNING_AUDIT.csv"
SRC_2858_QUOTIENT = RESIDUALS / "P8_Y5_R2FR_2858_QUOTIENT_COMPATIBILITY_AUDIT.csv"
SRC_2858_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2858_FINITE_FALLBACK_REQUIREMENTS.csv"
SRC_2858_VERDICT = RESIDUALS / "P8_Y5_R2FR_2858_VERDICT_LEDGER.csv"
SRC_2857_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2857_MINIMAL_DOUBLET_ACTION_ANSATZ.csv"
SRC_2857_ALGEBRA = RESIDUALS / "P8_Y5_R2FR_2857_ANSATZ_ALGEBRA_CHECK.csv"
SRC_2857_OWNERSHIP = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2854_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"
SRC_2854_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2854_SOURCE_REQUEST_PACK.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2853_REENTRY = RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2859_SOURCE_REGISTER.csv",
    "search": RESIDUALS / "P8_Y5_R2FR_2859_UAMP_CORPUS_SEARCH_AUDIT.csv",
    "origin": RESIDUALS / "P8_Y5_R2FR_2859_PARENT_ORIGIN_SCAN.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2859_DERIVATION_ATTEMPT_LEDGER.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2859_CLOSURE_DEMOTION_LEDGER.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_2859_FINITE_SOURCE_FALLBACK_QUEUE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2859_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2859_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2859_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2859_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2859_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "origin_copy": LOCAL_BOUNDS / "RAB_UAMP_PARENT_ORIGIN_SCAN_2859_NONCLAIM.csv",
    "demotion_copy": SOURCE_WEIGHT / "RAB_UAMP_CLOSURE_DEMOTION_2859_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2859_finite_source_row_acquisition_NEXT.csv",
    "fallback_copy": BETA_DOCS / "RAB_FINITE_SOURCE_FALLBACK_QUEUE_2859_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2859_0_2858_doc", SRC_2858_DOC, "NEXT2858_0_2859;VAL2858_OVERALL", "2858 handoff"),
        ("SRC2859_1_2858_next", SRC_2858_NEXT, "NEXT2858_0_2859", "2859 selected"),
        ("SRC2859_2_2858_validation", SRC_2858_VALIDATION, "VAL2858_OVERALL", "2858 validation"),
        ("SRC2859_3_2858_consistency", SRC_2858_CONSISTENCY, "GATE2858_0_algebra;GATE2858_4_action_origin", "consistency gate"),
        ("SRC2859_4_2858_nontuning", SRC_2858_NONTUNING, "NT2858_0_before_readout;NT2858_5_verdict", "non-tuning audit"),
        ("SRC2859_5_2858_quotient", SRC_2858_QUOTIENT, "QCA2858_1_Dq;QCA2858_5_verdict", "quotient audit"),
        ("SRC2859_6_2858_fallback", SRC_2858_FALLBACK, "FB2858_0_Q_CAB;FB2858_6_runner", "finite fallback requirements"),
        ("SRC2859_7_2858_verdict", SRC_2858_VERDICT, "VER2858_0_algebra;VER2858_3_best_next", "2858 verdict"),
        ("SRC2859_8_2857_ansatz", SRC_2857_ANSATZ, "ANS2857_2_quotient_invariant;ANS2857_3_action", "U_amp ansatz"),
        ("SRC2859_9_2857_algebra", SRC_2857_ALGEBRA, "ALG2857_0_invariant;ALG2857_5_tuning_guard", "U_amp algebra"),
        ("SRC2859_10_2857_ownership", SRC_2857_OWNERSHIP, "OWN2857_0_sigma;OWN2857_6_full_vector", "ownership gates"),
        ("SRC2859_11_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2859_12_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2859_13_2854_blockers", SRC_2854_BLOCKERS, "BLOCK2854_0_Q_CAB;BLOCK2854_6_full_vector", "blocker ledger"),
        ("SRC2859_14_2854_requests", SRC_2854_REQUESTS, "REQ2854_0_parent_equations;REQ2854_6_full_vector", "source request pack"),
        ("SRC2859_15_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2859_16_2853_reentry", SRC_2853_REENTRY, "RE2853_0_parent_source_equation;RE2853_3_full_vector", "parent action reentry hooks"),
    ]
    return [source_row(*spec) for spec in specs]


def corpus_search_rows() -> list[dict[str, Any]]:
    patterns = ["U_amp", "delta_R - sigma_R C_AB", "delta_R-sigma_R C_AB"]
    included_hits: list[str] = []
    excluded_hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".csv"}:
            continue
        if "runs" in path.parts:
            continue
        text = read_text(path)
        if not any(pattern in text for pattern in patterns):
            continue
        rel = str(path.relative_to(ROOT))
        if any(marker in rel for marker in ["2857", "2858", "2859", "RAB_MINIMAL_DOUBLET", "RAB_UAMP"]):
            excluded_hits.append(rel)
        else:
            included_hits.append(rel)
    return [
        nonclaim(
            {
                "search_id": "SEARCH2859_0_pre_ansatz_parent_hits",
                "patterns": ";".join(patterns),
                "pre_2857_parent_hit_count": len(included_hits),
                "pre_2857_parent_hits": ";".join(included_hits[:20]),
                "ansatz_checkpoint_hit_count": len(excluded_hits),
                "ansatz_checkpoint_hits_sample": ";".join(excluded_hits[:20]),
                "result": "NO_PRIOR_PARENT_UAMP_SOURCE_FOUND" if not included_hits else "PRIOR_HITS_REQUIRE_REVIEW",
                "control_only": True,
            }
        )
    ]


def origin_rows() -> list[dict[str, Any]]:
    specs = [
        ("ORG2859_0_direct_parent_uamp", "direct parent U_amp definition", "NO_PRIOR_PARENT_SOURCE_FOUND", "corpus search finds U_amp only in 2857/2858 ansatz/checkpoint outputs", "cannot treat U_amp as pre-existing parent object"),
        ("ORG2859_1_sigma_origin", "sigma_R from parent sign/operator", "NOT_SOURCED", "CONTRACT2844_5_sign remains MISSING_SIGN_CONVENTION", "ratio in U_amp is not parent-owned"),
        ("ORG2859_2_quotient_origin", "q(Phi_parent) makes v_amp vertical and U_amp physical", "NOT_SOURCED", "QCA2858/VQC1022 keep q/Dq conditional or missing", "quotient compatibility not proven"),
        ("ORG2859_3_action_origin", "parent action depends on U_amp because of symmetry", "NOT_SOURCED", "2857 action is ANSATZ_ONLY_NOT_PARENT_ACTION", "action origin remains closure-only"),
        ("ORG2859_4_generator_origin", "v_amp is Omega-raised generator", "NOT_SOURCED", "DVM formal map exists but parent Omega/DC absent", "generator can be written but not owned"),
        ("ORG2859_5_boundary_origin", "K_amp/B terms are fixed before readout", "NOT_SOURCED", "boundary differentiability/silence missing", "integrated charge identity blocked"),
        ("ORG2859_6_matter_full_vector_origin", "same branch descends through matter/source/full vector", "NOT_SOURCED", "matter descent, GM glue and full PPN vector remain open", "local GR/Newton claim blocked"),
    ]
    return [
        nonclaim(
            {
                "origin_id": origin_id,
                "required_origin": required,
                "status": status,
                "evidence": evidence,
                "effect": effect,
                "accepted_parent_origin": False,
                "control_only": True,
            }
        )
        for origin_id, required, status, evidence, effect in specs
    ]


def derivation_rows() -> list[dict[str, Any]]:
    specs = [
        ("DER2859_0_possible_form", "If parent fields split as (U_amp,V_amp) with S_parent independent of V_amp, then v_amp is vertical and S_amp depends only on U_amp.", "valid conditional theorem shape", "CONDITIONAL_ONLY"),
        ("DER2859_1_source_identity", "For S_src=-<J_U,U_amp>, variation gives J_CAB=-sigma_R J_U and J_R=J_U.", "algebraically derives the 2856 current identity", "CONDITIONAL_ONLY"),
        ("DER2859_2_missing_origin", "The current corpus does not show why parent fields must split into U_amp and V_amp with that sigma_R before readout.", "this is the exact missing parent-origin step", "OPEN_BLOCKER"),
        ("DER2859_3_no_claim_rule", "Without parent origin, U_amp theorem-zero cannot be used in PPN/R10/Newton/local-GR claims.", "prevents answer-shaped ansatz from masquerading as derivation", "ACTIVE_GUARD"),
    ]
    return [
        nonclaim(
            {
                "derivation_id": derivation_id,
                "statement": statement,
                "meaning": meaning,
                "status": status,
                "parent_derived": False,
                "control_only": True,
            }
        )
        for derivation_id, statement, meaning, status in specs
    ]


def demotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEM2859_0_candidate_status", "U_amp doublet mechanism", "RETAIN_AS_PRIVATE_CANDIDATE", "algebra is clean and still the best derivation-shaped route"),
        ("DEM2859_1_claim_status", "theorem-zero amplitude cancellation", "DEMOTE_TO_CLOSURE_ONLY_FOR_NOW", "parent origin not sourced"),
        ("DEM2859_2_runner_status", "finite-source fallback", "PROMOTE_TO_ACTIVE_NEXT_WORK", "honest path if parent-origin route is not closed"),
        ("DEM2859_3_reentry_status", "parent-origin reentry", "KEEP_OPEN", "a future source/action/quotient proof can reactivate theorem route"),
    ]
    return [
        nonclaim(
            {
                "demotion_id": demotion_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "theorem_claim_allowed": False,
                "control_only": True,
            }
        )
        for demotion_id, obj, status, reason in specs
    ]


def fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("FSQ2859_0_Q_CAB", "Q_CAB", "source-backed finite charge or parent-zero owner", "BLOCK2854_0_Q_CAB;PACK2844_0_Q_CAB", "required for 2853 runner"),
        ("FSQ2859_1_q_R_eff", "q_R_eff", "same-convention finite Green charge", "PACK2844_4_q_R_eff", "required for A_total"),
        ("FSQ2859_2_sigma_R", "sigma_R", "operator/Green sign convention", "CONTRACT2844_5_sign", "required for either U_amp or finite scoring"),
        ("FSQ2859_3_boundary", "K_amp/B_CAB/B_R", "zero/exact/included boundary or finite bound", "BLOCK2854_4_tail;FB2858_3_boundary", "required before integrated identity"),
        ("FSQ2859_4_GM", "measured GM glue", "worldtube source measure plus metric 1/r readout", "BLOCK2854_5_GM", "required for Newton normalization"),
        ("FSQ2859_5_full_vector", "full PPN/local vector", "beta/preferred/source/clock/orbital/q_loc rows", "BLOCK2854_6_full_vector", "required for local-GR claim"),
        ("FSQ2859_6_strict_runner", "2853 strict runner", str(SRC_2853_RUNNER), "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "rerun only after source rows are real"),
    ]
    return [
        nonclaim(
            {
                "fallback_id": fallback_id,
                "quantity": quantity,
                "required_input": required,
                "source_anchor_or_path": anchor,
                "why_needed": why,
                "fallback_active": True,
                "ready_for_runner": False,
                "control_only": True,
            }
        )
        for fallback_id, quantity, required, anchor, why in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2859_0_origin_scan", "U_amp parent-origin scan completed", "PASS_CONTROL_ONLY", "no accepted parent origin found"),
        ("CG2859_1_parent_origin", "U_amp is parent-derived", "BLOCKED", "U_amp appears as 2857/2858 ansatz rather than parent-sourced object"),
        ("CG2859_2_theorem_zero", "Q_CAB + sigma_R q_R_eff = 0 theorem", "BLOCKED", "origin/sign/boundary still open"),
        ("CG2859_3_finite_runner", "2853 finite runner can score", "BLOCKED", "fallback rows remain missing/source-incomplete"),
        ("CG2859_4_local_GR_Newton", "local GR/Newton reduction", "BLOCKED", "GM glue and full vector remain open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2859_0_origin", "No current parent-origin proof for U_amp.", "demote theorem-zero claim route for now"),
        ("DEC2859_1_candidate", "Keep U_amp as best private candidate mechanism.", "it remains algebraically clean and derivation-shaped"),
        ("DEC2859_2_fallback", "Activate finite source-row acquisition as next work.", "the framework must become testable without relying on an unproven zero theorem"),
        ("DEC2859_3_reentry", "Keep parent-origin reentry open.", "if a real action/quotient/sign source appears, theorem route can be reopened"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "control_only": True,
            }
        )
        for decision_id, decision, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2859_0_2860",
                "status": "selected_primary",
                "target_doc": "2860-Y5-R2FR-finite-source-row-acquisition-after-Uamp-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_source_row_acquisition_after_Uamp_demotion_under_AX1090_2860.py",
                "mission": "build the finite-source acquisition pack for Q_CAB, q_R_eff, sigma_R, boundary/tail, GM, and full-vector rows, then attempt a strict nonclaim import path for the 2853 runner without allowing theorem-zero/local-GR claims",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2859_0_origin", OUTPUTS["origin"], BRANCH_OUTPUTS["origin_copy"], "U_amp parent-origin scan nonclaim copy"),
        ("COPY2859_1_demotion", OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"], "closure demotion nonclaim copy"),
        ("COPY2859_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2860"),
        ("COPY2859_3_fallback", OUTPUTS["fallback"], BRANCH_OUTPUTS["fallback_copy"], "finite source fallback queue copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table", "source_anchor_or_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_parent_origin",
        "parent_derived",
        "theorem_claim_allowed",
        "ready_for_runner",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2859_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2859_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2859_2_corpus_search_done", len(rows_by_name["search"]) == 1, "U_amp corpus search audit was written"),
        ("VAL2859_3_no_prior_parent_uamp", rows_by_name["search"][0]["pre_2857_parent_hit_count"] == 0, "no pre-2857 parent U_amp source was found"),
        ("VAL2859_4_no_origin_accepted", not any(row["accepted_parent_origin"] for row in rows_by_name["origin"]), "no parent origin row is accepted"),
        ("VAL2859_5_demoted_claim_route", any(row["status"] == "DEMOTE_TO_CLOSURE_ONLY_FOR_NOW" for row in rows_by_name["demotion"]), "theorem-zero route is demoted for now"),
        ("VAL2859_6_fallback_active", all(row["fallback_active"] for row in rows_by_name["fallback"]), "finite-source fallback queue is active"),
        ("VAL2859_7_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2859_8_next_target_2860", any(row["next_id"] == "NEXT2859_0_2860" and row["selected"] for row in rows_by_name["next"]), "2860 finite source acquisition target selected"),
        ("VAL2859_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2859_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2859_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2859_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2859_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2859_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2859_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2859_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2859_OVERALL",
            "passed": overall,
            "detail": "2859 finds no pre-existing parent origin for U_amp, demotes theorem-zero claim use to closure-only for now, keeps U_amp as a candidate, and selects finite-source acquisition for 2860.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2859 - Y5 R2FR Uamp Parent Origin Or Finite Source Fallback Under AX1090

Status: `Y5_R2FR_2859_Uamp_origin_not_sourced_theorem_route_demoted_finite_fallback_next`

## Private Verdict

The `U_amp` route is still the best-looking mechanism, but it is not parent-derived in the current corpus.

The corpus search found `U_amp` only in the new 2857/2858 ansatz/checkpoint layer, not as an older parent-sourced field, quotient coordinate, or action invariant. That means we cannot honestly use it as a theorem-zero proof yet.

So the decision is disciplined:

- Keep `U_amp = delta_R - sigma_R C_AB` as the leading private candidate mechanism.
- Demote theorem-zero use of it to closure-only for now.
- Move the active path back to finite-source rows: `Q_CAB`, `q_R_eff`, `sigma_R`, boundary/tail, measured `GM`, and the full local vector.

This is not the mechanism dying. It is us refusing to let a good-looking ansatz cosplay as derivation. If a parent source for `U_amp` appears later, the route can re-enter immediately.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## U_amp Corpus Search Audit

{markdown_table(rows["search"], ["search_id", "pre_2857_parent_hit_count", "result", "ansatz_checkpoint_hit_count", "valid_for_claim"])}

## Parent Origin Scan

{markdown_table(rows["origin"], ["origin_id", "required_origin", "status", "evidence", "effect", "accepted_parent_origin", "valid_for_claim"])}

## Derivation Attempt Ledger

{markdown_table(rows["derivation"], ["derivation_id", "statement", "meaning", "status", "parent_derived", "valid_for_claim"])}

## Closure Demotion Ledger

{markdown_table(rows["demotion"], ["demotion_id", "object", "status", "reason", "theorem_claim_allowed", "valid_for_claim"])}

## Finite Source Fallback Queue

{markdown_table(rows["fallback"], ["fallback_id", "quantity", "required_input", "why_needed", "fallback_active", "ready_for_runner", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["search"] = corpus_search_rows()
    rows["origin"] = origin_rows()
    rows["derivation"] = derivation_rows()
    rows["demotion"] = demotion_rows()
    rows["fallback"] = fallback_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "search", "origin", "derivation", "demotion", "fallback", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2859_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2859_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
