from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1323"
TITLE = "1323-Y5-R10-RAB-clock-direct-product-source-pack-and-acceptance-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BOUND_LINK_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_BOUND_LINK.csv"
SOURCE_PACK_PATH = OUT_DIR / f"{PACK_ID}_DIRECT_CLOCK_PRODUCT_SOURCE_PACK.csv"
ACCEPTANCE_RULES_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTANCE_RULES.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTANCE_RUNNER.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1323_VALIDATION.csv"


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
        BOUND_LINK_PATH,
        SOURCE_PACK_PATH,
        ACCEPTANCE_RULES_PATH,
        RUNNER_PATH,
        BLOCKER_LEDGER_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def numeric_value(value: object) -> float | None:
    try:
        return float(str(value))
    except ValueError:
        return None


def missing_token(value: object) -> bool:
    text = str(value).strip()
    return not text or "MISSING" in text or text.lower() in {"none", "null", "nan"}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1323_0_1322_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_NEXT_TARGET.csv",
            "needle": "NEXT1322_0_1323",
            "role": "handoff into direct clock product source pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_1_1322_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_DIRECT_PRODUCT_SOURCE_REQUIREMENTS.csv",
            "needle": "DCP1322_1_direct_product",
            "role": "direct clock product requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_2_1322_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_RUNNER_UPDATE.csv",
            "needle": "CLKRUN1322_0_tau_derivation_attempt",
            "role": "refused tau/readout runner state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_3_1322_shortcuts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_ANTI_SHORTCUT_GATES.csv",
            "needle": "SHORT1322_3_no_standalone_balpha",
            "role": "inherited no-standalone-balpha/no-transfer gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_4_1321_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_BOUND_IMPORT.csv",
            "needle": "ACB1052_2",
            "role": "selected Yb comparison bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_5_646_sensitivity",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "needle": "CAS646_1_YbE3E2",
            "role": "source-backed Yb clock sensitivity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1323_6_948_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv",
            "needle": "CLK948_1_CAS646_1_YbE3E2",
            "role": "prior clock product runner with missing MTS product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    bounds = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_BOUND_IMPORT.csv"))
    selected_bound = next(row for row in bounds if row["source_bound_id"] == "ACB1052_2")
    sensitivity_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"))
    yb_sensitivity = next(row for row in sensitivity_rows if row["clock_pair_id"] == "CAS646_1_YbE3E2")

    bound_link = [
        {
            "bound_link_id": "CBL1323_0_yb_e3e2",
            "source_bound_id": selected_bound["source_bound_id"],
            "clock_pair_id": yb_sensitivity["clock_pair_id"],
            "clock_pair": selected_bound["clock_pair"],
            "delta_K_alpha": selected_bound["delta_K_alpha"],
            "product_bound_1sigma_yr_inv": selected_bound["product_bound_1sigma_yr_inv"],
            "product_bound_2sigma_yr_inv": selected_bound["product_bound_2sigma_yr_inv"],
            "sensitivity_source_status": yb_sensitivity["delta_K_alpha_source_status"],
            "source_urls": yb_sensitivity["source_urls"],
            "comparison_role": "comparison_bound_only",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_pack = [
        {
            "product_row_id": "DCLK1323_0_yb_direct_product",
            "bound_link_id": "CBL1323_0_yb_e3e2",
            "clock_pair": selected_bound["clock_pair"],
            "delta_K_alpha": selected_bound["delta_K_alpha"],
            "predicted_product_value": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "predicted_product_units": "MISSING_YR_INV_UNITS",
            "product_definition": "MISSING_MTS_CLOCK_PRODUCT_DEFINITION",
            "readout_model": "MISSING_MTS_CLOCK_READOUT_KERNEL",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "equation_ref": "MISSING_EQUATION_REF",
            "provenance_note": "MISSING_PROVENANCE",
            "sign_convention": "MISSING_SIGN_OR_ABS_CONVENTION",
            "cross_arena_policy": "NO_TRANSFER_TO_WEP_R10_LOCAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    acceptance_rules = [
        {
            "rule_id": "AR1323_0_numeric_product",
            "rule": "predicted product must be numeric finite yr^-1 value",
            "reject_if": "MISSING_DIRECT_P_CLOCK_ALPHA;non_numeric;wrong_units",
            "current_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "AR1323_1_provenance",
            "rule": "source_path, source_anchor, equation_ref, and provenance note must be present",
            "reject_if": "any source/provenance field is missing",
            "current_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "AR1323_2_readout_model",
            "rule": "MTS clock readout kernel must match the Yb E3/E2 convention",
            "reject_if": "readout model missing or cross-arena transferred",
            "current_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "AR1323_3_bound_comparison",
            "rule": "compare abs(predicted_product_value) <= product_bound_1sigma_yr_inv after all source gates pass",
            "reject_if": "prediction missing, source gates fail, or abs prediction exceeds selected bound",
            "current_status": "NOT_SCORED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "AR1323_4_no_balpha",
            "rule": "standalone b_alpha inference is forbidden",
            "reject_if": "row is produced by dividing clock bound by tau assumption",
            "current_status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = []
    blocker_rows = []
    bound_value = numeric_value(selected_bound["product_bound_1sigma_yr_inv"])
    for source_row in source_pack:
        predicted = numeric_value(source_row["predicted_product_value"])
        missing_fields = [
            field
            for field in [
                "predicted_product_value",
                "predicted_product_units",
                "product_definition",
                "readout_model",
                "source_path",
                "source_anchor",
                "equation_ref",
                "provenance_note",
                "sign_convention",
            ]
            if missing_token(source_row[field])
        ]
        unit_ok = source_row["predicted_product_units"] in {"yr^-1", "1/yr", "yr_inv"}
        source_ok = not any(field in missing_fields for field in ["source_path", "source_anchor", "equation_ref", "provenance_note"])
        product_ok = predicted is not None and unit_ok and source_ok and not missing_fields
        comparison_pass = product_ok and bound_value is not None and abs(predicted) <= bound_value
        if missing_fields:
            for field in missing_fields:
                blocker_rows.append(
                    {
                        "blocker_id": f"BLK1323_{len(blocker_rows)}",
                        "product_row_id": source_row["product_row_id"],
                        "blocked_field": field,
                        "blocker": source_row[field],
                        "required_resolution": "replace placeholder with numeric/provenanced direct clock product input",
                        "valid_for_claim": False,
                        "claim_allowed": False,
                    }
                )
        runner_rows.append(
            {
                "runner_id": "ACCEPT1323_0_yb_direct_product",
                "product_row_id": source_row["product_row_id"],
                "clock_pair": source_row["clock_pair"],
                "bound_1sigma_yr_inv": selected_bound["product_bound_1sigma_yr_inv"],
                "predicted_product_value": source_row["predicted_product_value"],
                "predicted_product_units": source_row["predicted_product_units"],
                "missing_field_count": len(missing_fields),
                "missing_fields": ";".join(missing_fields),
                "numeric_product_ok": predicted is not None,
                "unit_ok": unit_ok,
                "source_provenance_ok": source_ok,
                "comparison_status": "PASS" if comparison_pass else "NOT_SCORED_OR_REFUSED",
                "runner_status": "PASS_NONCLAIM_REVIEW" if comparison_pass else "REFUSED",
                "refusal_reason": "placeholder_or_missing_direct_product_source_pack" if not comparison_pass else "nonclaim_review_only",
                "score_ready": product_ok,
                "valid_prediction_row": product_ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    anti_shortcut = [
        {
            "gate_id": "SHORT1323_0_no_placeholder_pass",
            "shortcut": "allow placeholder direct product rows to compare",
            "enforcement": "REFUSED until all MISSING fields are replaced",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1323_1_no_bound_as_prediction",
            "shortcut": "copy the clock bound into predicted_product_value",
            "enforcement": "REFUSED; bound is comparison data only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1323_2_no_tau_balpha",
            "shortcut": "use tau/H0 assumptions or standalone b_alpha to backfill direct product",
            "enforcement": "REFUSED; direct product source must stand on its own",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1323_3_no_cross_arena_transfer",
            "shortcut": "reuse this clock row as WEP/R10/local evidence",
            "enforcement": "REFUSED; cross-arena transfer remains blocked",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1323_0_source_pack_created",
            "decision": "direct clock product source pack created",
            "because": "1322 rejected tau/readout derivation but preserved direct product as the honest fallback",
            "next_action": "attempt to derive or source the direct P_clock_alpha value/readout kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1323_1_runner_refuses",
            "decision": "acceptance runner refuses current direct product row",
            "because": "predicted product, units, readout model, source path, source anchor, equation reference, and provenance are missing",
            "next_action": "1324 should attempt direct product derivation/source fill or demote clock to wait-state and move to WEP decomposition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1323_2_no_claim",
            "decision": "no clock pass or b_alpha claim",
            "because": "source pack is a gate, not evidence",
            "next_action": "preserve Yb bound as comparison-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1323_0_1324",
            "target_file": "1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate.md",
            "target_script": "scripts/Y5_R10_RAB_clock_direct_product_derivation_source_fill_or_waitstate.py",
            "task": "try to fill the direct P_clock_alpha product from MTS readout theory or a source-backed expression; if not possible, move clock to wait-state and proceed to WEP source-normalization decomposition",
            "success_condition": "direct clock product is either sourced/derived with units/provenance or explicitly wait-stated with exact missing fields and next WEP route selected",
            "do_not": "do not use bound-as-prediction, tau/H0 assumptions, standalone b_alpha, or cross-arena transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1323_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    validation.append(
        validation_row(
            "VAL1323_1_bound_link_ready",
            "Yb E3/E2 comparison bound and sensitivity are linked",
            len(bound_link) == 1
            and bound_link[0]["clock_pair_id"] == "CAS646_1_YbE3E2"
            and numeric_value(bound_link[0]["product_bound_1sigma_yr_inv"]) is not None,
            f"{bound_link[0]['clock_pair']} bound={bound_link[0]['product_bound_1sigma_yr_inv']} yr^-1",
        )
    )
    required_columns = {
        "predicted_product_value",
        "predicted_product_units",
        "product_definition",
        "readout_model",
        "source_path",
        "source_anchor",
        "equation_ref",
        "provenance_note",
        "sign_convention",
    }
    validation.append(
        validation_row(
            "VAL1323_2_source_pack_schema_complete",
            "direct source pack contains all required fill fields",
            len(source_pack) == 1 and required_columns.issubset(source_pack[0].keys()),
            ";".join(sorted(required_columns)),
        )
    )
    validation.append(
        validation_row(
            "VAL1323_3_acceptance_rules_written",
            "acceptance rules block missing product, provenance, readout, and b_alpha shortcuts",
            len(acceptance_rules) == 5
            and any(row["rule_id"] == "AR1323_4_no_balpha" for row in acceptance_rules),
            ";".join(row["rule_id"] for row in acceptance_rules),
        )
    )
    validation.append(
        validation_row(
            "VAL1323_4_runner_refuses_placeholders",
            "acceptance runner refuses current placeholder source pack",
            len(runner_rows) == 1
            and runner_rows[0]["runner_status"] == "REFUSED"
            and int(runner_rows[0]["missing_field_count"]) == len(required_columns),
            runner_rows[0]["missing_fields"],
        )
    )
    validation.append(
        validation_row(
            "VAL1323_5_blockers_recorded",
            "all missing direct product fields are recorded as blockers",
            len(blocker_rows) == len(required_columns),
            f"blockers={len(blocker_rows)}",
        )
    )
    validation.append(
        validation_row(
            "VAL1323_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("bound", bound_link),
        ("pack", source_pack),
        ("rules", acceptance_rules),
        ("runner", runner_rows),
        ("blockers", blocker_rows),
        ("shortcuts", anti_shortcut),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1323_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1323_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1323_9_next_target_1324",
            "next target routes to direct product fill or wait-state",
            next_target[0]["target_file"].startswith("1324-Y5-R10-RAB-clock-direct-product"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1323_10_overall",
            "overall 1323 validation",
            all(row["status"] == "PASS" for row in validation),
            "1323 creates direct clock product source pack, links Yb bound, refuses placeholders, and preserves nonclaim gates",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(BOUND_LINK_PATH, bound_link)
    write_csv(SOURCE_PACK_PATH, source_pack)
    write_csv(ACCEPTANCE_RULES_PATH, acceptance_rules)
    write_csv(RUNNER_PATH, runner_rows)
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1323: RAB Clock Direct Product Source Pack And Acceptance Runner

**Current verdict:** 1323 builds the direct `P_clock_alpha` source pack and acceptance runner. It does not claim a clock pass; the current source pack is intentionally refused because the MTS product is still missing.

**Main progress:** the Yb E3/E2 clock bound is now linked to a placeholder-free acceptance contract: a future direct product row must provide a numeric yr^-1 prediction, readout model, source path, source anchor, equation reference, provenance, and sign convention before comparison.

**Decision:** try one direct product fill attempt next. If no MTS readout/source expression exists, move the clock row to wait-state and shift to WEP source-normalization decomposition.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Clock Bound Link
{markdown_table(bound_link, ["bound_link_id", "source_bound_id", "clock_pair_id", "clock_pair", "delta_K_alpha", "product_bound_1sigma_yr_inv", "product_bound_2sigma_yr_inv", "sensitivity_source_status", "comparison_role", "valid_for_claim", "claim_allowed"])}

## Direct Clock Product Source Pack
{markdown_table(source_pack, ["product_row_id", "bound_link_id", "clock_pair", "delta_K_alpha", "predicted_product_value", "predicted_product_units", "product_definition", "readout_model", "source_path", "source_anchor", "equation_ref", "provenance_note", "sign_convention", "cross_arena_policy", "valid_for_claim", "claim_allowed"])}

## Acceptance Rules
{markdown_table(acceptance_rules, ["rule_id", "rule", "reject_if", "current_status", "valid_for_claim", "claim_allowed"])}

## Acceptance Runner
{markdown_table(runner_rows, ["runner_id", "product_row_id", "clock_pair", "bound_1sigma_yr_inv", "predicted_product_value", "predicted_product_units", "missing_field_count", "missing_fields", "numeric_product_ok", "unit_ok", "source_provenance_ok", "comparison_status", "runner_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Blocker Ledger
{markdown_table(blocker_rows, ["blocker_id", "product_row_id", "blocked_field", "blocker", "required_resolution", "valid_for_claim", "claim_allowed"])}

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
