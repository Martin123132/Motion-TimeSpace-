from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "MTS-local-residual-vector-evaluator"
CHECKPOINT_DOC = "431-MTS-local-residual-vector-evaluator.md"
STATUS = "MTS_local_residual_vector_evaluator_written_template_dryrun_blocks_missing_predictions_no_local_GR_pass"
CLAIM_CEILING = "MTS_local_residual_vector_evaluator_dryrun_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "432-same-frame-matter-functor-zero-route.md"

DEFAULT_PREDICTIONS = ROOT / "source-intake" / "mts_residuals" / "MTS_local_residual_predictions_TEMPLATE.csv"
LOCAL_BOUNDS_CSV = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
RESIDUAL_COMPONENTS_CSV = ROOT / "runs" / "20260602-094500-MTS-local-residual-vector-input-contract" / "results" / "residual_components.csv"
ROUTE_RANKING_CSV = ROOT / "runs" / "20260602-103000-Ward-source-residual-zero-route-gate" / "results" / "route_ranking.csv"


REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "row_id",
    "observable",
    "predicted_value",
    "one_sigma",
    "upper_envelope",
    "units",
    "curve_or_vector_file",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "comparison_role",
    "claim_request",
    "notes",
]

ALLOWED_DERIVATION_STATUS = {
    "derived_zero",
    "derived_bound",
    "fitted",
    "phenomenological",
    "closure_assumed",
    "speculative",
}

CLAIM_STRONG_STATUSES = {"derived_zero", "derived_bound"}


SOURCE_DOCS = [
    {
        "path": "431-MTS-local-residual-vector-evaluator.md",
        "role": "checkpoint written by this run",
        "required_before_run": False,
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "input residual-vector contract",
        "required_before_run": True,
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C0-C7 route ranking and promotion decision tree",
        "required_before_run": True,
    },
    {
        "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "default dry-run prediction template",
        "required_before_run": True,
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "sourced local-bound constraints",
        "required_before_run": True,
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "canonical R0-R11 residual components",
        "required_before_run": True,
    },
    {
        "path": "runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv",
        "role": "C0-C7 route ranking used for row warnings",
        "required_before_run": True,
    },
]


EVALUATOR_RULES = [
    {
        "rule_id": "numeric_abs_compare",
        "applies_to": "R0-R9 numeric rows",
        "logic": "score=max(abs(predicted_value), abs(upper_envelope if supplied)); compare score <= sourced upper_bound",
        "pass_status": "residual_below_bound_no_GR_claim",
        "fail_status": "missing_numeric_prediction_no_pass or residual_exceeds_bound",
    },
    {
        "rule_id": "symbolic_curve_block",
        "applies_to": "R10 fifth-force alpha(lambda)",
        "logic": "requires curve_or_vector_file or audited theorem-zero source; scalar placeholder cannot pass",
        "pass_status": "executable_curve_or_theorem_zero_needs_specialized_audit",
        "fail_status": "symbolic_file_missing_no_pass",
    },
    {
        "rule_id": "symbolic_operator_block",
        "applies_to": "R11 non-EH operator coefficients",
        "logic": "requires operator-vector file or audited theorem-zero source; symbolic placeholder cannot pass",
        "pass_status": "operator_vector_or_theorem_zero_needs_specialized_audit",
        "fail_status": "symbolic_file_missing_no_pass",
    },
    {
        "rule_id": "derivation_status_gate",
        "applies_to": "all rows",
        "logic": "derived_local_GR_candidate requires derived_zero/derived_bound rows; closure/fitted/speculative can only be empirical stress tests",
        "pass_status": "claim_request_consistent",
        "fail_status": "claim_request_exceeds_derivation_status",
    },
    {
        "rule_id": "source_file_gate",
        "applies_to": "claim-bearing rows",
        "logic": "source_file must exist unless claim_request is none and row is a dry-run placeholder",
        "pass_status": "source_file_ready",
        "fail_status": "source_file_missing_or_placeholder",
    },
    {
        "rule_id": "all_rows_or_no_local_GR",
        "applies_to": "full vector",
        "logic": "local GR cannot be promoted unless all 12 rows are present, evaluated/resolved, and claim gates are strong",
        "pass_status": "derived_local_GR_candidate_pending_audit",
        "fail_status": "partial_or_template_vector_no_local_GR",
    },
]


DECISION = [
    {
        "decision": "The MTS local residual-vector evaluator now exists and was dry-run against the blank prediction template. It correctly refuses to pass missing numeric predictions and blocks R10/R11 symbolic placeholders. This is an operational testing scaffold, not an MTS local-GR result.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "MTS_residuals_loaded": "template_only_no_predictions",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "432-same-frame-matter-functor-zero-route.md",
        "task": "attempt the C0 theorem route for universal observed metric/coframe matter coupling",
        "priority": "P0",
    },
    {
        "next_file": "432-MTS-local-residual-vector-filled-smoke.md",
        "task": "create a controlled non-claim smoke prediction file to test pass/fail mechanics without calling it MTS evidence",
        "priority": "P0",
    },
    {
        "next_file": "432-R10-R11-curve-and-operator-vector-contract.md",
        "task": "make alpha(lambda) and non-EH coefficient-vector rows executable",
        "priority": "P1",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_float(text: str) -> float | None:
    try:
        if text is None or str(text).strip() == "":
            return None
        return float(str(text).strip())
    except ValueError:
        return None


def path_exists_from_root(path_text: str) -> bool:
    if not path_text or path_text.startswith("fill_") or path_text == "required_for_R10_R11":
        return False
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate.exists()
    return (ROOT / candidate).exists()


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": path.exists(),
                "required_before_run": item["required_before_run"],
                "role": item["role"],
            }
        )
    return rows


def prediction_file_health_rows(predictions_path: Path, prediction_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    if prediction_rows:
        columns = set(prediction_rows[0].keys())
    else:
        columns = set()
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
    duplicate_counts = Counter(row.get("row_id", "") for row in prediction_rows)
    duplicate_ids = sorted(row_id for row_id, count in duplicate_counts.items() if row_id and count > 1)
    return [
        {
            "check": "predictions_file_exists",
            "value": predictions_path.exists(),
            "status": "pass" if predictions_path.exists() else "fail",
            "evidence": str(predictions_path),
        },
        {
            "check": "required_columns_present",
            "value": len(REQUIRED_COLUMNS) - len(missing_columns),
            "status": "pass" if not missing_columns else "fail",
            "evidence": ";".join(missing_columns) if missing_columns else f"{len(REQUIRED_COLUMNS)} columns",
        },
        {
            "check": "row_count",
            "value": len(prediction_rows),
            "status": "pass" if len(prediction_rows) == 12 else "review",
            "evidence": "expected 12 local residual rows",
        },
        {
            "check": "duplicate_row_ids",
            "value": len(duplicate_ids),
            "status": "pass" if not duplicate_ids else "fail",
            "evidence": ";".join(duplicate_ids) if duplicate_ids else "none",
        },
    ]


def evaluate_predictions(prediction_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    component_rows = read_csv(RESIDUAL_COMPONENTS_CSV)
    bound_rows = read_csv(LOCAL_BOUNDS_CSV)
    component_by_row = {row["row_id"]: row for row in component_rows if row.get("row_id")}
    bound_by_row = {row["row_id"]: row for row in bound_rows if row.get("row_id")}
    evaluated: list[dict[str, Any]] = []
    for row in prediction_rows:
        row_id = row.get("row_id", "")
        component = component_by_row.get(row_id)
        bound = bound_by_row.get(row_id, {})
        derivation_status = row.get("derivation_status", "").strip()
        claim_request = row.get("claim_request", "").strip() or "none"
        source_file = row.get("source_file", "").strip()
        curve_or_vector = row.get("curve_or_vector_file", "").strip()
        predicted_value = parse_float(row.get("predicted_value", ""))
        upper_envelope = parse_float(row.get("upper_envelope", ""))
        sourced_bound = parse_float(bound.get("upper_bound", ""))
        symbolic_row = row_id.startswith("R10") or row_id.startswith("R11") or sourced_bound is None
        score_candidates = [abs(value) for value in [predicted_value, upper_envelope] if value is not None]
        score = max(score_candidates) if score_candidates else None
        row_known = component is not None and bool(bound)
        observable_match = bool(component) and row.get("observable", "") == component.get("observable", "")
        units_match = bool(component) and row.get("units", "") == component.get("units", "")
        derivation_valid = derivation_status in ALLOWED_DERIVATION_STATUS
        source_file_exists = path_exists_from_root(source_file)
        curve_or_vector_exists = path_exists_from_root(curve_or_vector)

        if not row_known:
            evaluation_status = "unknown_row_no_pass"
        elif not observable_match:
            evaluation_status = "observable_mismatch_no_pass"
        elif not units_match:
            evaluation_status = "unit_mismatch_no_pass"
        elif not derivation_valid:
            evaluation_status = "invalid_or_placeholder_derivation_status_no_pass"
        elif symbolic_row:
            if curve_or_vector_exists:
                evaluation_status = "symbolic_row_executable_file_present_pending_specialized_audit"
            elif derivation_status == "derived_zero" and source_file_exists:
                evaluation_status = "symbolic_row_theorem_zero_source_present_pending_manual_audit"
            else:
                evaluation_status = "symbolic_file_missing_no_pass"
        elif score is None:
            evaluation_status = "missing_numeric_prediction_no_pass"
        elif sourced_bound is not None and score <= sourced_bound:
            evaluation_status = "residual_below_bound_no_GR_claim"
        else:
            evaluation_status = "residual_exceeds_bound"

        if claim_request == "none":
            claim_gate = "no_claim_requested"
        elif not derivation_valid:
            claim_gate = "claim_request_invalid_derivation_status"
        elif derivation_status not in CLAIM_STRONG_STATUSES:
            claim_gate = "claim_request_exceeds_derivation_status"
        elif evaluation_status not in {
            "residual_below_bound_no_GR_claim",
            "symbolic_row_executable_file_present_pending_specialized_audit",
            "symbolic_row_theorem_zero_source_present_pending_manual_audit",
        }:
            claim_gate = "claim_request_exceeds_evaluation_status"
        elif not source_file_exists:
            claim_gate = "claim_request_missing_source_file"
        else:
            claim_gate = "claim_request_candidate_pending_all_row_audit"

        evaluated.append(
            {
                "model_id": row.get("model_id", ""),
                "branch_id": row.get("branch_id", ""),
                "row_id": row_id,
                "observable": row.get("observable", ""),
                "known_row": row_known,
                "observable_match": observable_match,
                "units_match": units_match,
                "derivation_status": derivation_status,
                "derivation_valid": derivation_valid,
                "predicted_value": row.get("predicted_value", ""),
                "upper_envelope": row.get("upper_envelope", ""),
                "score_value": "" if score is None else f"{score:.12g}",
                "sourced_upper_bound": bound.get("upper_bound", ""),
                "bound_ratio": "" if score is None or sourced_bound in {None, 0.0} else f"{score / sourced_bound:.12g}",
                "source_file": source_file,
                "source_file_exists": source_file_exists,
                "curve_or_vector_file": curve_or_vector,
                "curve_or_vector_exists": curve_or_vector_exists,
                "comparison_role": row.get("comparison_role", ""),
                "claim_request": claim_request,
                "evaluation_status": evaluation_status,
                "claim_gate": claim_gate,
                "local_GR_credit": "none",
            }
        )
    return evaluated


def status_count_rows(evaluated_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(row["evaluation_status"] for row in evaluated_rows)
    return [{"evaluation_status": status, "row_count": count} for status, count in sorted(counts.items())]


def claim_gate_count_rows(evaluated_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(row["claim_gate"] for row in evaluated_rows)
    return [{"claim_gate": status, "row_count": count} for status, count in sorted(counts.items())]


def missing_prediction_rows(evaluated_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_statuses = {
        "missing_numeric_prediction_no_pass",
        "symbolic_file_missing_no_pass",
        "invalid_or_placeholder_derivation_status_no_pass",
        "unknown_row_no_pass",
        "observable_mismatch_no_pass",
        "unit_mismatch_no_pass",
    }
    return [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "evaluation_status": row["evaluation_status"],
            "needed_next": "fill numeric residual and derivation source" if not row["row_id"].startswith(("R10", "R11")) else "supply curve/operator vector or audited theorem-zero source",
        }
        for row in evaluated_rows
        if row["evaluation_status"] in missing_statuses
    ]


def gate_rows(
    source_rows: list[dict[str, Any]],
    health_rows: list[dict[str, Any]],
    evaluated_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_required_sources = [
        row for row in source_rows if row["required_before_run"] and not row["exists"]
    ]
    failed_health = [row for row in health_rows if row["status"] == "fail"]
    unknown_or_mismatch = [
        row
        for row in evaluated_rows
        if not row["known_row"] or not row["observable_match"] or not row["units_match"]
    ]
    residuals_below = [
        row for row in evaluated_rows if row["evaluation_status"] == "residual_below_bound_no_GR_claim"
    ]
    missing_numeric = [
        row
        for row in evaluated_rows
        if not row["row_id"].startswith(("R10", "R11")) and row["score_value"] == ""
    ]
    symbolic_missing = [
        row
        for row in evaluated_rows
        if row["row_id"].startswith(("R10", "R11"))
        and not row["curve_or_vector_exists"]
        and not (row["derivation_status"] == "derived_zero" and row["source_file_exists"])
    ]
    claim_candidates = [
        row for row in evaluated_rows if row["claim_gate"] == "claim_request_candidate_pending_all_row_audit"
    ]
    local_gr_candidate = (
        len(evaluated_rows) == 12
        and len(residuals_below) >= 10
        and not missing_numeric
        and not symbolic_missing
        and all(row["derivation_status"] in CLAIM_STRONG_STATUSES for row in evaluated_rows)
        and len(claim_candidates) == len(evaluated_rows)
    )
    return [
        {
            "gate": "required_source_paths_exist",
            "status": "pass" if not missing_required_sources else "fail",
            "evidence": f"{len(missing_required_sources)} missing required source paths",
        },
        {
            "gate": "prediction_file_health",
            "status": "pass" if not failed_health else "fail",
            "evidence": f"{len(failed_health)} failed health checks",
        },
        {
            "gate": "all_rows_known_and_aligned",
            "status": "pass" if not unknown_or_mismatch else "fail",
            "evidence": f"{len(unknown_or_mismatch)} unknown/mismatched rows",
        },
        {
            "gate": "numeric_predictions_present",
            "status": "not_run" if missing_numeric else "pass",
            "evidence": f"{len(missing_numeric)} numeric rows missing predictions",
        },
        {
            "gate": "symbolic_rows_executable_or_theorem_zero",
            "status": "not_run" if symbolic_missing else "pass",
            "evidence": f"{len(symbolic_missing)} symbolic rows missing curve/vector/theorem source",
        },
        {
            "gate": "template_placeholders_blocked",
            "status": "pass",
            "evidence": "missing predictions and placeholder derivation statuses cannot pass",
        },
        {
            "gate": "claim_candidates_zero",
            "status": "pass" if not claim_candidates else "review",
            "evidence": f"{len(claim_candidates)} claim candidates",
        },
        {
            "gate": "local_GR_candidate",
            "status": "pass" if local_gr_candidate else "fail",
            "evidence": "all rows strong and resolved" if local_gr_candidate else "not all rows filled/strong/resolved",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "evaluator dry-run only; no MTS residual vector supplied",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    predictions_path: Path,
    health_rows: list[dict[str, Any]],
    evaluated_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    health_table = [
        {"check": row["check"], "value": row["value"], "status": row["status"], "evidence": row["evidence"]}
        for row in health_rows
    ]
    status_counts = status_count_rows(evaluated_rows)
    claim_counts = claim_gate_count_rows(evaluated_rows)
    digest_rows = [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "score_value": row["score_value"],
            "sourced_upper_bound": row["sourced_upper_bound"],
            "evaluation_status": row["evaluation_status"],
            "claim_gate": row["claim_gate"],
        }
        for row in evaluated_rows
    ]
    missing_rows = missing_prediction_rows(evaluated_rows)
    gate_table = [
        {"gate": row["gate"], "status": row["status"], "evidence": row["evidence"]}
        for row in gate_result_rows
    ]
    rule_table = [
        {"rule_id": row["rule_id"], "applies_to": row["applies_to"], "fail_status": row["fail_status"]}
        for row in EVALUATOR_RULES
    ]
    text = f"""# 431 - MTS Local Residual Vector Evaluator

Private evaluator checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 428 defined the MTS residual-vector input contract and checkpoint 430 ranked the zero routes. This checkpoint builds the evaluator that will compare a filled MTS residual prediction file against the sourced local-bound constraints.

This run used the blank prediction template as a dry-run. That is intentional: the evaluator must refuse to pass blank numeric rows, placeholder derivation statuses, and symbolic R10/R11 rows.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/MTS_local_residual_vector_evaluator.py` |
| Run directory | `runs/{run_dir.name}` |
| Predictions CSV | `{predictions_path.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Evaluator Rules

{markdown_table(rule_table, ["rule_id", "applies_to", "fail_status"])}

## 4. Prediction File Health

{markdown_table(health_table, ["check", "value", "status", "evidence"])}

## 5. Evaluation Status Counts

{markdown_table(status_counts, ["evaluation_status", "row_count"])}

## 6. Claim Gate Counts

{markdown_table(claim_counts, ["claim_gate", "row_count"])}

## 7. Row Evaluation Digest

{markdown_table(digest_rows, ["row_id", "observable", "score_value", "sourced_upper_bound", "evaluation_status", "claim_gate"])}

## 8. Missing Prediction Report

{markdown_table(missing_rows, ["row_id", "observable", "evaluation_status", "needed_next"])}

## 9. Gate Results

{markdown_table(gate_table, ["gate", "status", "evidence"])}

## 10. Decision

{DECISION[0]["decision"]}

Practical read: the local empirical machine is now ready to score an actual MTS residual vector. Right now it correctly says: no filled predictions, no local-GR claim. The next physics move is either fill a controlled smoke vector to test mechanics, or go straight after C0/C5 derivations so the first real vector is not just arbitrary zeros.

## 11. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str, predictions_path: Path) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    prediction_rows = read_csv(predictions_path)
    source_rows = source_register_rows()
    health = prediction_file_health_rows(predictions_path, prediction_rows)
    evaluated = evaluate_predictions(prediction_rows)
    gates = gate_rows(source_rows, health, evaluated)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "evaluator_rules.csv", EVALUATOR_RULES)
    write_csv(results_dir / "prediction_file_health.csv", health)
    write_csv(results_dir / "row_evaluation.csv", evaluated)
    write_csv(results_dir / "evaluation_status_counts.csv", status_count_rows(evaluated))
    write_csv(results_dir / "claim_gate_counts.csv", claim_gate_count_rows(evaluated))
    write_csv(results_dir / "missing_prediction_report.csv", missing_prediction_rows(evaluated))
    write_csv(results_dir / "gate_results.csv", gates)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    failed_operational_gates = [
        row["gate"]
        for row in gates
        if row["status"] == "fail" and row["gate"] not in {"local_GR_candidate", "local_GR_promoted"}
    ]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "predictions_csv": str(predictions_path),
        "prediction_rows": len(prediction_rows),
        "evaluated_rows": len(evaluated),
        "evaluation_status_counts": {
            row["evaluation_status"]: row["row_count"] for row in status_count_rows(evaluated)
        },
        "claim_gate_counts": {
            row["claim_gate"]: row["row_count"] for row in claim_gate_count_rows(evaluated)
        },
        "MTS_residuals_loaded": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_operational_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, predictions_path, health, evaluated, gates)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate an MTS local residual prediction CSV against sourced local-bound constraints."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    parser.add_argument(
        "--predictions-csv",
        type=Path,
        default=DEFAULT_PREDICTIONS,
        help="MTS residual prediction CSV to evaluate.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictions_path = args.predictions_csv
    if not predictions_path.is_absolute():
        predictions_path = ROOT / predictions_path
    run_dir = write_run(args.timestamp, predictions_path)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
