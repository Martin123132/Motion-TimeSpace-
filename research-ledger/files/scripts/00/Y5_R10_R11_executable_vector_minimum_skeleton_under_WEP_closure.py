from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_R11_minimum_skeleton_built_nonclaim_under_explicit_WEP_closure"
CLAIM_CEILING = "no_EH_only_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "657-Y5-R10-source-normalization-family-first-real-R11-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md"

FORMALIZATION_WORKBENCH = (
    ROOT.parent / "formalization-workbench"
)
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "653_wep_closure_demotion": ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
    "654_local_gr_spine": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
    "655_eh_or_r11_gate": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "438_r11_contract": ROOT / "438-R11-nonEH-coefficient-vector-contract.md",
    "463_eh_or_r11_executable_gate": ROOT / "463-EH-only-or-R11-executable-vector-gate.md",
    "425_eh_operator_ledger": ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
    "439_eh_only_premise_ladder": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
    "440_metric_only_reduction_attempt": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "443_levi_civita_or_r11_row": ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
    "655_validation_csv": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "655_r11_status_csv": RESIDUALS / "P8_Y5_R10_655_R11_RETAINED_OPERATOR_VECTOR_STATUS.csv",
    "655_decision_gates_csv": RESIDUALS / "P8_Y5_R10_655_EH_OR_R11_DECISION_GATES.csv",
    "655_observable_map_csv": RESIDUALS / "P8_Y5_R10_655_OBSERVABLE_IMPACT_MAP.csv",
    "639_local_bound_matrix_csv": RESIDUALS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv",
    "r11_template_csv": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
    "r11_connection_template_csv": RESIDUALS / "R11_P4_connection_rows_TEMPLATE.csv",
}

COEFFICIENT_SYMBOLS = {
    "boundary_topological_terms": "c_boundary",
    "R2_fR_scalar_mode": "c_R2_fR",
    "Ricci_Weyl_squared": "c_Ricci_Weyl",
    "scalar_tensor_class_metric": "c_ST",
    "vector_preferred_frame": "c_VPF",
    "torsion_nonmetricity": "c_TQ",
    "bulk_X_force_law": "c_X",
    "nonlocal_memory_kernel": "c_mem",
    "source_normalization_operator": "c_mu",
    "projector_domain_stress": "c_PD",
}

QUEUE_ORDER = {
    "source_normalization_operator": 1,
    "torsion_nonmetricity": 2,
    "scalar_tensor_class_metric": 3,
    "vector_preferred_frame": 4,
    "bulk_X_force_law": 5,
    "boundary_topological_terms": 6,
    "R2_fR_scalar_mode": 7,
    "projector_domain_stress": 8,
    "nonlocal_memory_kernel": 9,
    "Ricci_Weyl_squared": 10,
}

MISSING_INPUTS = [
    {
        "missing_input": "coefficient_value_or_parent_zero_theorem",
        "status": "MISSING_NUMERIC_COEFFICIENT_OR_PARENT_ZERO_THEOREM",
        "required_for": "residual prediction, zero claim, and any R11/local-GR scoring",
        "clear_condition": "provide numeric coefficient with units, or a parent-signed theorem that the coefficient vanishes in the local branch",
    },
    {
        "missing_input": "coefficient_units",
        "status": "MISSING_UNITS",
        "required_for": "dimensional consistency and comparison to local bounds",
        "clear_condition": "state coefficient dimensions after action normalization and field conventions are fixed",
    },
    {
        "missing_input": "EH_or_measured_G_normalization",
        "status": "MISSING_NORMALIZATION_RELATIVE_TO_EH_OR_MEASURED_G",
        "required_for": "Newtonian limit, source normalization, and cross-arena local tests",
        "clear_condition": "derive the coefficient normalization relative to EH, measured G, source mass, or an explicitly defined cutoff",
    },
    {
        "missing_input": "weak_field_projection_map",
        "status": "MISSING_WEAK_FIELD_MAP_TO_AFFECTED_R_ROWS",
        "required_for": "PPN, WEP, R10, clock, orbital, and local-observable residuals",
        "clear_condition": "derive the weak-field residual formula or a validated runner mapping the coefficient into each affected R row",
    },
    {
        "missing_input": "coefficient_source_path",
        "status": "MISSING_SOURCE_PATH_FOR_COEFFICIENT",
        "required_for": "auditability and claim eligibility",
        "clear_condition": "cite a local derivation, theorem, notebook, or data artifact that supplies the coefficient or zero theorem",
    },
]


def generated_utc() -> str:
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, str]]:
    rows = []
    now = generated_utc()
    for source_id, path in SOURCE_PATHS.items():
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "role": "prior_contract_or_input_for_656_R11_minimum_skeleton",
                "generated_utc": now,
            }
        )
    return rows


def sanitized_family_key(operator_family: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", operator_family).strip("_")


def r11_minimum_skeleton_rows(
    status_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    template_by_family = {row["operator_family"]: row for row in template_rows}
    rows = []
    now = generated_utc()
    for index, status_row in enumerate(status_rows, start=1):
        family = status_row["operator_family"]
        template_row = template_by_family.get(family, {})
        coefficient = COEFFICIENT_SYMBOLS.get(family, f"c_{sanitized_family_key(family)}")
        affected_rows = status_row.get("affected_rows", "")
        minimum_to_clear = status_row.get("minimum_to_clear", "")
        rows.append(
            {
                "skeleton_id": f"R11SK656_{index:02d}",
                "model_id": "MTS_post_checkpoint_private",
                "branch_id": "WEP_CLOSURE_LOCAL_GR_R11_SKELETON",
                "vector_id": "R11_MIN_SKELETON_656",
                "operator_family": family,
                "coefficient_symbol": coefficient,
                "coefficient_value_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "coefficient_units_status": "MISSING_UNITS",
                "normalization_status": "MISSING_NORMALIZATION_RELATIVE_TO_EH_OR_MEASURED_G",
                "operator_form": template_row.get("operator_form", "MISSING_OPERATOR_FORM_FROM_TEMPLATE"),
                "weak_field_map_status": "MISSING_WEAK_FIELD_MAP",
                "affected_rows": affected_rows,
                "induced_observable_status": "MISSING_OBSERVABLE_RESIDUAL_MAP",
                "predicted_residual_or_bound_source_status": "MISSING_NUMERIC_RESIDUAL_OR_BOUND_MAP",
                "derivation_status": "closure_retained_symbolic_nonclaim",
                "source_file_status": "MISSING_SOURCE_PATH_FOR_COEFFICIENT",
                "source_basis_paths": ";".join(
                    [
                        rel(SOURCE_PATHS["655_r11_status_csv"]),
                        rel(SOURCE_PATHS["r11_template_csv"]),
                        rel(SOURCE_PATHS["655_eh_or_r11_gate"]),
                    ]
                ),
                "priority": status_row.get("priority", ""),
                "minimum_to_clear": minimum_to_clear,
                "score_ready": "false",
                "valid_for_claim": "false",
                "claim_blocker": (
                    "R11 vector is branch-specific but not executable: coefficient value, units, "
                    "normalization, weak-field map, and coefficient source are still missing"
                ),
                "notes": (
                    "656 replaces generic template placeholders with explicit branch blockers; "
                    "this row is a fill target, not evidence for EH/local-GR reduction"
                ),
                "generated_utc": now,
            }
        )
    return rows


def missing_input_ledger_rows(skeleton_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    now = generated_utc()
    for skeleton_row in skeleton_rows:
        for index, missing_input in enumerate(MISSING_INPUTS, start=1):
            rows.append(
                {
                    "missing_id": f"M656_{skeleton_row['skeleton_id']}_{index:02d}",
                    "operator_family": skeleton_row["operator_family"],
                    "coefficient_symbol": skeleton_row["coefficient_symbol"],
                    "missing_input": missing_input["missing_input"],
                    "status": missing_input["status"],
                    "required_for": missing_input["required_for"],
                    "clear_condition": missing_input["clear_condition"],
                    "affected_rows": skeleton_row["affected_rows"],
                    "priority": skeleton_row["priority"],
                    "score_ready": "false",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def scoreability_gate_rows(skeleton_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    family_count = len(skeleton_rows)
    true_score_rows = sum(1 for row in skeleton_rows if row["score_ready"].lower() == "true")
    true_claim_rows = sum(1 for row in skeleton_rows if row["valid_for_claim"].lower() == "true")
    now = generated_utc()
    return [
        {
            "gate_id": "G656_0_family_coverage",
            "gate": "R11 retained family skeleton exists",
            "result": "pass" if family_count == 10 else "fail",
            "detail": f"{family_count} operator families materialized from 655 retained vector status",
            "claim_effect": "structural scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G656_1_coefficient_values",
            "gate": "all coefficient values or zero theorems supplied",
            "result": "blocked",
            "detail": "all skeleton rows still carry MISSING_NUMERIC_OR_THEOREM_ZERO",
            "claim_effect": "blocks R11 scoring and local-GR claim",
            "generated_utc": now,
        },
        {
            "gate_id": "G656_2_units_and_normalization",
            "gate": "all units and EH/measured-G normalizations supplied",
            "result": "blocked",
            "detail": "all skeleton rows still carry MISSING_UNITS and MISSING_NORMALIZATION_RELATIVE_TO_EH_OR_MEASURED_G",
            "claim_effect": "blocks dimensional comparison to PPN/WEP/R10/clocks/orbits",
            "generated_utc": now,
        },
        {
            "gate_id": "G656_3_weak_field_maps",
            "gate": "all weak-field residual maps supplied",
            "result": "blocked",
            "detail": "all skeleton rows still carry MISSING_WEAK_FIELD_MAP",
            "claim_effect": "blocks executable vector residual predictions",
            "generated_utc": now,
        },
        {
            "gate_id": "G656_4_source_paths",
            "gate": "all coefficient source paths supplied",
            "result": "blocked",
            "detail": "all skeleton rows still carry MISSING_SOURCE_PATH_FOR_COEFFICIENT",
            "claim_effect": "blocks auditability and any claim row",
            "generated_utc": now,
        },
        {
            "gate_id": "G656_5_claim_guard",
            "gate": "no score-ready or claim-valid rows are emitted",
            "result": "pass" if true_score_rows == 0 and true_claim_rows == 0 else "fail",
            "detail": f"score_ready_true={true_score_rows}; valid_for_claim_true={true_claim_rows}",
            "claim_effect": CLAIM_CEILING,
            "generated_utc": now,
        },
    ]


def priority_fill_queue_rows(skeleton_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    now = generated_utc()
    ordered = sorted(
        skeleton_rows,
        key=lambda row: (
            QUEUE_ORDER.get(row["operator_family"], 999),
            row["operator_family"],
        ),
    )
    rows = []
    for rank, row in enumerate(ordered, start=1):
        family = row["operator_family"]
        if family == "source_normalization_operator":
            reason = "highest-priority because measured-G/source normalization contaminates Newton, WEP, clocks, R10, and orbital rows"
            first_fill_target = "derive constant measured-G theorem or explicit mu_extra/Gdot/range/source residual map"
        elif family == "torsion_nonmetricity":
            reason = "clears the Levi-Civita metric-compatibility branch before PPN bookkeeping"
            first_fill_target = "derive Levi-Civita parent theorem or torsion/nonmetricity coefficient maps"
        elif family == "scalar_tensor_class_metric":
            reason = "common route for clocks, PPN, R10, and Gdot leakage"
            first_fill_target = "derive scalar silence/no-coupling theorem or clock/PPN/Gdot/R10 map"
        else:
            reason = f"retained {row['priority']} priority R11 family affecting {row['affected_rows']}"
            first_fill_target = row["minimum_to_clear"]
        rows.append(
            {
                "queue_rank": rank,
                "operator_family": family,
                "coefficient_symbol": row["coefficient_symbol"],
                "priority": row["priority"],
                "reason": reason,
                "first_fill_target": first_fill_target,
                "affected_rows": row["affected_rows"],
                "next_artifact": NEXT_TARGET if rank == 1 else "later_657_or_following_family_fill",
                "claim_permission": "false",
                "generated_utc": now,
            }
        )
    return rows


def row_prefix(row_id: str) -> str:
    match = re.match(r"^(R\d+)", row_id)
    return match.group(1) if match else row_id


def observable_row_coverage_rows(
    local_bound_rows: list[dict[str, str]],
    skeleton_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows = []
    for local_row in local_bound_rows:
        prefix = row_prefix(local_row.get("row_id", ""))
        covering = [
            skeleton_row["operator_family"]
            for skeleton_row in skeleton_rows
            if prefix in [part.strip() for part in skeleton_row["affected_rows"].split(";")]
        ]
        rows.append(
            {
                "matrix_id": local_row.get("matrix_id", ""),
                "row_id": local_row.get("row_id", ""),
                "arena": local_row.get("arena", ""),
                "observable": local_row.get("observable", ""),
                "bound_present": local_row.get("bound_present", ""),
                "prediction_numeric_ready": local_row.get("prediction_numeric_ready", ""),
                "covering_operator_families": ";".join(covering),
                "coverage_status": (
                    "covered_by_retained_R11_skeleton_nonclaim"
                    if covering
                    else "NO_RETAINED_OPERATOR_COVERAGE"
                ),
                "score_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def contains_fill_placeholder(rows: list[dict[str, str]]) -> bool:
    for row in rows:
        for value in row.values():
            if isinstance(value, str) and "fill_" in value.lower():
                return True
    return False


def validation_rows(
    source_rows: list[dict[str, str]],
    prior_655_validation: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    skeleton_rows: list[dict[str, str]],
    missing_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    prior_failures = [row for row in prior_655_validation if row.get("result", "").lower() != "pass"]
    status_families = {row["operator_family"] for row in status_rows}
    skeleton_families = {row["operator_family"] for row in skeleton_rows}
    source_missing = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    formalization_changed = 0
    if FORMALIZATION_WORKBENCH.exists():
        for path in FORMALIZATION_WORKBENCH.rglob("*"):
            if path.is_file():
                naive_mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if naive_mtime > FORMALIZATION_CUTOFF:
                    formalization_changed += 1
    blocked_gates = [row for row in gate_rows if row["result"] == "blocked"]
    coverage_missing = [
        row["row_id"] for row in coverage_rows if row["coverage_status"] == "NO_RETAINED_OPERATOR_COVERAGE"
    ]
    checks = [
        (
            "V656_0_source_paths_exist",
            not source_missing,
            "all cited local source paths exist" if not source_missing else f"missing sources: {';'.join(source_missing)}",
        ),
        (
            "V656_1_prior_655_validation_clean",
            not prior_failures,
            "655 validation remains clean" if not prior_failures else f"655 failures={len(prior_failures)}",
        ),
        (
            "V656_2_skeleton_family_count",
            len(skeleton_rows) == 10,
            f"skeleton_rows={len(skeleton_rows)}",
        ),
        (
            "V656_3_skeleton_matches_655_families",
            status_families == skeleton_families,
            f"missing={sorted(status_families - skeleton_families)} extra={sorted(skeleton_families - status_families)}",
        ),
        (
            "V656_4_no_generic_fill_placeholders",
            not contains_fill_placeholder(skeleton_rows),
            "656 skeleton contains explicit MISSING statuses, not generic fill placeholders",
        ),
        (
            "V656_5_missing_statuses_present",
            all(
                row["coefficient_value_status"].startswith("MISSING_")
                and row["coefficient_units_status"].startswith("MISSING_")
                and row["normalization_status"].startswith("MISSING_")
                and row["weak_field_map_status"].startswith("MISSING_")
                and row["source_file_status"].startswith("MISSING_")
                for row in skeleton_rows
            ),
            "all rows carry explicit MISSING coefficient/units/normalization/map/source statuses",
        ),
        (
            "V656_6_no_score_or_claim_true",
            all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in skeleton_rows),
            "all skeleton rows remain score_ready=false and valid_for_claim=false",
        ),
        (
            "V656_7_missing_ledger_complete",
            len(missing_rows) == len(skeleton_rows) * len(MISSING_INPUTS),
            f"missing_rows={len(missing_rows)} expected={len(skeleton_rows) * len(MISSING_INPUTS)}",
        ),
        (
            "V656_8_scoreability_blocked",
            len(blocked_gates) >= 4,
            f"blocked_gates={len(blocked_gates)}",
        ),
        (
            "V656_9_observable_rows_covered",
            len(coverage_rows) == 12 and not coverage_missing,
            f"coverage_rows={len(coverage_rows)} missing={';'.join(coverage_missing)}",
        ),
        (
            "V656_10_next_target_selected",
            NEXT_TARGET.startswith("657-") and "source-normalization" in NEXT_TARGET,
            NEXT_TARGET,
        ),
        (
            "V656_11_claim_ceiling_active",
            CLAIM_CEILING == "no_EH_only_no_Newton_no_PPN_no_R10_no_local_GR_claim",
            CLAIM_CEILING,
        ),
        (
            "V656_12_formalization_workbench_untouched",
            formalization_changed == 0,
            f"formalization_changed_after_cutoff={formalization_changed}",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def nonclaim_summary_rows(
    skeleton_rows: list[dict[str, str]],
    missing_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "skeleton_rows": len(skeleton_rows),
            "missing_input_rows": len(missing_rows),
            "score_ready_rows": sum(1 for row in skeleton_rows if row["score_ready"] == "true"),
            "valid_for_claim_rows": sum(1 for row in skeleton_rows if row["valid_for_claim"] == "true"),
            "blocked_scoreability_gates": sum(1 for row in gate_rows if row["result"] == "blocked"),
            "validation_failures": sum(1 for row in validation if row["result"] != "pass"),
            "next_target": NEXT_TARGET,
            "generated_utc": generated_utc(),
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str], limit: int | None = None) -> str:
    visible_rows = rows if limit is None else rows[:limit]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in visible_rows:
        body.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns)
            + " |"
        )
    if limit is not None and len(rows) > limit:
        body.append("| " + " | ".join(["..."] * len(columns)) + " |")
    return "\n".join([header, separator, *body])


def write_document(
    source_rows: list[dict[str, str]],
    skeleton_rows: list[dict[str, str]],
    missing_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 656 Y5/R10: R11 Executable-Vector Minimum Skeleton Under WEP Closure

## Verdict

Status: `{STATUS}`.

This checkpoint does not prove EH-only reduction, Newtonian recovery, PPN safety, R10 safety, or local-GR recovery. It converts the 655 retained R11 template into a branch-specific, source-traceable work order with explicit blockers. Every retained operator family remains `score_ready=false` and `valid_for_claim=false`.

## Source Register

{markdown_table(source_rows, ["source_id", "exists", "role"])}

## R11 Minimum Skeleton

The skeleton is now concrete enough to fill: each family has a branch id, coefficient symbol, affected rows, and a named minimum-to-clear. The missing quantities are deliberately explicit rather than hidden behind generic template placeholders.

{markdown_table(skeleton_rows, ["operator_family", "coefficient_symbol", "coefficient_value_status", "normalization_status", "weak_field_map_status", "affected_rows", "priority", "valid_for_claim"])}

## Missing Input Ledger

Each operator family has five required inputs before it can be scored: coefficient or zero theorem, coefficient units, EH/measured-G normalization, weak-field projection map, and coefficient source path.

{markdown_table(missing_rows, ["operator_family", "coefficient_symbol", "missing_input", "status", "priority"], limit=20)}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "claim_effect"])}

## Priority Fill Queue

{markdown_table(queue_rows, ["queue_rank", "operator_family", "coefficient_symbol", "reason", "next_artifact"])}

## Observable Row Coverage

{markdown_table(coverage_rows, ["row_id", "arena", "observable", "covering_operator_families", "coverage_status"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "skeleton_rows", "missing_input_rows", "score_ready_rows", "valid_for_claim_rows", "blocked_scoreability_gates", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

The useful result is not a physics win yet; it is a control-system win. The R11 branch is no longer a vague bucket. It is a set of ten named operator families with named coefficients, named affected arenas, and named missing inputs. The next best route is the source-normalization operator because it sits under measured G, Newtonian source mass, WEP leakage, clock leakage, R10 range bounds, and orbital residuals.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    status_rows = read_csv(SOURCE_PATHS["655_r11_status_csv"])
    template_rows = read_csv(SOURCE_PATHS["r11_template_csv"])
    local_bound_rows = read_csv(SOURCE_PATHS["639_local_bound_matrix_csv"])
    prior_655_validation = read_csv(SOURCE_PATHS["655_validation_csv"])

    skeleton_rows = r11_minimum_skeleton_rows(status_rows, template_rows)
    missing_rows = missing_input_ledger_rows(skeleton_rows)
    gate_rows = scoreability_gate_rows(skeleton_rows)
    queue_rows = priority_fill_queue_rows(skeleton_rows)
    coverage_rows = observable_row_coverage_rows(local_bound_rows, skeleton_rows)
    validation = validation_rows(
        source_rows,
        prior_655_validation,
        status_rows,
        skeleton_rows,
        missing_rows,
        gate_rows,
        coverage_rows,
    )
    summary_rows = nonclaim_summary_rows(skeleton_rows, missing_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_656_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_R11_MINIMUM_SKELETON.csv",
        skeleton_rows,
        [
            "skeleton_id",
            "model_id",
            "branch_id",
            "vector_id",
            "operator_family",
            "coefficient_symbol",
            "coefficient_value_status",
            "coefficient_units_status",
            "normalization_status",
            "operator_form",
            "weak_field_map_status",
            "affected_rows",
            "induced_observable_status",
            "predicted_residual_or_bound_source_status",
            "derivation_status",
            "source_file_status",
            "source_basis_paths",
            "priority",
            "minimum_to_clear",
            "score_ready",
            "valid_for_claim",
            "claim_blocker",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_MISSING_INPUT_LEDGER.csv",
        missing_rows,
        [
            "missing_id",
            "operator_family",
            "coefficient_symbol",
            "missing_input",
            "status",
            "required_for",
            "clear_condition",
            "affected_rows",
            "priority",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_PRIORITY_FILL_QUEUE.csv",
        queue_rows,
        [
            "queue_rank",
            "operator_family",
            "coefficient_symbol",
            "priority",
            "reason",
            "first_fill_target",
            "affected_rows",
            "next_artifact",
            "claim_permission",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_OBSERVABLE_ROW_COVERAGE.csv",
        coverage_rows,
        [
            "matrix_id",
            "row_id",
            "arena",
            "observable",
            "bound_present",
            "prediction_numeric_ready",
            "covering_operator_families",
            "coverage_status",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_656_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "skeleton_rows",
            "missing_input_rows",
            "score_ready_rows",
            "valid_for_claim_rows",
            "blocked_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_656_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(
        source_rows,
        skeleton_rows,
        missing_rows,
        gate_rows,
        queue_rows,
        coverage_rows,
        summary_rows,
        validation,
    )

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"skeleton_rows={len(skeleton_rows)}")
    print(f"missing_input_rows={len(missing_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
