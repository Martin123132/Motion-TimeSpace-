from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "radial_bound_runner_dryrun_implemented_no_sourced_numeric_inputs_no_bound_claim_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "radial_bound_runner_dryrun_only_no_epsilon_radial_bound_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "503-fill-radial-bound-inputs-or-return-to-parent-glue.md"

DOC_PATH = Path("502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_SOURCE_REGISTER.csv")
FORMULA_MAP_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_FORMULA_MAP.csv")
INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv")
DRYRUN_RESULTS_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_DRYRUN_RESULTS.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_ACCEPTANCE_GATES.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_ROUTE_UPDATE.csv")

EQUALITY_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_INPUT_TEMPLATE.csv")
LOCAL_BOUNDS_PATH = Path("source-intake/local_bounds/local_bound_claims.csv")
P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
TOPO_HILBERT_EQUALITY_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv")
TOPO_HILBERT_OBSTRUCTION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv")


SOURCE_REGISTER = [
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "equality theorem failed and bound runner input template was selected",
    },
    {
        "source_file": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
        "role": "radial bound runner spec and no-cancellation policy",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "parent identity integral and source-channel decomposition",
    },
    {
        "source_file": str(EQUALITY_INPUT_TEMPLATE_PATH),
        "role": "501 equality residual input template",
    },
    {
        "source_file": str(LOCAL_BOUNDS_PATH),
        "role": "local empirical row locks for R3/R4/R9/R10/R11 mapping",
    },
    {
        "source_file": str(P8_TEMPLATE_PATH),
        "role": "P8 source-normalization residual template rows",
    },
    {
        "source_file": str(TOPO_HILBERT_EQUALITY_PATH),
        "role": "501 equality attempt rows",
    },
    {
        "source_file": str(TOPO_HILBERT_OBSTRUCTION_PATH),
        "role": "501 obstruction rows",
    },
    {
        "source_file": "scripts/radial_bound_runner_implementation_or_Hilbert_topological_glue.py",
        "role": "this checkpoint generator and dry-run scaffold",
    },
]


FORMULA_MAP_ROWS = [
    {
        "formula_id": "RB502_0_parent_integral",
        "quantity": "I_parent_radial_total",
        "formula": "I_parent_radial_total = I_R_eq + I_B_zero + sum_channel I_extra_channel + I_commutator + I_anomaly",
        "units_required": "same units as M_eff_ref/c_M",
        "maps_to": "epsilon_radial_Meff",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "RB502_1_epsilon",
        "quantity": "epsilon_radial_Meff",
        "formula": "epsilon_radial_Meff = c_M * I_parent_radial_total / M_eff_ref",
        "units_required": "dimensionless after normalization",
        "maps_to": "P8_radial_source_hair; R4; R10; R11",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "RB502_2_profile",
        "quantity": "dln_mu_dlnr",
        "formula": "dln_mu_dlnr = Delta ln(mu_obs) / Delta ln(r) or sourced profile derivative",
        "units_required": "dimensionless",
        "maps_to": "radial measured-GM profile and fifth-force/source-normalization rows",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "RB502_3_no_cancellation",
        "quantity": "channelwise_gate",
        "formula": "each nonzero channel must be below its own mapped row lock unless a theorem-zero certificate exists",
        "units_required": "row-specific",
        "maps_to": "no hidden cancellation between open residuals",
        "valid_for_claim": "false",
    },
]


INPUT_TEMPLATE_ROWS = [
    {
        "input_id": "IN502_0_R_eq",
        "system_id": "fill_system_id",
        "channel": "R_eq",
        "r1": "fill_r1",
        "r2": "fill_r2",
        "c_M": "fill_c_M",
        "M_eff_ref": "fill_M_eff_ref",
        "I_value": "fill_R_eq_integral",
        "I_units": "fill_units",
        "affected_rows": "R4;R11",
        "source_file": "fill_source_path",
        "assumptions": "fill_assumptions",
        "numeric_status": "missing",
        "valid_for_claim": "false",
    },
    {
        "input_id": "IN502_1_boundary",
        "system_id": "fill_system_id",
        "channel": "boundary_improvement_or_B_zero",
        "r1": "fill_r1",
        "r2": "fill_r2",
        "c_M": "fill_c_M",
        "M_eff_ref": "fill_M_eff_ref",
        "I_value": "fill_B_zero_or_boundary_flux",
        "I_units": "fill_units",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "source_file": "fill_source_path",
        "assumptions": "fill_assumptions",
        "numeric_status": "missing",
        "valid_for_claim": "false",
    },
    {
        "input_id": "IN502_2_extra_channel",
        "system_id": "fill_system_id",
        "channel": "boundary_domain_bulk_nonEH_kappa_frame_species",
        "r1": "fill_r1",
        "r2": "fill_r2",
        "c_M": "fill_c_M",
        "M_eff_ref": "fill_M_eff_ref",
        "I_value": "fill_channel_integral",
        "I_units": "fill_units",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "source_file": "fill_source_path",
        "assumptions": "fill_assumptions",
        "numeric_status": "missing",
        "valid_for_claim": "false",
    },
    {
        "input_id": "IN502_3_observed_profile",
        "system_id": "fill_system_id",
        "channel": "observed_radial_profile",
        "r1": "fill_r1",
        "r2": "fill_r2",
        "c_M": "not_applicable",
        "M_eff_ref": "not_applicable",
        "I_value": "fill_dln_mu_dlnr_or_profile_bound",
        "I_units": "dimensionless_or_profile_units",
        "affected_rows": "R4;R10;R11",
        "source_file": "fill_source_path",
        "assumptions": "fill_assumptions",
        "numeric_status": "missing",
        "valid_for_claim": "false",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "G502_0_units",
        "gate": "every numeric integral has declared compatible units and normalization",
        "required_for_claim": "true",
        "current_result": "fail_no_numeric_inputs",
        "claim_effect": "runner dry-run only",
    },
    {
        "gate_id": "G502_1_source_paths",
        "gate": "every numeric value has a source path or theorem certificate",
        "required_for_claim": "true",
        "current_result": "fail_no_numeric_inputs",
        "claim_effect": "no bound score",
    },
    {
        "gate_id": "G502_2_channelwise_no_cancellation",
        "gate": "each open residual channel is individually below its mapped bound or theorem-zero",
        "required_for_claim": "true",
        "current_result": "not_evaluated",
        "claim_effect": "prevents cancellation cheat",
    },
    {
        "gate_id": "G502_3_local_bound_mapping",
        "gate": "epsilon_radial_Meff maps to R4/R10/R11 and any boundary/domain rows map to their locks",
        "required_for_claim": "true",
        "current_result": "schema_written_not_scored",
        "claim_effect": "bound runner ready but no pass",
    },
    {
        "gate_id": "G502_4_no_promotion",
        "gate": "dry-run cannot promote source-normalized Newton or local GR",
        "required_for_claim": "true",
        "current_result": "pass_policy",
        "claim_effect": "local_GR_claim_allowed=false",
    },
]


DRYRUN_RESULT_ROWS = [
    {
        "result_id": "DR502_0",
        "run_status": "dryrun_blocked_no_sourced_numeric_inputs",
        "numeric_input_rows": "0",
        "computed_epsilon_radial_Meff": "not_computed",
        "computed_dln_mu_dlnr": "not_computed",
        "bound_decision": "not_scored",
        "reason": "template rows are missing placeholders; no source-backed residual values supplied",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D502_0_runner",
        "status": "implemented_dryrun_only",
        "meaning": "radial bound runner formulas, input template, dry-run result, and acceptance gates are written",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D502_1_bound",
        "status": "not_scored",
        "meaning": "no epsilon_radial_Meff or dln_mu_dlnr bound is computed because no sourced numeric inputs exist",
        "next_action": "fill inputs or return to parent glue theorem",
    },
    {
        "decision_id": "D502_2_promotion",
        "status": "forbidden",
        "meaning": "no equality theorem, radial bound, mu_extra zero, Newtonian recovery, PPN pass, or local-GR pass is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RADIAL_BOUND_FALLBACK",
        "previous_status": "equality_residual_input_template_written",
        "new_status": "dryrun_runner_implemented_no_numeric_inputs",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "TOPOLOGICAL_HILBERT_EQUALITY",
        "previous_status": "not_derived_parent_glue_missing",
        "new_status": "parallel_parent_glue_route_retained_but_no_new_theorem",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_parent_glue_calibration_and_second_order_source_stability",
        "new_status": "still_blocked_no_bound_score_no_parent_glue",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    return [{**row, "exists": str((ROOT / row["source_file"]).exists())} for row in SOURCE_REGISTER]


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    equality_template = read_csv(EQUALITY_INPUT_TEMPLATE_PATH)
    local_bounds = read_csv(LOCAL_BOUNDS_PATH)
    p8_template = read_csv(P8_TEMPLATE_PATH)
    equality_rows = read_csv(TOPO_HILBERT_EQUALITY_PATH)
    obstruction_rows = read_csv(TOPO_HILBERT_OBSTRUCTION_PATH)

    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_formula_rows = [row for row in FORMULA_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_input_rows = [row for row in INPUT_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    claim_dryrun_rows = [row for row in DRYRUN_RESULT_ROWS if row["valid_for_claim"] == "true"]
    required_rows = {"R4_beta", "R10_fifth_force", "R11_EH_operator_ledger"}
    local_bound_rows = {row.get("row_id", "") for row in local_bounds}

    return [
        {
            "rule_id": "V502_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V502_1_prior_inputs_loaded",
            "rule": "501 template, local bounds, P8 template, equality rows, and obstruction rows are loaded",
            "result": "pass" if equality_template and local_bounds and p8_template and equality_rows and obstruction_rows else "fail",
            "evidence": f"equality_template={len(equality_template)};local_bounds={len(local_bounds)};p8_template={len(p8_template)};equality_rows={len(equality_rows)};obstructions={len(obstruction_rows)}",
            "claim_effect": "runner tied to prior gates",
        },
        {
            "rule_id": "V502_2_formula_map_written",
            "rule": "formula map contains parent integral, epsilon, radial profile, and no-cancellation rows",
            "result": "pass" if len(FORMULA_MAP_ROWS) == 4 else "fail",
            "evidence": f"formula_rows={len(FORMULA_MAP_ROWS)}",
            "claim_effect": "runner equations explicit",
        },
        {
            "rule_id": "V502_3_input_template_written",
            "rule": "numeric input template contains equality, boundary, extra-channel, and observed-profile rows",
            "result": "pass" if len(INPUT_TEMPLATE_ROWS) == 4 else "fail",
            "evidence": f"input_template_rows={len(INPUT_TEMPLATE_ROWS)}",
            "claim_effect": "future source inputs structured",
        },
        {
            "rule_id": "V502_4_local_bound_mapping_available",
            "rule": "local bound table contains R4/R10/R11 rows needed for radial/source-normalization mapping",
            "result": "pass" if required_rows.issubset(local_bound_rows) else "fail",
            "evidence": ";".join(sorted(required_rows.intersection(local_bound_rows))),
            "claim_effect": "mapping available but not scored",
        },
        {
            "rule_id": "V502_5_no_false_claims",
            "rule": "no formula, input, or dry-run row is claim-valid",
            "result": "pass" if not claim_formula_rows and not claim_input_rows and not claim_dryrun_rows else "fail",
            "evidence": f"formula_claims={len(claim_formula_rows)};input_claims={len(claim_input_rows)};dryrun_claims={len(claim_dryrun_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 502 - Radial Bound Runner Implementation Or Hilbert Topological Glue

Private source-normalization runner checkpoint. This is not a public radial-bound result, closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `501` did not prove:

```text
Pi_M J_H = J_M_top.
```

So this checkpoint implements the fallback runner scaffold for:

```text
epsilon_radial_Meff = c_M I_parent_radial_total / M_eff_ref.
```

Short answer:

```text
The radial bound runner is implemented as a dry-run scaffold.
It writes formulas, input schema, acceptance gates, and a blocked dry-run result.
It refuses to score because no sourced numeric residual inputs exist yet.
No radial bound or local-GR promotion is made.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/radial_bound_runner_implementation_or_Hilbert_topological_glue.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Formula Map

{markdown_table(FORMULA_MAP_ROWS)}

## 5. Numeric Input Template

{markdown_table(INPUT_TEMPLATE_ROWS)}

## 6. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

## 7. Dry-Run Result

{markdown_table(DRYRUN_RESULT_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The radial bound runner scaffold is implemented and dry-run validated.
The runner has an explicit no-data/no-claim state.
```

Forbidden:

```text
MTS has computed a radial bound.
MTS has derived Pi_M J_H = J_M_top.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | either fill source-backed residual integrals for the runner, or derive the parent Hilbert/topological glue instead |
| 2 | source input audit | locate any existing numerical radial/source-normalization residual inputs before inventing none |
| 3 | calibration lock | even a passed radial bound would still need measured-GM/Poisson/Gauss and constant universal G |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-radial-bound-runner-implementation-or-Hilbert-topological-glue"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (FORMULA_MAP_PATH, FORMULA_MAP_ROWS),
        (INPUT_TEMPLATE_PATH, INPUT_TEMPLATE_ROWS),
        (DRYRUN_RESULTS_PATH, DRYRUN_RESULT_ROWS),
        (ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS),
        (VALIDATION_PATH, validations),
        (DECISION_PATH, DECISION_ROWS),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "formula_map": str(ROOT / FORMULA_MAP_PATH),
        "input_template": str(ROOT / INPUT_TEMPLATE_PATH),
        "dryrun_results": str(ROOT / DRYRUN_RESULTS_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "formula_rows": len(FORMULA_MAP_ROWS),
        "input_template_rows": len(INPUT_TEMPLATE_ROWS),
        "acceptance_gate_rows": len(ACCEPTANCE_GATE_ROWS),
        "dryrun_result_rows": len(DRYRUN_RESULT_ROWS),
        "failed_validation_rows": len(failed_validations),
        "radial_bound_runner_implemented": True,
        "radial_bound_runner_dryrun": True,
        "numeric_input_rows": 0,
        "epsilon_radial_Meff_computed": False,
        "dln_mu_dlnr_computed": False,
        "radial_bound_scored": False,
        "Hilbert_topological_current_equality_derived": False,
        "epsilon_radial_Meff_zero_derived": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
