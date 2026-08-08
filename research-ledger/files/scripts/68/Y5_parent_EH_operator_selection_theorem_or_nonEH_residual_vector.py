from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1512-Y5-parent-EH-operator-selection-theorem-or-nonEH-residual-vector.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1511_validation": OUT / "P8_Y5_BRR545_1511_VALIDATION.csv",
    "1511_contract": OUT / "P8_Y5_PARENT_GR_NEWTON_1511_MINIMAL_LOCAL_LIMIT_CONTRACT.csv",
    "1511_blockers": OUT / "P8_Y5_PARENT_GR_NEWTON_1511_OPEN_BLOCKER_STACK.csv",
    "1511_priority": OUT / "P8_Y5_PARENT_GR_NEWTON_1511_DERIVATION_PRIORITY_DECISION.csv",
    "958_eh_premise": OUT / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
    "958_eh_attempt": OUT / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
    "959_doc": ROOT / "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
    "960_doc": ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "964_doc": ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
    "local_eh_r11_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "local_eh_selector": OUT / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv",
    "local_eh_decision": OUT / "P8_LOCAL_EH_R11_DECISION.csv",
    "r11_vector": OUT / "R11_nonEH_operator_vector_executable.csv",
}

THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_EH_1512_SELECTION_THEOREM_ATTEMPT.csv"
PREMISE_AUDIT = OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv"
NON_EH_VECTOR = OUT / "P8_Y5_PARENT_EH_1512_NON_EH_RESIDUAL_VECTOR.csv"
OPERATOR_DECISION = OUT / "P8_Y5_PARENT_EH_1512_OPERATOR_DECISION.csv"
NEWTON_PPN_IMPACT = OUT / "P8_Y5_PARENT_EH_1512_NEWTON_PPN_IMPACT.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_EH_1512_LOCAL_GR_NEWTON_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_EH_1512_SCORE_READINESS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_EH_1512_REJECTION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_EH_1512_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1512_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1512"
QUAR_THEOREM = QUARANTINE / "EH_SELECTION_THEOREM_ATTEMPT_NONCLAIM.csv"
QUAR_VECTOR = QUARANTINE / "NON_EH_RESIDUAL_VECTOR_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "OPERATOR_DECISION_NONCLAIM.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "parent_eh_selection_theorem_attempt_nonclaim_1512.csv"
BRANCH_VECTOR = BRANCH_RESIDUALS / "non_eh_residual_vector_nonclaim_1512.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "parent_eh_operator_decision_nonclaim_1512.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "passes_for_claim", "accepted_for_scoring"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1512_0_conditional_EH_selection",
            "statement": "If the compact local exterior branch is 4D, local, diffeomorphism-invariant, metric-only, Levi-Civita, has second-order metric equations, and all boundary/topological terms are harmless, then the local metric operator is EH plus Lambda/topological boundary terms.",
            "mathematical_form": "S_ext[g]=int sqrt(-g)(a R - 2 Lambda)+S_boundary/topological; E_MTS^{mu nu}=a G^{mu nu}+a Lambda g^{mu nu}",
            "proof_status": "EXACT_CONDITIONAL_LOVELOCK_STYLE_ROUTE",
            "current_parent_status": "PREMISES_NOT_PARENT_SIGNED",
            "source_paths": source_list("958_eh_attempt", "1511_contract"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1512_1_no_smuggling_guard",
            "statement": "EH may be used as a reference operator only after the parent branch supplies the selection premises; importing Einstein equations as the left-hand side is not a derivation.",
            "mathematical_form": "G_parent_LHS = Delta_EH_operator + Delta_Qtau_parent + Delta_Bianchi_Ward + Delta_GR_smuggling + higher_operator_tail",
            "proof_status": "GUARDRAIL_FROM_1212_1511",
            "current_parent_status": "EH_IMPORT_FORBIDDEN_FOR_CLAIM",
            "source_paths": source_list("1511_contract", "1511_blockers"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1512_2_current_verdict",
            "statement": "The current corpus has the EH theorem shape but not the parent-signed metric-only, second-order, Levi-Civita, no-extra-field/minimality premises; therefore non-EH residual vector retention is required.",
            "mathematical_form": "E_MTS^{mu nu}=G^{mu nu}+Lambda g^{mu nu}+DeltaE_R11^{mu nu}; DeltaE_R11 retained",
            "proof_status": "DERIVED_GATE_LOGIC_NOT_EH_CLAIM",
            "current_parent_status": "NON_EH_VECTOR_REQUIRED",
            "source_paths": source_list("1511_priority", "local_eh_r11_audit", "r11_vector"),
            **flags(),
        },
    ]


def premise_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRE1512_0_local_4D", "local 4D compact exterior branch", "needed before Lovelock-style selection applies", "STRUCTURAL_TARGET_NOT_PARENT_SIGNED", "1511/958"),
        ("PRE1512_1_metric_only", "metric-only observed action", "excludes independent scalar/vector/domain/projector/memory/coframe/connection carriers", "NOT_PARENT_DERIVED", "958/959"),
        ("PRE1512_2_second_order", "second-order metric equations", "kills R2/fR/Ricci2/Weyl2/nonlocal higher derivative leakage", "CENTRAL_BLOCKER_NOT_DERIVED", "958/963/964"),
        ("PRE1512_3_Levi_Civita", "Levi-Civita observed connection", "kills torsion/nonmetricity and independent connection readout effects", "NOT_PARENT_DERIVED", "958/960"),
        ("PRE1512_4_no_extra_fields", "no extra local stress/charge carriers", "kills bulk X, scalar class, vector preferred frame, memory, projector/domain stress", "ACTIVE_PRIMARY_OBSTRUCTION", "957/959/R11"),
        ("PRE1512_5_boundary_harmless", "boundary/topological no-flux harmlessness", "prevents boundary mass, shear, preferred-location, alpha3, xi and Gdot leakage", "CONDITIONAL_NOT_DERIVED", "958/R11"),
        ("PRE1512_6_parent_minimality", "primitive no-natural-marker/no-extension minimality", "would forbid marker-prefactor and integrated-out curvature tower countermodels", "THEOREM_NOT_PROVEN", "964"),
        ("PRE1512_7_acceptance", "EH operator claim", "allowed only if PRE1512_0 through PRE1512_6 close or every failure is explicitly bounded", "BLOCKED", "1511"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": premise_id,
            "premise": premise,
            "why_needed": why,
            "current_status": status,
            "source_cluster": cluster,
            "parent_signed": False,
            **flags(),
        }
        for premise_id, premise, why, status, cluster in rows
    ]


def non_eh_rows() -> list[dict[str, Any]]:
    retained = []
    for row in read_csv(SOURCE_FILES["r11_vector"]):
        retained.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "vector_id": f"R11_1512_{len(retained):02d}",
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "coefficient_value": row["coefficient_value"],
                "operator_form": row["operator_form"],
                "weak_field_map": row["weak_field_map"],
                "induced_observable": row["induced_observable"],
                "current_status": "RETAINED_NON_EH_RESIDUAL",
                "needed_to_remove": "parent zero theorem, topological/no-flux theorem, double-zero selector, or sourced numeric coefficient/bound",
                "source_file": rel(SOURCE_FILES["r11_vector"]),
                **flags(),
            }
        )
    return retained


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1512_0_EH_route",
            "decision": "EH selection theorem is exact but conditional",
            "rationale": "the theorem only fires after local 4D metric-only second-order LC/no-extra-field/no-flux premises are parent-owned",
            "result": "NO_EH_CLAIM",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1512_1_residual_route",
            "decision": "retain executable non-EH residual vector",
            "rationale": "current R11 families cover the legal counterterms and extra carriers that would otherwise be silently dropped",
            "result": "NON_EH_VECTOR_REQUIRED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1512_2_next",
            "decision": "attack primitive no-higher-derivative/minimality first",
            "rationale": "R2/fR and higher-curvature leakage are the cleanest direct violations of EH operator selection; metric-only/LC and extra-field silence remain next in line",
            "result": "NEXT_1513_MINIMALITY",
            **flags(),
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    rows = [
        ("IMP1512_0_Newton", "Newton limit", "still blocked", "without EH operator selection, Poisson coefficient algebra is premature"),
        ("IMP1512_1_PPN", "PPN residual vector", "still blocked", "gamma/beta/preferred-frame/Gdot rows need operator/source branch first"),
        ("IMP1512_2_GM", "measured-GM transfer", "deferred", "source-GM transfer is meaningful only after exterior operator branch is owned enough"),
        ("IMP1512_3_R10", "R10 finite-range", "frozen", "R10 remains empirical plumbing, not EH operator proof"),
        ("IMP1512_4_theory_spine", "field-theory spine", "improved", "EH theorem shape and residual fallback are now explicit"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "impact_id": impact_id,
            "target": target,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for impact_id, target, status, reason in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1512_0",
            "object": "EH operator selection",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "effect": "no local-GR/Newton claim; proceed to premise derivation",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1512_1",
            "object": "non-EH residual vector",
            "status": "RETAINED_REQUIRED",
            "effect": "prevents silent dropping of higher-curvature, connection, scalar, vector, memory, boundary, source-normalization, and projector terms",
            **flags(),
        },
    ]


def score_rows(vector: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1512_0",
            "status": "NOT_SCORE_READY",
            "reason": "operator-selection checkpoint; all retained non-EH rows still lack zero theorem or numeric sourced coefficients",
            "retained_vector_rows": len(vector),
            **flags(),
        }
    ]


def rejection_rows() -> list[dict[str, Any]]:
    shortcuts = [
        ("REJ1512_0", "claim EH because the Lovelock theorem exists", "Lovelock route requires parent-signed premises; theorem shape is not a premise proof"),
        ("REJ1512_1", "claim second-order by ignoring R2/fR", "R2/fR countermodels remain legal until minimality/no-higher-derivative theorem closes"),
        ("REJ1512_2", "claim Levi-Civita by using observed metric notation", "torsion/nonmetricity rows remain unless parent metric-only/no-hypermomentum route closes"),
        ("REJ1512_3", "drop residual vector to simplify Newton limit", "that would fake GR and lose Bianchi/PPN accountability"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "rejected_shortcut": shortcut,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, reason in shortcuts
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1512_0_1513",
            "next_target": "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md",
            "script": "scripts/Y5_parent_primitive_minimality_no_higher_derivative_theorem_or_R11_vector_lock.py",
            "objective": "try to prove the primitive quotient/no-natural-marker/no-higher-derivative minimality clause that would remove R2/fR and higher-curvature leakage; if it fails, lock the non-EH vector as the active local operator branch",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (THEOREM_ATTEMPT, QUAR_THEOREM),
        (NON_EH_VECTOR, QUAR_VECTOR),
        (OPERATOR_DECISION, QUAR_DECISION),
        (THEOREM_ATTEMPT, BRANCH_THEOREM),
        (NON_EH_VECTOR, BRANCH_VECTOR),
        (OPERATOR_DECISION, BRANCH_DECISION),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], premises: list[dict[str, Any]], vector: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    conditional_theorem = any(row["theorem_id"] == "THM1512_0_conditional_EH_selection" and row["proof_status"] == "EXACT_CONDITIONAL_LOVELOCK_STYLE_ROUTE" for row in theorem)
    premises_block_eh = any(row["premise_id"] == "PRE1512_7_acceptance" and row["current_status"] == "BLOCKED" for row in premises)
    no_parent_signed = all(row["parent_signed"] is False for row in premises)
    vector_retained = len(vector) >= 10 and all(row["current_status"] == "RETAINED_NON_EH_RESIDUAL" for row in vector)
    next_minimality = any(row["decision_id"] == "DEC1512_2_next" and row["result"] == "NEXT_1513_MINIMALITY" for row in decisions)
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_THEOREM, QUAR_VECTOR, QUAR_DECISION, BRANCH_THEOREM, BRANCH_VECTOR, BRANCH_DECISION])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1512_0_sources", source_paths_exist, "all cited EH/R11 source paths exist"),
        ("VAL1512_1_conditional_theorem", conditional_theorem, "EH selection theorem recorded as exact conditional route"),
        ("VAL1512_2_eh_blocked", premises_block_eh, "EH acceptance remains blocked until premises close"),
        ("VAL1512_3_no_parent_signed", no_parent_signed, "no decisive premise is falsely marked parent-signed"),
        ("VAL1512_4_vector_retained", vector_retained, "non-EH residual vector retained with at least 10 families"),
        ("VAL1512_5_next_minimality", next_minimality, "next target selects primitive minimality/no-higher-derivative theorem"),
        ("VAL1512_6_csv_parse", csv_parse_ok, "all generated 1512 CSVs parse cleanly"),
        ("VAL1512_7_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
        ("VAL1512_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1512_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1512_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1512_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1512 kept EH selection conditional, retained the non-EH residual vector, and selected primitive minimality/no-higher-derivative as next target"
            if overall
            else "1512 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    theorem: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    impacts: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1512 - Parent EH Operator Selection Theorem or Non-EH Residual Vector",
                "",
                "## Verdict",
                "- The EH/Lovelock-style route is mathematically clean but still conditional: the parent has not signed the local 4D, metric-only, Levi-Civita, second-order, no-extra-field, no-flux premises.",
                "- Therefore MTS does not yet earn a local EH/Newton claim; the non-EH residual vector must stay active.",
                "- The next best derivation target is primitive minimality/no-higher-derivative/no-natural-marker, because that is the cleanest way to remove R2/fR and higher-curvature leakage.",
                "",
                "## EH Selection Theorem Attempt",
                md_table(theorem, ["theorem_id", "proof_status", "current_parent_status"]),
                "",
                "## Premise Signing Audit",
                md_table(premises, ["premise_id", "premise", "current_status", "parent_signed"]),
                "",
                "## Retained Non-EH Vector",
                md_table(vector, ["vector_id", "operator_family", "coefficient_symbol", "current_status"]),
                "",
                "## Operator Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Newton/PPN Impact",
                md_table(impacts, ["impact_id", "target", "status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    theorem = theorem_rows()
    premises = premise_rows()
    vector = non_eh_rows()
    decisions = decision_rows()
    impacts = impact_rows()
    local_status = local_status_rows()
    score = score_rows(vector)
    rejections = rejection_rows()
    next_rows = next_target_rows()

    write_csv(THEOREM_ATTEMPT, theorem)
    write_csv(PREMISE_AUDIT, premises)
    write_csv(NON_EH_VECTOR, vector)
    write_csv(OPERATOR_DECISION, decisions)
    write_csv(NEWTON_PPN_IMPACT, impacts)
    write_csv(LOCAL_STATUS, local_status)
    write_csv(SCORE_READINESS, score)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        THEOREM_ATTEMPT,
        PREMISE_AUDIT,
        NON_EH_VECTOR,
        OPERATOR_DECISION,
        NEWTON_PPN_IMPACT,
        LOCAL_STATUS,
        SCORE_READINESS,
        REJECTION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, premises, vector, decisions)
    write_csv(VALIDATION, validation)
    write_doc(theorem, premises, vector, decisions, impacts, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
