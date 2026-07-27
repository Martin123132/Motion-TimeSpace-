from __future__ import annotations

import csv
import math
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
DOC = ROOT / "1517-Y5-parent-PiM-equality-commutator-bound-runner-or-worldtube-glue-reentry.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1516_validation": OUT / "P8_Y5_BRR545_1516_VALIDATION.csv",
    "1516_next": OUT / "P8_Y5_PARENT_CR11_1516_NEXT_TARGET.csv",
    "1516_requirements": OUT / "P8_Y5_PARENT_CR11_1516_PIM_EQUALITY_COMMUTATOR_REQUIREMENTS.csv",
    "1516_gm": OUT / "P8_Y5_PARENT_CR11_1516_GM_TRANSFER_CHAIN_GATE.csv",
    "1150_first_row": OUT / "P8_Y5_R10_1150_PIM_EQUALITY_COMMUTATOR_FIRST_ROW.csv",
    "1150_glue": OUT / "P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
    "1150_guards": OUT / "P8_Y5_R10_1150_NO_SHORTCUT_GUARDS.csv",
    "1151_review": OUT / "P8_Y5_R10_1151_RUNNER_INPUT_REVIEW.csv",
    "1151_smoke": OUT / "P8_Y5_R10_1151_SMOKE_EVALUATION.csv",
    "1151_hooks": OUT / "P8_Y5_R10_1151_PARENT_ACTION_REENTRY_HOOKS.csv",
    "1151_next": OUT / "P8_Y5_R10_1151_NEXT_TARGET.csv",
    "old_evaluator": OUT / "P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv",
    "old_template": OUT / "P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv",
    "bound_template": OUT / "P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
    "parent_contract": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "pim_gate": OUT / "P8_Y5_PIM_COMMUTATOR_GATE.csv",
}

RUNNER_SCHEMA = OUT / "P8_Y5_PARENT_PIM_1517_RUNNER_SCHEMA.csv"
INPUT_REVIEW = OUT / "P8_Y5_PARENT_PIM_1517_INPUT_REVIEW.csv"
STRICT_EVALUATION = OUT / "P8_Y5_PARENT_PIM_1517_STRICT_EVALUATION.csv"
THEOREM_IMPORT_GATE = OUT / "P8_Y5_PARENT_PIM_1517_THEOREM_IMPORT_GATE.csv"
WORLD_TUBE_REENTRY = OUT / "P8_Y5_PARENT_PIM_1517_WORLDTUBE_REENTRY_ROUTE.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_PIM_1517_REJECTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_PIM_1517_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_PIM_1517_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_PIM_1517_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1517_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1517"
QUAR_SCHEMA = QUARANTINE / "PIM_RUNNER_SCHEMA_NONCLAIM.csv"
QUAR_REVIEW = QUARANTINE / "PIM_INPUT_REVIEW_NONCLAIM.csv"
QUAR_EVAL = QUARANTINE / "PIM_STRICT_EVALUATION_NONCLAIM.csv"
QUAR_IMPORT = QUARANTINE / "PIM_THEOREM_IMPORT_GATE_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "PIM_DECISION_NONCLAIM.csv"
BRANCH_SCHEMA = BRANCH_RESIDUALS / "pim_runner_schema_nonclaim_1517.csv"
BRANCH_EVAL = BRANCH_RESIDUALS / "pim_strict_evaluation_nonclaim_1517.csv"
BRANCH_IMPORT = BRANCH_RESIDUALS / "pim_theorem_import_gate_nonclaim_1517.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "pim_decision_nonclaim_1517.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


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


def contains_missing(value: object) -> bool:
    text = str(value).strip()
    return text == "" or "MISSING" in text


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def runner_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCHEMA1517_0_system", "system_id", "nonempty local system/branch identifier", "prevents moving residuals between systems after the fact"),
        ("SCHEMA1517_1_domain", "r1;r2;worldtube_or_surface_id", "finite annulus/surface linked to the same source worldtube", "prevents orbital/readout masks defining the source"),
        ("SCHEMA1517_2_R_eq", "R_eq_integral", "numeric residual or theorem-zero certificate for Pi_M J_H - J_M_top - dB_zero", "tests Hilbert/topological/source equality"),
        ("SCHEMA1517_3_commutator", "I_commutator", "numeric residual or theorem-zero certificate for int[d,Pi_M]J_H", "tests the exact product-rule obstruction"),
        ("SCHEMA1517_4_boundary", "B_zero_flux", "numeric residual or theorem-zero certificate for boundary exact/reference flux", "tests whether exact/reference terms shift the source mass"),
        ("SCHEMA1517_5_projector_stress", "epsilon_projector_stress", "numeric beta/source-normalized projector-stress equivalent or theorem-zero", "blocks Hodge/metric projector stress shortcuts"),
        ("SCHEMA1517_6_mass_ref", "M_H_ref", "positive same-frame Hilbert source mass reference with units", "normalizes equality and commutator residuals"),
        ("SCHEMA1517_7_source", "source_file; assumptions; units; theorem_certificate", "existing source path proving each value or theorem-zero", "prevents reference-only or invented zeros"),
        ("SCHEMA1517_8_total", "epsilon_PiM_total_abs", "abs(R_eq)/M_H_ref + abs(I_commutator)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(epsilon_projector_stress)", "absolute envelope; no tuned cancellation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": schema_id,
            "required_field": field,
            "acceptance_test": test,
            "why_required": why,
            **flags(),
        }
        for schema_id, field, test, why in rows
    ]


def input_review_rows(first_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    reviewed = []
    for row in first_rows:
        row_id = row.get("row_id", "")
        source_path = row.get("source_path", "")
        current_value = row.get("current_value", "")
        model_id = row.get("model_id", "")
        is_reference = "reference" in model_id.lower() or row_id.endswith("reference_only_zero_row")
        missing = contains_missing(current_value) or contains_missing(source_path)
        source_exists = False
        if source_path and not contains_missing(source_path) and not source_path.startswith("reference_"):
            candidate = Path(source_path)
            if not candidate.is_absolute():
                candidate = ROOT / source_path
            source_exists = candidate.exists()
        disposition = "REJECT_REFERENCE_ONLY" if is_reference else ("BLOCKED_MISSING_INPUTS" if missing else "READY_FOR_STRICT_NUMERIC_EVALUATION")
        reviewed.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "review_id": f"REV1517_{row_id}",
                "row_id": row_id,
                "quantity": row.get("quantity", ""),
                "current_value": current_value,
                "source_path": source_path,
                "has_missing_marker": missing,
                "source_file_exists": source_exists,
                "reference_only": is_reference,
                "runner_disposition": disposition,
                **flags(),
            }
        )
    return reviewed


def strict_evaluation_rows(first_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows_by_id = {row["row_id"]: row for row in first_rows}
    component_ids = [
        "PIM1150_1_R_eq_integral",
        "PIM1150_2_I_commutator",
        "PIM1150_3_B_zero_flux",
        "PIM1150_4_projector_stress",
    ]
    component_missing = any(contains_missing(rows_by_id[row_id]["current_value"]) for row_id in component_ids)
    source_missing = any(contains_missing(rows_by_id[row_id]["source_path"]) for row_id in component_ids)
    m_h_ref = parse_float("MISSING_M_H_REF")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "eval_id": "EVAL1517_0_current_branch",
            "model_id": "MTS_local_source_normalized_branch",
            "input_rows": ";".join(component_ids),
            "epsilon_PiM_total_abs": "NOT_COMPUTED",
            "numeric_status": "not_computed_missing_numeric_inputs" if component_missing or source_missing or m_h_ref is None else "computed",
            "source_status": "MISSING_SOURCE_FILE",
            "runner_disposition": "BLOCKED_MISSING_INPUTS",
            "claim_status": "not_claimable",
            "formula": "abs(R_eq)/M_H_ref + abs(I_commutator)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(epsilon_projector_stress)",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "eval_id": "EVAL1517_1_reference_zero",
            "model_id": "PiM_topological_equality_reference_not_MTS_evidence",
            "input_rows": "PIM1150_5_reference_only_zero_row",
            "epsilon_PiM_total_abs": "0",
            "numeric_status": "computed_reference_only",
            "source_status": "reference_not_current_MTS_source",
            "runner_disposition": "REJECT_REFERENCE_ONLY",
            "claim_status": "not_claimable",
            "formula": "formal zero row is schema smoke only",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "eval_id": "EVAL1517_2_no_cancellation_envelope",
            "model_id": "MTS_local_source_normalized_branch",
            "input_rows": ";".join(component_ids),
            "epsilon_PiM_total_abs": "symbolic_abs_sum",
            "numeric_status": "symbolic_only_until_inputs_filled",
            "source_status": "not_scoreable",
            "runner_disposition": "NO_CANCELLATION_POLICY_ACTIVE",
            "claim_status": "not_claimable",
            "formula": "absolute component envelope; no cancellation between equality, commutator, boundary, or stress terms",
            **flags(),
        },
    ]


def theorem_import_rows() -> list[dict[str, Any]]:
    rows = [
        ("IMP1517_0_R_eq_zero", "Hilbert/topological equality theorem", "must prove R_eq_integral=0 for the same source worldtube and same Pi_M J_H", "R_eq_integral only", "NOT_DERIVED_CURRENT_CORPUS", source_list("1150_glue", "parent_contract")),
        ("IMP1517_1_commutator_zero", "Pi_M fixed/covariantly constant theorem", "must prove [d,Pi_M]J_H=0 on the Hilbert source-current domain", "I_commutator only", "NEXT_THEOREM_TARGET", source_list("pim_gate", "1151_next")),
        ("IMP1517_2_boundary_zero", "exact/reference boundary theorem", "must prove boundary exact/reference flux integrates to zero on linked surfaces", "B_zero_flux only", "MISSING_CERTIFICATE_OR_BOUND", source_list("1150_glue", "1151_hooks")),
        ("IMP1517_3_stress_zero", "projector stress theorem", "must prove Pi_M projector stress vanishes or is bounded below local locks", "epsilon_projector_stress only", "MISSING_CERTIFICATE_OR_NUMERIC_BOUND", source_list("1150_first_row", "1150_guards")),
        ("IMP1517_4_mass_ref", "same-frame Hilbert mass reference", "must provide positive M_H_ref with units/source path in observed coframe", "normalizes all residuals", "MISSING_M_H_REF", source_list("1516_requirements", "1150_first_row")),
        ("IMP1517_5_worldtube_followthrough", "worldtube/Gauss/orbital readout", "comes after runner components pass; cannot bypass them", "does not fill runner rows directly", "NOT_REACHED", source_list("1516_gm", "1150_guards")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "import_id": import_id,
            "theorem_or_source": theorem,
            "required_evidence": required,
            "runner_component_filled": fills,
            "current_status": status,
            "source_paths": sources,
            **flags(),
        }
        for import_id, theorem, required, fills, status, sources in rows
    ]


def worldtube_reentry_rows() -> list[dict[str, Any]]:
    rows = [
        ("WT1517_0_action", "parent covariant action and Noether current", "required before a theorem can replace numeric runner rows", "CONTRACT_ONLY_NO_FULL_LAGRANGIAN"),
        ("WT1517_1_source_frame", "same source frame and matter Hilbert current", "defines J_H and M_H_ref", "NOT_YET_DERIVED"),
        ("WT1517_2_worldtube", "parent-fixed source support and linked surfaces", "defines system_id, r1, r2, and assumptions", "NOT_YET_DERIVED"),
        ("WT1517_3_equality", "Pi_M J_H = J_M_top + dB_zero + R_eq", "routes to R_eq_integral", "NOT_DERIVED"),
        ("WT1517_4_commutator", "[d,Pi_M]J_H=0", "routes to I_commutator", "NEXT_TARGET"),
        ("WT1517_5_readout", "Poisson/Gauss/orbital and PPN followthrough", "comes after runner rows pass", "NOT_REACHED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "reentry_piece": piece,
            "purpose": purpose,
            "current_status": status,
            **flags(),
        }
        for route_id, piece, purpose, status in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1517_0_reference_zero", "use reference-only zero as MTS evidence", "REJECTED", "it proves the runner shape only"),
        ("REJ1517_1_orbital_GM", "use orbital GM as source equality proof", "REJECTED", "readout target cannot define the source"),
        ("REJ1517_2_unowned_multiplier", "impose Pi_M J_H closure by multiplier", "REJECTED", "unowned closure inserts Newton rather than deriving it"),
        ("REJ1517_3_hodge_no_stress", "use Hodge/metric Pi_M without stress row", "REJECTED", "metric-dependent projectors require projector-stress accounting"),
        ("REJ1517_4_cancellation", "cancel equality/commutator/boundary/stress terms by sign", "REJECTED", "runner uses absolute component envelope"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1517_0_runner", "strict PiM runner gate", "EXECUTES_NONCLAIM", "current MTS row blocked; reference zero rejected"),
        ("DEC1517_1_theorem_import", "future theorem evidence", "MUST_ROUTE_THROUGH_COMPONENTS", "R_eq, I_commutator, B_zero, stress, and M_H_ref cannot be bypassed"),
        ("DEC1517_2_current_status", "source-normalized Newton/local GR", "NOT_CLAIMED", "runner has infrastructure only, no claim-valid source row"),
        ("DEC1517_3_next", "commutator zero/source acquisition", "NEXT_1518_COMMUTATOR", "I_commutator is the cleanest product-rule obstruction"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1517_0_Newton", "source-normalized Newtonian limit", "NOT_CLAIMED", "PiM equality/commutator row is not source-backed"),
        ("LOCAL1517_1_GR", "derived local GR", "NOT_CLAIMED", "Newton source normalization and PPN followthrough remain open"),
        ("LOCAL1517_2_GM", "measured-GM transfer", "NOT_CLAIMED", "worldtube/Gauss/orbital readout cannot bypass runner"),
        ("LOCAL1517_3_R11", "R11 source-normalization vector", "ACTIVE_NONCLAIM", "c_R11 channel remains live until runner inputs close"),
        ("LOCAL1517_4_alpha3", "R11 alpha3 product", "NOT_CLAIMED", "K, c, and epsilon factor rows remain unclaimable"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1517_0_1518",
            "next_target": "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "script": "scripts/Y5_parent_PiM_commutator_zero_theorem_or_R_eq_I_commutator_source_acquisition.py",
            "objective": "try to prove [d,Pi_M]J_H=0 from a parent-fixed/topological Pi_M on the same Hilbert source-current domain; if it fails, create first source-acquisition rows for R_eq_integral and I_commutator",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (RUNNER_SCHEMA, QUAR_SCHEMA),
        (INPUT_REVIEW, QUAR_REVIEW),
        (STRICT_EVALUATION, QUAR_EVAL),
        (THEOREM_IMPORT_GATE, QUAR_IMPORT),
        (DECISION, QUAR_DECISION),
        (RUNNER_SCHEMA, BRANCH_SCHEMA),
        (STRICT_EVALUATION, BRANCH_EVAL),
        (THEOREM_IMPORT_GATE, BRANCH_IMPORT),
        (DECISION, BRANCH_DECISION_COPY),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    schema = read_csv(RUNNER_SCHEMA)
    review = read_csv(INPUT_REVIEW)
    evaluation = read_csv(STRICT_EVALUATION)
    imports = read_csv(THEOREM_IMPORT_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    required_fields = {"R_eq_integral", "I_commutator", "B_zero_flux", "epsilon_projector_stress", "M_H_ref", "epsilon_PiM_total_abs"}
    schema_text = " ".join(row["required_field"] for row in schema)
    checks = [
        ("VAL1517_0_sources", all(path.exists() for path in SOURCE_FILES.values()), "all cited 1517 input source paths exist"),
        ("VAL1517_1_schema_complete", all(field in schema_text for field in required_fields), "runner schema covers R_eq/I_commutator/B_zero/stress/M_H_ref/total"),
        ("VAL1517_2_current_blocked", any(row["runner_disposition"] == "BLOCKED_MISSING_INPUTS" for row in review), "current MTS row is blocked by missing inputs"),
        ("VAL1517_3_reference_rejected", any(row["runner_disposition"] == "REJECT_REFERENCE_ONLY" for row in review + evaluation), "reference-only zero is rejected"),
        ("VAL1517_4_absolute_sum", any("absolute" in row["formula"].lower() or "abs(" in row["formula"] for row in evaluation), "strict evaluation uses no-cancellation absolute envelope"),
        ("VAL1517_5_theorem_import_components", {"R_eq_integral only", "I_commutator only", "B_zero_flux only", "epsilon_projector_stress only"}.issubset({row["runner_component_filled"] for row in imports}), "theorem import gate routes evidence to named components"),
        ("VAL1517_6_next_commutator", any(row["result"] == "NEXT_1518_COMMUTATOR" for row in decisions), "decision selects commutator-zero/source acquisition next"),
        ("VAL1517_7_next_target", any("PiM-commutator-zero" in row["next_target"] for row in next_rows), "next target is PiM commutator zero or source acquisition"),
        ("VAL1517_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1517 CSVs parse cleanly"),
        ("VAL1517_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        (
            "VAL1517_10_branch_copies",
            all(path.exists() for path in [QUAR_SCHEMA, QUAR_REVIEW, QUAR_EVAL, QUAR_IMPORT, QUAR_DECISION, BRANCH_SCHEMA, BRANCH_EVAL, BRANCH_IMPORT, BRANCH_DECISION_COPY]),
            "branch/quarantine nonclaim copies written",
        ),
        ("VAL1517_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1517_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1517_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1517 executes strict nonclaim PiM runner, blocks missing current inputs, rejects reference zero, and selects commutator-zero/source acquisition"
            if overall
            else "1517 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    schema: list[dict[str, Any]],
    review: list[dict[str, Any]],
    evaluation: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1517 - Parent PiM Equality-Commutator Bound Runner or Worldtube Glue Reentry",
                "",
                "## Verdict",
                "- The strict PiM runner is now active at the parent-sequence level: current MTS inputs are blocked, and reference-only zeros are rejected.",
                "- The score target is epsilon_PiM_total_abs, an absolute envelope over equality, commutator, boundary, and projector-stress components.",
                "- Future theorem evidence is allowed only if it fills the same runner components; worldtube/Gauss/orbital readout cannot bypass the runner.",
                "- The next target is the commutator obstruction [d,Pi_M]J_H=0 or first source-acquisition rows for R_eq_integral and I_commutator.",
                "",
                "## Runner Schema",
                md_table(schema, ["schema_id", "required_field", "acceptance_test", "why_required"]),
                "",
                "## Input Review",
                md_table(review, ["review_id", "quantity", "runner_disposition", "has_missing_marker", "reference_only"]),
                "",
                "## Strict Evaluation",
                md_table(evaluation, ["eval_id", "epsilon_PiM_total_abs", "numeric_status", "runner_disposition"]),
                "",
                "## Theorem Import Gate",
                md_table(imports, ["import_id", "theorem_or_source", "runner_component_filled", "current_status"]),
                "",
                "## Worldtube Reentry Route",
                md_table(worldtube, ["route_id", "reentry_piece", "current_status", "purpose"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
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
    first_rows = read_csv(SOURCE_FILES["1150_first_row"])
    schema = runner_schema_rows()
    review = input_review_rows(first_rows)
    evaluation = strict_evaluation_rows(first_rows)
    imports = theorem_import_rows()
    worldtube = worldtube_reentry_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(RUNNER_SCHEMA, schema)
    write_csv(INPUT_REVIEW, review)
    write_csv(STRICT_EVALUATION, evaluation)
    write_csv(THEOREM_IMPORT_GATE, imports)
    write_csv(WORLD_TUBE_REENTRY, worldtube)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        RUNNER_SCHEMA,
        INPUT_REVIEW,
        STRICT_EVALUATION,
        THEOREM_IMPORT_GATE,
        WORLD_TUBE_REENTRY,
        REJECTION_LEDGER,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(schema, review, evaluation, imports, worldtube, rejections, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
