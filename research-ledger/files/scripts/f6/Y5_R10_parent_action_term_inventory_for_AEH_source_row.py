from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_action_AEH_term_inventory_written_all_variable_prefactor_channels_retained_nonclaim"
CLAIM_CEILING = "AEH_parent_term_inventory_only_no_channel_cleared_no_AEH_value_no_epsilon_G_zero_no_kappa_gradient_bound_no_Delta_Poisson_fill_no_local_GR_claim"
NEXT_TARGET = "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "706-Y5-R10-parent-action-term-inventory-for-AEH-source-row.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_706_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
    RESIDUALS / "P8_Y5_R10_706_TERM_CLASSIFICATION_RUBRIC.csv",
    RESIDUALS / "P8_Y5_R10_706_AEH_INVENTORY_CANDIDATE_FILL.csv",
    RESIDUALS / "P8_Y5_R10_706_CHANNEL_PRIORITY.csv",
    RESIDUALS / "P8_Y5_R10_706_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_706_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_706_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_706_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_706_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "652_doc": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "653_doc": ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "704_prefactor": RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
    "704_delta": RESIDUALS / "P8_Y5_R10_704_DELTA_POISSON_UPDATE.csv",
    "705_doc": ROOT / "705-Y5-R10-AEH-prefactor-source-row-or-no-FchiR-theorem.md",
    "705_validation": RESIDUALS / "P8_Y5_BRR545_705_VALIDATION.csv",
    "705_schema": RESIDUALS / "P8_Y5_R10_705_AEH_SOURCE_ROW_SCHEMA.csv",
    "705_no_fchir": RESIDUALS / "P8_Y5_R10_705_NO_FCHIR_THEOREM_AUDIT.csv",
    "705_channels": RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
    "705_fill": RESIDUALS / "P8_Y5_R10_705_AEH_CANDIDATE_FILL_ROW.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
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
        "402_doc": "EH/source-normalization parent pair",
        "429_doc": "Ward/Bianchi source residual owner",
        "440_doc": "metric-only second-order sector inventory source",
        "523_doc": "Gauss/orbital source-normalization scorecard",
        "652_doc": "common-geometry source-normalization theorem attempt",
        "653_doc": "parent matter functor signature predecessor",
        "655_doc": "EH operator selection and R11 fallback",
        "657_doc": "source-normalization family and channel vector",
        "696_doc": "M_H_ref/G_ref circularity guard",
        "704_prefactor": "704 A_EH formalization",
        "704_delta": "704 Delta_Poisson update",
        "705_doc": "A_EH source-row predecessor",
        "705_validation": "705 validation gate",
        "705_schema": "705 A_EH source-row schema",
        "705_no_fchir": "705 no-FchiR theorem audit",
        "705_channels": "705 variable prefactor channels",
        "705_fill": "705 A_EH candidate fill row",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def term_inventory_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("AEHT706_0_core_EH", "core_EH", "1 * R[g_obs]", "required_core", "candidate_core_not_parent_extracted", "must be present with coefficient one", "no claim until parent equation path supplied", "highest"),
        ("AEHT706_1_scalar_class", "scalar_class", "delta_AEH_scalar from F(phi,C)R", "variable_prefactor", "retained_not_reduced", "prove absent/constant/gauge or bound delta_AEH_scalar", "blocks A_EH=1", "highest"),
        ("AEHT706_2_memory_kernel", "memory_kernel", "delta_AEH_memory from F(theta)R or nonlocal kernel reduction", "variable_prefactor", "retained_symbolic", "compact-local kernel silence or bound", "blocks grad A_EH", "high"),
        ("AEHT706_3_selector_domain", "selector_domain", "delta_AEH_domain from F(chi_D,P_D,L_cg)R", "variable_prefactor", "retained_symbolic", "first-class/topological/no-stress theorem or bound", "blocks frame/domain neutrality", "high"),
        ("AEHT706_4_bulk_X", "bulk_X", "delta_AEH_X from F(X_A)R after auxiliary/load reduction", "variable_prefactor", "operator_and_sources_not_parent_derived", "source-free no-hair or finite-range map", "blocks R10/source normalization", "high"),
        ("AEHT706_5_higher_curvature", "higher_curvature", "delta_AEH_curv from f(R), R^2, Ricci^2, Weyl^2 weak-field reduction", "operator_disguise", "central_open", "second-order restriction or R11 coefficient map", "blocks EH-only operator", "highest"),
        ("AEHT706_6_torsion_nonmetric", "torsion_nonmetric", "delta_AEH_connection or source transfer from non-Levi-Civita geometry", "connection_transfer", "not_parent_derived", "Levi-Civita theorem or connection residual rows", "blocks same-frame source variation", "high"),
        ("AEHT706_7_boundary_counterterm", "boundary_counterterm", "delta_AEH_boundary from boundary/topological/counterterm convention", "boundary_shift", "not_parent_signed", "boundary no-hair/counterterm guard", "blocks G_ref/M_H_ref interpretation", "high"),
        ("AEHT706_8_frame_transfer", "frame_transfer", "delta_AEH_frame hidden by Weyl/disformal redefinition", "frame_transfer", "not_parent_signed", "same-frame matter functor and no disformal debt", "blocks matter/source universality", "highest"),
        ("AEHT706_9_constant_offset", "constant_offset", "delta_AEH_C where A_EH=C constant", "constant_prefactor", "conditional_not_claim_ready", "independent G_ref plus same-frame source normalization", "cannot be counted as Newton proof alone", "medium"),
        ("AEHT706_10_unmodelled", "unmodelled_parent_terms", "delta_AEH_unknown", "unknown", "MISSING_FULL_PARENT_INVENTORY", "complete parent action term list", "keeps A_EH row unfilled", "highest"),
        ("AEHT706_11_verdict", "inventory_verdict", "A_EH = 1 + sum_i delta_AEH_i", "aggregate", "fail_current_corpus", "all delta_AEH_i absent/zero/bounded with source paths", "no A_EH claim", "highest"),
    ]
    return [
        {
            "term_id": term_id,
            "sector": sector,
            "possible_AEH_contribution": contribution,
            "term_class": term_class,
            "current_status": status,
            "minimum_to_clear": minimum,
            "claim_effect": effect,
            "priority": priority,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "655_doc", "705_channels", "705_no_fchir"),
            "generated_utc": generated,
        }
        for term_id, sector, contribution, term_class, status, minimum, effect, priority in rows
    ]


def classification_rubric_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("RUB706_0_absent", "absent_by_parent_symmetry", "term is forbidden by parent symmetry/field content", "can clear only with source path to parent action or theorem", "claim_possible_if_all_other_rows_clear"),
        ("RUB706_1_gauge", "pure_gauge_or_topological", "metric variation and source/readout variation vanish locally", "must show no boundary/source mass shift", "claim_possible_if_guarded"),
        ("RUB706_2_constant", "harmless_constant", "A_EH=C constant independent of time/range/species/frame/domain", "needs independent G_ref and source normalization", "nonclaim_until_Gref_guard"),
        ("RUB706_3_bound", "bounded_residual", "term survives but has sourced value/derivative bounds", "feeds epsilon_G and kappa-gradient bound, not theorem-zero", "testable_nonclaim_until_bound_loaded"),
        ("RUB706_4_retained", "retained_operator", "term survives as modified-gravity operator/source channel", "requires R10/R11/PPN/source residual map", "no_local_GR_claim"),
        ("RUB706_5_unknown", "unknown_or_uninventoried", "term not yet classified", "blocks A_EH source row", "hard_fail_for_claim"),
    ]
    return [
        {
            "rubric_id": rubric_id,
            "classification": classification,
            "meaning": meaning,
            "required_evidence": evidence,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("705_schema", "705_no_fchir", "704_prefactor"),
            "generated_utc": generated,
        }
        for rubric_id, classification, meaning, evidence, effect in rows
    ]


def candidate_fill_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "fill_id": "AIF706_0_inventory_sum",
            "target": "A_EH",
            "formula": "A_EH = 1 + delta_AEH_scalar + delta_AEH_memory + delta_AEH_domain + delta_AEH_X + delta_AEH_curv + delta_AEH_connection + delta_AEH_boundary + delta_AEH_frame + delta_AEH_C + delta_AEH_unknown",
            "value_or_bound": "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS",
            "source_path": "MISSING_PARENT_ACTION_TERM_INVENTORY_SOURCE_PATH",
            "valid_for_claim": "false",
            "source_paths": source_list("704_delta", "705_fill", "705_channels"),
            "generated_utc": generated,
        },
        {
            "fill_id": "AIF706_1_claim_ready_condition",
            "target": "A_EH=1",
            "formula": "all delta_AEH_i=0 and no unknown parent terms",
            "value_or_bound": "CONDITIONAL_THEOREM_ONLY",
            "source_path": "MISSING_ALL_CHANNEL_ZERO_SOURCE_PATHS",
            "valid_for_claim": "false",
            "source_paths": source_list("705_no_fchir", "705_schema"),
            "generated_utc": generated,
        },
    ]


def channel_priority_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("PRI706_0", "scalar_class", "highest", "direct F(phi,C)R is the canonical variable-coupling failure mode", NEXT_TARGET),
        ("PRI706_1", "higher_curvature", "highest", "f(R)/R2 can masquerade as variable EH coefficient and PPN/R10 residuals", "708-Y5-R10-higher-curvature-AEH-disguise-or-R11-bound.md"),
        ("PRI706_2", "frame_transfer", "highest", "Weyl/disformal frame choices can fake A_EH=1 while moving debt into matter", "709-Y5-R10-frame-transfer-guard-for-AEH-source-row.md"),
        ("PRI706_3", "selector_domain", "high", "domain/projector stress is central to local/source residuals", "710-Y5-R10-selector-domain-prefactor-zero-or-bound.md"),
    ]
    return [
        {
            "priority_id": priority_id,
            "channel": channel,
            "priority": priority,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for priority_id, channel, priority, reason, next_action in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL706_0_inventory", "Can the A_EH inventory fill the source row?", "No. It creates the inventory sum, but every non-core channel is retained, unknown, or conditional.", "fail_blocked", NEXT_TARGET),
        ("EVAL706_1_best_channel", "Which channel should be attacked first?", "Scalar/class F(phi,C)R, because it is the cleanest direct variable-EH-prefactor failure mode.", "route_selected", NEXT_TARGET),
        ("EVAL706_2_claim", "Can A_EH=1 be claimed?", "No. A_EH=1 requires all delta_AEH_i zero plus no unknown parent terms.", "fail_blocked", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("705_doc", "705_channels", "705_fill"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG706_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG706_1_prior_705", "705 validation clean", "705 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG706_2_inventory_complete", "full parent term inventory", "MISSING_FULL_PARENT_INVENTORY", "fail_blocked", "no A_EH source row claim"),
        ("CG706_3_channels_cleared", "all delta_AEH channels zero/bounded", "all non-core channels retained", "fail_blocked", "no A_EH=1 theorem"),
        ("CG706_4_candidate_fill", "A_EH inventory candidate fill", "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS", "fail_blocked", "no epsilon_G claim"),
        ("CG706_5_Delta_Poisson", "Delta_Poisson fill", "not reached", "fail_blocked", "no local Poisson claim"),
        ("CG706_6_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("705_validation", "705_schema", "705_channels", "705_fill"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D706_0_inventory", "A_EH parent term inventory", "written", "A_EH is decomposed into core plus ten possible delta_AEH channels", NEXT_TARGET),
        ("D706_1_claim_status", "A_EH=1 claim", "rejected", "all variable-prefactor channels remain retained/conditional/unknown", NEXT_TARGET),
        ("D706_2_next", "next target", "selected", "attack scalar/class F(phi,C)R first as the cleanest direct A_EH failure mode", NEXT_TARGET),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S706_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "A_EH is now an inventory sum over explicit parent-sector channels, but every non-core channel remains retained, conditional, or unknown",
            "hardest_blocker": "scalar/class F(phi,C)R and higher-curvature/frame-transfer channels are not parent-cleared",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, inventory, rubric, fill, priority, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("705_validation"))
    prior_channels = read_csv(SOURCE_PATHS["705_channels"])
    prior_channel_coverage = len(prior_channels) >= 10
    inventory_verdict = any(row["term_id"] == "AEHT706_11_verdict" and row["current_status"] == "fail_current_corpus" for row in inventory)
    inventory_coverage = len(inventory) >= 12 and any(row["sector"] == "scalar_class" for row in inventory)
    rubric_coverage = len(rubric) == 6
    fill_unfilled = any(row["fill_id"] == "AIF706_0_inventory_sum" and has_missing_marker(row) for row in fill)
    priority_selected = priority[0]["next_action"] == NEXT_TARGET
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [inventory, rubric, fill, priority, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V706_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V706_1_prior_705_clean", prior_failures == 0, f"705_validation_failures={prior_failures}"),
        ("V706_2_prior_channel_coverage", prior_channel_coverage, f"prior_channels={len(prior_channels)}"),
        ("V706_3_inventory_coverage", inventory_coverage, f"inventory_rows={len(inventory)}"),
        ("V706_4_inventory_verdict_blocks", inventory_verdict, "AEHT706 verdict blocks claim"),
        ("V706_5_rubric_coverage", rubric_coverage, f"rubric_rows={len(rubric)}"),
        ("V706_6_candidate_fill_unfilled", fill_unfilled, "A_EH inventory fill keeps MISSING markers"),
        ("V706_7_priority_next_selected", priority_selected, NEXT_TARGET),
        ("V706_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V706_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V706_10_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V706_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V706_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V706_13_status_nonclaim", "no_channel_cleared" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, inventory, rubric, fill, priority, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 706 - Y5 R10 Parent Action Term Inventory For AEH Source Row

## Verdict

706 turns the `A_EH` problem into an explicit parent-sector inventory:

```text
A_EH = 1
     + delta_AEH_scalar
     + delta_AEH_memory
     + delta_AEH_domain
     + delta_AEH_X
     + delta_AEH_curv
     + delta_AEH_connection
     + delta_AEH_boundary
     + delta_AEH_frame
     + delta_AEH_C
     + delta_AEH_unknown.
```

This is not a pass. It is the referee-grade punch list. To claim `A_EH=1`, every `delta_AEH_i` must be absent by parent symmetry, pure gauge/topological with no source shift, harmless constant with independent `G_ref`, numerically bounded, or retained as an explicit modified-gravity residual.

The cleanest next target is the scalar/class `F(phi,C)R` channel, because that is the direct variable-coupling failure mode.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## AEH Term Inventory

{markdown_table(inventory, ["term_id", "sector", "term_class", "current_status", "minimum_to_clear", "priority", "valid_for_claim"])}

## Term Classification Rubric

{markdown_table(rubric, ["rubric_id", "classification", "meaning", "claim_effect", "valid_for_claim"])}

## AEH Inventory Candidate Fill

{markdown_table(fill, ["fill_id", "target", "value_or_bound", "source_path", "valid_for_claim"])}

## Channel Priority

{markdown_table(priority, ["priority_id", "channel", "priority", "reason", "next_action", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    inventory = term_inventory_rows()
    rubric = classification_rubric_rows()
    fill = candidate_fill_rows()
    priority = channel_priority_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, inventory, rubric, fill, priority, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_706_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv", inventory, ["term_id", "sector", "possible_AEH_contribution", "term_class", "current_status", "minimum_to_clear", "claim_effect", "priority", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_TERM_CLASSIFICATION_RUBRIC.csv", rubric, ["rubric_id", "classification", "meaning", "required_evidence", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_AEH_INVENTORY_CANDIDATE_FILL.csv", fill, ["fill_id", "target", "formula", "value_or_bound", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_CHANNEL_PRIORITY.csv", priority, ["priority_id", "channel", "priority", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_706_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_706_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, inventory, rubric, fill, priority, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"inventory_rows={len(inventory)}")
    print(f"rubric_rows={len(rubric)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
