from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v4-real-data-interface"
CHECKPOINT_DOC = "411-local-bound-runner-v4-real-data-interface.md"
STATUS = "local_bound_runner_v4_real_data_interface_written_schema_command_manifest_and_dryrun_guardrails_no_data_claim_no_local_GR_pass"
CLAIM_CEILING = "local_bound_runner_v4_real_data_interface_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "412-v4-source-charge-channel-map-review.md"


SOURCE_DOCS = [
    {
        "path": "406-local-runner-v4-derived-vs-closure-queue.md",
        "role": "runner-v4 state matrix and promotion rules",
    },
    {
        "path": "408-local-bound-data-runner-v4-smoke.md",
        "role": "runner-v4 smoke evaluator and local-bound profile semantics",
    },
    {
        "path": "409-runner-v4-red-team.md",
        "role": "false-promotion and baseline-fairness audit",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "R0 remains closure_zero after quotient-matter functor attempt",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv",
        "role": "row-channel map used by local-bound evaluator",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "machine-readable runner-v4 row states",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/row_bound_pressure.csv",
        "role": "machine-readable tightest source-lock map",
    },
    {
        "path": "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/profile_summary.csv",
        "role": "machine-readable smoke profile outcomes",
    },
    {
        "path": "runs/20260602-054500-runner-v4-red-team/results/false_promotion_routes.csv",
        "role": "machine-readable anti-promotion checks",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/row_transition_attempt.csv",
        "role": "machine-readable 410 row-transition result",
    },
]


REQUIRED_BOUNDS_COLUMNS = [
    "dataset_id",
    "test_arena",
    "row_id",
    "observable",
    "measured_value",
    "one_sigma",
    "upper_bound",
    "units",
    "confidence_label",
    "baseline_model",
    "reference_path_or_url",
    "reference_note",
]


LOCAL_DATA_TARGETS = [
    {
        "target_id": "WEP_differential_acceleration",
        "test_arena": "MICROSCOPE/Eotvos/composition",
        "row_id": "R0_identity_coframe_direct",
        "observable": "eta_WEP_direct_geometry",
        "input_quantity": "upper bound on composition-independent direct geometry slip contribution",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "closure control only unless theorem-zero proof is supplied",
    },
    {
        "target_id": "WEP_source_charge",
        "test_arena": "MICROSCOPE/Eotvos/composition",
        "row_id": "R1_WEP_source_charge",
        "observable": "eta_WEP_source_charge",
        "input_quantity": "upper bound or fitted value for species/source charge split",
        "interface_status": "ready_for_bound_csv_channel_review_needed",
        "claim_role": "retained contingent budget",
    },
    {
        "target_id": "clock_redshift",
        "test_arena": "redshift/clocks",
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "input_quantity": "redshift violation parameter or clock-drift bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "Shapiro_gamma",
        "test_arena": "Cassini/VLBI/solar-system light propagation",
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "input_quantity": "PPN gamma minus one bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "perihelion_beta",
        "test_arena": "planetary ephemerides/LLR",
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "input_quantity": "PPN beta minus one bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "preferred_frame_alpha1",
        "test_arena": "pulsar/solar-system preferred-frame",
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "input_quantity": "alpha1 bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "preferred_frame_alpha2",
        "test_arena": "solar-spin/pulsar preferred-frame",
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "input_quantity": "alpha2 bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "self_acceleration_alpha3",
        "test_arena": "pulsar/solar-system momentum flux",
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "input_quantity": "alpha3 or momentum-flux bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained contingent budget",
    },
    {
        "target_id": "preferred_location_xi",
        "test_arena": "local anisotropy/preferred-location",
        "row_id": "R8_xi",
        "observable": "xi",
        "input_quantity": "xi/preferred-location bound",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained budget",
    },
    {
        "target_id": "Gdot_over_G",
        "test_arena": "LLR/ephemerides/pulsars",
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "input_quantity": "secular Gdot/G bound per year",
        "interface_status": "ready_for_bound_csv",
        "claim_role": "retained contingent budget",
    },
    {
        "target_id": "inverse_square_yukawa",
        "test_arena": "fifth-force/inverse-square",
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "input_quantity": "alpha(lambda), source charge, range, and screening curve",
        "interface_status": "symbolic_curve_required_not_scalar_claim",
        "claim_role": "unscored parameterized",
    },
    {
        "target_id": "non_EH_operator_ledger",
        "test_arena": "local operator closure",
        "row_id": "R11_EH_operator_ledger",
        "observable": "non_EH_operator_coefficients",
        "input_quantity": "operator coefficient ledger or theorem-zero derivation source",
        "interface_status": "symbolic_ledger_required_not_scalar_claim",
        "claim_role": "retained residual",
    },
]


INTERFACE_CONTRACT = [
    {
        "contract_item": "dry_run_first",
        "requirement": "script must run without external data and write schema/template/status/log/results",
        "status": "implemented",
    },
    {
        "contract_item": "bounds_csv_schema",
        "requirement": "external data must arrive as explicit row-level bound entries with references",
        "status": "implemented",
    },
    {
        "contract_item": "runner_row_validation",
        "requirement": "every data row must map to a known runner-v4 row_id",
        "status": "implemented",
    },
    {
        "contract_item": "state_semantics_preserved",
        "requirement": "data strength can be evaluated but cannot set theorem_credit_allowed or claim_allowed",
        "status": "implemented",
    },
    {
        "contract_item": "log_status_done_protocol",
        "requirement": "future VS Code runs write log.txt, status.json, results/*.csv, and DONE.txt",
        "status": "implemented",
    },
    {
        "contract_item": "symbolic_rows_protected",
        "requirement": "fifth-force curves and non-EH ledgers cannot be flattened into scalar passes",
        "status": "implemented",
    },
]


COMMAND_MANIFEST = [
    {
        "command_id": "dry_run",
        "purpose": "create schema, template, target map, and guardrail outputs without external data",
        "powershell_command": "$py = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\.venv-score\\Scripts\\python.exe'; $pc = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\\local_bound_runner_v4_real_data_interface.py') --mode dry-run",
        "wait_policy": "safe_short_run",
    },
    {
        "command_id": "evaluate_bounds_csv",
        "purpose": "evaluate a user-provided local-bound CSV against runner-v4 source locks",
        "powershell_command": "$py = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\.venv-score\\Scripts\\python.exe'; $pc = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\\local_bound_runner_v4_real_data_interface.py') --mode evaluate --bounds-csv (Join-Path $pc 'source-intake\\local_bounds\\local_bound_claims.csv')",
        "wait_policy": "run_in_VS_Code_then_prompt_Codex_after_DONE",
    },
    {
        "command_id": "long_run_status_check",
        "purpose": "check whether a future local-bound evaluation has finished without making Codex wait",
        "powershell_command": "Get-ChildItem 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\runs' -Directory | Sort-Object Name -Descending | Select-Object -First 1 | ForEach-Object { Get-ChildItem $_.FullName }",
        "wait_policy": "manual_status_check",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Runner-v4 now has a real-data interface contract. The interface names the local-bound targets, writes the required bounds CSV schema, produces a fillable template, validates row IDs against runner-v4, compares supplied numeric bounds to internal source locks where meaningful, and writes log/status/results/DONE artifacts for VS Code runs. It does not claim a local-GR pass, does not promote closure_zero to theorem_zero, and protects fifth-force/operator rows from being flattened into scalar evidence.",
        "interface_ready": True,
        "external_bounds_loaded": False,
        "theorem_credit_rows": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "review whether the R1 source-charge stress map should count three or four active channels",
        "pass_condition": "source-charge channel count is documented before relying on real WEP data",
    },
    {
        "priority": 2,
        "target": "413-no-marker-parent-action-theorem-attempt.md",
        "task": "try to derive the no-marker theorem needed by the quotient-matter route",
        "pass_condition": "marker extension is either forbidden or explicitly retained as closure",
    },
    {
        "priority": 3,
        "target": "414-local-bounds-data-intake-first-pass.md",
        "task": "fill the local-bound CSV from verified local-bound sources and run the evaluator",
        "pass_condition": "real data rows evaluate with references and no claim leaks",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def runner_rows_by_id() -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in runner_v4_rows()}


def row_bound_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/row_bound_pressure.csv")


def source_locks_by_row() -> dict[str, dict[str, str]]:
    rows_by_id: dict[str, dict[str, str]] = {}
    for row in runner_v4_rows():
        rows_by_id[row["row_id"]] = row
    return rows_by_id


def schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "column": column,
            "required": True,
            "meaning": {
                "dataset_id": "stable dataset/test identifier",
                "test_arena": "human-readable experiment or bound class",
                "row_id": "runner-v4 row ID",
                "observable": "observable constrained by the data row",
                "measured_value": "central value if available, else blank",
                "one_sigma": "1 sigma uncertainty if available, else blank",
                "upper_bound": "absolute upper bound used by the evaluator",
                "units": "units for measured_value/one_sigma/upper_bound",
                "confidence_label": "confidence level or fit label",
                "baseline_model": "GR/PPN/null/comparison model used by the source",
                "reference_path_or_url": "local file path, DOI, URL, or corpus source",
                "reference_note": "short provenance note",
            }[column],
        }
        for column in REQUIRED_BOUNDS_COLUMNS
    ]


def local_bounds_template_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    locks = source_locks_by_row()
    for target in LOCAL_DATA_TARGETS:
        lock = locks.get(target["row_id"], {})
        rows.append(
            {
                "dataset_id": target["target_id"],
                "test_arena": target["test_arena"],
                "row_id": target["row_id"],
                "observable": target["observable"],
                "measured_value": "",
                "one_sigma": "",
                "upper_bound": lock.get("source_lock", ""),
                "units": lock.get("source_lock_units", ""),
                "confidence_label": "template_internal_lock_not_external_data",
                "baseline_model": "runner_v4_internal_source_lock",
                "reference_path_or_url": "replace_with_verified_source",
                "reference_note": "template row only; replace upper_bound before empirical use",
            }
        )
    return rows


def target_map_rows() -> list[dict[str, Any]]:
    runner_rows = runner_rows_by_id()
    bound_pressure = {row["row_id"]: row for row in row_bound_rows()}
    rows: list[dict[str, Any]] = []
    for target in LOCAL_DATA_TARGETS:
        runner_row = runner_rows.get(target["row_id"], {})
        pressure_row = bound_pressure.get(target["row_id"], {})
        rows.append(
            {
                "target_id": target["target_id"],
                "test_arena": target["test_arena"],
                "row_id": target["row_id"],
                "observable": target["observable"],
                "runner_v4_state": runner_row.get("runner_v4_state", "missing"),
                "zero_kind": runner_row.get("zero_kind", "missing"),
                "source_lock": runner_row.get("source_lock", "missing"),
                "source_lock_units": runner_row.get("source_lock_units", "missing"),
                "tightest_channel": pressure_row.get("tightest_channel", "missing"),
                "interface_status": target["interface_status"],
                "claim_role": target["claim_role"],
                "claim_allowed": False,
                "theorem_credit_allowed": False,
            }
        )
    return rows


def parse_float(text: str) -> float | None:
    try:
        if text.strip() == "":
            return None
        return float(text)
    except ValueError:
        return None


def evaluate_bounds_csv(bounds_csv: Path | None) -> tuple[list[dict[str, Any]], list[str], bool]:
    if bounds_csv is None:
        return [], [], False
    if not bounds_csv.exists():
        return [], [f"bounds_csv_missing:{bounds_csv}"], False

    rows = read_csv(bounds_csv)
    missing_columns = [column for column in REQUIRED_BOUNDS_COLUMNS if rows and column not in rows[0]]
    if missing_columns:
        return [], [f"bounds_csv_missing_columns:{';'.join(missing_columns)}"], True

    runner_rows = runner_rows_by_id()
    evaluation_rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, row in enumerate(rows, start=2):
        row_id = row.get("row_id", "")
        runner_row = runner_rows.get(row_id)
        if runner_row is None:
            errors.append(f"line_{index}_unknown_row_id:{row_id}")
            continue
        upper_bound = parse_float(row.get("upper_bound", ""))
        source_lock = parse_float(runner_row.get("source_lock", ""))
        runner_state = runner_row.get("runner_v4_state", "")
        if runner_state in {"unscored_parameterized", "retained_residual"}:
            data_bound_status = "symbolic_or_curve_input_recorded_no_scalar_pass"
            ratio = ""
        elif upper_bound is None or source_lock is None:
            data_bound_status = "missing_numeric_bound_or_source_lock"
            ratio = ""
        else:
            ratio_value = upper_bound / source_lock if source_lock != 0.0 else float("inf")
            ratio = f"{ratio_value:.12g}"
            data_bound_status = (
                "external_bound_at_or_stronger_than_internal_lock_no_claim"
                if upper_bound <= source_lock
                else "external_bound_weaker_than_internal_lock_no_claim"
            )
        evaluation_rows.append(
            {
                "dataset_id": row.get("dataset_id", ""),
                "test_arena": row.get("test_arena", ""),
                "row_id": row_id,
                "observable": row.get("observable", runner_row.get("observable", "")),
                "runner_v4_state": runner_state,
                "zero_kind": runner_row.get("zero_kind", ""),
                "upper_bound": row.get("upper_bound", ""),
                "upper_bound_units": row.get("units", ""),
                "source_lock": runner_row.get("source_lock", ""),
                "source_lock_units": runner_row.get("source_lock_units", ""),
                "bound_to_source_lock_ratio": ratio,
                "data_bound_status": data_bound_status,
                "reference_path_or_url": row.get("reference_path_or_url", ""),
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return evaluation_rows, errors, True


def interface_summary_rows(
    target_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    errors: list[str],
    external_bounds_loaded: bool,
) -> list[dict[str, Any]]:
    return [
        {
            "summary_item": "targets_mapped",
            "value": len(target_rows),
            "status": "pass" if all(row["runner_v4_state"] != "missing" for row in target_rows) else "fail",
        },
        {
            "summary_item": "schema_columns",
            "value": len(REQUIRED_BOUNDS_COLUMNS),
            "status": "pass",
        },
        {
            "summary_item": "external_bounds_loaded",
            "value": external_bounds_loaded,
            "status": "pass" if external_bounds_loaded else "dry_run_no_external_data",
        },
        {
            "summary_item": "external_rows_evaluated",
            "value": len(evaluation_rows),
            "status": "pass" if external_bounds_loaded and evaluation_rows else "dry_run_or_empty",
        },
        {
            "summary_item": "evaluation_errors",
            "value": len(errors),
            "status": "pass" if not errors else "fail",
        },
        {
            "summary_item": "claim_allowed_rows",
            "value": sum(1 for row in evaluation_rows if row["claim_allowed"]),
            "status": "pass",
        },
        {
            "summary_item": "theorem_credit_rows",
            "value": sum(1 for row in evaluation_rows if row["theorem_credit_allowed"]),
            "status": "pass",
        },
    ]


def gate_rows(
    source_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    errors: list[str],
    external_bounds_loaded: bool,
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    missing_targets = [row["row_id"] for row in target_rows if row["runner_v4_state"] == "missing"]
    claim_rows = [row for row in target_rows + evaluation_rows if row["claim_allowed"]]
    theorem_rows = [row for row in target_rows + evaluation_rows if row["theorem_credit_allowed"]]
    closure_target = next(row for row in target_rows if row["row_id"] == "R0_identity_coframe_direct")
    symbolic_targets = [
        row
        for row in target_rows
        if row["runner_v4_state"] in {"unscored_parameterized", "retained_residual"}
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "interface_schema_written",
            "status": "pass",
            "evidence": f"{len(REQUIRED_BOUNDS_COLUMNS)} required CSV columns",
        },
        {
            "gate": "local_targets_mapped_to_runner_rows",
            "status": "pass" if not missing_targets else "fail",
            "evidence": f"{len(target_rows) - len(missing_targets)} of {len(target_rows)} targets mapped",
        },
        {
            "gate": "dry_run_template_written",
            "status": "pass",
            "evidence": f"{len(LOCAL_DATA_TARGETS)} template rows generated",
        },
        {
            "gate": "external_bounds_loaded",
            "status": "pass" if external_bounds_loaded else "dry_run_pass",
            "evidence": f"{len(evaluation_rows)} external rows evaluated" if external_bounds_loaded else "no external data requested in dry-run",
        },
        {
            "gate": "evaluation_errors",
            "status": "pass" if not errors else "fail",
            "evidence": ";".join(errors) if errors else "0 validation errors",
        },
        {
            "gate": "closure_zero_not_promoted",
            "status": "pass" if closure_target["zero_kind"] == "closure_zero_not_theorem_zero" else "fail",
            "evidence": f"R0 state={closure_target['runner_v4_state']} zero_kind={closure_target['zero_kind']}",
        },
        {
            "gate": "symbolic_rows_protected",
            "status": "pass" if len(symbolic_targets) >= 2 else "fail",
            "evidence": f"{len(symbolic_targets)} symbolic/unscored targets retained",
        },
        {
            "gate": "no_theorem_credit_or_claim_leaks",
            "status": "pass" if not theorem_rows and not claim_rows else "fail",
            "evidence": f"theorem_credit={len(theorem_rows)} claim_allowed={len(claim_rows)}",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "real-data interface only; no EH/Newton/PPN/local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    target_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    target_table_rows = [
        {
            "target": row["target_id"],
            "row": row["row_id"],
            "state": row["runner_v4_state"],
            "source_lock": row["source_lock"],
            "status": row["interface_status"],
        }
        for row in target_rows
    ]
    summary_table_rows = [
        {
            "item": row["summary_item"],
            "value": row["value"],
            "status": row["status"],
        }
        for row in summary_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    command_table_rows = [
        {
            "command": row["command_id"],
            "purpose": row["purpose"],
            "wait_policy": row["wait_policy"],
        }
        for row in COMMAND_MANIFEST
    ]
    text = f"""# 411 - Local-Bound Runner-v4 Real-Data Interface

Private local-bound interface checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 410 left `R0` as closure-zero, not theorem-zero. This checkpoint makes the next empirical step safer: real local-bound data can now be attached to runner-v4 rows without changing row states, awarding theorem credit, or letting a closure branch masquerade as GR.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_real_data_interface.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Interface Contract

The bounds CSV must contain these columns:

```text
{", ".join(REQUIRED_BOUNDS_COLUMNS)}
```

The script writes `log.txt`, `status.json`, `DONE.txt`, and machine-readable CSVs under `results/`. Future long runs should be started from VS Code, left to finish, and then this chat can be prompted after the completion marker appears.

## 4. Local Data Targets

{markdown_table(target_table_rows, ["target", "row", "state", "source_lock", "status"])}

## 5. Command Manifest

{markdown_table(command_table_rows, ["command", "purpose", "wait_policy"])}

## 6. Interface Summary

{markdown_table(summary_table_rows, ["item", "value", "status"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: this is how we stop Python from being the final boss. The interface is boring on purpose: verified data in, row-level pressure out, no accidental victory lap.

## 9. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_log(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run(timestamp: str, mode: str, bounds_csv: Path | None) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    run_dir.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"started_at_utc={datetime.now(timezone.utc).isoformat()}",
        f"mode={mode}",
        f"bounds_csv={bounds_csv if bounds_csv is not None else ''}",
        "claim_policy=no theorem credit and no local-GR claim from this interface",
    ]
    source_rows = source_register_rows()
    target_rows = target_map_rows()
    evaluation_rows, errors, external_bounds_loaded = evaluate_bounds_csv(bounds_csv if mode == "evaluate" else None)
    summary_rows = interface_summary_rows(target_rows, evaluation_rows, errors, external_bounds_loaded)
    gate_result_rows = gate_rows(source_rows, target_rows, evaluation_rows, errors, external_bounds_loaded)
    log_lines.extend(
        [
            f"targets_mapped={len(target_rows)}",
            f"external_bounds_loaded={external_bounds_loaded}",
            f"external_rows_evaluated={len(evaluation_rows)}",
            f"errors={len(errors)}",
        ]
    )

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "interface_schema.csv", schema_rows())
    write_csv(results_dir / "local_bounds_template.csv", local_bounds_template_rows())
    write_csv(results_dir / "local_data_targets.csv", target_rows)
    write_csv(results_dir / "interface_contract.csv", INTERFACE_CONTRACT)
    write_csv(results_dir / "command_manifest.csv", COMMAND_MANIFEST)
    write_csv(results_dir / "external_bound_evaluation.csv", evaluation_rows)
    write_csv(results_dir / "interface_summary.csv", summary_rows)
    write_csv(results_dir / "validation_errors.csv", [{"error": error} for error in errors])
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "mode": mode,
        "bounds_csv": str(bounds_csv) if bounds_csv is not None else "",
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "local_data_targets": len(target_rows),
        "schema_columns": len(REQUIRED_BOUNDS_COLUMNS),
        "external_bounds_loaded": external_bounds_loaded,
        "external_rows_evaluated": len(evaluation_rows),
        "validation_errors": len(errors),
        "theorem_credit_rows": 0,
        "claim_allowed_rows": 0,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    write_log(run_dir / "log.txt", log_lines)
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, target_rows, summary_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 411 local-bound runner-v4 real-data interface artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "evaluate"],
        default="dry-run",
        help="Dry-run writes schema/template only; evaluate reads --bounds-csv.",
    )
    parser.add_argument(
        "--bounds-csv",
        type=Path,
        default=None,
        help="Optional bounds CSV matching results/interface_schema.csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp, args.mode, args.bounds_csv)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
