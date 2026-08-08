from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_class_FR_prefactor_zero_theorem_failed_AEH_bound_contract_written_nonclaim"
CLAIM_CEILING = "scalar_class_FR_prefactor_contract_only_no_delta_AEH_scalar_zero_no_AEH_value_no_epsilon_G_zero_no_R10_R11_bound_no_local_GR_claim"
NEXT_TARGET = "708-Y5-R10-scalar-class-source-row-or-R11-R10-bound-map.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_707_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_AEH_BOUND_PACK.csv",
    RESIDUALS / "P8_Y5_R10_707_R10_R11_FALLBACK_MAP.csv",
    RESIDUALS / "P8_Y5_R10_707_AEH_INVENTORY_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_707_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_707_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_707_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_707_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_707_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "705_channels": RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
    "706_doc": ROOT / "706-Y5-R10-parent-action-term-inventory-for-AEH-source-row.md",
    "706_validation": RESIDUALS / "P8_Y5_BRR545_706_VALIDATION.csv",
    "706_inventory": RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
    "706_fill": RESIDUALS / "P8_Y5_R10_706_AEH_INVENTORY_CANDIDATE_FILL.csv",
    "706_priority": RESIDUALS / "P8_Y5_R10_706_CHANNEL_PRIORITY.csv",
    "704_prefactor": RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
    "704_gradient": RESIDUALS / "P8_Y5_R10_704_KAPPA_GRADIENT_BOUND_PACK.csv",
    "704_delta": RESIDUALS / "P8_Y5_R10_704_DELTA_POISSON_UPDATE.csv",
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
        "440_doc": "metric-only second-order scalar/class source",
        "655_doc": "EH operator selection and scalar/class R11 fallback",
        "657_doc": "source-normalization family and R10/R11 map",
        "705_channels": "705 variable prefactor channels",
        "706_doc": "A_EH inventory predecessor",
        "706_validation": "706 validation gate",
        "706_inventory": "706 A_EH term inventory",
        "706_fill": "706 A_EH inventory candidate fill",
        "706_priority": "706 channel priority",
        "704_prefactor": "704 A_EH formalization",
        "704_gradient": "704 kappa-gradient bound pack",
        "704_delta": "704 Delta_Poisson update",
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


def scalar_zero_theorem_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("SCZ707_0_definition", "scalar/class prefactor", "delta_AEH_scalar := F(phi,C)-1 in sqrt(-g)F(phi,C)R[g_obs]", "definition_written", "none_definition_only"),
        ("SCZ707_1_absent", "absent by parent field content", "no scalar phi, class scalar C, quotient scalar, or class metric can multiply R", "not_parent_signed", "blocks absence proof"),
        ("SCZ707_2_constant", "constant universal scalar/class value", "phi,C are constant universal and source/time/range/species/frame independent", "not_parent_signed", "constant offset still needs G_ref guard"),
        ("SCZ707_3_gauge_topological", "pure gauge/topological scalar/class sector", "metric variation and source/readout variation vanish locally", "not_parent_signed", "cannot clear local stress/source channel"),
        ("SCZ707_4_algebraic_harmless", "algebraic harmless constraint", "scalar/class equation gives local algebraic solution with zero derivative and no f(R)/higher-curvature remnant", "not_parent_signed", "integrating out can generate f(R)"),
        ("SCZ707_5_massive_decoupled", "massive/source-free decoupling", "scalar has infinite/large mass and zero source/test charge through tested ranges", "not_parent_signed", "finite-range/R10 channel remains"),
        ("SCZ707_6_no_frame_transfer", "no Weyl/disformal transfer", "setting F to one does not move variable coupling into matter", "not_parent_signed", "frame debt remains"),
        ("SCZ707_7_conditional_theorem", "conditional scalar zero theorem", "SCZ707_1 or SCZ707_2+Gref guard or SCZ707_3 or SCZ707_4 or SCZ707_5 with source-free proof implies delta_AEH_scalar=0/bounded", "proved_as_conditional_template", "theorem shape only"),
        ("SCZ707_8_verdict", "claim-ready scalar/class prefactor zero", "delta_AEH_scalar=0 or claim-ready bound", "fail_current_corpus", "scalar/class channel remains retained"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "clause": clause,
            "mathematical_requirement": requirement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "655_doc", "706_inventory", "705_channels"),
            "generated_utc": generated,
        }
        for theorem_id, clause, requirement, status, effect in rows
    ]


def scalar_bound_pack_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("SAB707_0_delta_AEH_scalar", "delta_AEH_scalar", "delta_AEH_scalar = F(phi,C)-1", "MISSING_VALUE_OR_ZERO_THEOREM", "dimensionless", "feeds epsilon_G"),
        ("SAB707_1_epsilon_G_scalar", "epsilon_G_scalar", "epsilon_G_scalar = abs(delta_AEH_scalar)/(abs(1+delta_AEH_scalar))", "MISSING_BOUND", "dimensionless", "partial A_EH coupling mismatch"),
        ("SAB707_2_gradient_scalar", "grad_ln_AEH_scalar", "grad ln F(phi,C)", "MISSING_GRADIENT_BOUND", "per_time;per_length;per_range;per_species", "feeds kappa-gradient channel"),
        ("SAB707_3_mass_range", "m_scalar_or_lambda_scalar", "finite-range scalar length/mass if scalar survives", "MISSING_MASS_OR_RANGE", "length_or_mass", "feeds R10 fifth-force"),
        ("SAB707_4_source_charge", "Q_scalar_source_test", "source/test scalar charges or theorem-zero", "MISSING_SOURCE_TEST_CHARGE", "dimensionless_or_model_units", "feeds WEP/R10/source-normalization"),
        ("SAB707_5_ppn_map", "gamma_beta_map", "map delta_AEH_scalar or scalar coupling to gamma-1,beta-1", "MISSING_PPN_MAP", "dimensionless", "feeds R3/R4"),
        ("SAB707_6_verdict", "claim-ready scalar bound", "all scalar value/gradient/range/charge/PPN inputs filled", "fail_current_corpus", "mixed", "no scalar bound claim"),
    ]
    return [
        {
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value,
            "units": units,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("704_prefactor", "704_gradient", "706_inventory", "source_norm_scorecard"),
            "generated_utc": generated,
        }
        for bound_id, target, formula, value, units, effect in rows
    ]


def fallback_map_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("FB707_0_R11_operator", "R11", "scalar_tensor_class_metric", "R11_nonEH_operator_vector_TEMPLATE", "MISSING_SCALAR_CLASS_COEFFICIENT_ROW", "retained modified-gravity operator if zero theorem fails"),
        ("FB707_1_R10_range", "R10", "finite_range_scalar", "alpha(lambda) curve", "MISSING_ALPHA_LAMBDA_MAP", "fifth-force test route"),
        ("FB707_2_R3_gamma", "R3", "PPN_slip", "gamma_minus_1", "MISSING_GAMMA_MAP", "light-bending/slip route"),
        ("FB707_3_R4_beta", "R4", "nonlinear_source", "beta_minus_1", "MISSING_BETA_MAP", "nonlinear/source-stability route"),
        ("FB707_4_R9_Gdot", "R9", "time_varying_coupling", "Gdot/G", "MISSING_GDOT_MAP", "time-drift route"),
        ("FB707_5_R1_WEP", "R1", "species_source_charge", "eta_source_AB", "MISSING_WEP_SOURCE_CHARGE_MAP", "species-composition route"),
        ("FB707_6_verdict", "fallback", "scalar/class retained branch", "R10/R11/PPN/source map", "fail_current_corpus", "not executable until maps are real"),
    ]
    return [
        {
            "fallback_id": fallback_id,
            "arena": arena,
            "channel": channel,
            "observable_or_artifact": artifact,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "657_doc", "657_channels", "source_norm_scorecard"),
            "generated_utc": generated,
        }
        for fallback_id, arena, channel, artifact, status, effect in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "update_id": "AIU707_0_scalar_channel",
            "target": "delta_AEH_scalar",
            "inventory_row": "AEHT706_1_scalar_class",
            "formula": "delta_AEH_scalar = F(phi,C)-1",
            "value_or_bound": "MISSING_VALUE_OR_ZERO_THEOREM",
            "current_status": "retained_not_reduced_after_707",
            "valid_for_claim": "false",
            "source_paths": source_list("706_inventory", "706_fill", "704_delta"),
            "generated_utc": generated,
        },
        {
            "update_id": "AIU707_1_AEH_sum",
            "target": "A_EH",
            "inventory_row": "AIF706_0_inventory_sum",
            "formula": "A_EH = 1 + delta_AEH_scalar + remaining delta_AEH_i",
            "value_or_bound": "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS",
            "current_status": "still_unfilled_after_707",
            "valid_for_claim": "false",
            "source_paths": source_list("706_fill", "704_delta"),
            "generated_utc": generated,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL707_0_zero", "Can scalar/class F(phi,C)R be zeroed now?", "No. Absence, constant-universal value, gauge/topological status, algebraic harmlessness, and decoupling are all unsigned.", "fail_blocked", NEXT_TARGET),
        ("EVAL707_1_bound", "Can a scalar/class AEH bound be loaded now?", "No. The bound shape is written, but value, gradient, mass/range, source charge, and PPN maps are missing.", "fail_blocked", NEXT_TARGET),
        ("EVAL707_2_next", "Best next strike?", "Create the scalar/class source row or R10/R11 map rather than pretending the channel vanished.", "route_selected", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("706_doc", "706_inventory", "440_doc", "655_doc"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG707_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG707_1_prior_706", "706 validation clean", "706 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG707_2_zero_theorem", "scalar/class zero theorem", "not_parent_signed", "fail_blocked", "no delta_AEH_scalar zero claim"),
        ("CG707_3_bound", "scalar/class AEH bound", "MISSING_VALUE_OR_ZERO_THEOREM", "fail_blocked", "no epsilon_G_scalar claim"),
        ("CG707_4_R10_R11", "fallback maps", "MISSING_SCALAR_CLASS_COEFFICIENT_ROW", "fail_blocked", "no retained branch score"),
        ("CG707_5_AEH", "A_EH fill", "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS", "fail_blocked", "no A_EH claim"),
        ("CG707_6_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("706_validation", "706_inventory", "706_fill", "705_channels"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D707_0_zero", "scalar/class zero theorem", "failed_current_corpus", "no parent theorem proves absent/constant/gauge/harmless/decoupled scalar-class prefactor", NEXT_TARGET),
        ("D707_1_bound", "scalar/class AEH bound", "schema_written_unfilled", "delta_AEH_scalar bound requires value/gradient/range/source/PPN maps", NEXT_TARGET),
        ("D707_2_retained", "fallback retained branch", "map_written_unfilled", "if not zero, scalar/class channel must enter R10/R11/PPN/source rows", NEXT_TARGET),
        ("D707_3_next", "next target", "selected", "source scalar/class coefficients or R10/R11 maps", NEXT_TARGET),
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
            "summary_id": "S707_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "scalar/class F(phi,C)R is not cleared; it is now converted into delta_AEH_scalar plus R10/R11/PPN fallback requirements",
            "hardest_blocker": "no parent proof that scalar/class sector is absent, constant universal, gauge/topological, algebraically harmless, or source-free decoupled",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, zero, bound, fallback, update, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("706_validation"))
    inventory_rows = read_csv(SOURCE_PATHS["706_inventory"])
    scalar_inventory_retained = any(
        row.get("term_id") == "AEHT706_1_scalar_class" and row.get("current_status") == "retained_not_reduced"
        for row in inventory_rows
    )
    zero_conditional = any(row["theorem_id"] == "SCZ707_7_conditional_theorem" and row["current_status"] == "proved_as_conditional_template" for row in zero)
    zero_blocks = any(row["theorem_id"] == "SCZ707_8_verdict" and row["current_status"] == "fail_current_corpus" for row in zero)
    bound_blocks = any(row["bound_id"] == "SAB707_6_verdict" and row["value_or_bound"] == "fail_current_corpus" for row in bound)
    fallback_blocks = any(row["fallback_id"] == "FB707_6_verdict" and row["current_status"] == "fail_current_corpus" for row in fallback)
    update_unfilled = any(row["update_id"] == "AIU707_0_scalar_channel" and has_missing_marker(row) for row in update)
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [zero, bound, fallback, update, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V707_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V707_1_prior_706_clean", prior_failures == 0, f"706_validation_failures={prior_failures}"),
        ("V707_2_scalar_inventory_retained", scalar_inventory_retained, "AEHT706_1_scalar_class remains retained_not_reduced"),
        ("V707_3_zero_conditional_theorem_written", zero_conditional, "SCZ707 conditional theorem present"),
        ("V707_4_zero_not_promoted", zero_blocks, "SCZ707 verdict blocks claim"),
        ("V707_5_bound_pack_blocks", bound_blocks, "SAB707 verdict blocks claim"),
        ("V707_6_fallback_map_blocks", fallback_blocks, "FB707 verdict blocks claim"),
        ("V707_7_AEH_update_unfilled", update_unfilled, "scalar update keeps MISSING markers"),
        ("V707_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V707_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V707_10_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V707_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V707_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V707_13_status_nonclaim", "no_delta_AEH_scalar_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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


def write_doc(source_rows, zero, bound, fallback, update, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 707 - Y5 R10 Scalar Class FR Prefactor Zero Or AEH Bound

## Verdict

707 attacks the first `A_EH` inventory channel:

```text
sqrt(-g) F(phi,C) R[g_obs]
delta_AEH_scalar := F(phi,C)-1
epsilon_G_scalar ~= |delta_AEH_scalar|
```

The channel does not clear. The current corpus has not proved that the scalar/class sector is absent, constant universal, pure gauge/topological, algebraically harmless, or source-free decoupled. So it cannot be silently set to zero.

The honest fallback is now explicit: either supply a source row for `delta_AEH_scalar`, `grad ln F`, scalar mass/range, source/test charge, and PPN maps, or retain the channel as R10/R11/PPN/source-normalization debt.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Scalar Zero-Theorem Audit

{markdown_table(zero, ["theorem_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Scalar AEH Bound Pack

{markdown_table(bound, ["bound_id", "target", "value_or_bound", "units", "claim_effect", "valid_for_claim"])}

## R10 R11 Fallback Map

{markdown_table(fallback, ["fallback_id", "arena", "channel", "current_status", "claim_effect", "valid_for_claim"])}

## AEH Inventory Update

{markdown_table(update, ["update_id", "target", "value_or_bound", "current_status", "valid_for_claim"])}

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
    zero = scalar_zero_theorem_rows()
    bound = scalar_bound_pack_rows()
    fallback = fallback_map_rows()
    update = aeh_update_rows()
    evaluator = evaluator_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, zero, bound, fallback, update, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_707_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv", zero, ["theorem_id", "clause", "mathematical_requirement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_AEH_BOUND_PACK.csv", bound, ["bound_id", "target", "formula", "value_or_bound", "units", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_R10_R11_FALLBACK_MAP.csv", fallback, ["fallback_id", "arena", "channel", "observable_or_artifact", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_AEH_INVENTORY_UPDATE.csv", update, ["update_id", "target", "inventory_row", "formula", "value_or_bound", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_707_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_707_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, zero, bound, fallback, update, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"zero_rows={len(zero)}")
    print(f"bound_rows={len(bound)}")
    print(f"fallback_rows={len(fallback)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
