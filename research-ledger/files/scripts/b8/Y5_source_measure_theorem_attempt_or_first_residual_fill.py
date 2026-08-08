from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_source_measure_theorem_attempt_conditional_current_MTS_not_closed_first_boundary_residual_template_written"
CLAIM_CEILING = "conditional_source_measure_theorem_and_first_residual_template_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md"

DOC_PATH = Path("542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv")
GATE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_HSM541_GATE_UPDATE.csv")
FIRST_RESIDUAL_INPUT_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv")
FIRST_RESIDUAL_EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_EVALUATOR.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "source-measure contract and residual scorecard",
    },
    {
        "source_file": "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
        "role": "source-measure, Gauss, and PPN gate tests",
    },
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian Pi_M candidate branch",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "EH-style worldtube source-measure theorem route and residual runner",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional parent Noether charge closure theorem",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Hilbert worldtube glue and C-term leakage ledger",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Hamiltonian charge to measured orbital GM calibration gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "role": "541 source-measure contract rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
        "role": "541 source-measure scorecard rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
        "role": "541 residual input specifications",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "510 M_eff residual runner rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv",
        "role": "505 C-term ledger",
    },
    {
        "source_file": "scripts/Y5_source_measure_theorem_attempt_or_first_residual_fill.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_ATTEMPT_ROWS = [
    {
        "theorem_id": "SMT542_0_conditional_statement",
        "target": "source-measure theorem for Hamiltonian Pi_M branch",
        "mathematical_form": "If HSM541_1,HSM541_2,HSM541_3 pass, then M_source[W]=H_tau[S]-H_ref is radially stable and equals the Pi_M^H charge at source-measure level",
        "derived_part": "conditional implication follows from covariant phase-space charge plus Stokes theorem",
        "current_MTS_gap": "premises not parent-derived",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "SMT542_1_integrable_charge",
        "target": "HSM541_1_integrable_charge",
        "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta), with fixed tau and fixed reference",
        "derived_part": "formal covariant-phase-space identity if parent action, boundary term, and reference are supplied",
        "current_MTS_gap": "fixed reference and boundary/symplectic terms are not derived for current MTS",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "SMT542_2_observed_worldtube_source",
        "target": "HSM541_2_observed_worldtube_source",
        "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref before orbital fitting",
        "derived_part": "definition is coherent and matches the GR-style dressed source charge guardrail",
        "current_MTS_gap": "same observed frame/source support theorem not derived",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "SMT542_3_radial_closure",
        "target": "HSM541_3_radial_closure",
        "mathematical_form": "int_S2 Q_tau - int_S1 Q_tau = int_A(C_EH+C_extra+C_projector+C_boundary)",
        "derived_part": "zero follows conditionally if all C terms vanish",
        "current_MTS_gap": "C_extra, C_projector, and C_boundary remain open",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "SMT542_4_first_residual_trigger",
        "target": "HSI541_0_boundary_reference",
        "mathematical_form": "epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref",
        "derived_part": "first failed theorem component has an executable residual envelope",
        "current_MTS_gap": "no source-backed B_zero_flux/Delta_symp row exists",
        "valid_for_claim": "false",
    },
]


GATE_UPDATE_ROWS = [
    {
        "contract_id": "HSM541_1_integrable_charge",
        "before_542": "fail_current_claim",
        "after_542": "conditional_theorem_identity_only",
        "residual_activated": "HSI541_0_boundary_reference",
        "next_artifact": "boundary/reference theorem or source-backed first residual row",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_2_observed_worldtube_source",
        "before_542": "fail_current_claim",
        "after_542": "definition_guardrail_retained_not_derived",
        "residual_activated": "HSI541_1_worldtube_frame",
        "next_artifact": "same-frame worldtube theorem or frame/calibration residual row",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_3_radial_closure",
        "before_542": "fail_current_claim",
        "after_542": "conditional_zero_if_C_terms_vanish",
        "residual_activated": "HSI541_2_radial_mass_closure",
        "next_artifact": "C-term zero theorem or radial mass residual row",
        "valid_for_claim": "false",
    },
]


FIRST_RESIDUAL_INPUT_ROWS = [
    {
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "surface_pair": "S_inner_to_S_outer",
        "B_zero_flux": "MISSING_B_ZERO_FLUX",
        "Delta_symp": "MISSING_DELTA_SYMP",
        "M_H_ref": "MISSING_M_H_REF",
        "epsilon_boundary_reference_abs": "",
        "units": "dimensionless_after_dividing_by_M_H_ref",
        "source_file": "MISSING_SOURCE_FILE",
        "assumptions": "MISSING_FIXED_REFERENCE_BOUNDARY_SYMPLECTIC_ASSUMPTIONS",
        "derivation_status": "unfilled_template",
        "valid_for_claim": "false",
    },
    {
        "system_id": "reference_zero_not_MTS_evidence",
        "surface_pair": "reference_only",
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
        "decision_id": "D542_0_conditional_theorem_written",
        "status": "source_measure_conditional_theorem_attempt_written",
        "meaning": "HSM541_1-HSM541_3 are sufficient in principle, but current MTS has not derived them",
        "claim_status": "conditional_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D542_1_first_residual_template_written",
        "status": "boundary_reference_first_residual_template_written",
        "meaning": "failure of integrable charge/reference gate now has an evaluator rather than vague closure",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D542_2_no_promotion",
        "status": "no_measured_GM_Newton_or_local_GR_promotion",
        "meaning": "source-measure theorem did not close for current MTS and the first residual row is unfilled",
        "claim_status": "safe_private_work",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D542_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "contract_scorecard_written_all_claim_gates_open",
        "new_status": "conditional_theorem_attempt_written_current_MTS_not_closed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BOUNDARY_REFERENCE_RESIDUAL",
        "previous_status": "HSI541_0_not_filled",
        "new_status": "template_and_evaluator_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_HSS541_0_to_HSS541_6",
        "new_status": "still_blocked_HSM541_1_to_HSM541_3_not_closed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_contract_scorecard_unfilled",
        "new_status": "still_blocked_source_measure_and_PPN_followthrough",
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


def first_residual_evaluator_rows(input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
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
                "surface_pair": row.get("surface_pair", ""),
                "epsilon_boundary_reference_abs": "" if epsilon is None else epsilon,
                "numeric_status": numeric_status,
                "source_file_exists": source_exists(row.get("source_file", "")),
                "current_status": "claim_ready" if valid_for_claim else "not_claimable",
                "valid_for_claim": str(valid_for_claim).lower(),
                "notes": "reference-only zero is not MTS evidence" if row.get("derivation_status") == "reference_only" else "requires sourced boundary/reference row or theorem zero",
            }
        )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    evaluator: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"))
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv"))
    residual_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv"))
    c_terms = read_csv(Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv"))
    claim_theorem_rows = [row for row in THEOREM_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_gate_rows = [row for row in GATE_UPDATE_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V542_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V542_1_prior_541_loaded",
            "result": "pass" if len(contract) == 8 and len(scorecard) == 8 and len(residual_inputs) == 7 else "fail",
            "detail": f"contract_rows={len(contract)};scorecard_rows={len(scorecard)};residual_input_rows={len(residual_inputs)}",
        },
        {
            "check_id": "V542_2_C_term_ledger_loaded",
            "result": "pass" if len(c_terms) >= 4 else "fail",
            "detail": f"C_term_rows={len(c_terms)}",
        },
        {
            "check_id": "V542_3_theorem_attempt_targets_first_three_gates",
            "result": "pass" if len(THEOREM_ATTEMPT_ROWS) == 5 and len(GATE_UPDATE_ROWS) == 3 else "fail",
            "detail": f"theorem_rows={len(THEOREM_ATTEMPT_ROWS)};gate_update_rows={len(GATE_UPDATE_ROWS)}",
        },
        {
            "check_id": "V542_4_first_residual_evaluator_written",
            "result": "pass" if len(FIRST_RESIDUAL_INPUT_ROWS) == 2 and len(evaluator) == 2 else "fail",
            "detail": f"input_rows={len(FIRST_RESIDUAL_INPUT_ROWS)};evaluator_rows={len(evaluator)}",
        },
        {
            "check_id": "V542_5_no_claim_rows",
            "result": "pass" if not claim_theorem_rows and not claim_gate_rows and not claim_eval_rows else "fail",
            "detail": f"claim_theorem_rows={len(claim_theorem_rows)};claim_gate_rows={len(claim_gate_rows)};claim_eval_rows={len(claim_eval_rows)}",
        },
        {
            "check_id": "V542_6_no_overclaim",
            "result": "pass" if not claim_theorem_rows and not claim_gate_rows and not claim_eval_rows else "fail",
            "detail": "source_measure_theorem_derived=false; first_residual_claim_filled=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 542 - Y5 Source-Measure Theorem Attempt or First Residual Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The source-measure theorem route works only conditionally.

The theorem shape is clean:

```text
integrable Hamiltonian charge
+ same observed Hilbert worldtube source
+ zero exterior C-terms
=> dressed source charge is radially stable and source-measure compatible.
```

Current MTS has not derived the first three gates. Therefore no measured-GM/Newton/PPN/local-GR promotion is allowed.

The fallback is now executable at the first failure point:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref.
```

The row is still unfilled; that is good discipline, not a failure.

## 2. Theorem Attempt

{markdown_table(THEOREM_ATTEMPT_ROWS)}

## 3. HSM541 Gate Update

{markdown_table(GATE_UPDATE_ROWS)}

## 4. First Residual Input

{markdown_table(FIRST_RESIDUAL_INPUT_ROWS)}

## 5. First Residual Evaluator

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
MTS has a conditional source-measure theorem shape.
MTS has an executable first boundary/reference residual template and evaluator.
```

Forbidden:

```text
MTS has derived the source-measure theorem for current MTS.
MTS has filled the first residual with claim-valid data.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is exactly the right sort of boring machinery. If the boundary/reference theorem lands, the first row can go theorem-zero. If it does not, the row becomes a measured residual with units and a source path. Either way, no magic mass words.

## 12. Next Target

`{NEXT_TARGET}`

Next: attack the boundary/reference residual directly. Either prove `B_zero_flux=Delta_symp=0` for the Hamiltonian `Pi_M` branch, or fill the first row with source-backed values.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-source-measure-theorem-attempt-or-first-residual-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator = first_residual_evaluator_rows(FIRST_RESIDUAL_INPUT_ROWS)
    validations = validation_rows(sources, evaluator)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_ATTEMPT_PATH, THEOREM_ATTEMPT_ROWS),
        (GATE_UPDATE_PATH, GATE_UPDATE_ROWS),
        (FIRST_RESIDUAL_INPUT_PATH, FIRST_RESIDUAL_INPUT_ROWS),
        (FIRST_RESIDUAL_EVALUATOR_PATH, evaluator),
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
        "gate_update": str(ROOT / GATE_UPDATE_PATH),
        "first_residual_input": str(ROOT / FIRST_RESIDUAL_INPUT_PATH),
        "first_residual_evaluator": str(ROOT / FIRST_RESIDUAL_EVALUATOR_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "theorem_attempt_rows": len(THEOREM_ATTEMPT_ROWS),
        "gate_update_rows": len(GATE_UPDATE_ROWS),
        "first_residual_input_rows": len(FIRST_RESIDUAL_INPUT_ROWS),
        "first_residual_evaluator_rows": len(evaluator),
        "claim_eval_rows": len(claim_eval_rows),
        "source_measure_theorem_derived": False,
        "first_boundary_reference_residual_claim_filled": False,
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
        "done\nprivate_no_github\nconditional_source_measure_only_first_residual_template_no_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
