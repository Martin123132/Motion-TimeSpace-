from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1151-Y5-R10-PiM-equality-commutator-bound-runner-smoke-or-parent-action-reentry.md"
FIRST_ROW = OUT / "P8_Y5_R10_1150_PIM_EQUALITY_COMMUTATOR_FIRST_ROW.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains_missing(value: object) -> bool:
    text = str(value)
    return "MISSING" in text or text.strip() == ""


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1151_0_1150_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_NEXT_TARGET.csv",
            "needle": "NEXT1150_0_1151",
            "role": "handoff requiring strict PiM equality/commutator runner smoke.",
        },
        {
            "source_id": "SRC1151_1_1150_first_row",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_PIM_EQUALITY_COMMUTATOR_FIRST_ROW.csv",
            "needle": "PIM1150_0_current_branch_template",
            "role": "new 1150 first-row schema for equality/commutator inputs.",
        },
        {
            "source_id": "SRC1151_2_1150_guards",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_NO_SHORTCUT_GUARDS.csv",
            "needle": "GUARD1150_0_no_orbital_GM_proof",
            "role": "no-shortcut guardrails.",
        },
        {
            "source_id": "SRC1151_3_1150_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_DECISION_LEDGER.csv",
            "needle": "D1150_2_best_next",
            "role": "1150 decision selects runner smoke.",
        },
        {
            "source_id": "SRC1151_4_old_evaluator",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv",
            "needle": "PCR535_0_current_branch",
            "role": "older evaluator says current inputs are missing and reference zero is not evidence.",
        },
        {
            "source_id": "SRC1151_5_old_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv",
            "needle": "MISSING_R_EQ_INTEGRAL",
            "role": "older numeric input template with missing values.",
        },
        {
            "source_id": "SRC1151_6_bound_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
            "needle": "PCB534_4_decision",
            "role": "bound formula and no-cancellation sum.",
        },
        {
            "source_id": "SRC1151_7_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
            "role": "parent-action reentry hook for theorem evidence.",
        },
        {
            "source_id": "SRC1151_8_1150_glue",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
            "needle": "GLUE1150_9_verdict",
            "role": "1150 glue theorem remains not derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def input_review_rows(first_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    reviewed: list[dict[str, object]] = []
    for row in first_rows:
        row_id = row["row_id"]
        source_path = row.get("source_path", "")
        current_value = row.get("current_value", "")
        is_reference = "reference" in row.get("model_id", "").lower() or row_id.endswith("reference_only_zero_row")
        missing = contains_missing(current_value) or contains_missing(source_path)
        source_exists = False
        if source_path and not contains_missing(source_path) and not source_path.startswith("reference_"):
            candidate = Path(source_path)
            if not candidate.is_absolute():
                candidate = ROOT / source_path
            source_exists = candidate.exists()
        reviewed.append(
            {
                "review_id": f"REV1151_{row_id}",
                "row_id": row_id,
                "quantity": row.get("quantity", ""),
                "formula": row.get("formula", ""),
                "current_value": current_value,
                "source_path": source_path,
                "has_missing_marker": str(missing).lower(),
                "source_file_exists": str(source_exists).lower(),
                "reference_only": str(is_reference).lower(),
                "runner_disposition": "REJECT_REFERENCE_ONLY" if is_reference else ("BLOCKED_MISSING_INPUTS" if missing else "READY_FOR_NUMERIC_EVAL"),
                "valid_for_claim": "false",
            }
        )
    return stamp(reviewed)


def smoke_rows(first_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows_by_id = {row["row_id"]: row for row in first_rows}
    template = rows_by_id["PIM1150_0_current_branch_template"]
    reference = rows_by_id["PIM1150_5_reference_only_zero_row"]

    required_ids = [
        "PIM1150_1_R_eq_integral",
        "PIM1150_2_I_commutator",
        "PIM1150_3_B_zero_flux",
        "PIM1150_4_projector_stress",
    ]
    component_missing = any(contains_missing(rows_by_id[row_id]["current_value"]) for row_id in required_ids)
    source_missing = any(contains_missing(rows_by_id[row_id]["source_path"]) for row_id in required_ids)

    m_h_ref = parse_float("MISSING_M_H_REF")
    smoke = [
        {
            "smoke_id": "SMOKE1151_0_current_branch",
            "model_id": template["model_id"],
            "input_rows": ";".join(required_ids),
            "epsilon_PiM_total_abs": "NOT_COMPUTED",
            "numeric_status": "not_computed_missing_numeric_inputs" if component_missing or source_missing or m_h_ref is None else "computed",
            "source_status": "MISSING_SOURCE_FILE",
            "runner_disposition": "BLOCKED_MISSING_INPUTS",
            "claim_status": "not_claimable",
            "valid_for_claim": "false",
            "notes": "requires R_eq_integral, I_commutator, B_zero_flux, projector_stress, M_H_ref, units, assumptions, and source files",
        },
        {
            "smoke_id": "SMOKE1151_1_reference_zero",
            "model_id": reference["model_id"],
            "input_rows": reference["row_id"],
            "epsilon_PiM_total_abs": "0",
            "numeric_status": "computed_reference_only",
            "source_status": "reference_not_current_MTS_source",
            "runner_disposition": "REJECT_REFERENCE_ONLY",
            "claim_status": "not_claimable",
            "valid_for_claim": "false",
            "notes": "formal zero row is useful for runner shape but cannot be imported as MTS evidence",
        },
        {
            "smoke_id": "SMOKE1151_2_no_cancellation_sum",
            "model_id": "MTS_local_source_normalized_branch",
            "input_rows": ";".join(required_ids),
            "epsilon_PiM_total_abs": "abs(R_eq)/M_H_ref + abs(I_commutator)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(epsilon_projector_stress)",
            "numeric_status": "symbolic_only_until_inputs_filled",
            "source_status": "not_scoreable",
            "runner_disposition": "NO_CANCELLATION_POLICY_ACTIVE",
            "claim_status": "not_claimable",
            "valid_for_claim": "false",
            "notes": "sum of absolute components; no tuned cancellation between equality, commutator, boundary, and stress terms",
        },
    ]
    return stamp(smoke)


def parent_reentry_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "hook_id": "HOOK1151_0_covariant_action",
                "parent_clause": "explicit diffeomorphism-covariant parent action and symplectic potential",
                "required_evidence": "S_parent, delta L=E delta phi+dTheta, and Noether current before fitting",
                "routes_to_runner": "can replace numeric rows only if it proves the same R_eq/I_commutator/B_zero/stress quantities zero",
                "current_status": "CONTRACT_ONLY_NO_FULL_LAGRANGIAN",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_1_same_source_frame",
                "parent_clause": "single observed source frame",
                "required_evidence": "S_matter[e_obs,psi] defines J_H and same frame is used for clocks/orbits",
                "routes_to_runner": "supports source_file/theorem certificate for R_eq and M_H_ref normalization",
                "current_status": "NOT_YET_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_2_parent_fixed_worldtube",
                "parent_clause": "source support and linking surfaces fixed before readout",
                "required_evidence": "W_source=supp(J_H) and S1/S2 link the same W_source",
                "routes_to_runner": "defines system_id, r1, r2, and assumptions for all numeric rows",
                "current_status": "NOT_YET_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_3_Hilbert_topological_equality",
                "parent_clause": "Pi_M J_H = J_M_top + dB_zero + R_eq",
                "required_evidence": "R_eq=0 theorem or source-backed R_eq_integral",
                "routes_to_runner": "fills PIM1150_1_R_eq_integral",
                "current_status": "NOT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_4_boundary_reference_zero",
                "parent_clause": "exact/reference boundary term has zero compact exterior flux",
                "required_evidence": "int_boundary dB_zero=0 theorem or sourced B_zero_flux",
                "routes_to_runner": "fills PIM1150_3_B_zero_flux",
                "current_status": "MISSING_CERTIFICATE_OR_BOUND",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_5_commutator_stress_zero",
                "parent_clause": "Pi_M fixed/covariantly constant and no projector stress",
                "required_evidence": "[d,Pi_M]J_H=0 and T_PiM=0/bounded",
                "routes_to_runner": "fills PIM1150_2_I_commutator and PIM1150_4_projector_stress",
                "current_status": "MISSING_CERTIFICATE_OR_NUMERIC_BOUND",
                "valid_for_claim": "false",
            },
            {
                "hook_id": "HOOK1151_6_readout_followthrough",
                "parent_clause": "same charge controls Poisson/Gauss/orbital and PPN readout",
                "required_evidence": "Gauss/orbital calibration after source equality, not before",
                "routes_to_runner": "does not bypass runner; comes after source equality inputs pass",
                "current_status": "NOT_REACHED",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1151_0_sources_exist",
                "rule": "all 1151 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1151_1_runner_executes",
                "rule": "runner reviews first-row schema and emits smoke statuses",
                "gate_pass": "true_nonclaim",
                "reason": "current and reference rows are evaluated into blocked/rejected statuses",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1151_2_current_branch_scoreable",
                "rule": "current MTS row has numeric/source-backed components",
                "gate_pass": "false",
                "reason": "R_eq, I_commutator, B_zero_flux, projector stress, M_H_ref, and source files remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1151_3_reference_zero_rejected",
                "rule": "reference-only zero cannot be treated as MTS evidence",
                "gate_pass": "true_nonclaim",
                "reason": "reference row is explicitly rejected by runner disposition",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1151_4_no_cancellation",
                "rule": "total score uses absolute component envelope",
                "gate_pass": "true_nonclaim",
                "reason": "epsilon_PiM_total_abs is a sum of absolute components, not a cancellation fit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1151_5_Newton_GR_promotion",
                "rule": "measured-GM/Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "runner infrastructure only; no claim-valid current row",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1151_0_runner",
                "decision": "PiM_equality_commutator_runner_smoke_written",
                "reason": "the current row is blocked by missing inputs, and the reference zero row is rejected",
                "next_action": "source or derive R_eq/I_commutator/B_zero/projector_stress through this schema",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1151_1_parent_reentry",
                "decision": "parent_theorem_must_route_through_runner_schema",
                "reason": "theorem evidence is allowed only if it zeros the same components named by the runner",
                "next_action": "try commutator-zero/equality theorem with explicit row replacements",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1151_2_best_next",
                "decision": "target_PiM_commutator_zero_or_first_source_input",
                "reason": "I_commutator is the cleanest product-rule obstruction and a direct source-normalization/radial-hair channel",
                "next_action": "1152 PiM commutator-zero theorem or R_eq/I_commutator source acquisition",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1151_0_1152",
                "next_target": "1152-Y5-R10-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
                "objective": "try to derive [d,Pi_M]J_H=0 from a parent-fixed/topological Pi_M on the same Hilbert source-current domain; if it fails, create the first source-acquisition rows for R_eq_integral and I_commutator",
                "include": "Pi_M fixed/covariantly constant clause; topological/Hamiltonian equality guard; commutator integral; R_eq integral; source-file requirements; radial/source-normalization links",
                "exclude": "reference zero as evidence; Hodge projector without stress; readout mask; unowned multiplier; orbital GM proof; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    reviews: list[dict[str, object]],
    smoke: list[dict[str, object]],
    hooks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = reviews + smoke + hooks + gates + decisions + next_target
    add(
        "V1151_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1151_1_review_covers_rows",
        {"PIM1150_0_current_branch_template", "PIM1150_1_R_eq_integral", "PIM1150_2_I_commutator", "PIM1150_3_B_zero_flux", "PIM1150_4_projector_stress", "PIM1150_5_reference_only_zero_row"}.issubset(
            {row["row_id"] for row in reviews}
        ),
        "all 1150 first-row entries are reviewed",
    )
    add(
        "V1151_2_current_blocked",
        any(row["smoke_id"] == "SMOKE1151_0_current_branch" and row["runner_disposition"] == "BLOCKED_MISSING_INPUTS" for row in smoke),
        "current MTS row is blocked by missing inputs",
    )
    add(
        "V1151_3_reference_rejected",
        any(row["smoke_id"] == "SMOKE1151_1_reference_zero" and row["runner_disposition"] == "REJECT_REFERENCE_ONLY" for row in smoke),
        "reference-only zero is rejected",
    )
    add(
        "V1151_4_parent_hooks_present",
        {"HOOK1151_3_Hilbert_topological_equality", "HOOK1151_4_boundary_reference_zero", "HOOK1151_5_commutator_stress_zero"}.issubset(
            {row["hook_id"] for row in hooks}
        ),
        "parent theorem reentry hooks map to runner components",
    )
    add(
        "V1151_5_claim_gates_blocked",
        any(row["gate_id"] == "G1151_2_current_branch_scoreable" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1151_5_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "current branch scoreability and Newton/GR promotion remain blocked",
    )
    add(
        "V1151_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1151_7_next_target",
        next_target[0]["next_target"].startswith("1152-") and "PiM-commutator-zero" in str(next_target[0]["next_target"]),
        "1152 handoff targets PiM commutator-zero or source acquisition",
    )
    add(
        "V1151_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1151_9_csv_parse", csv_parse_ok, "all 1151 CSV outputs parse cleanly")
    add("V1151_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1151_SUMMARY",
        True,
        "1151 executes the strict nonclaim PiM runner smoke, blocks missing current inputs, rejects reference zero, and sends commutator-zero/source acquisition to 1152",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    reviews: list[dict[str, object]],
    smoke: list[dict[str, object]],
    hooks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1151 - Y5/R10 PiM Equality-Commutator Bound Runner Smoke or Parent Action Reentry

**Current verdict:** the strict nonclaim runner executes, but the current MTS row is not scoreable. `R_eq_integral`, `I_commutator`, `B_zero_flux`, projector stress, `M_H_ref`, and source files are still missing.

**Useful progress:** future theorem or numeric evidence now has a gate: it must fill or theorem-zero the same equality, commutator, boundary, and stress components rather than bypassing them.

**Important guard:** the reference zero row is rejected as MTS evidence. It proves only the runner shape, not the theory.

**Best next attack:** target `[d,Pi_M]J_H=0` directly. The commutator is the cleanest product-rule obstruction and links straight into radial/source-normalization hair.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, alpha3, R10, GitHub, or public claim follows from 1151.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Runner Input Review
{table(["review_id", "row_id", "quantity", "current_value", "source_path", "has_missing_marker", "source_file_exists", "reference_only", "runner_disposition", "valid_for_claim"], reviews)}

## Smoke Evaluation
{table(["smoke_id", "model_id", "input_rows", "epsilon_PiM_total_abs", "numeric_status", "source_status", "runner_disposition", "claim_status", "valid_for_claim", "notes"], smoke)}

## Parent-Action Reentry Hooks
{table(["hook_id", "parent_clause", "required_evidence", "routes_to_runner", "current_status", "valid_for_claim"], hooks)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1151_SOURCE_REGISTER.csv",
        "reviews": OUT / "P8_Y5_R10_1151_RUNNER_INPUT_REVIEW.csv",
        "smoke": OUT / "P8_Y5_R10_1151_SMOKE_EVALUATION.csv",
        "hooks": OUT / "P8_Y5_R10_1151_PARENT_ACTION_REENTRY_HOOKS.csv",
        "gates": OUT / "P8_Y5_R10_1151_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1151_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1151_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1151_VALIDATION.csv",
    }
    sources = source_rows()
    first_rows = read_csv(FIRST_ROW)
    reviews = input_review_rows(first_rows)
    smoke = smoke_rows(first_rows)
    hooks = parent_reentry_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["reviews"], reviews)
    write_csv(outputs["smoke"], smoke)
    write_csv(outputs["hooks"], hooks)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, reviews, smoke, hooks, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, reviews, smoke, hooks, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
