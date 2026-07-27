from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_PiM_commutator_bound_runner_written_no_numeric_inputs_no_epsilon_charge_or_Newton_promotion"
CLAIM_CEILING = "PiM_commutator_bound_runner_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md"

DOC_PATH = Path("535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_RUNNER_SOURCE_REGISTER.csv")
NUMERIC_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv")
WORLDTUBE_GLUE_CERTIFICATE_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv")
SCORECARD_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_SCORECARD_UPDATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_RUNNER_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_RUNNER_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_RUNNER_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md",
        "role": "Pi_M equality certificate and commutator template",
    },
    {
        "source_file": "533-Y5-epsilon-charge-first-row-runner-or-source-current-theorem.md",
        "role": "epsilon_charge runner fed by Pi_M equality/commutator rows",
    },
    {
        "source_file": "502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md",
        "role": "older broad radial runner pattern",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "Hilbert/topological equality theorem attempt",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M commutator and radial bound inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
        "role": "534 commutator/equality bound template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_TO_EPSILON_CHARGE_MAP.csv",
        "role": "534 Pi_M to epsilon_charge map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv",
        "role": "533 epsilon_charge evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "role": "501 Hilbert equality rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv",
        "role": "502 broad radial runner numeric input template",
    },
    {
        "source_file": "scripts/Y5_PiM_commutator_bound_runner_or_Hilbert_worldtube_glue.py",
        "role": "this checkpoint generator",
    },
]


NUMERIC_INPUT_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_local_source_normalized_branch",
        "branch_id": "Y5_PiM_commutator_bound_runner",
        "row_id": "PCR535_0_current_branch",
        "R_eq_integral": "MISSING_R_EQ_INTEGRAL",
        "I_commutator": "MISSING_I_COMMUTATOR",
        "B_zero_flux": "MISSING_B_ZERO_FLUX",
        "projector_stress_beta_equiv": "MISSING_PROJECTOR_STRESS_MAP",
        "M_H_ref": "MISSING_M_H_REF",
        "epsilon_PiM_equality": "",
        "epsilon_commutator": "",
        "epsilon_boundary_exact": "",
        "epsilon_projector_stress": "",
        "epsilon_PiM_total_abs": "",
        "units": "dimensionless_after_normalization",
        "source_file": "MISSING_SOURCE_FILE",
        "assumptions": "MISSING_WORLDTUBE_PIM_TOPOLOGY_COMMUTATOR_ASSUMPTIONS",
        "derivation_status": "unfilled_template",
        "valid_for_claim": "false",
    },
    {
        "model_id": "PiM_topological_equality_reference_not_MTS_evidence",
        "branch_id": "reference_only",
        "row_id": "PCR535_1_reference_zero",
        "R_eq_integral": "0",
        "I_commutator": "0",
        "B_zero_flux": "0",
        "projector_stress_beta_equiv": "0",
        "M_H_ref": "1",
        "epsilon_PiM_equality": "",
        "epsilon_commutator": "",
        "epsilon_boundary_exact": "",
        "epsilon_projector_stress": "",
        "epsilon_PiM_total_abs": "",
        "units": "dimensionless_after_normalization",
        "source_file": "reference_not_current_MTS_source",
        "assumptions": "reference only",
        "derivation_status": "reference_only",
        "valid_for_claim": "false",
    },
]


WORLDTUBE_GLUE_CERTIFICATE_ROWS = [
    {
        "certificate_id": "HWG535_0_worldtube_fixed_before_readout",
        "required_identity": "compact Hilbert source worldtube is selected by parent structure before orbital readout",
        "math_form": "W_source subset M fixed by parent source/support/topology, not by fitted mu_obs",
        "current_status": "missing_certificate",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "HWG535_1_source_measure_owned",
        "required_identity": "the measure used to define Q_M is the same observed Hilbert source measure",
        "math_form": "Q_M=int_W rho_H dV_H with dV_H owned by e_obs/source variation",
        "current_status": "missing_certificate",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "HWG535_2_topological_representative_matches_worldtube_boundary",
        "required_identity": "omega_M_top represents the boundary class of the same Hilbert source worldtube",
        "math_form": "int_boundary(W_source) omega_M_top=1 and no independent topological label",
        "current_status": "missing_certificate",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "HWG535_3_exact_term_zero",
        "required_identity": "the exact difference term has zero compact boundary integral",
        "math_form": "Pi_M J_H-J_M_top=dB_zero and int_boundary dB_zero=0",
        "current_status": "missing_certificate_or_bound",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "HWG535_4_commutator_zero",
        "required_identity": "the parent Pi_M is fixed/covariantly constant on the Hilbert current space",
        "math_form": "[d,Pi_M]J_H=0",
        "current_status": "missing_certificate_or_bound",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "HWG535_5_no_projector_stress",
        "required_identity": "projector variation stress is absent/topological or mapped below local locks",
        "math_form": "T_PiM_munu=0 or source-backed residual vector below locks",
        "current_status": "missing_certificate_or_map",
        "valid_for_claim": "false",
    },
]


SCORECARD_UPDATE_ROWS = [
    {
        "score_id": "SRC523_0_charge_current_normalization",
        "component": "epsilon_PiM_equality;epsilon_commutator;epsilon_boundary_exact;epsilon_projector_stress",
        "runner_status": "PiM_commutator_runner_written_no_inputs",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
    {
        "score_id": "SRC523_6_Meff_flux_derivative",
        "component": "epsilon_commutator",
        "runner_status": "commutator_integral_template_written",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
    {
        "score_id": "SRC523_8_radial_source_hair",
        "component": "I_commutator and R_eq radial contribution",
        "runner_status": "maps_to_radial_source_hair_but_no_numeric_profile",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D535_0_runner_written",
        "status": "PiM_commutator_bound_runner_written",
        "meaning": "Pi_M equality, commutator, boundary exact term, and projector-stress components can now be evaluated together",
        "claim_status": "runner_only_no_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D535_1_current_inputs_missing",
        "status": "no_sourced_numeric_or_theorem_inputs",
        "meaning": "current MTS still has no claim-valid Pi_M equality/commutator input",
        "claim_status": "epsilon_charge_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D535_2_parent_route",
        "status": "Hilbert_worldtube_glue_certificate_written",
        "meaning": "the theorem route is now specifically the Hilbert worldtube/source-measure glue, not generic topology",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D535_3_no_promotion",
        "status": "no_epsilon_charge_measured_GM_Newton_or_local_GR_promotion",
        "meaning": "the runner is executable infrastructure only",
        "claim_status": "safe_private_work",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D535_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PIM_COMMUTATOR_BOUND",
        "previous_status": "topological_equality_certificate_written_commutator_bound_template_active",
        "new_status": "runner_written_no_numeric_inputs",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HILBERT_WORLDTUBE_GLUE",
        "previous_status": "worldtube_Hilbert_glue_missing",
        "new_status": "certificate_written_as_next_theorem_target",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SRC523_0_EPSILON_CHARGE",
        "previous_status": "still_blocked_by_PiM_equality_and_commutator_inputs",
        "new_status": "still_blocked_PiM_runner_has_no_claim_input",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_PiM_certificate_or_bound_unfilled",
        "new_status": "still_blocked_no_PiM_bound_or_worldtube_glue",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_measured_GM_source_current_PiM_gate",
        "new_status": "still_blocked_first_source_current_row_unfilled",
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
        r_eq = parse_float(row.get("R_eq_integral"))
        commutator = parse_float(row.get("I_commutator"))
        boundary = parse_float(row.get("B_zero_flux"))
        stress = parse_float(row.get("projector_stress_beta_equiv"))
        mass_ref = parse_float(row.get("M_H_ref"))
        source_file = row.get("source_file", "")
        has_mass = mass_ref not in (None, 0.0)
        if has_mass and all(value is not None for value in [r_eq, commutator, boundary, stress]):
            epsilon_eq = r_eq / mass_ref
            epsilon_comm = commutator / mass_ref
            epsilon_boundary = boundary / mass_ref
            epsilon_stress = stress
            total_abs = abs(epsilon_eq) + abs(epsilon_comm) + abs(epsilon_boundary) + abs(epsilon_stress)
            numeric_status = "computed"
        else:
            epsilon_eq = None
            epsilon_comm = None
            epsilon_boundary = None
            epsilon_stress = None
            total_abs = None
            numeric_status = "not_computed_missing_numeric_inputs"
        row_valid = row.get("valid_for_claim") == "true"
        valid_for_claim = (
            numeric_status == "computed"
            and row_valid
            and source_exists(source_file)
            and row.get("units") == "dimensionless_after_normalization"
        )
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "row_id": row.get("row_id", ""),
                "epsilon_PiM_equality": "" if epsilon_eq is None else epsilon_eq,
                "epsilon_commutator": "" if epsilon_comm is None else epsilon_comm,
                "epsilon_boundary_exact": "" if epsilon_boundary is None else epsilon_boundary,
                "epsilon_projector_stress": "" if epsilon_stress is None else epsilon_stress,
                "epsilon_PiM_total_abs": "" if total_abs is None else total_abs,
                "numeric_status": numeric_status,
                "source_file_exists": source_exists(source_file),
                "current_status": "claim_ready" if valid_for_claim else "not_claimable",
                "valid_for_claim": str(valid_for_claim).lower(),
                "notes": "reference-only zero is not MTS evidence" if row.get("derivation_status") == "reference_only" else "requires sourced numeric row or theorem certificate",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    template = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv"))
    pmap = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_TO_EPSILON_CHARGE_MAP.csv"))
    epsilon_eval = read_csv(Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv"))
    hilbert = read_csv(Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv"))
    broad_runner = read_csv(Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv"))
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    claim_cert_rows = [row for row in WORLDTUBE_GLUE_CERTIFICATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V535_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V535_1_534_templates_loaded",
            "result": "pass" if len(template) == 5 and len(pmap) == 5 else "fail",
            "detail": f"comm_template_rows={len(template)};epsilon_map_rows={len(pmap)}",
        },
        {
            "check_id": "V535_2_prior_runners_loaded",
            "result": "pass" if len(epsilon_eval) >= 2 and len(broad_runner) >= 4 else "fail",
            "detail": f"epsilon_eval_rows={len(epsilon_eval)};broad_runner_rows={len(broad_runner)}",
        },
        {
            "check_id": "V535_3_Hilbert_equality_rows_loaded",
            "result": "pass" if len(hilbert) >= 6 else "fail",
            "detail": f"hilbert_eq_rows={len(hilbert)}",
        },
        {
            "check_id": "V535_4_runner_outputs_written",
            "result": "pass" if len(NUMERIC_INPUT_TEMPLATE_ROWS) == 2 and len(evaluator) == 2 else "fail",
            "detail": f"numeric_template_rows={len(NUMERIC_INPUT_TEMPLATE_ROWS)};evaluator_rows={len(evaluator)}",
        },
        {
            "check_id": "V535_5_worldtube_certificate_written",
            "result": "pass" if len(WORLDTUBE_GLUE_CERTIFICATE_ROWS) == 6 else "fail",
            "detail": f"worldtube_certificate_rows={len(WORLDTUBE_GLUE_CERTIFICATE_ROWS)}",
        },
        {
            "check_id": "V535_6_no_claim_rows",
            "result": "pass" if not claim_eval_rows and not claim_cert_rows else "fail",
            "detail": f"claim_eval_rows={len(claim_eval_rows)};claim_cert_rows={len(claim_cert_rows)}",
        },
        {
            "check_id": "V535_7_no_overclaim",
            "result": "pass" if not claim_eval_rows and not claim_cert_rows else "fail",
            "detail": "PiM_bound_computed=false; Hilbert_worldtube_glue_derived=false; epsilon_charge_filled=false; local_GR_claim_allowed=false",
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
    return f"""# 535 - Y5 PiM Commutator Bound Runner or Hilbert Worldtube Glue

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The `Pi_M` equality/commutator fallback is now executable.

The runner evaluates:

```text
epsilon_PiM_total_abs
= |R_eq|/M_H
+ |I_commutator|/M_H
+ |B_zero_flux|/M_H
+ |projector_stress_beta_equiv|.
```

Current MTS has no sourced numeric inputs and no Hilbert-worldtube glue certificate, so the runner correctly refuses claim credit.

## 2. Numeric Input Template

{markdown_table(NUMERIC_INPUT_TEMPLATE_ROWS)}

## 3. Evaluator

{markdown_table(evaluator)}

## 4. Hilbert Worldtube Glue Certificate

{markdown_table(WORLDTUBE_GLUE_CERTIFICATE_ROWS)}

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
The Pi_M commutator/equality runner exists.
The Hilbert-worldtube glue certificate is explicit.
Current MTS has no claim-valid Pi_M bound or theorem certificate.
```

Forbidden:

```text
MTS has filled epsilon_charge.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This converts the Pi_M problem from "maybe topology saves it" into two hard doors: either the Hilbert worldtube defines the same topological charge before readout, or the equality/commutator residuals must be numerically bounded. That is exactly the kind of door a serious field theory should have.

## 12. Next Target

`{NEXT_TARGET}`

Next: derive the Hilbert worldtube/source-measure glue if possible; otherwise audit the corpus for actual Pi_M numeric inputs before inventing any.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator = evaluator_rows(NUMERIC_INPUT_TEMPLATE_ROWS)
    validations = validation_rows(sources, evaluator)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (NUMERIC_INPUT_TEMPLATE_PATH, NUMERIC_INPUT_TEMPLATE_ROWS),
        (EVALUATOR_PATH, evaluator),
        (WORLDTUBE_GLUE_CERTIFICATE_PATH, WORLDTUBE_GLUE_CERTIFICATE_ROWS),
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
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "worldtube_glue_certificate": str(ROOT / WORLDTUBE_GLUE_CERTIFICATE_PATH),
        "scorecard_update": str(ROOT / SCORECARD_UPDATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "numeric_input_rows": len(NUMERIC_INPUT_TEMPLATE_ROWS),
        "evaluator_rows": len(evaluator),
        "worldtube_glue_certificate_rows": len(WORLDTUBE_GLUE_CERTIFICATE_ROWS),
        "claim_eval_rows": len(claim_eval_rows),
        "PiM_commutator_bound_runner_written": True,
        "PiM_bound_computed": False,
        "Hilbert_worldtube_glue_derived": False,
        "epsilon_charge_filled": False,
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
        "done\nprivate_no_github\nno_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
