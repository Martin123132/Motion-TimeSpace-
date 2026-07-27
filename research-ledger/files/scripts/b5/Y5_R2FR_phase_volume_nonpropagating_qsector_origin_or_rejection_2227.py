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
DOC = ROOT / "2227-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_PHASE_VOLUME_QSECTOR_ORIGIN_2227"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2226_doc": ROOT / "2226-Y5-R2FR-minimal-parent-q-sector-action-ansatz-or-rejection.md",
    "2226_validation": OUT / "P8_Y5_BRR545_2226_VALIDATION.csv",
    "2226_next": OUT / "P8_Y5_PARENT_QLOC_2226_NEXT_TARGET.csv",
    "1554_doc": ROOT / "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
    "1554_validation": OUT / "P8_Y5_BRR545_1554_VALIDATION.csv",
    "1554_origin": OUT / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_ORIGIN_AUDIT.csv",
    "1554_mapping": OUT / "P8_Y5_PARENT_QLOC_1554_QSECTOR_MAPPING_NONCLAIM.csv",
    "1554_obstruction": OUT / "P8_Y5_PARENT_QLOC_1554_ORIGIN_OBSTRUCTION_LEDGER.csv",
    "1554_runner": OUT / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_RUNNER_NONCLAIM.csv",
    "1554_decision": OUT / "P8_Y5_PARENT_QLOC_1554_DECISION.csv",
    "1554_next": OUT / "P8_Y5_PARENT_QLOC_1554_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2227_SOURCE_REGISTER.csv"
ORIGIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2227_PHASE_VOLUME_ORIGIN_AUDIT.csv"
QSECTOR_MAPPING = OUT / "P8_Y5_PARENT_QLOC_2227_QSECTOR_MAPPING_NONCLAIM.csv"
OBSTRUCTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_2227_ORIGIN_OBSTRUCTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2227_PHASE_VOLUME_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2227_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2227_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2227_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2227_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2227_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2227_PHASE_VOLUME_QSECTOR_ORIGIN_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "phase_volume_qsector_origin_nonclaim_2227.csv",
    "beta_docs": BETA_DOCS / "PHASE_VOLUME_QSECTOR_ORIGIN_2227_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    ORIGIN_AUDIT,
    QSECTOR_MAPPING,
    OBSTRUCTION_LEDGER,
    RUNNER,
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


def formalization_2227_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2227" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current minimal q-sector handoff" if key.startswith("2226") else "older phase-volume/nonpropagating origin evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2227_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def origin_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "ORG2227_0_radial_cell_rule",
            "radial t-r observer-cell preservation",
            "J_q=T sqrt(S)=1 <=> T^2 S=1 <=> R_AB=0",
            "selects p=1 exactly for S=(1-L)^(-p)",
            "separate radial cell preservation is not derived from parent action",
            "MOTIVATED_NOT_PARENT_DERIVED",
        ),
        (
            "ORG2227_1_generic_phase_volume",
            "generic Liouville/canonical phase-volume preservation",
            "J_q J_p=(T sqrt(S))*(1/(T sqrt(S)))=1",
            "canonical phase volume is preserved for every p",
            "does not select GR lane p=1",
            "REJECTED_TOO_WEAK",
        ),
        (
            "ORG2227_2_nonpropagating_constraint",
            "hard nonpropagating constraint",
            "S_constraint=int lambda_R ln(T^2 S) dV",
            "R_AB=0 without exterior reciprocal kinetic hair",
            "lambda_R parent origin remains missing",
            "CLOSURE_ROUTE_NOT_PARENT_DERIVED",
        ),
        (
            "ORG2227_3_cell_current",
            "conserved radial observer-cell current",
            "partial_r(W partial_r R_AB)=0 => W partial_r R_AB=Q_R",
            "conserved reciprocal charge",
            "does not prove Q_R=0 and permits exterior Q_R/r hair",
            "REJECTED_NO_CHARGE_OBSTRUCTION",
        ),
        (
            "ORG2227_4_motion_capacity_balance",
            "motion-capacity balance",
            "clock-capacity loss d ln T is compensated by radial routing d ln sqrt(S)",
            "could motivate d ln(T sqrt(S))=0",
            "needs a parent conservation/no-charge theorem, not just a story",
            "PROMISING_BUT_UNSIGNED",
        ),
        (
            "ORG2227_5_current_verdict",
            "accepted phase-volume q-sector origin",
            "none accepted",
            "no parent q-norm or lambda origin yet",
            "phase-volume motivates nonpropagating q but does not derive parent action/norm",
            "NO_ACCEPTED_ORIGIN",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "origin_id": origin_id,
            "candidate_origin": candidate,
            "mathematical_form": formula,
            "what_it_derives": derives,
            "failure_or_limit": failure,
            "current_status": status,
            **flags(),
        }
        for origin_id, candidate, formula, derives, failure, status in entries
    ]


def mapping_rows() -> list[dict[str, Any]]:
    entries = [
        ("MAP2227_0_q_variable", "q := R_AB = ln(T^2 S)", "maps scalar reciprocal strain into q-sector candidate", "CONDITIONAL_SYMBOLIC_MAP", "does not define full q^A field family or tracefree/PPN sectors"),
        ("MAP2227_1_auxiliary_constraint", "S_lambda=int lambda_q q dV", "nonpropagating closure can force q=0", "CLOSURE_ONLY", "no positive q-norm E follows from multiplier alone"),
        ("MAP2227_2_auxiliary_penalty", "S_penalty=1/2 int mu_q^2 q^2 dV", "would supply algebraic q-norm without gradient hair", "NOT_PARENT_DERIVED", "mu_q^2/G_AB coefficient is inserted unless phase-volume theorem supplies it"),
        ("MAP2227_3_source_current", "J_q=delta S_matter/delta q", "needed for T_source_norm", "MISSING_PARENT_COUPLING", "phase-volume route does not provide matter q-variation"),
        ("MAP2227_4_Cqm", "C_qm=||Dq[v_m]||_E", "needed for same-norm envelope", "MISSING_PARENT_NORM", "no accepted E from phase-volume alone"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "qsector_object": obj,
            "role": role,
            "current_status": status,
            "blocker": blocker,
            **flags(),
        }
        for map_id, obj, role, status, blocker in entries
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    entries = [
        ("OBS2227_0_generic_volume", "generic phase-volume fails", "too weak; true for all p or selects wrong p", "REJECTED"),
        ("OBS2227_1_separate_cell", "separate radial cell is extra", "J_q=1 is exactly the missing theorem", "OPEN"),
        ("OBS2227_2_lambda_origin", "lambda_R origin missing", "constraint works only as closure unless parent supplies multiplier principle", "OPEN"),
        ("OBS2227_3_no_charge", "cell-current no-charge theorem missing", "current conservation gives Q_R constant not zero", "OPEN"),
        ("OBS2227_4_norm", "positive q-norm missing", "constraint gives q=0 but not E for T_source_norm*C_qm", "OPEN"),
        ("OBS2227_5_matter", "matter coupling missing", "phase-volume does not derive J_q", "OPEN"),
        ("OBS2227_6_tracefree", "scalar scope only", "T^2 S=1 does not derive tracefree metric transfer", "OPEN"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "reason": reason,
            "current_status": status,
            **flags(),
        }
        for obstruction_id, obstruction, reason, status in entries
    ]


def runner_rows() -> list[dict[str, Any]]:
    entries = [
        ("RUN2227_0_radial_cell", "radial t-r cell selects p=1", "PASS_CONDITIONAL_NONCLAIM", "works algebraically but origin is unsigned"),
        ("RUN2227_1_generic_phase_volume", "generic phase-volume derives p=1", "REFUSED_REJECTED_TOO_WEAK", "Liouville/canonical volume works for every p"),
        ("RUN2227_2_constraint", "nonpropagating constraint derives q=0", "PASS_CLOSURE_NONCLAIM", "valid closure form but lambda origin missing"),
        ("RUN2227_3_penalty_norm", "phase-volume derives algebraic q-norm", "REFUSED_MISSING_COEFFICIENT_ORIGIN", "mu_q/G_AB not supplied"),
        ("RUN2227_4_cell_current", "cell-current kills reciprocal charge", "REFUSED_NO_CHARGE_OBSTRUCTION", "Q_R hair remains possible"),
        ("RUN2227_5_source_norm", "phase-volume supplies J_q and C_qm", "REFUSED_MISSING_PARENT_COUPLING_AND_NORM", "source current and norm still absent"),
        ("RUN2227_6_score_status", "local GR/Newton score", "REFUSED_NOT_SCORE_READY", "no parent origin accepted"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, check, status, reason in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2227_0_origin_audit", "phase-volume origin audit", "PASS_NONCLAIM", "origin routes and obstructions are explicit"),
        ("CG2227_1_radial_cell", "radial cell selects p=1", "PASS_CONDITIONAL_NONCLAIM", "algebraic selection only"),
        ("CG2227_2_parent_origin", "parent phase-volume theorem", "BLOCKED", "separate radial cell conservation not derived"),
        ("CG2227_3_qnorm", "positive q-norm E", "BLOCKED", "constraint/phase-volume route does not supply E"),
        ("CG2227_4_source", "J_q matter source", "BLOCKED", "matter q-variation missing"),
        ("CG2227_5_local_tests", "local arena claims", "BLOCKED_NO_CLAIM", "no local scoring from phase-volume motivation"),
        ("CG2227_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "lambda/norm/source/tracefree gates remain open"),
        ("CG2227_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private proof line remains mid-derivation"),
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
        ("DEC2227_0_progress", "Phase-volume origin is clarified but not closed.", "MOTIVATED_NOT_DERIVED", "radial cell rule selects p=1 but is not a parent theorem"),
        ("DEC2227_1_closure", "Keep nonpropagating q=R_AB closure available but explicit.", "CLOSURE_ONLY", "it avoids hair but lacks lambda/norm/source origin"),
        ("DEC2227_2_no_promotion", "Do not promote phase-volume language to derivation.", "NO_ACCEPTED_ORIGIN", "generic phase volume is too weak and separate radial cell preservation is extra"),
        ("DEC2227_3_next", "Move to gauge/Noether zero-charge origin for q=R_AB.", "NEXT_2228_GAUGE_NOETHER_ORIGIN", "only a true gauge/no-charge theorem can kill Q_R without inserting the constraint"),
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
            "next_id": "NEXT2227_0_2228",
            "target_file": "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md",
            "target_script": "scripts/Y5_R2FR_gauge_noether_zero_charge_qsector_origin_audit_2228.py",
            "objective": "test whether observer-splitting gauge symmetry or a Noether identity can force Q_R=0 and supply a nonpropagating q-sector origin without importing GR",
            "success_condition": "a parent first-class/gauge/Noether identity forces zero reciprocal charge and supplies the nonpropagating q origin, or the route remains closure-only",
            "do_not": "do not treat coordinate gauge as physical proof; do not drop boundary charge; do not claim GR/Newton reduction",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(OBSTRUCTION_LEDGER, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(OBSTRUCTION_LEDGER),
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
    origin: list[dict[str, Any]],
    mapping: list[dict[str, Any]],
    obstruction: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2227 - Y5/R2FR Phase-Volume Nonpropagating q-sector Origin Or Rejection",
            "## Verdict\n"
            "- 2227 imports the old `1554` phase-volume/nonpropagating q-sector origin audit into the current R2FR line.\n"
            "- The radial observer-cell rule is interesting: it algebraically selects `T^2 S=1`, hence the GR-like scalar lane `p=1`.\n"
            "- It is not yet a derivation because separate radial cell preservation is exactly the missing parent theorem.\n"
            "- Generic Liouville/canonical phase-volume preservation is too weak because it holds for every `p`, not just the GR lane.\n"
            "- The nonpropagating closure remains useful, but `lambda_R`, `E/G_AB`, `J_q`, zero charge, and tracefree transfer remain open.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Phase-Volume Origin Audit\n"
            + md_table(origin, ["origin_id", "candidate_origin", "mathematical_form", "what_it_derives", "failure_or_limit", "current_status"]),
            "## q-sector Mapping\n"
            + md_table(mapping, ["map_id", "qsector_object", "role", "current_status", "blocker"]),
            "## Origin Obstruction Ledger\n"
            + md_table(obstruction, ["obstruction_id", "obstruction", "reason", "current_status"]),
            "## Phase-Volume Runner\n"
            + md_table(runner, ["runner_id", "check", "current_status", "reason"]),
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
            "This checkpoint says the motion/time/space simplification is not nonsense; it has a real algebraic target. But it is still a motivated route, not a field-theory derivation. To make it serious, the next proof must turn the radial cell condition into a parent gauge, Noether, or first-class constraint theorem that kills the reciprocal charge `Q_R` without borrowing GR or silently deleting boundary flux.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2227 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2226_validation"]) and validation_pass(SOURCE_FILES["1554_validation"]) else "FAIL",
            "detail": "2226 and 1554 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_02_origin_audit",
            "result": "PASS" if any(row["current_status"] == "NO_ACCEPTED_ORIGIN" for row in read_csv(ORIGIN_AUDIT)) else "FAIL",
            "detail": "phase-volume audit records no accepted origin",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_03_radial_cell_conditional",
            "result": "PASS" if any(row["current_status"] == "MOTIVATED_NOT_PARENT_DERIVED" for row in read_csv(ORIGIN_AUDIT)) else "FAIL",
            "detail": "radial cell rule retained only as motivated/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_04_generic_phase_volume_rejected",
            "result": "PASS" if any(row["current_status"] == "REJECTED_TOO_WEAK" for row in read_csv(ORIGIN_AUDIT)) else "FAIL",
            "detail": "generic phase-volume route rejected as too weak",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_05_mapping_nonclaim",
            "result": "PASS" if any(row["current_status"] == "CLOSURE_ONLY" for row in read_csv(QSECTOR_MAPPING)) else "FAIL",
            "detail": "q-sector mapping remains nonclaim/closure-only",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_06_obstructions",
            "result": "PASS" if sum(row["current_status"] == "OPEN" for row in read_csv(OBSTRUCTION_LEDGER)) >= 5 else "FAIL",
            "detail": "origin obstructions recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_07_claims_blocked",
            "result": "PASS" if all("BLOCKED" in row["status"] or row["status"].startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "GR/Newton and empirical claims remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_08_decision_next",
            "result": "PASS" if any(row["result"] == "NEXT_2228_GAUGE_NOETHER_ORIGIN" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects gauge/Noether zero-charge origin next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_09_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["target_file"].startswith("2228-Y5-R2FR-gauge-noether") else "FAIL",
            "detail": "next target is current-numbered gauge/Noether origin audit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_10_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2227 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_11_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_12_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_13_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_14_formalization_no_2227",
            "result": "PASS" if formalization_2227_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no 2227 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_15_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2227 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2227_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2227 imports the phase-volume origin audit, keeps radial-cell selection conditional, rejects generic phase-volume as too weak, and selects gauge/Noether zero-charge origin next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    origin = origin_rows()
    mapping = mapping_rows()
    obstruction = obstruction_rows()
    runner = runner_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(ORIGIN_AUDIT, origin)
    write_csv(QSECTOR_MAPPING, mapping)
    write_csv(OBSTRUCTION_LEDGER, obstruction)
    write_csv(RUNNER, runner)
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
            origin,
            mapping,
            obstruction,
            runner,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2227 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
