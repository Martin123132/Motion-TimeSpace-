from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1321"
TITLE = "1321-Y5-R10-RAB-clock-readout-direct-product-first-fill-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BOUND_IMPORT_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_BOUND_IMPORT.csv"
FIRST_FILL_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_FIRST_FILL_TEMPLATE.csv"
PRODUCT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_PRODUCT_SCHEMA.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_FIRST_FILL_RUNNER.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1321_VALIDATION.csv"


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        BOUND_IMPORT_PATH,
        FIRST_FILL_TEMPLATE_PATH,
        PRODUCT_SCHEMA_PATH,
        RUNNER_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def numeric_positive(value: object) -> bool:
    try:
        return float(str(value)) > 0
    except ValueError:
        return False


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1321_0_1320_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1320_NEXT_TARGET.csv",
            "needle": "NEXT1320_0_1321",
            "role": "handoff into clock direct-product/readout first-fill runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_1_1320_priority",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1320_FINITE_SOURCE_PRIORITY_MAP.csv",
            "needle": "SURV1319_1_clock",
            "role": "clock selected as rank-1 finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_2_1320_first_fill",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1320_FIRST_FILL_ROUTE_MATRIX.csv",
            "needle": "FF1320_0_selected_next",
            "role": "clock first-fill route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_3_1320_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1320_ACCEPTANCE_GATES.csv",
            "needle": "GATE1320_1_clock",
            "role": "no standalone b_alpha clock gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_4_1052_clock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "needle": "ACB1052_2",
            "role": "best current source-backed clock product bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_5_1316_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
            "needle": "REQ1316_4_tau_clock",
            "role": "clock source requirement ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_6_1317_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv",
            "needle": "TPL1317_5_clock_sensitivity_readout_model",
            "role": "clock fillable source template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1321_7_1317_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv",
            "needle": "RUN1317_1_run1314_1_clock",
            "role": "current refused clock runner row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    clock_bounds = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"))
    bound_import = []
    for row in clock_bounds:
        is_best = row["bound_id"] == "ACB1052_2"
        bound_import.append(
            {
                "bound_import_id": f"CBI1321_{len(bound_import)}",
                "source_bound_id": row["bound_id"],
                "row_type": row["row_type"],
                "clock_pair": row["clock_pair"],
                "delta_K_alpha": row["delta_K_alpha"],
                "product_bound_1sigma_yr_inv": row["product_bound_1sigma_yr_inv"],
                "product_bound_2sigma_yr_inv": row["product_bound_2sigma_yr_inv"],
                "h0_normalized_diagnostic": row["H0_normalized_diagnostic"],
                "is_selected_best_bound": is_best,
                "bound_interpretation": "comparison_bound_for_direct_clock_product_only",
                "standalone_balpha_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    first_fill_template = [
        {
            "template_id": "CLK1321_0_direct_product",
            "route": "direct P_clock_alpha prediction",
            "required_fields": "clock_pair;delta_K_alpha;predicted_product_value;predicted_product_units;readout_model;source_path;source_anchor;provenance_note",
            "current_fill": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "acceptance_rule": "abs(predicted_product_value)<=product_bound only after predicted value is numeric, sourced, and same clock/readout convention",
            "refusal_if_missing": "MISSING_DIRECT_CLOCK_PRODUCT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "CLK1321_1_factorized_product",
            "route": "factorized b_alpha*tau_clock_time",
            "required_fields": "b_alpha_or_zero_certificate;tau_clock_time;clock_pair;readout_model;units;source_path;source_anchor;provenance_note",
            "current_fill": "MISSING_B_ALPHA_AND_TAU_CLOCK_TIME",
            "acceptance_rule": "factorized product can score only if both b_alpha and tau_clock_time are sourced or theorem-signed",
            "refusal_if_missing": "MISSING_FACTORISED_CLOCK_PRODUCT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "CLK1321_2_tau_readout",
            "route": "tau_clock_time/readout map",
            "required_fields": "tau_clock_time;time_units;definition;parent_branch;clock_sensitivity;source_path;source_anchor",
            "current_fill": "MISSING_CLOCK_READOUT_MAP",
            "acceptance_rule": "tau is not assumed from H0 diagnostic; it must be derived or sourced as a readout projection",
            "refusal_if_missing": "MISSING_TAU_CLOCK_READOUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "CLK1321_3_clock_model",
            "route": "clock sensitivity/readout model",
            "required_fields": "clock_pair;transition_sensitivity_delta_K_alpha;observable_definition;readout_kernel;units;source_path;source_anchor",
            "current_fill": "PARTIAL_BOUND_ROW_ONLY",
            "acceptance_rule": "bound clock pair/sensitivity can be imported, but MTS readout kernel remains missing",
            "refusal_if_missing": "MISSING_MTS_CLOCK_MODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_schema = [
        {
            "schema_id": "CPS1321_0_compare_direct",
            "product_form": "P_clock_alpha_direct",
            "formula": "abs(P_clock_alpha_direct) <= product_bound_yr_inv",
            "required_inputs": "numeric P_clock_alpha_direct;yr^-1 units;source path;matching clock_pair;readout model",
            "forbidden_inputs": "threshold_as_prediction;unsourced product;cross-arena transferred product",
            "current_status": "MISSING_NUMERIC_DIRECT_PRODUCT",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CPS1321_1_compare_factorized",
            "product_form": "b_alpha*tau_clock_time",
            "formula": "abs(b_alpha*tau_clock_time) <= product_bound_yr_inv",
            "required_inputs": "source-backed b_alpha or theorem-zero;source-backed tau_clock_time;yr^-1 convention;readout source",
            "forbidden_inputs": "assuming tau=H0;dividing bound by guessed tau;using b_alpha threshold as prediction",
            "current_status": "MISSING_B_ALPHA_AND_TAU_CLOCK_TIME",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CPS1321_2_no_standalone_balpha",
            "product_form": "standalone b_alpha from clock bound",
            "formula": "NOT_ALLOWED: b_alpha <= product_bound/tau_assumed",
            "required_inputs": "none; route is forbidden unless tau is independently sourced and then product only is scored",
            "forbidden_inputs": "tau assumption;H0 normalized diagnostic as tau;clock-to-WEP/R10 transfer",
            "current_status": "FORBIDDEN_SHORTCUT",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    selected_bound = next(row for row in bound_import if row["source_bound_id"] == "ACB1052_2")
    runner_rows = [
        {
            "runner_id": "CLKRUN1321_0_best_clock_bound",
            "source_bound_id": selected_bound["source_bound_id"],
            "clock_pair": selected_bound["clock_pair"],
            "delta_K_alpha": selected_bound["delta_K_alpha"],
            "comparison_bound_1sigma_yr_inv": selected_bound["product_bound_1sigma_yr_inv"],
            "comparison_bound_2sigma_yr_inv": selected_bound["product_bound_2sigma_yr_inv"],
            "predicted_product_value": "MISSING_DIRECT_PRODUCT_OR_B_ALPHA_TAU",
            "predicted_product_units": "MISSING_UNITS",
            "readout_model": "MISSING_MTS_CLOCK_READOUT_MODEL",
            "tau_clock_time": "MISSING_CLOCK_READOUT_MAP",
            "b_alpha_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO",
            "runner_status": "REFUSED",
            "refusal_reason": "no_numeric_predicted_product;missing_tau_or_direct_product;missing_readout_model;standalone_balpha_forbidden",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1321_0_no_standalone_balpha",
            "shortcut": "infer standalone b_alpha by dividing clock product bound by assumed tau",
            "enforcement": "REFUSED; clock bound constrains product only unless tau is independently sourced",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1321_1_no_tau_h0_assumption",
            "shortcut": "use H0-normalized diagnostic as tau_clock_time",
            "enforcement": "REFUSED; H0 diagnostic is not a readout derivation",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1321_2_no_threshold_prediction",
            "shortcut": "use clock bound as predicted product",
            "enforcement": "REFUSED; bound is comparison fence only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1321_3_no_cross_arena_transfer",
            "shortcut": "transfer clock product into WEP/R10/local rows",
            "enforcement": "REFUSED until shared parent branch/readout functor is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1321_4_no_parent_reopen",
            "shortcut": "reopen closure-only parent theorem route from clock bound",
            "enforcement": "REFUSED; clock product data cannot sign parent object-language clauses",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1321_0_runner_created",
            "decision": "clock first-fill runner created",
            "because": "clock is the most source-ready finite row after 1320 ranking",
            "next_action": "try to derive or source tau_clock_time/readout map, or source a direct P_clock_alpha prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1321_1_product_only",
            "decision": "clock bound remains product-only",
            "because": "tau_clock_time and b_alpha are not independently sourced",
            "next_action": "do not report standalone b_alpha; fill direct product route first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1321_2_derivation_next",
            "decision": "next target is clock tau/readout derivation or exact source rejection",
            "because": "runner is now ready but every current clock product row is refused",
            "next_action": "1322 should attack tau_clock_time/readout map from MTS time/clock structure before fallback sourcing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1321_0_1322",
            "target_file": "1322-Y5-R10-RAB-clock-tau-readout-map-derivation-or-source-rejection.md",
            "target_script": "scripts/Y5_R10_RAB_clock_tau_readout_map_derivation_or_source_rejection.py",
            "task": "try to derive tau_clock_time/readout map from MTS time/clock structure; if not derivable, produce exact source requirements for a direct P_clock_alpha fill",
            "success_condition": "clock row either gains a signed tau/readout expression or receives a precise nonclaim source requirement ledger; standalone b_alpha remains refused",
            "do_not": "do not infer b_alpha from the clock bound; do not use H0 diagnostic as tau; do not transfer clock product to WEP/R10/local tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1321_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    best_bound_ok = (
        selected_bound["source_bound_id"] == "ACB1052_2"
        and numeric_positive(selected_bound["product_bound_1sigma_yr_inv"])
        and compact_bool(selected_bound["is_selected_best_bound"])
    )
    validation.append(
        validation_row(
            "VAL1321_1_best_clock_bound_imported",
            "best current clock product bound is imported as comparison-only",
            best_bound_ok,
            f"{selected_bound['clock_pair']} bound={selected_bound['product_bound_1sigma_yr_inv']} yr^-1",
        )
    )
    validation.append(
        validation_row(
            "VAL1321_2_fill_template_complete",
            "clock first-fill template covers direct product, factorized product, tau, and clock model",
            len(first_fill_template) == 4
            and all(row["current_fill"].startswith("MISSING") or row["current_fill"] == "PARTIAL_BOUND_ROW_ONLY" for row in first_fill_template),
            ";".join(row["template_id"] for row in first_fill_template),
        )
    )
    validation.append(
        validation_row(
            "VAL1321_3_product_schema_blocks_standalone_balpha",
            "product schema explicitly forbids standalone b_alpha inference",
            any(row["schema_id"] == "CPS1321_2_no_standalone_balpha" and row["current_status"] == "FORBIDDEN_SHORTCUT" for row in product_schema),
            "standalone b_alpha route forbidden",
        )
    )
    validation.append(
        validation_row(
            "VAL1321_4_runner_refuses_current_clock_row",
            "runner refuses current clock row until direct product or tau/readout is filled",
            len(runner_rows) == 1 and runner_rows[0]["runner_status"] == "REFUSED",
            runner_rows[0]["refusal_reason"],
        )
    )
    validation.append(
        validation_row(
            "VAL1321_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("bound", bound_import),
        ("template", first_fill_template),
        ("schema", product_schema),
        ("runner", runner_rows),
        ("shortcuts", anti_shortcut),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1321_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1321_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1321_8_next_target_1322",
            "next target routes to clock tau/readout map derivation or source rejection",
            next_target[0]["target_file"].startswith("1322-Y5-R10-RAB-clock-tau-readout"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1321_9_overall",
            "overall 1321 validation",
            all(row["status"] == "PASS" for row in validation),
            "1321 creates clock first-fill runner, imports product bound, refuses standalone b_alpha, and routes to tau/readout derivation",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(BOUND_IMPORT_PATH, bound_import)
    write_csv(FIRST_FILL_TEMPLATE_PATH, first_fill_template)
    write_csv(PRODUCT_SCHEMA_PATH, product_schema)
    write_csv(RUNNER_PATH, runner_rows)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1321: RAB Clock Readout Direct Product First-Fill Runner

**Current verdict:** 1321 creates the clock first-fill runner but does not claim a clock pass or a standalone `b_alpha`. The imported clock bound is comparison-only.

**Main progress:** the selected Yb clock product bound is now wired into a refusal runner with two allowed future routes: a direct sourced `P_clock_alpha`, or a fully sourced factorized `b_alpha*tau_clock_time`. Both are currently missing.

**Decision:** attack `tau_clock_time`/readout derivation next. If that fails, the direct-product source requirement remains the honest fallback.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Clock Bound Import
{markdown_table(bound_import, ["bound_import_id", "source_bound_id", "row_type", "clock_pair", "delta_K_alpha", "product_bound_1sigma_yr_inv", "product_bound_2sigma_yr_inv", "h0_normalized_diagnostic", "is_selected_best_bound", "bound_interpretation", "standalone_balpha_ready", "valid_for_claim", "claim_allowed"])}

## Clock First-Fill Template
{markdown_table(first_fill_template, ["template_id", "route", "required_fields", "current_fill", "acceptance_rule", "refusal_if_missing", "valid_for_claim", "claim_allowed"])}

## Clock Product Schema
{markdown_table(product_schema, ["schema_id", "product_form", "formula", "required_inputs", "forbidden_inputs", "current_status", "score_ready", "valid_for_claim", "claim_allowed"])}

## Clock First-Fill Runner
{markdown_table(runner_rows, ["runner_id", "source_bound_id", "clock_pair", "delta_K_alpha", "comparison_bound_1sigma_yr_inv", "comparison_bound_2sigma_yr_inv", "predicted_product_value", "readout_model", "tau_clock_time", "b_alpha_status", "runner_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
