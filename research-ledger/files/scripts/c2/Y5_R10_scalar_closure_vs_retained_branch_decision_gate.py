from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_closure_vs_retained_branch_decision_gate_retained_queue_selected_nonclaim"
CLAIM_CEILING = "decision_gate_only_no_parent_signed_closure_no_retained_scalar_score_no_R10_PPN_WEP_Gdot_or_local_GR_claim"
NEXT_TARGET = "715-Y5-R10-retained-scalar-source-row-minimum-executable-coefficient-pack.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "714-Y5-R10-scalar-closure-vs-retained-branch-decision-gate.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_714_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_714_PARENT_SIGNING_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_714_CLOSURE_ADMISSIBILITY_GATE.csv",
    RESIDUALS / "P8_Y5_R10_714_RETAINED_BRANCH_SOURCE_QUEUE.csv",
    RESIDUALS / "P8_Y5_R10_714_ROUTE_DECISION_GATE.csv",
    RESIDUALS / "P8_Y5_R10_714_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_714_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_714_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_714_VALIDATION.csv",
]

SOURCE_PATHS = {
    "713_doc": ROOT / "713-Y5-R10-run-scalar-closure-residual-smoke-against-local-bound-baselines.md",
    "713_validation": RESIDUALS / "P8_Y5_BRR545_713_VALIDATION.csv",
    "713_smoke": RESIDUALS / "P8_Y5_R10_713_SCALAR_CLOSURE_BOUND_SMOKE.csv",
    "713_gate": RESIDUALS / "P8_Y5_R10_713_CLAIM_GATE_EVALUATION.csv",
    "710_descent": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
    "711_qda": RESIDUALS / "P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
    "711_owner": RESIDUALS / "P8_Y5_R10_711_DPC710_OWNERSHIP_MAP.csv",
    "711_demotion": RESIDUALS / "P8_Y5_R10_711_SCALAR_ZERO_DEMOTION_LEDGER.csv",
    "711_retained": RESIDUALS / "P8_Y5_R10_711_RETAINED_BRANCH_REQUIREMENTS.csv",
    "712_route": RESIDUALS / "P8_Y5_R10_712_CLOSURE_VS_RETAINED_ROUTE.csv",
    "712_rules": RESIDUALS / "P8_Y5_R10_712_FORBIDDEN_PROMOTION_RULES.csv",
    "708_contract": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    "708_r10": RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
    "708_r11": RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    "local_template": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "713_doc": "previous scalar closure smoke checkpoint",
        "713_validation": "previous validation gate",
        "713_smoke": "closure smoke comparison table",
        "713_gate": "previous claim gates",
        "710_descent": "candidate parent descent clause",
        "711_qda": "quotient descent derivation audit",
        "711_owner": "DPC710 ownership map",
        "711_demotion": "scalar zero demotion rules",
        "711_retained": "retained branch requirements",
        "712_route": "closure versus retained route map",
        "712_rules": "forbidden promotion rules",
        "708_contract": "retained scalar source-row contract",
        "708_r10": "retained scalar R10 row template",
        "708_r11": "retained scalar R11 row template",
        "local_template": "canonical local residual template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": str(path.exists()).lower(),
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def parent_signing_audit_rows() -> list[dict[str, str]]:
    generated = now()
    dpc_rows = read_csv(SOURCE_PATHS["710_descent"])
    owner_rows = read_csv(SOURCE_PATHS["711_owner"])
    owner_by_clause = {row["dpc710_clause"]: row for row in owner_rows}
    rows: list[dict[str, str]] = []
    for dpc in dpc_rows:
        owner = owner_by_clause.get(dpc["clause_id"], {})
        clause_status = dpc["current_status"]
        owner_status = owner.get("current_status", "not_mapped")
        if dpc["clause_id"] == "DPC710_8_conditional_theorem":
            gate_result = "conditional_theorem_shape_only"
            route_effect = "may be cited as theorem shape, not as parent-signed result"
        elif dpc["clause_id"] == "DPC710_9_verdict":
            gate_result = "fail_parent_signing"
            route_effect = "closure cannot be promoted"
        elif "fail" in owner_status or "not_derived" in owner_status or "open" in owner_status or "partial" in owner_status:
            gate_result = "fail_unsigned_owner"
            route_effect = "retained source row remains required"
        else:
            gate_result = "not_parent_signed"
            route_effect = "candidate clause remains conditional"
        rows.append(
            {
                "audit_id": f"PSA714_{len(rows)}_{dpc['clause_id']}",
                "dpc710_clause": dpc["clause_id"],
                "clause": dpc["clause"],
                "clause_status": clause_status,
                "owner_status": owner_status,
                "gate_result": gate_result,
                "route_effect": route_effect,
                "valid_for_claim": "false",
                "source_paths": source_list("710_descent", "711_qda", "711_owner"),
                "generated_utc": generated,
            }
        )
    return rows


def closure_admissibility_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "CAD714_0_private_use",
            "MTS_scalar_class_silent_closure",
            "allowed_private_branch",
            "may be used for internal branch testing and code plumbing",
            "does not score local gravity",
        ),
        (
            "CAD714_1_name_lock",
            "closure branch must remain labelled",
            "allowed_with_label_only",
            "all rows must retain closure_assumed and valid_for_claim=false",
            "prevents claim laundering",
        ),
        (
            "CAD714_2_parent_promotion",
            "promotion to theorem-zero",
            "forbidden_current_corpus",
            "requires DPC710_0..DPC710_7 plus QDA711 owners with no fail/open/not_derived markers",
            "blocks theorem-zero",
        ),
        (
            "CAD714_3_R10_R11",
            "R10/R11 claims from closure",
            "forbidden_current_corpus",
            "R10 needs source-charge theorem or real alpha curve; R11 needs executable coefficient vector or EH-only theorem",
            "blocks R10/R11",
        ),
        (
            "CAD714_4_live_route",
            "claim-bearing route",
            "retained_branch_queue_selected",
            "until parent signing succeeds, build the retained scalar source row rather than relying on closure",
            "selects 715",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "subject": subject,
            "status": status,
            "rule": rule,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("711_demotion", "712_rules", "713_gate"),
            "generated_utc": generated,
        }
        for gate_id, subject, status, rule, effect in rows
    ]


def retained_branch_queue_rows() -> list[dict[str, str]]:
    generated = now()
    contract_rows = read_csv(SOURCE_PATHS["708_contract"])
    priority_by_contract = {
        "SCR708_0_parent_action_form": "P0",
        "SCR708_7_frame_normalization": "P0",
        "SCR708_2_prefactor_gradient": "P1",
        "SCR708_5_matter_charges": "P1",
        "SCR708_3_kinetic_metric": "P2",
        "SCR708_4_mass_matrix": "P2",
        "SCR708_6_diagonalization": "P2",
        "SCR708_1_background": "P2",
        "SCR708_8_bound_sources": "P3",
        "SCR708_9_verdict": "P9",
    }
    first_action_by_contract = {
        "SCR708_0_parent_action_form": "extract_or_write the exact scalar/class sector in parent-action notation",
        "SCR708_7_frame_normalization": "fix observed/Jordan/Einstein frame and measured-G convention before any alpha or PPN score",
        "SCR708_2_prefactor_gradient": "derive or source a_I=partial_I ln A_EH at local background",
        "SCR708_5_matter_charges": "derive or source b_A,I and decide universal/zero/species-dependent coupling",
        "SCR708_3_kinetic_metric": "source Z_IJ and classify gauge/null/positive modes",
        "SCR708_4_mass_matrix": "source M_IJ^2 or prove no propagating local scalar mode",
        "SCR708_6_diagonalization": "canonicalize modes after Z_IJ and M_IJ^2 exist",
        "SCR708_1_background": "define u0 and A_EH(u0) in the observed local vacuum branch",
        "SCR708_8_bound_sources": "reuse existing local guards and real R10 curve contract; do not claim until rows are real",
        "SCR708_9_verdict": "only evaluate after all queue rows are numeric/theorem-zero and sourced",
    }
    rows: list[dict[str, str]] = []
    for contract in contract_rows:
        contract_id = contract["contract_id"]
        rows.append(
            {
                "queue_id": f"RBQ714_{len(rows)}_{contract_id}",
                "contract_id": contract_id,
                "required_object": contract["required_object"],
                "current_value_or_status": contract["current_value_or_status"],
                "priority": priority_by_contract.get(contract_id, "P4"),
                "first_action": first_action_by_contract.get(contract_id, "fill retained scalar source-row field with sourced value or theorem-zero"),
                "blocks_observables": "R1;R2;R3;R4;R9;R10;R11" if contract_id != "SCR708_8_bound_sources" else "comparison/scoring only",
                "route_effect": "retained_branch_required_until_parent_closure_signed",
                "valid_for_claim": "false",
                "source_paths": source_list("708_contract", "708_r10", "708_r11", "711_retained"),
                "generated_utc": generated,
            }
        )
    return rows


def route_decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "RDG714_0_parent_closure",
            "parent-sign scalar closure",
            "not_selected_for_claim",
            "DPC710 remains candidate-only and QDA711/OWN711 retain fail/open/not_derived markers",
            "closure stays private branch",
        ),
        (
            "RDG714_1_closure_smoke",
            "continue scalar closure smoke",
            "allowed_nonclaim",
            "useful for pipeline discipline but cannot reduce MTS to GR by itself",
            "keep branch labelled",
        ),
        (
            "RDG714_2_retained_branch",
            "build retained scalar source row",
            "selected_next",
            "least-scrutiny route is explicit coefficients/couplings rather than an assumed zero",
            NEXT_TARGET,
        ),
        (
            "RDG714_3_claim_ceiling",
            "public/local-GR claim",
            "forbidden",
            "neither closure theorem nor retained scalar score exists yet",
            "no R10/PPN/WEP/Gdot/local-GR claim",
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "route": route,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, route, result, reason, next_action in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEHU714_0_closure_status",
            "delta_AEH_scalar;grad_ln_AEH_scalar",
            "closure_zero_only",
            "not_parent_signed",
            "do not promote scalar A_EH silence",
        ),
        (
            "AEHU714_1_retained_status",
            "A_EH(u0);partial_I_ln_A_EH",
            "MISSING_BACKGROUND_AND_PREFACTOR_GRADIENT",
            "retained_queue_selected",
            "fill in 715 before PPN/Gdot/R10 scoring",
        ),
        (
            "AEHU714_2_coupling_status",
            "b_A,I;matter frame B_A(u)",
            "MISSING_MATTER_CHARGE_VECTOR",
            "retained_queue_selected",
            "coupling is now the live bottleneck",
        ),
        (
            "AEHU714_3_operator_status",
            "scalar_tensor_class_metric",
            "MISSING_R11_EXECUTABLE_COEFFICIENT",
            "retained_queue_selected",
            "R11 row remains active if closure rejected",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_status": value,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("708_contract", "711_retained", "712_route", "713_gate"),
            "generated_utc": generated,
        }
        for update_id, target, value, status, effect in rows
    ]


def claim_gate_rows(
    source_rows: list[dict[str, str]],
    signing_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("713_validation")
    signing_failures = [row for row in signing_rows if "fail" in row["gate_result"] or row["gate_result"] == "not_parent_signed"]
    queue_missing = [row for row in queue_rows if "MISSING" in row["current_value_or_status"] or "fail" in row["current_value_or_status"]]
    rows = [
        (
            "CG714_0_sources",
            "all source files load",
            f"missing_sources={len(missing_sources)}",
            "pass_structure" if not missing_sources else "fail_blocked",
            "allows decision gate only",
        ),
        (
            "CG714_1_prior_713",
            "713 validation clean",
            f"713_validation_failures={len(prior_failures)}",
            "pass_structure" if not prior_failures else "fail_blocked",
            "inherits clean smoke gate",
        ),
        (
            "CG714_2_parent_signing",
            "parent closure signing",
            f"unsigned_or_failed_clauses={len(signing_failures)}",
            "fail_blocked",
            "closure not promoted",
        ),
        (
            "CG714_3_closure_admissibility",
            "closure branch status",
            f"gate_rows={len(closure_rows)} private_only=true",
            "pass_blocked_recorded",
            "closure allowed only as nonclaim branch",
        ),
        (
            "CG714_4_retained_queue",
            "retained source queue",
            f"queue_rows={len(queue_rows)} missing_or_failed={len(queue_missing)}",
            "pass_blocked_recorded",
            "next work item is exact and unclaimed",
        ),
        (
            "CG714_5_claim_status",
            "claim promotion",
            "no parent-signed closure and no retained executable scalar source row",
            "fail_blocked",
            "no R10/PPN/WEP/Gdot/local-GR claim",
        ),
        (
            "CG714_6_next_target",
            "next target",
            NEXT_TARGET,
            "pass_structure",
            "retained scalar coefficient pack selected",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": state,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("713_validation", "710_descent", "711_qda", "711_owner", "708_contract"),
            "generated_utc": generated,
        }
        for gate_id, gate, state, result, effect in rows
    ]


def nonclaim_summary_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    generated = now()
    p0_rows = [row for row in queue_rows if row["priority"] == "P0"]
    p1_rows = [row for row in queue_rows if row["priority"] == "P1"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "parent_closure_promoted": "false",
            "retained_branch_selected": "true",
            "p0_queue_items": str(len(p0_rows)),
            "p1_queue_items": str(len(p1_rows)),
            "main_result": "closure remains private/nonclaim; retained scalar coefficient/coupling source queue is now the live route",
            "remaining_blocker": "parent action form, observed-frame convention, A_EH gradient, and matter charge vector",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*tables: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for table in tables:
        rows.extend(table)
    return rows


def validation_rows(
    source_rows: list[dict[str, str]],
    signing_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("713_validation")
    all_rows = all_generated_rows(source_rows, signing_rows, closure_rows, queue_rows, decision_rows, aeh_rows, gate_rows, summary_rows)
    changed_count = formalization_changed_count()
    checks = [
        (
            "V714_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ",".join(row["source_id"] for row in missing_sources),
        ),
        (
            "V714_1_prior_713_clean",
            not prior_failures,
            f"713_validation_failures={len(prior_failures)}",
        ),
        (
            "V714_2_parent_signing_audit_complete",
            len(signing_rows) >= 10,
            f"signing_rows={len(signing_rows)}",
        ),
        (
            "V714_3_parent_closure_not_promoted",
            any(row["dpc710_clause"] == "DPC710_9_verdict" and row["gate_result"] == "fail_parent_signing" for row in signing_rows),
            "DPC710 verdict blocks promotion",
        ),
        (
            "V714_4_closure_private_only",
            any(row["status"] == "forbidden_current_corpus" for row in closure_rows)
            and any(row["status"] == "retained_branch_queue_selected" for row in closure_rows),
            "closure admissibility gates block claims and select retained queue",
        ),
        (
            "V714_5_retained_queue_complete",
            len(queue_rows) == 10,
            f"queue_rows={len(queue_rows)}",
        ),
        (
            "V714_6_retained_queue_has_p0_p1",
            any(row["priority"] == "P0" for row in queue_rows) and any(row["priority"] == "P1" for row in queue_rows),
            "P0/P1 blockers present",
        ),
        (
            "V714_7_route_decision_selects_715",
            any(row["result"] == "selected_next" and row["next_action"] == NEXT_TARGET for row in decision_rows),
            NEXT_TARGET,
        ),
        (
            "V714_8_claim_gates_blocked",
            any(row["gate_id"] == "CG714_2_parent_signing" and row["result"] == "fail_blocked" for row in gate_rows)
            and any(row["gate_id"] == "CG714_5_claim_status" and row["result"] == "fail_blocked" for row in gate_rows),
            "parent signing and claim status remain blocked",
        ),
        (
            "V714_9_AEH_update_retained_queue",
            any(row["current_status"] == "retained_queue_selected" for row in aeh_rows),
            "AEH/coupling retained queue selected",
        ),
        (
            "V714_10_no_claim_rows_promoted",
            all(row.get("valid_for_claim", "false") == "false" for row in all_rows),
            "all generated rows valid_for_claim=false",
        ),
        (
            "V714_11_summary_nonclaim",
            summary_rows[0]["parent_closure_promoted"] == "false" and summary_rows[0]["retained_branch_selected"] == "true",
            "summary preserves nonclaim route decision",
        ),
        (
            "V714_12_outputs_scoped",
            all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS),
            "all outputs under post-checkpoint-work",
        ),
        (
            "V714_13_formalization_workbench_untouched",
            changed_count == 0,
            f"formalization_changed_after_cutoff={changed_count}",
        ),
        (
            "V714_14_status_nonclaim",
            CLAIM_CEILING in summary_rows[0]["claim_ceiling"],
            CLAIM_CEILING,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_markdown(
    source_rows: list[dict[str, str]],
    signing_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    content = f"""# 714 - Y5 R10 Scalar Closure Vs Retained Branch Decision Gate

## Summary

714 makes the fork explicit. The scalar/class silent closure remains useful as a disciplined private branch, but it is **not** parent-signed. The claim-bearing path therefore cannot rely on closure zeros. The live route is now the retained scalar branch: write the minimum executable coefficient/coupling source pack before any R10, PPN, WEP, Gdot, R11, or local-GR scoring.

| Status | `{STATUS}` |
| --- | --- |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Parent Signing Audit

{markdown_table(signing_rows, ["audit_id", "dpc710_clause", "clause_status", "owner_status", "gate_result", "route_effect", "valid_for_claim"])}

## Closure Admissibility Gate

{markdown_table(closure_rows, ["gate_id", "subject", "status", "rule", "claim_effect", "valid_for_claim"])}

## Retained Branch Source Queue

{markdown_table(queue_rows, ["queue_id", "contract_id", "required_object", "current_value_or_status", "priority", "first_action", "valid_for_claim"])}

## Route Decision Gate

{markdown_table(decision_rows, ["decision_id", "route", "result", "reason", "next_action", "valid_for_claim"])}

## Aeh Scalar Update

{markdown_table(aeh_rows, ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "parent_closure_promoted", "retained_branch_selected", "main_result", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}

## Verdict

The closure route did not die, but it has been quarantined: useful for private branch testing, useless as evidence until the parent action signs it. The less brittle next move is retained-branch coefficient work, especially the coupling row: `A_EH(u)`, `partial_I ln A_EH`, `Z_IJ`, `M_IJ^2`, `b_A,I`, canonical modes, and frame normalization. That is where the theory stops hand-waving and starts earning its local-GR reduction.
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    source_rows = source_register_rows()
    signing_rows = parent_signing_audit_rows()
    closure_rows = closure_admissibility_rows()
    queue_rows = retained_branch_queue_rows()
    route_rows = route_decision_rows()
    aeh_rows = aeh_update_rows()
    gate_rows = claim_gate_rows(source_rows, signing_rows, closure_rows, queue_rows)
    summary_rows = nonclaim_summary_rows(queue_rows)
    validation_rows_ = validation_rows(source_rows, signing_rows, closure_rows, queue_rows, route_rows, aeh_rows, gate_rows, summary_rows)

    write_csv(
        RESIDUALS / "P8_Y5_R10_714_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_PARENT_SIGNING_AUDIT.csv",
        signing_rows,
        [
            "audit_id",
            "dpc710_clause",
            "clause",
            "clause_status",
            "owner_status",
            "gate_result",
            "route_effect",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_CLOSURE_ADMISSIBILITY_GATE.csv",
        closure_rows,
        ["gate_id", "subject", "status", "rule", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_RETAINED_BRANCH_SOURCE_QUEUE.csv",
        queue_rows,
        [
            "queue_id",
            "contract_id",
            "required_object",
            "current_value_or_status",
            "priority",
            "first_action",
            "blocks_observables",
            "route_effect",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_ROUTE_DECISION_GATE.csv",
        route_rows,
        ["decision_id", "route", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_AEH_SCALAR_UPDATE.csv",
        aeh_rows,
        ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_CLAIM_GATE_EVALUATION.csv",
        gate_rows,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_714_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "parent_closure_promoted",
            "retained_branch_selected",
            "p0_queue_items",
            "p1_queue_items",
            "main_result",
            "remaining_blocker",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_714_VALIDATION.csv",
        validation_rows_,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_markdown(source_rows, signing_rows, closure_rows, queue_rows, route_rows, aeh_rows, gate_rows, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"{STATUS}: validation_passes={len(validation_rows_) - len(failures)}/{len(validation_rows_)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
