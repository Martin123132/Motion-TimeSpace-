from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1246"
TITLE = "1246-Y5-R10-parent-QR-zero-theorem-or-finite-residual-source-hunt"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
THEOREM_CLAUSES_PATH = OUT_DIR / f"{PACK_ID}_PARENT_QR_ZERO_THEOREM_CLAUSES.csv"
THEOREM_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_QR_ZERO_THEOREM_ATTEMPT.csv"
FINITE_SOURCE_HUNT_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QR_SOURCE_HUNT.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_STATUS.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1246_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def is_false(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"false", "0", "no"}


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1246_0_1245_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1245_NEXT_TARGET.csv",
            "needle": "NEXT1245_0_1246",
            "purpose": "handoff naming the Q_R theorem/value bottleneck",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_1_1245_hunt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1245_SOURCE_HUNT_UPDATE.csv",
            "needle": "HUNT1245_0_parent_zero",
            "purpose": "source hunt confirms parent Q_R=0 and finite q_R_hat are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_2_1245_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1245_POLICY_FED_RESULTS.csv",
            "needle": "REFUSED_MISSING_QR",
            "purpose": "policy-fed runner fails only at missing q_R/theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_3_1240_zero_attempt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
            "needle": "ZERO_CHARGE_THEOREM_NOT_DERIVED",
            "purpose": "prior Q_R zero theorem audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_4_07_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "algebraic nonpropagating constraint route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_5_07_parent_open",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "parent origin is still open",
            "purpose": "constraint route is not parent-derived in current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_6_11_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "W partial_r R_AB = Q_R",
            "purpose": "ordinary conserved-current route creates constant reciprocal charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_7_11_hair",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "R_AB = -Q_R/r",
            "purpose": "asymptotic reciprocity still permits exterior reciprocal hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_8_11_topological",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "topological_zero_charge",
            "purpose": "named but not derived topological no-charge route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_9_12_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "Noether identity derives R_AB=0",
            "purpose": "prior audit says Noether identity does not derive the constraint in current scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_10_12_first_class",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "first-class parent constraint",
            "purpose": "possible parent route but not present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_11_1242_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1242_QR_HAT_INPUT_CONTRACT.csv",
            "needle": "zero_theorem_statement",
            "purpose": "accepted future theorem/value input contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1246_12_1244_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "4.6e-05",
            "purpose": "strict q_R_hat guardrail remains available for future finite rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    policy_feed = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv"))[0]

    theorem_clauses = [
        {
            "clause_id": "QZT1246_0_target",
            "route": "parent_QR_zero_theorem",
            "required_statement": "derive Q_R=0 without imposing R_AB=0 closure and without using GR Schwarzschild AB=1 as an imported premise",
            "current_evidence": "1245 narrows live refusal to missing q_R_hat or parent Q_R=0 theorem",
            "status": "TARGET",
            "blocker": "needs parent action or source representation that removes the reciprocal charge mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_1_conserved_current",
            "route": "ordinary_current_conservation",
            "required_statement": "partial_r(W partial_r R_AB)=0 should imply Q_R=0",
            "current_evidence": "11 gives W partial_r R_AB = Q_R",
            "status": "FAILS_ZERO_THEOREM",
            "blocker": "conservation makes Q_R constant, not zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_2_asymptotic_boundary",
            "route": "asymptotic_reciprocity",
            "required_statement": "R_infinity=0 should remove Q_R hair",
            "current_evidence": "11 gives R_AB = -Q_R/r after the constant offset is killed",
            "status": "FAILS_ZERO_THEOREM",
            "blocker": "asymptotic boundary kills only the offset, not reciprocal charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_3_nonprop_constraint",
            "route": "lambda_R_constraint",
            "required_statement": "parent action contains S_constraint=integral lambda_R R_AB as a genuine constrained variable",
            "current_evidence": "07 shows the algebraic constraint gives R_AB=0 and no conserved Q_R, but also says parent origin is open",
            "status": "WORKS_ONLY_IF_PARENT_SIGNED",
            "blocker": "currently a clean closure/contract, not yet a derived parent term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_4_noether",
            "route": "gauge_noether_identity",
            "required_statement": "Noether identity itself forces R_AB=0",
            "current_evidence": "12 says a Noether identity relates equations and cannot set R_AB=0 unless a constraint equation is already present",
            "status": "FAILS_CURRENT_CORPUS",
            "blocker": "Noether can explain a constraint after the parent variable exists; it cannot replace the parent derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_5_topological",
            "route": "topological_source_neutrality",
            "required_statement": "Q_R = integral rho_R = 0 by source representation or topological selection",
            "current_evidence": "11 names topological_zero_charge as the best possible route but does not derive it",
            "status": "CONDITIONAL_NOT_DERIVED",
            "blocker": "missing parent source complex, boundary class, and proof that allowed local sources are neutral",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "QZT1246_6_first_class",
            "route": "first_class_parent_constraint",
            "required_statement": "R_AB is eliminated by a first-class parent constraint in constrained Hamiltonian form",
            "current_evidence": "12 identifies this as possible in principle but says the parent theory is not present",
            "status": "POSSIBLE_NOT_PRESENT",
            "blocker": "missing constraint algebra, multiplier origin, and matter-coupling compatibility",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_attempt = [
        {
            "attempt_id": "QTA1246_0_parent_zero_verdict",
            "claim_piece": "parent Q_R=0 theorem",
            "formal_statement": "Q_R=0 follows from the parent MTS action/constraint/source complex, not from imposed R_AB=0 closure",
            "attempt_result": "NOT_DERIVED_CURRENT_CORPUS",
            "reason": "all inspected routes either conserve nonzero Q_R, remove only the offset, or require an unsigned parent constraint/topological source theorem",
            "runner_consequence": "REFUSED_MISSING_QR remains correct for finite local-PPN row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QTA1246_1_cleanest_conditional_route",
            "claim_piece": "nonpropagating reciprocity constraint",
            "formal_statement": "If a parent-signed multiplier lambda_R enforces R_AB=0, then the kinetic Q_R hair channel is absent",
            "attempt_result": "CONDITIONAL_ROUTE_IDENTIFIED",
            "reason": "07 gives the algebra, but parent origin remains open",
            "runner_consequence": "may be carried as explicit closure branch; not valid as derived MTS evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QTA1246_2_finite_route_required",
            "claim_piece": "finite q_R_hat alternative",
            "formal_statement": "If no parent zero theorem closes, future runner needs a numeric dimensionless q_R_hat with source and GM convention",
            "attempt_result": "SOURCE_HUNT_REQUIRED",
            "reason": "1244/1245 already provide policy and GM convention; only theorem/value is missing",
            "runner_consequence": f"future finite rows must satisfy abs(q_R_hat)<={policy_feed['q_R_hat_abs_guardrail']} for strict nonclaim smoke pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_source_hunt = [
        {
            "hunt_id": "FQH1246_0_parent_multiplier",
            "target": "parent-signed lambda_R multiplier",
            "minimum_evidence": "parent action term, variation showing R_AB=0, proof lambda_R is not inserted as an after-the-fact closure, and compatibility with matter coupling",
            "acceptance_gate": "route_type=parent_zero_theorem; q_R_hat=0; closure_used=false; derivation_status=parent_derived_zero",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "next_action": "derive constrained parent action or demote permanently to closure benchmark",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "FQH1246_1_topological_neutrality",
            "target": "topological/source no-charge theorem",
            "minimum_evidence": "source complex with Q_R as a boundary/topological integral plus proof the allowed local source class has zero charge",
            "acceptance_gate": "zero_theorem_statement names rho_R/source class and proves Q_R=0 without R_AB closure",
            "current_status": "MISSING_SOURCE_COMPLEX",
            "next_action": "construct source representation or abandon topological route for finite residual scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "FQH1246_2_finite_direct_qRhat",
            "target": "direct finite q_R_hat",
            "minimum_evidence": "dimensionless numeric q_R_hat with source path, derivation status, no closure, and policy fields N_sigma=1 sigma_gamma=2.3e-5",
            "acceptance_gate": f"finite_qR_hat row can be smoke-scored; strict pass requires abs(q_R_hat)<={policy_feed['q_R_hat_abs_guardrail']}",
            "current_status": "MISSING_NUMERIC_QR_HAT",
            "next_action": "derive q_R_hat from parent coefficients or create a nonclaim sourced phenomenological bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "FQH1246_3_raw_QR_plus_GM",
            "target": "raw Q_R plus GM normalization",
            "minimum_evidence": "raw Q_R units, source body, measured GM convention, coordinate convention, and conversion to q_R_hat=Q_R c^2/(G M_source)",
            "acceptance_gate": "finite_qR_hat contract fields from 1242 plus GM convention from 1244",
            "current_status": "MISSING_RAW_QR_AND_SOURCE_BODY",
            "next_action": "if parent derivation produces dimensional Q_R, bind it to the 1244 GM convention before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_feed = [
        {
            "feed_id": "RFEED1246_0_policy_GM_ready",
            "target_runner": "1245 policy-fed Q_R PPN smoke runner",
            "policy_status": "READY_NONCLAIM",
            "GM_status": "READY_CONTRACT_ONLY",
            "q_R_hat_status": "MISSING_QR_VALUE_UNCHANGED",
            "zero_theorem_status": "NOT_DERIVED_CURRENT_CORPUS",
            "expected_runner_status": "REFUSED_MISSING_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "RFEED1246_1_closure_branch",
            "target_runner": "closure benchmark only",
            "policy_status": "NOT_SCORING_EVIDENCE",
            "GM_status": "NOT_REQUIRED_FOR_CLOSURE_DISPLAY",
            "q_R_hat_status": "0_BY_EXPLICIT_CLOSURE_ONLY",
            "zero_theorem_status": "CLOSURE_NOT_PARENT_THEOREM",
            "expected_runner_status": "REFUSED_CLOSURE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1246_0_no_parent_zero_claim",
            "decision": "do not claim Q_R=0 as derived",
            "because": "nonpropagating constraint works algebraically only after a parent multiplier is accepted; current corpus says parent origin is open",
            "next_action": "attack parent constrained-action legitimacy explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1246_1_closure_stays_useful",
            "decision": "retain R_AB=0 as explicit closure benchmark",
            "because": "it is the clean local-GR target but not yet a theorem",
            "next_action": "keep closure and finite-residual branches separate in all tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1246_2_finite_hunt_ready",
            "decision": "stage finite q_R_hat source hunt",
            "because": "if the theorem route fails, the runner is already ready to smoke-score a sourced finite residual",
            "next_action": "future finite row must satisfy 1242 contract and 1244 policy/GM convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1246_0_policy_and_GM",
            "claim": "policy/GM prerequisites are ready",
            "status": "PASS_NONCLAIM",
            "reason": "1244/1245 already cleared these plumbing blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1246_1_parent_QR_zero",
            "claim": "parent Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "nonpropagating constraint, first-class constraint, and topological zero routes are unsigned in current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1246_2_finite_qR_hat",
            "claim": "finite q_R_hat value exists",
            "status": "BLOCKED",
            "reason": "no numeric q_R_hat row has been sourced; only future source-hunt requirements are staged",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1246_3_local_PPN",
            "claim": "local PPN gamma pass",
            "status": "BLOCKED",
            "reason": "runner cannot score an MTS prediction without theorem-zero or finite q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1246_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED",
            "reason": "Q_R, beta, conservation, source coupling, and left-hand field equations remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1246_0_1247",
            "target_file": "1247-Y5-R10-parent-lambdaR-constraint-legitimacy-gate.md",
            "target_script": "scripts/Y5_R10_parent_lambdaR_constraint_legitimacy_gate.py",
            "task": "try to parent-sign the cleanest route: prove that lambda_R is a legitimate constrained variable from motion-load/observer-map structure rather than an imposed reciprocity closure",
            "success_condition": "either a parent action/constraint algebra licenses S_constraint=integral lambda_R R_AB, or the lambda_R route is explicitly demoted to closure-only and finite q_R_hat source acquisition becomes primary",
            "do_not": "do not call the constraint derived merely because it gives the desired local GR branch; do not use GR Schwarzschild AB=1 as input",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        theorem_clauses,
        theorem_attempt,
        finite_source_hunt,
        runner_feed,
        decisions,
        claim_gates,
        next_target,
    ]

    output_paths = [
        SOURCE_REGISTER_PATH,
        THEOREM_CLAUSES_PATH,
        THEOREM_ATTEMPT_PATH,
        FINITE_SOURCE_HUNT_PATH,
        RUNNER_FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(THEOREM_CLAUSES_PATH, theorem_clauses)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_attempt)
    write_csv(FINITE_SOURCE_HUNT_PATH, finite_source_hunt)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    theorem_not_promoted = theorem_attempt[0]["attempt_result"] == "NOT_DERIVED_CURRENT_CORPUS"
    conditional_route_identified = any(row["status"] == "WORKS_ONLY_IF_PARENT_SIGNED" for row in theorem_clauses)
    failure_modes_recorded = all(
        any(row["clause_id"] == clause and row["status"] in {"FAILS_ZERO_THEOREM", "FAILS_CURRENT_CORPUS", "CONDITIONAL_NOT_DERIVED", "POSSIBLE_NOT_PRESENT"} for row in theorem_clauses)
        for clause in ["QZT1246_1_conserved_current", "QZT1246_2_asymptotic_boundary", "QZT1246_4_noether", "QZT1246_5_topological", "QZT1246_6_first_class"]
    )
    finite_hunt_ready = len(finite_source_hunt) == 4 and all(str(row["current_status"]).startswith("MISSING") for row in finite_source_hunt)
    runner_still_refuses_missing_qr = any(
        row["expected_runner_status"] == "REFUSED_MISSING_QR" and row["q_R_hat_status"] == "MISSING_QR_VALUE_UNCHANGED"
        for row in runner_feed
    )
    no_claim_pass = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )
    next_is_1247 = next_target[0]["next_id"] == "NEXT1246_0_1247"
    policy_guardrail_preserved = policy_feed["q_R_hat_abs_guardrail"] == "4.6e-05"

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in output_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:PARSE_FAIL:{exc}")

    fw_recent = recent_formalization_writes()

    validation = [
        validation_row("VAL1246_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1246_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1246_2_theorem_not_promoted", "parent Q_R=0 theorem is not overclaimed", theorem_not_promoted, theorem_attempt[0]["attempt_result"]),
        validation_row("VAL1246_3_conditional_route", "clean lambda_R route is identified as conditional", conditional_route_identified, "QZT1246_3_nonprop_constraint -> WORKS_ONLY_IF_PARENT_SIGNED"),
        validation_row("VAL1246_4_failure_modes", "failed zero-proof routes are explicitly recorded", failure_modes_recorded, "current, boundary, Noether, topological, and first-class routes audited"),
        validation_row("VAL1246_5_finite_hunt_ready", "finite q_R_hat source hunt is staged", finite_hunt_ready, f"finite_source_hunt_rows={len(finite_source_hunt)}"),
        validation_row("VAL1246_6_runner_feed", "runner feed still refuses missing q_R", runner_still_refuses_missing_qr, "RFEED1246_0_policy_GM_ready -> REFUSED_MISSING_QR"),
        validation_row("VAL1246_7_policy_guardrail", "1244 strict q_R_hat guardrail preserved", policy_guardrail_preserved, f"q_R_hat_abs_guardrail={policy_feed['q_R_hat_abs_guardrail']}"),
        validation_row("VAL1246_8_claim_gates", "claim gates remain nonclaim/blocked", no_claim_pass, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1246_9_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1246_10_next_target_1247", "next target is lambda_R legitimacy gate", next_is_1247, next_target[0]["target_file"]),
        validation_row("VAL1246_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1246_12_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1246_13_overall",
            "overall 1246 validation",
            all(row["status"] == "PASS" for row in validation),
            "1246 attempts the parent Q_R=0 theorem, refuses to promote it, and stages finite q_R_hat source acquisition with the runner still blocked honestly",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1246 does not derive `Q_R=0` from the current parent corpus. The cleanest route remains the nonpropagating `lambda_R R_AB` constraint, but it is only a theorem if the parent action signs the multiplier/constraint rather than us inserting closure by hand.",
        "",
        "**Main progress:** the local-PPN bottleneck is now sharply isolated. Policy and GM are ready; ordinary conservation, asymptotic boundary, Noether identity, and named topological neutrality do not yet prove zero charge. The next real target is parent-signing `lambda_R` or accepting finite `q_R_hat` source acquisition.",
        "",
        "**No-claim guard:** no derived GR, local PPN pass, R10/WEP pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Parent QR Zero Theorem Clauses",
        markdown_table(theorem_clauses, list(theorem_clauses[0].keys())),
        "",
        "## Parent QR Zero Theorem Attempt",
        markdown_table(theorem_attempt, list(theorem_attempt[0].keys())),
        "",
        "## Finite QR Source Hunt",
        markdown_table(finite_source_hunt, list(finite_source_hunt[0].keys())),
        "",
        "## Runner Feed Status",
        markdown_table(runner_feed, list(runner_feed[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
