from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_epsilon_charge_first_row_runner_written_inputs_missing_no_measured_GM_or_Newton_promotion"
CLAIM_CEILING = "epsilon_charge_first_row_runner_only_no_measured_GM_Newton_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md"

DOC_PATH = Path("533-Y5-epsilon-charge-first-row-runner-or-source-current-theorem.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RUNNER_SOURCE_REGISTER.csv")
NUMERIC_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_NUMERIC_INPUT_TEMPLATE.csv")
THEOREM_CERTIFICATE_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_THEOREM_CERTIFICATE_TEMPLATE.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv")
SCORECARD_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_SCORECARD_UPDATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RUNNER_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RUNNER_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RUNNER_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "role": "defines epsilon_charge theorem/input target",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "source-normalization scorecard with SRC523_0",
    },
    {
        "source_file": "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "role": "Ward bridge and projected-current obstruction",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M ownership and commutator route",
    },
    {
        "source_file": "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "role": "extra mass projection channels",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "role": "532 source-current closure rungs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_INPUT_TEMPLATE.csv",
        "role": "532 epsilon-charge input modes",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_FIRST_INPUT_FILL.csv",
        "role": "532 first-fill status",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RESIDUAL_DECOMPOSITION.csv",
        "role": "532 component decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "523 scorecard rows",
    },
    {
        "source_file": "scripts/Y5_epsilon_charge_first_row_runner_or_source_current_theorem.py",
        "role": "this checkpoint generator",
    },
]


NUMERIC_INPUT_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_local_source_normalized_branch",
        "branch_id": "Y5_epsilon_charge_first_row_runner",
        "row_id": "ECH533_0_current_branch_input",
        "Bxi_over_Geff": "MISSING_BXI_OVER_GEFF",
        "MH_PiMJH": "MISSING_MH_PIMJH",
        "epsilon_charge": "",
        "epsilon_charge_abs": "",
        "units": "dimensionless",
        "normalization": "(Bxi_over_Geff - MH_PiMJH)/MH_PiMJH",
        "bound_or_target": "derived_zero_or_below_source_normalization_lock",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_template",
        "assumptions": "MISSING_OBSERVED_TIME_PIM_SOURCE_CURRENT_NORMALIZATION_ASSUMPTIONS",
        "valid_for_claim": "false",
    },
    {
        "model_id": "GR_reference_not_MTS_evidence",
        "branch_id": "reference_only",
        "row_id": "ECH533_1_GR_reference",
        "Bxi_over_Geff": "1",
        "MH_PiMJH": "1",
        "epsilon_charge": "",
        "epsilon_charge_abs": "",
        "units": "dimensionless",
        "normalization": "reference equality only",
        "bound_or_target": "zero",
        "source_file": "reference_not_current_MTS_source",
        "derivation_status": "reference_only",
        "assumptions": "not claim evidence",
        "valid_for_claim": "false",
    },
]


THEOREM_CERTIFICATE_ROWS = [
    {
        "certificate_id": "ECT533_0_observed_time_charge",
        "rung_id": "SC532_0_observed_time_charge",
        "required_certificate": "source-backed observed-time Hamiltonian charge with normalized xi",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_1_Hilbert_source_current",
        "rung_id": "SC532_1_Hilbert_source_current",
        "required_certificate": "same-frame Hilbert/source current defined before orbital fitting",
        "current_status": "conditional_not_claim",
        "source_file": "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_2_charge_current_variation_identity",
        "rung_id": "SC532_2_charge_current_variation_identity",
        "required_certificate": "delta B_xi equals delta integral of Pi_M J_H and fixes absolute normalization",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_3_parent_owned_PiM",
        "rung_id": "SC532_3_parent_owned_PiM",
        "required_certificate": "Pi_M is parent-owned/topological/Hamiltonian charge projector, not readout mask",
        "current_status": "missing_certificate",
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_4_zero_projector_commutator",
        "rung_id": "SC532_4_zero_projector_commutator",
        "required_certificate": "[d,Pi_M]J_H=0 or bounded commutator integral",
        "current_status": "missing_certificate_or_bound",
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_5_zero_extra_projection",
        "rung_id": "SC532_5_zero_extra_projection",
        "required_certificate": "Pi_M dJ_extra=0 channelwise or all channels bounded",
        "current_status": "missing_certificate_or_channel_bounds",
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_6_absolute_normalization",
        "rung_id": "SC532_6_absolute_normalization",
        "required_certificate": "G_eff normalization is constant/universal/source-blind before measured-GM fitting",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "ECT533_7_no_downstream_closure_cheat",
        "rung_id": "SC532_7_measured_GM_next_gate",
        "required_certificate": "epsilon_charge is not advertised as measured GM before Poisson/Gauss/orbital rows close",
        "current_status": "policy_pass_no_claim",
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "valid_for_claim": "false",
    },
]


SCORECARD_UPDATE_ROWS = [
    {
        "score_id": "SRC523_0_charge_current_normalization",
        "previous_status": "unfilled",
        "runner_status": "epsilon_charge_runner_written",
        "current_value": "not_loaded",
        "score_status": "unfilled_missing_theorem_or_numeric_input",
        "valid_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
    {
        "score_id": "SRC523_11_total_no_cancellation_score",
        "previous_status": "not_run_preconditions_unfilled",
        "runner_status": "blocked_by_SRC523_0_unfilled",
        "current_value": "not_computed",
        "score_status": "not_run",
        "valid_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D533_0_runner_written",
        "status": "epsilon_charge_runner_written",
        "meaning": "the first source-normalization score row can now be evaluated from theorem or numeric input",
        "claim_status": "runner_only_no_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D533_1_current_inputs_missing",
        "status": "no_theorem_or_numeric_input_loaded",
        "meaning": "current MTS still has no claim-valid epsilon_charge certificate",
        "claim_status": "SRC523_0_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D533_2_best_next",
        "status": "attack_PiM_topological_equality_or_commutator_bound",
        "meaning": "the bottleneck inside epsilon_charge is Pi_M equality/commutator, not generic Ward conservation",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D533_3_no_promotion",
        "status": "no_measured_GM_Newton_beta_PPN_or_local_GR_promotion",
        "meaning": "the runner is infrastructure, not proof",
        "claim_status": "safe_private_work",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D533_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SRC523_0_EPSILON_CHARGE",
        "previous_status": "first_input_template_written_no_value_or_theorem_supplied",
        "new_status": "runner_written_inputs_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PIM_PROJECTOR",
        "previous_status": "central_premise_for_epsilon_charge_zero",
        "new_status": "next_target_topological_equality_or_commutator_bound",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_epsilon_charge_unfilled_plus_downstream_Gauss_orbital_rows",
        "new_status": "still_blocked_SRC523_0_runner_has_no_input",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_no_measured_GM_source_current_closure",
        "new_status": "still_blocked_first_source_score_row_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def parse_float(value: Any) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def source_exists(source_file: str) -> bool:
    if not source_file or source_file.startswith("MISSING") or source_file.startswith("reference"):
        return False
    return (ROOT / source_file).exists()


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evaluator_rows(input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in input_rows:
        bxi = parse_float(row.get("Bxi_over_Geff"))
        mh = parse_float(row.get("MH_PiMJH"))
        source_file = row.get("source_file", "")
        derivation_status = row.get("derivation_status", "")
        row_valid = row.get("valid_for_claim") == "true"
        if bxi is not None and mh not in (None, 0.0):
            epsilon = (bxi - mh) / mh
            epsilon_abs = abs(epsilon)
            numeric_status = "computed"
        else:
            epsilon = None
            epsilon_abs = None
            numeric_status = "not_computed_missing_numeric_inputs"

        theorem_zero = derivation_status == "derived_zero" and source_exists(source_file) and row_valid
        numeric_claim_ready = (
            numeric_status == "computed"
            and source_exists(source_file)
            and row_valid
            and row.get("units") == "dimensionless"
        )
        valid_for_claim = theorem_zero or numeric_claim_ready
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "row_id": row.get("row_id", ""),
                "Bxi_over_Geff": "" if bxi is None else bxi,
                "MH_PiMJH": "" if mh is None else mh,
                "epsilon_charge": "" if epsilon is None else epsilon,
                "epsilon_charge_abs": "" if epsilon_abs is None else epsilon_abs,
                "numeric_status": numeric_status,
                "source_file_exists": source_exists(source_file),
                "derivation_status": derivation_status,
                "current_status": "claim_ready" if valid_for_claim else "not_claimable",
                "valid_for_claim": str(valid_for_claim).lower(),
                "notes": "reference rows are never current MTS evidence" if derivation_status == "reference_only" else "requires theorem-zero or sourced numeric row",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    closure_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv"))
    input_modes = read_csv(Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_INPUT_TEMPLATE.csv"))
    first_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_FIRST_INPUT_FILL.csv"))
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    src523_0_rows = [row for row in scorecard if row.get("score_id") == "SRC523_0_charge_current_normalization"]
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    claim_cert_rows = [row for row in THEOREM_CERTIFICATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V533_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V533_1_532_inputs_loaded",
            "result": "pass" if len(closure_rows) == 8 and len(input_modes) == 3 and len(first_fill) == 3 else "fail",
            "detail": f"closure_rows={len(closure_rows)};input_modes={len(input_modes)};first_fill={len(first_fill)}",
        },
        {
            "check_id": "V533_2_SRC523_0_found",
            "result": "pass" if len(src523_0_rows) == 1 else "fail",
            "detail": f"SRC523_0_rows={len(src523_0_rows)}",
        },
        {
            "check_id": "V533_3_templates_written",
            "result": "pass" if len(NUMERIC_INPUT_TEMPLATE_ROWS) == 2 and len(THEOREM_CERTIFICATE_ROWS) == 8 else "fail",
            "detail": f"numeric_template_rows={len(NUMERIC_INPUT_TEMPLATE_ROWS)};theorem_certificate_rows={len(THEOREM_CERTIFICATE_ROWS)}",
        },
        {
            "check_id": "V533_4_evaluator_written",
            "result": "pass" if len(evaluator) == 2 else "fail",
            "detail": f"evaluator_rows={len(evaluator)}",
        },
        {
            "check_id": "V533_5_no_claim_rows",
            "result": "pass" if not claim_eval_rows and not claim_cert_rows else "fail",
            "detail": f"claim_eval_rows={len(claim_eval_rows)};claim_cert_rows={len(claim_cert_rows)}",
        },
        {
            "check_id": "V533_6_scorecard_update_written",
            "result": "pass" if len(SCORECARD_UPDATE_ROWS) == 2 else "fail",
            "detail": f"scorecard_update_rows={len(SCORECARD_UPDATE_ROWS)}",
        },
        {
            "check_id": "V533_7_no_overclaim",
            "result": "pass" if not claim_eval_rows and not claim_cert_rows else "fail",
            "detail": "epsilon_charge_filled=false; measured_GM_derived=false; Newton_derived=false; local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    evaluator: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 533 - Y5 Epsilon-Charge First Row Runner or Source-Current Theorem

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The first source-normalization row now has a runner.

It evaluates:

```text
epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H[Pi_M J_H].
```

Current MTS still has no theorem-zero certificate and no numeric source row. The GR reference row computes to zero, but it is reference-only and earns no MTS claim credit.

## 2. Numeric Input Template

{markdown_table(NUMERIC_INPUT_TEMPLATE_ROWS)}

## 3. Theorem Certificate Template

{markdown_table(THEOREM_CERTIFICATE_ROWS)}

## 4. Evaluator

{markdown_table(evaluator)}

## 5. Scorecard Update

{markdown_table(SCORECARD_UPDATE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The epsilon_charge runner exists.
Current MTS has no claim-valid epsilon_charge input.
Pi_M equality/commutator is the next bottleneck.
```

Forbidden:

```text
MTS has filled epsilon_charge.
MTS has derived measured GM or source-normalized Newton.
MTS has derived beta, PPN, or local GR.
```

## 11. Practical Read

This is the right engineering shape. The first Newton row is now a gauge: feed it a real parent theorem or a real numeric residual and it moves; feed it placeholders and it refuses to move. No drama, no hand-waving, just the machine saying "prove it or bound it."

## 12. Next Target

`{NEXT_TARGET}`

Next: attack `Pi_M` equality and the commutator. If `Pi_M` can be made topological/parent-owned and equal to the Hilbert source current, `epsilon_charge` has a real zero route. If not, the commutator bound becomes the honest residual branch.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-epsilon-charge-first-row-runner-or-source-current-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator = evaluator_rows(NUMERIC_INPUT_TEMPLATE_ROWS)
    validations = validation_rows(sources, evaluator)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (NUMERIC_INPUT_TEMPLATE_PATH, NUMERIC_INPUT_TEMPLATE_ROWS),
        (THEOREM_CERTIFICATE_TEMPLATE_PATH, THEOREM_CERTIFICATE_ROWS),
        (EVALUATOR_PATH, evaluator),
        (SCORECARD_UPDATE_PATH, SCORECARD_UPDATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, evaluator, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "numeric_input_template": str(ROOT / NUMERIC_INPUT_TEMPLATE_PATH),
        "theorem_certificate_template": str(ROOT / THEOREM_CERTIFICATE_TEMPLATE_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "scorecard_update": str(ROOT / SCORECARD_UPDATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "numeric_input_rows": len(NUMERIC_INPUT_TEMPLATE_ROWS),
        "theorem_certificate_rows": len(THEOREM_CERTIFICATE_ROWS),
        "evaluator_rows": len(evaluator),
        "claim_eval_rows": len(claim_eval_rows),
        "epsilon_charge_runner_written": True,
        "epsilon_charge_filled": False,
        "source_current_closure_derived_for_MTS": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nno_measured_GM_Newton_beta_PPN_or_local_GR_promotion\n", encoding="utf-8"
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
