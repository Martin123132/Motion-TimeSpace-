from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_boundary_reference_zero_theorem_attempt_failed_for_current_MTS_first_residual_fill_pack_written"
CLAIM_CEILING = "boundary_reference_residual_fill_pack_only_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md"

DOC_PATH = Path("543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_ZERO_THEOREM_ATTEMPT.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv")
FILL_PACK_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_EVALUATOR.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
        "role": "source-measure theorem attempt and first residual evaluator",
    },
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "source-measure contract and residual scorecard",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue and boundary/reference requirements",
    },
    {
        "source_file": "456-PiM-projector-variation-stress-ledger.md",
        "role": "projector variation stress and boundary-only no-hair warning",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "boundary no-flux shortcut rejection and tensor/vector flux warning",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "boundary/R11 stress theorem stack and closure fill pack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv",
        "role": "542 first residual input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_EVALUATOR.csv",
        "role": "542 first residual evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "Pi_M projector variation/stress contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv",
        "role": "local-zero boundary/R11 implication audit",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv",
        "role": "R11 boundary stress theorem stack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv",
        "role": "boundary/R11 closure fill pack",
    },
    {
        "source_file": "scripts/Y5_boundary_reference_residual_theorem_or_fill_first_row.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_ATTEMPT_ROWS = [
    {
        "theorem_id": "BRT543_0_fixed_reference",
        "required_zero": "fixed reference subtraction carries no source-dependent compact flux",
        "mathematical_form": "Delta_symp_ref=0 or constant_global with partial_t,r,A,lambda,frame=0",
        "current_result": "not_derived",
        "why_not_enough": "reference choice and Hamiltonian boundary subtraction are not fixed for current MTS",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "BRT543_1_exact_boundary_zero",
        "required_zero": "exact/improvement term has zero linked-surface flux",
        "mathematical_form": "int_boundary dB_zero=0",
        "current_result": "not_derived",
        "why_not_enough": "exact term can still carry finite boundary monopole unless class/reference theorem is supplied",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "BRT543_2_boundary_no_hair",
        "required_zero": "boundary stress is class-only scalar monopole or zero",
        "mathematical_form": "T_boundary_tracefree=T_boundary_vector=partial_r T_boundary=partial_t T_boundary=0",
        "current_result": "not_derived",
        "why_not_enough": "485 showed scalar volume no-flux does not kill vector/tensor boundary flux",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "BRT543_3_projector_variation_silence",
        "required_zero": "Pi_M variation creates no metric/projector boundary stress",
        "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H and (delta Pi_M)J_H=0/topological or retained",
        "current_result": "not_derived",
        "why_not_enough": "456 keeps Hodge/metric/domain projector stress retained unless proved topological",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "BRT543_4_first_row_theorem_zero",
        "required_zero": "first residual envelope vanishes",
        "mathematical_form": "epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref=0",
        "current_result": "not_derived",
        "why_not_enough": "both numerator terms remain missing for current branch",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "BRO543_0_reference_shift",
        "obstruction": "Hamiltonian reference subtraction can shift the measured monopole",
        "observable_risk": "absolute mass/source normalization offset or radial drift",
        "repair": "fixed reference theorem or source-backed Delta_symp row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BRO543_1_boundary_improvement_flux",
        "obstruction": "exact/improvement term can carry compact boundary flux",
        "observable_risk": "B_zero_flux contributes to epsilon_boundary_reference_abs",
        "repair": "zero linked-surface flux theorem or source-backed B_zero_flux row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BRO543_2_vector_tensor_boundary_hair",
        "obstruction": "scalar/trace no-flux does not kill vector, shear, preferred-frame, radial, or time hair",
        "observable_risk": "alpha_i/xi/source-normalization residuals survive",
        "repair": "boundary scalar-only no-hair theorem or coefficient vector",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BRO543_3_projector_stress",
        "obstruction": "metric-dependent Pi_M variation can induce boundary or bulk stress",
        "observable_risk": "projector stress shifts Newton/PPN despite charge-map notation",
        "repair": "topological Pi_M variation-zero theorem or retained stress map",
        "valid_for_claim": "false",
    },
]


FILL_PACK_ROWS = [
    {
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "residual_id": "BRF543_0_boundary_reference_current",
        "surface_pair": "S_inner_to_S_outer",
        "boundary_type": "Hamiltonian_reference_and_exact_improvement",
        "B_zero_flux": "MISSING_B_ZERO_FLUX",
        "Delta_symp": "MISSING_DELTA_SYMP",
        "M_H_ref": "MISSING_M_H_REF",
        "epsilon_boundary_reference_abs": "",
        "units": "dimensionless_after_dividing_by_M_H_ref",
        "source_file": "MISSING_SOURCE_FILE",
        "assumptions": "MISSING_FIXED_REFERENCE_NO_HAIR_PROJECTOR_VARIATION_ASSUMPTIONS",
        "derivation_status": "unfilled_template",
        "valid_for_claim": "false",
    },
    {
        "system_id": "reference_zero_not_MTS_evidence",
        "residual_id": "BRF543_1_reference_zero",
        "surface_pair": "reference_only",
        "boundary_type": "reference_only",
        "B_zero_flux": "0",
        "Delta_symp": "0",
        "M_H_ref": "1",
        "epsilon_boundary_reference_abs": "",
        "units": "dimensionless_after_dividing_by_M_H_ref",
        "source_file": "reference_not_current_MTS_source",
        "assumptions": "reference only",
        "derivation_status": "reference_only",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D543_0_zero_theorem_failed_current_claim",
        "status": "boundary_reference_zero_not_derived",
        "meaning": "current MTS has no theorem proving B_zero_flux=Delta_symp=0",
        "claim_status": "source_measure_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D543_1_fill_pack_written",
        "status": "first_boundary_reference_fill_pack_written",
        "meaning": "the first source-measure residual row is now explicit and evaluable",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D543_2_no_shortcut",
        "status": "scalar_no_flux_and_topological_labels_not_enough",
        "meaning": "boundary and projector stress need their own zero theorem or residual data",
        "claim_status": "Newton_PPN_local_GR_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D543_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BOUNDARY_REFERENCE_ZERO",
        "previous_status": "template_and_evaluator_written",
        "new_status": "zero_theorem_attempt_failed_current_claim_fill_pack_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "conditional_theorem_attempt_written_current_MTS_not_closed",
        "new_status": "still_blocked_by_boundary_reference_first_row",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_HSM541_1_to_HSM541_3_not_closed",
        "new_status": "still_blocked_boundary_reference_residual_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_source_measure_and_PPN_followthrough",
        "new_status": "still_blocked_source_measure_first_residual_and_PPN",
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
        if str(value).strip() == "":
            return None
        return float(str(value))
    except (TypeError, ValueError):
        return None


def source_exists(source_file: str) -> bool:
    if not source_file or "MISSING" in source_file or source_file.startswith("reference"):
        return False
    return (ROOT / source_file).exists()


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def evaluator_rows(input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in input_rows:
        b_flux = parse_float(row.get("B_zero_flux"))
        delta_symp = parse_float(row.get("Delta_symp"))
        mass_ref = parse_float(row.get("M_H_ref"))
        has_numbers = b_flux is not None and delta_symp is not None and mass_ref not in (None, 0.0)
        if has_numbers:
            epsilon = (abs(b_flux) + abs(delta_symp)) / mass_ref
            numeric_status = "computed"
        else:
            epsilon = None
            numeric_status = "not_computed_missing_numeric_inputs"
        row_valid = row.get("valid_for_claim") == "true"
        valid_for_claim = (
            has_numbers
            and row_valid
            and source_exists(row.get("source_file", ""))
            and row.get("units") == "dimensionless_after_dividing_by_M_H_ref"
        )
        rows.append(
            {
                "system_id": row.get("system_id", ""),
                "residual_id": row.get("residual_id", ""),
                "epsilon_boundary_reference_abs": "" if epsilon is None else epsilon,
                "numeric_status": numeric_status,
                "source_file_exists": source_exists(row.get("source_file", "")),
                "current_status": "claim_ready" if valid_for_claim else "not_claimable",
                "valid_for_claim": str(valid_for_claim).lower(),
                "notes": "reference-only zero is not MTS evidence" if row.get("derivation_status") == "reference_only" else "requires theorem zero or source-backed boundary/reference row",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_input = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv"))
    prior_eval = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_EVALUATOR.csv"))
    projector_contract = read_csv(Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"))
    boundary_audit = read_csv(Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv"))
    boundary_pack = read_csv(Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"))
    claim_theorem_rows = [row for row in THEOREM_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_obstruction_rows = [row for row in OBSTRUCTION_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V543_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V543_1_prior_542_loaded",
            "result": "pass" if len(prior_input) == 2 and len(prior_eval) == 2 else "fail",
            "detail": f"prior_input_rows={len(prior_input)};prior_eval_rows={len(prior_eval)}",
        },
        {
            "check_id": "V543_2_boundary_projector_evidence_loaded",
            "result": "pass" if len(projector_contract) >= 8 and len(boundary_audit) >= 6 and len(boundary_pack) >= 4 else "fail",
            "detail": f"projector_rows={len(projector_contract)};boundary_audit_rows={len(boundary_audit)};boundary_pack_rows={len(boundary_pack)}",
        },
        {
            "check_id": "V543_3_theorem_and_obstruction_rows_complete",
            "result": "pass" if len(THEOREM_ATTEMPT_ROWS) == 5 and len(OBSTRUCTION_ROWS) == 4 else "fail",
            "detail": f"theorem_rows={len(THEOREM_ATTEMPT_ROWS)};obstruction_rows={len(OBSTRUCTION_ROWS)}",
        },
        {
            "check_id": "V543_4_fill_pack_and_evaluator_written",
            "result": "pass" if len(FILL_PACK_ROWS) == 2 and len(evaluator) == 2 else "fail",
            "detail": f"fill_pack_rows={len(FILL_PACK_ROWS)};evaluator_rows={len(evaluator)}",
        },
        {
            "check_id": "V543_5_no_claim_rows",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_eval_rows else "fail",
            "detail": f"claim_theorem_rows={len(claim_theorem_rows)};claim_obstruction_rows={len(claim_obstruction_rows)};claim_eval_rows={len(claim_eval_rows)}",
        },
        {
            "check_id": "V543_6_no_overclaim",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_eval_rows else "fail",
            "detail": "boundary_reference_zero_derived=false; first_residual_claim_filled=false; source_measure=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 543 - Y5 Boundary Reference Residual Theorem or Fill First Row

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The boundary/reference zero theorem does not close for current MTS.

The required zero is:

```text
B_zero_flux = 0
Delta_symp = 0
```

but the existing evidence says scalar no-flux, topological labels, and on-shell local-zero statements are not enough. Boundary vector/tensor hair, reference shifts, and projector variation stress remain independent debts.

So the first row remains residual-fill, not theorem-zero.

## 2. Zero-Theorem Attempt

{markdown_table(THEOREM_ATTEMPT_ROWS)}

## 3. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 4. First Row Fill Pack

{markdown_table(FILL_PACK_ROWS)}

## 5. Evaluator

{markdown_table(evaluator)}

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
MTS has attempted the boundary/reference zero theorem.
MTS has an explicit first-row boundary/reference fill pack and evaluator.
```

Forbidden:

```text
MTS has proved B_zero_flux=Delta_symp=0.
MTS has filled the first residual row with claim-valid data.
MTS has derived source-measure glue, measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is not a loss; it is us refusing a cheap win. A serious GR reduction cannot let boundary terms or projector stress vanish by vibes. The next door is either a real boundary/reference theorem or a real first-row input.

## 12. Next Target

`{NEXT_TARGET}`

Next: provide theorem-zero evidence or source-backed values for `B_zero_flux`, `Delta_symp`, and `M_H_ref` in the first row.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-boundary-reference-residual-theorem-or-fill-first-row"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator = evaluator_rows(FILL_PACK_ROWS)
    validations = validation_rows(sources, evaluator)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_ATTEMPT_PATH, THEOREM_ATTEMPT_ROWS),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_ROWS),
        (FILL_PACK_PATH, FILL_PACK_ROWS),
        (EVALUATOR_PATH, evaluator),
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
        "theorem_attempt": str(ROOT / THEOREM_ATTEMPT_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "fill_pack": str(ROOT / FILL_PACK_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "theorem_rows": len(THEOREM_ATTEMPT_ROWS),
        "obstruction_rows": len(OBSTRUCTION_ROWS),
        "fill_pack_rows": len(FILL_PACK_ROWS),
        "evaluator_rows": len(evaluator),
        "claim_eval_rows": len(claim_eval_rows),
        "boundary_reference_zero_derived": False,
        "first_boundary_reference_residual_claim_filled": False,
        "source_measure_theorem_derived": False,
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
        "done\nprivate_no_github\nboundary_reference_fill_pack_only_no_source_measure_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
