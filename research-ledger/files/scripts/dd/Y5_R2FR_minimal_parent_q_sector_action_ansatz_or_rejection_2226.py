from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2226-Y5-R2FR-minimal-parent-q-sector-action-ansatz-or-rejection.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_MINIMAL_QSECTOR_ANSATZ_2226"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2225_doc": ROOT / "2225-Y5-R2FR-Jq-unit-dimension-and-parent-source-variation-frontier-import.md",
    "2225_validation": OUT / "P8_Y5_BRR545_2225_VALIDATION.csv",
    "2225_reentry": OUT / "P8_Y5_PARENT_QLOC_2225_PARENT_QSECTOR_REENTRY_TEMPLATE.csv",
    "2225_next": OUT / "P8_Y5_PARENT_QLOC_2225_NEXT_TARGET.csv",
    "1553_doc": ROOT / "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md",
    "1553_validation": OUT / "P8_Y5_BRR545_1553_VALIDATION.csv",
    "1553_ansatz": OUT / "P8_Y5_PARENT_QLOC_1553_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv",
    "1553_runner": OUT / "P8_Y5_PARENT_QLOC_1553_ANSATZ_FILTER_RUNNER_NONCLAIM.csv",
    "1553_smoke": OUT / "P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv",
    "1553_rejection": OUT / "P8_Y5_PARENT_QLOC_1553_ANSATZ_REJECTION_LEDGER.csv",
    "1553_decision": OUT / "P8_Y5_PARENT_QLOC_1553_DECISION.csv",
    "1553_next": OUT / "P8_Y5_PARENT_QLOC_1553_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2226_SOURCE_REGISTER.csv"
ANSATZ_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2226_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv"
FILTER_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2226_ANSATZ_FILTER_RUNNER_NONCLAIM.csv"
QNORM_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2226_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_2226_ANSATZ_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2226_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2226_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2226_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2226_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2226_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2226_MINIMAL_QSECTOR_ANSATZ_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "minimal_qsector_ansatz_nonclaim_2226.csv",
    "beta_docs": BETA_DOCS / "MINIMAL_QSECTOR_ANSATZ_2226_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    ANSATZ_AUDIT,
    FILTER_RUNNER,
    QNORM_SMOKE,
    REJECTION_LEDGER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2226_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2226" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current parent q-sector reentry handoff" if key.startswith("2225") else "older minimal q-sector ansatz/rejection evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2226_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def ansatz_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "ANS2226_0_auxiliary_algebraic_positive_norm",
            "nonpropagating auxiliary q-sector",
            "S_q=1/2 int_W mu_q^2 (q^A-Q^A(Phi)) G_AB (q^B-Q^B(Phi)) dV_e",
            "can define a positive local q-norm without gradient/exterior hair if G_AB>0",
            "Q^A(Phi), G_AB, mu_q and matter q-coupling are not parent-derived",
            "BEST_FORMAL_CANDIDATE_NOT_ACCEPTED",
            "FORMAL_ANSATZ_NOT_PARENT_SOURCED",
        ),
        (
            "ANS2226_1_massive_kinetic_q",
            "massive derivative q-sector",
            "S_q=1/2 int_W (Z_AB nabla q^A nabla q^B + M_AB^2 q^A q^B) dV_e",
            "can provide Hessian/operator norm if Z/M are positive and sourced",
            "creates physical finite-range/exterior hair unless no-hair/source-zero/boundary locks close",
            "REJECT_FOR_MINIMAL_LOCAL_GR_ROUTE",
            "REJECTED_HAIR_RISK_AND_PARENT_INPUTS_MISSING",
        ),
        (
            "ANS2226_2_pure_constraint_q",
            "pure Lagrange multiplier constraint",
            "S_q=int_W lambda_A(q^A-Q^A(Phi)) dV_e",
            "removes independent q propagation and exterior hair",
            "degenerate: supplies constraint but no positive q-norm E for T_source_norm*C_qm",
            "REJECT_AS_NORM_SOURCE",
            "DEGENERATE_NO_QNORM",
        ),
        (
            "ANS2226_3_penalty_constraint_limit",
            "regularized penalty constraint",
            "S_q=int_W lambda_A(q^A-Q^A)+1/2 epsilon lambda_A H^AB lambda_B dV_e",
            "can interpolate between pure constraint and positive norm",
            "epsilon/H choice is inserted unless a parent regulator theorem derives it",
            "CONDITIONAL_REGULATOR_ROUTE_ONLY",
            "NOT_ACCEPTED_WITHOUT_PARENT_REGULATOR",
        ),
        (
            "ANS2226_4_reduced_quotient_norm",
            "quotient-reduced parent norm",
            "E_q = pullback/restriction of delta^2 S_red on Conf_parent/N_q",
            "cleanest if q is a true quotient coordinate and reduced Hessian is positive",
            "q/v_X/action/matter/boundary/degree certificate is not currently available",
            "FUTURE_THEOREM_ROUTE_ONLY",
            "CONDITIONAL_NOT_CURRENTLY_AVAILABLE",
        ),
        (
            "ANS2226_5_phase_volume_nonpropagating_origin",
            "phase-volume/nonpropagating q-origin",
            "q-sector arises as a local capacity/phase-volume balance constraint, not an exterior kinetic field",
            "aligns with the nonpropagating reciprocity route and avoids hair",
            "phase-volume principle is not yet a parent theorem and does not yet supply G_AB/E",
            "PROMISING_NEXT_DERIVATION_ROUTE",
            "ORIGIN_ROUTE_MISSING_THEOREM",
        ),
        (
            "ANS2226_6_current_verdict",
            "accepted minimal parent q-sector action",
            "none accepted",
            "none yet",
            "every minimal ansatz either lacks parent source, lacks a norm, risks exterior hair, or depends on an unproved origin principle",
            "REJECT_PROMOTION_KEEP_BEST_CANDIDATE_PRIVATE",
            "NO_ACCEPTED_PARENT_ACTION",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ansatz_id": ansatz_id,
            "candidate": candidate,
            "formula": formula,
            "what_it_solves": solves,
            "fatal_or_open_issue": issue,
            "filter_result": filter_result,
            "current_status": status,
            **flags(),
        }
        for ansatz_id, candidate, formula, solves, issue, filter_result, status in entries
    ]


def filter_rows() -> list[dict[str, Any]]:
    entries = [
        ("RUN2226_0_parent_source", "parent source exists", "FAIL_BLOCK", "no candidate is sourced as an actual parent action term"),
        ("RUN2226_1_positive_norm", "positive/coercive q-norm", "PASS_ONLY_FORMALLY_FOR_AUXILIARY", "auxiliary algebraic norm works only if G_AB and mu_q are parent-derived"),
        ("RUN2226_2_no_hair", "no exterior q hair", "PASS_FOR_NONPROPAGATING_ONLY", "kinetic branch fails this guard without no-hair theorem"),
        ("RUN2226_3_matter_coupling", "J_q from delta S_matter/delta q", "FAIL_BLOCK", "explicit matter q-coupling not supplied"),
        ("RUN2226_4_same_norm_Cqm", "Dq[v_m] computed in same E", "FAIL_BLOCK", "Dq[v_m] and G_AB are unsigned"),
        ("RUN2226_5_no_local_tuning", "no R10/PPN/clock/orbit coefficient fitting", "PASS_GUARD_NONCLAIM", "no candidate is promoted or scored"),
        ("RUN2226_6_verdict", "minimal q-sector action accepted", "REFUSED_NOT_PARENT_DERIVED", "best candidate remains private scaffolding"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "filter": filt,
            "result": result,
            "reason": reason,
            **flags(),
        }
        for runner_id, filt, result, reason in entries
    ]


def smoke_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "SMOKE2226_0_auxiliary_E",
            "auxiliary ansatz",
            "E_aux[delta q]^2=int_W mu_q^2 delta q^A G_AB delta q^B dV_e",
            "FORMALLY_EXTRACTABLE_IF_GAB_SOURCED",
            "G_AB, mu_q, q map and matter coupling are missing",
        ),
        (
            "SMOKE2226_1_auxiliary_Jq",
            "auxiliary ansatz source",
            "J_A=delta S_matter/delta q^A",
            "NOT_EXTRACTABLE_CURRENTLY",
            "no explicit S_matter[q]",
        ),
        (
            "SMOKE2226_2_auxiliary_Cqm",
            "auxiliary ansatz C_qm",
            "C_qm^2=int_W mu_q^2 Dq[v_m]^A G_AB Dq[v_m]^B dV_e",
            "NOT_EXTRACTABLE_CURRENTLY",
            "Dq[v_m] and G_AB are not parent-signed",
        ),
        (
            "SMOKE2226_3_constraint_E",
            "pure constraint ansatz",
            "no positive E from lambda(q-Q) alone",
            "REJECTED_DEGENERATE",
            "dual pairing requires a norm, not just a constraint equation",
        ),
        (
            "SMOKE2226_4_kinetic_E",
            "massive kinetic ansatz",
            "E_kin from Z_AB and M_AB^2",
            "REJECTED_FOR_CURRENT_ROUTE",
            "would need no-hair/source-zero/boundary theorem before local GR route",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": smoke_id,
            "route": route,
            "extraction_formula": formula,
            "current_status": status,
            "blocker": blocker,
            **flags(),
        }
        for smoke_id, route, formula, status, blocker in entries
    ]


def rejection_rows() -> list[dict[str, Any]]:
    entries = [
        ("REJ2226_0_no_promotion", "no ansatz promoted", "ansatz is not a parent derivation", "claim ceiling stays locked"),
        ("REJ2226_1_best_candidate", "auxiliary algebraic norm retained privately", "least hair-prone formal candidate but unsourced", "may guide future q-sector derivation"),
        ("REJ2226_2_best_origin", "phase-volume/nonpropagating origin retained", "best conceptual way to avoid inserted penalty terms", "next derivation target"),
        ("REJ2226_3_kinetic_route", "massive kinetic q rejected for current local route", "creates finite-range/hair branch without no-hair theorem", "only fallback empirical branch"),
        ("REJ2226_4_constraint_route", "pure constraint rejected as norm source", "does not supply E for T_source_norm*C_qm", "can still be part of origin story"),
        ("REJ2226_5_local_claim", "GR/Newton derivation still blocked", "no accepted q-sector action", "no local claim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "decision": decision,
            "reason": reason,
            "surviving_use": surviving_use,
            **flags(),
        }
        for rejection_id, decision, reason, surviving_use in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2226_0_import", "1553 minimal q-sector ansatz audit imported", "PASS_NONCLAIM", "candidate space is connected to current numbering"),
        ("CG2226_1_accepted_action", "accepted parent q-sector action", "BLOCKED_NONCLAIM", "no ansatz is parent-derived"),
        ("CG2226_2_auxiliary_candidate", "auxiliary algebraic q norm", "PRIVATE_CANDIDATE_ONLY", "best formal candidate but unsourced"),
        ("CG2226_3_positive_norm", "positive q-norm E supplied", "BLOCKED_NONCLAIM", "only formal extraction exists"),
        ("CG2226_4_matter_coupling", "J_q supplied", "BLOCKED_NONCLAIM", "no explicit matter q-coupling"),
        ("CG2226_5_local_GR", "derived GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "minimal ansatz route did not close"),
        ("CG2226_6_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private proof line remains mid-derivation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC2226_0_result", "No minimal q-sector ansatz is accepted as a parent derivation.", "NO_ACCEPTED_ANSATZ", "each candidate fails a required filter or lacks parent source"),
        ("DEC2226_1_retained", "Retain the auxiliary algebraic norm as the best formal candidate.", "PRIVATE_CANDIDATE_ONLY", "it can avoid exterior hair but needs a parent origin for G_AB and coupling"),
        ("DEC2226_2_route", "Reject the kinetic q-sector as the default local-GR route.", "REJECT_HAIR_ROUTE", "a propagating q field creates exactly the exterior local residual problem we are trying to avoid"),
        ("DEC2226_3_next", "Move to phase-volume/nonpropagating q-sector origin.", "NEXT_2227_PHASE_VOLUME_ORIGIN", "this is the least-cheaty path to derive the auxiliary norm rather than inserting it"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2226_0_2227",
            "target_file": "2227-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            "target_script": "scripts/Y5_R2FR_phase_volume_nonpropagating_qsector_origin_or_rejection_2227.py",
            "objective": "attempt to derive the auxiliary/nonpropagating q-sector norm from a phase-volume or motion-capacity balance principle, or reject that origin route explicitly",
            "success_condition": "phase-volume/nonpropagating origin supplies q, E/G_AB, no-hair/no-charge and matter-coupling slots, or the route remains closure-only",
            "do_not": "do not insert penalty coefficients by hand; do not reintroduce exterior hair; do not claim GR/Newton reduction",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REJECTION_LEDGER, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(REJECTION_LEDGER),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    ansatz: list[dict[str, Any]],
    filters: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2226 - Y5/R2FR Minimal Parent q-sector Action Ansatz Or Rejection",
            "## Verdict\n"
            "- 2226 imports the old `1553` minimal q-sector action attempt into the current R2FR line.\n"
            "- The best formal candidate is a nonpropagating auxiliary/algebraic q-sector because it can give a positive local norm without exterior hair.\n"
            "- It is not accepted as a parent derivation: `Q^A(Phi)`, `G_AB`, `mu_q`, `Dq[v_m]`, and the matter q-coupling are not parent-sourced.\n"
            "- The massive kinetic route is rejected as the default local-GR route because it reintroduces finite-range exterior hair unless a separate no-hair theorem closes.\n"
            "- Next target is phase-volume/nonpropagating origin: derive the auxiliary norm rather than inserting it.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Minimal q-sector Ansatz Audit\n"
            + md_table(ansatz, ["ansatz_id", "candidate", "formula", "what_it_solves", "fatal_or_open_issue", "filter_result", "current_status"]),
            "## Ansatz Filter Runner\n"
            + md_table(filters, ["runner_id", "filter", "result", "reason"]),
            "## q-norm Extraction Smoke\n"
            + md_table(smoke, ["smoke_id", "route", "extraction_formula", "current_status", "blocker"]),
            "## Rejection Ledger\n"
            + md_table(rejection, ["rejection_id", "decision", "reason", "surviving_use"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "rationale"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is a useful negative result, not wheel-spinning. The coupling gap has narrowed to one honest target: a nonpropagating parent q-sector must be derived from a deeper phase-volume, motion-capacity, gauge, or Noether principle. If that derivation exists, it may supply the algebraic norm without local hair; if it does not, the local-GR route should be demoted to an explicit closure rather than patched with fitted coefficients.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2226 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2225_validation"]) and validation_pass(SOURCE_FILES["1553_validation"]) else "FAIL",
            "detail": "2225 and 1553 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_02_ansatz_candidates",
            "result": "PASS" if len(read_csv(ANSATZ_AUDIT)) >= 7 else "FAIL",
            "detail": "minimal ansatz candidates audited",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_03_no_accepted_action",
            "result": "PASS" if any(row["current_status"] == "NO_ACCEPTED_PARENT_ACTION" for row in read_csv(ANSATZ_AUDIT)) else "FAIL",
            "detail": "no parent q-sector action accepted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_04_best_candidate_private",
            "result": "PASS" if any(row["result"] == "PRIVATE_CANDIDATE_ONLY" for row in read_csv(DECISION)) else "FAIL",
            "detail": "auxiliary algebraic norm retained privately, not promoted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_05_kinetic_rejected",
            "result": "PASS" if any(row["result"] == "REJECT_HAIR_ROUTE" for row in read_csv(DECISION)) else "FAIL",
            "detail": "massive kinetic q-sector rejected as default local-GR route",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_06_claims_blocked",
            "result": "PASS" if all("BLOCKED" in row["status"] or "PRIVATE" in row["status"] or row["status"].startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "local and empirical claims remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_07_decision_next",
            "result": "PASS" if any(row["result"] == "NEXT_2227_PHASE_VOLUME_ORIGIN" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects phase-volume/nonpropagating origin next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_08_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["target_file"].startswith("2227-Y5-R2FR-phase-volume") else "FAIL",
            "detail": "next target is current-numbered phase-volume origin or rejection",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_09_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2226 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_10_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_11_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_12_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_13_formalization_no_2226",
            "result": "PASS" if formalization_2226_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no 2226 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_14_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2226 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2226_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2226 imports the minimal q-sector ansatz audit, rejects promotion, keeps the auxiliary algebraic norm as private scaffolding, and selects phase-volume/nonpropagating origin next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    ansatz = ansatz_rows()
    filters = filter_rows()
    smoke = smoke_rows()
    rejection = rejection_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(ANSATZ_AUDIT, ansatz)
    write_csv(FILTER_RUNNER, filters)
    write_csv(QNORM_SMOKE, smoke)
    write_csv(REJECTION_LEDGER, rejection)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            ansatz,
            filters,
            smoke,
            rejection,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2226 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
