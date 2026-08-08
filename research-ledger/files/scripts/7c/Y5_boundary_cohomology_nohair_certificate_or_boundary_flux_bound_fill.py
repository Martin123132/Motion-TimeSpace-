from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_boundary_cohomology_nohair_certificate_failed_current_claim_boundary_flux_bound_row_written"
CLAIM_CEILING = "boundary_cohomology_nohair_attempt_and_boundary_flux_bound_row_only_no_BRR545_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md"

DOC_PATH = Path("549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_549_SOURCE_REGISTER.csv")
BOUNDARY_THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv")
BOUNDARY_OBSTRUCTIONS_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_OBSTRUCTION_LEDGER.csv")
BOUNDARY_FLUX_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv")
BOUNDARY_FLUX_EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_EVALUATOR.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_549_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_549_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_549_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
        "role": "reference-lock certificate failure and first Delta_symp bound row",
    },
    {
        "source_file": "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md",
        "role": "BRR545 residual input template and BRC547 certificate queue",
    },
    {
        "source_file": "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
        "role": "boundary/reference obstruction ledger",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "R11 boundary stress theorem stack and closure fill pack",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "local-zero boundary/R11 implication audit",
    },
    {
        "source_file": "229-second-order-beta-or-boundary-scalar-owner.md",
        "role": "scalar boundary owner and second-order beta warning",
    },
    {
        "source_file": "60-relative-cohomology-boundary-contract.md",
        "role": "relative cohomology boundary contract",
    },
    {
        "source_file": "300-boundary-state-local-silence-theorem-attempt.md",
        "role": "boundary-state local silence conditional theorem",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv",
        "role": "boundary alpha3 no-flux theorem attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv",
        "role": "boundary scalar action parent ownership attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv",
        "role": "R11 boundary stress theorem stack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv",
        "role": "R11 boundary stress closure fill pack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv",
        "role": "local-zero boundary/R11 implication audit CSV",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
        "role": "BRR545 local lock map",
    },
    {
        "source_file": "scripts/Y5_boundary_cohomology_nohair_certificate_or_boundary_flux_bound_fill.py",
        "role": "this checkpoint generator",
    },
]


BOUNDARY_THEOREM_ROWS = [
    {
        "step_id": "BCT549_0_target_certificate",
        "claim": "BRC547_1 and BRC547_2 require B_zero_flux=0 by boundary cohomology plus no-hair",
        "mathematical_form": "B_imp=dC, int_S2 B_imp-int_S1 B_imp=0, and T_B^TF=T_B^vector=n_mu P_loc_nu T_B^{mu nu}=0",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a proof",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_1_relative_cohomology_contract",
        "claim": "stationary/bound compact domains can be represented by a trivial relative boundary class",
        "mathematical_form": "[B_imp]=0 in H^2(boundary) or relative pair (j_3,b_2) has trivial local boundary component",
        "current_result": "conditional_contract_available",
        "why_not_enough": "relative class selection is not parent-derived and cannot be chosen to silence the local branch after the fact",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_2_exact_improvement_zero",
        "claim": "exact/improvement boundary terms have zero linked-sphere flux in the compact exterior",
        "mathematical_form": "int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0",
        "current_result": "not_derived",
        "why_not_enough": "exact/topological labels can still carry finite surface charges unless the relative class and reference are fixed",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_3_scalar_homogeneous_nohair",
        "claim": "a scalar-only homogeneous boundary action produces no vector or trace-free tensor boundary stress",
        "mathematical_form": "S_B=int_boundary sqrt(|gamma|)F(scalars), D_A scalars=0 => tau_AB proportional gamma_AB",
        "current_result": "conditional_mathematical_lemma",
        "why_not_enough": "current parent action does not prove the boundary carries only homogeneous scalar marker-free data",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_4_volume_no_flux_not_alpha3_no_flux",
        "claim": "local scalar volume no-flux implies full momentum/boundary no-flux",
        "mathematical_form": "X_D=0 => n_mu P_loc_nu K_boundary^{mu nu}=0",
        "current_result": "fail_as_general_statement",
        "why_not_enough": "scalar trace/volume zero does not remove tangential vector, shear, marker, or normal exchange components",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_5_derivative_silence",
        "claim": "remaining boundary monopole is constant and derivative-silent",
        "mathematical_form": "partial_t epsilon_B_flux_abs=partial_r epsilon_B_flux_abs=partial_frame epsilon_B_flux_abs=0",
        "current_result": "not_derived",
        "why_not_enough": "Gdot, radial, frame, beta, and source-normalization boundary rows remain unfilled",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BCT549_6_certificate_verdict",
        "claim": "BRC547_1 and BRC547_2 can be signed for current MTS",
        "mathematical_form": "BRC547_1.valid_for_claim=true and BRC547_2.valid_for_claim=true",
        "current_result": "fail_current_claim",
        "why_not_enough": "cohomology/no-hair route is conditional but not parent-owned; fallback boundary-flux bound row is required",
        "valid_for_claim": "false",
    },
]


BOUNDARY_OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "BCO549_0_relative_class_selection",
        "obstruction": "relative cohomology/local-boundary class is a contract, not a parent-selected theorem",
        "activated_residual": "epsilon_B_flux_abs",
        "repair": "derive local trivial boundary class from parent Euler/Ward/topological selector",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BCO549_1_finite_surface_charge",
        "obstruction": "exact/improvement terms can carry finite linked-sphere charge",
        "activated_residual": "epsilon_B_flux_abs;epsilon_boundary_reference_abs",
        "repair": "prove relative cohomology triviality for B_imp or fill B_zero_flux_over_MH",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BCO549_2_vector_tensor_hair",
        "obstruction": "scalar/trace no-flux does not eliminate vector, trace-free tensor, shear, marker, or normal exchange hair",
        "activated_residual": "alpha3;xi;beta;source_normalization",
        "repair": "parent-owned scalar homogeneous marker-free boundary action or coefficient map",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BCO549_3_derivative_hair",
        "obstruction": "boundary monopole may still have time/radial/frame/source dependence",
        "activated_residual": "Gdot;radial_source_hair;beta;xi",
        "repair": "derivative-zero theorem or source-backed time/radial/profile rows",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BCO549_4_projector_boundary_stress",
        "obstruction": "Pi_M/projector variation can create boundary-supported stress",
        "activated_residual": "projector_stress;epsilon_B_flux_abs;R11",
        "repair": "projector topological silence certificate or retained stress coefficient/profile",
        "valid_for_claim": "false",
    },
]


BOUNDARY_FLUX_FILL_ROWS = [
    {
        "fill_id": "FB549_0_boundary_flux_bound",
        "residual_component": "epsilon_B_flux_abs",
        "formula": "abs(B_zero_flux_over_MH)",
        "B_zero_flux_over_MH": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
        "c_B_flux_to_alpha3": "MISSING_ALPHA3_COEFFICIENT",
        "c_B_flux_to_xi": "MISSING_XI_COEFFICIENT",
        "c_B_flux_to_beta": "MISSING_BETA_COEFFICIENT",
        "partial_t_epsilon_B_flux_abs": "MISSING_TIME_PROFILE",
        "partial_r_epsilon_B_flux_abs": "MISSING_RADIAL_PROFILE",
        "mapped_lock_rows": "R7_alpha3;R8_xi;R4_beta;R9_Gdot;R11_EH_operator_ledger",
        "bound_rule": "each mapped product/profile must pass its lock individually or theorem-zero; no cancellation credit",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_boundary_cohomology_nohair_certificate_failure",
        "valid_for_claim": "false",
    }
]


DECISION_ROWS = [
    {
        "decision_id": "D549_0_boundary_certificates_failed",
        "status": "BRC547_1_and_BRC547_2_not_signed",
        "meaning": "current corpus has useful conditional cohomology/scalar no-hair lemmas but no parent-owned boundary zero theorem",
        "claim_status": "epsilon_B_flux_abs_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D549_1_boundary_flux_bound_row_written",
        "status": "epsilon_B_flux_abs_bound_row_written_unfilled",
        "meaning": "fallback numeric/profile row now states exactly what must be filled if theorem route fails",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D549_2_next_certificate",
        "status": "projector_symplectic_silence_next",
        "meaning": "after reference and boundary certificates fail, Pi_M/projector symplectic silence is the next active BRR545 lock",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D549_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BRC547_1_BOUNDARY_COHOMOLOGY_ZERO",
        "previous_status": "missing_certificate",
        "new_status": "attempted_failed_current_claim_boundary_flux_bound_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRC547_2_BOUNDARY_NO_HAIR",
        "previous_status": "missing_certificate",
        "new_status": "attempted_failed_current_claim_boundary_flux_bound_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_BOUNDARY_FLUX",
        "previous_status": "input_template_unfilled",
        "new_status": "epsilon_B_flux_abs_retained_with_first_bound_fill_row",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_reference_lock_failed_current_claim",
        "new_status": "still_blocked_boundary_cohomology_nohair_failed_current_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_no_reference_lock_or_bound_value",
        "new_status": "still_blocked_no_boundary_zero_or_bound_value",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


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


def boundary_flux_evaluator_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in BOUNDARY_FLUX_FILL_ROWS:
        rows.append(
            {
                "fill_id": row["fill_id"],
                "residual_component": row["residual_component"],
                "numeric_status": "not_computed_missing_B_zero_flux_over_MH_and_coefficients",
                "mapped_lock_rows": row["mapped_lock_rows"],
                "pass_status": "not_claimable",
                "valid_for_claim": "false",
                "notes": "boundary cohomology/no-hair certificates failed for current claim; fill this row only with theorem-zero source or source-backed numeric/profile data",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], evaluator_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_548_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    prior_certificates = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_THEOREM_CERTIFICATE_TEMPLATE.csv"))
    prior_lock_map = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"))
    boundary_alpha3 = read_csv(Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"))
    boundary_scalar = read_csv(Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"))
    r11_stack = read_csv(Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv"))
    local_zero = read_csv(Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv"))
    claim_theorem_rows = [row for row in BOUNDARY_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_obstruction_rows = [row for row in BOUNDARY_OBSTRUCTION_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in BOUNDARY_FLUX_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V549_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V549_1_prior_548_clean",
            "result": "pass" if len(prior_validation) == 8 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V549_2_prior_templates_loaded",
            "result": "pass" if len(prior_certificates) == 5 and len(prior_lock_map) == 10 else "fail",
            "detail": f"certificate_rows={len(prior_certificates)};lock_rows={len(prior_lock_map)}",
        },
        {
            "check_id": "V549_3_boundary_evidence_loaded",
            "result": "pass" if len(boundary_alpha3) >= 8 and len(boundary_scalar) >= 8 and len(r11_stack) >= 7 and len(local_zero) >= 7 else "fail",
            "detail": f"boundary_alpha3={len(boundary_alpha3)};boundary_scalar={len(boundary_scalar)};r11_stack={len(r11_stack)};local_zero={len(local_zero)}",
        },
        {
            "check_id": "V549_4_theorem_attempt_complete",
            "result": "pass" if len(BOUNDARY_THEOREM_ROWS) == 7 and len(BOUNDARY_OBSTRUCTION_ROWS) == 5 else "fail",
            "detail": f"theorem_rows={len(BOUNDARY_THEOREM_ROWS)};obstruction_rows={len(BOUNDARY_OBSTRUCTION_ROWS)}",
        },
        {
            "check_id": "V549_5_boundary_bound_row_written",
            "result": "pass" if len(BOUNDARY_FLUX_FILL_ROWS) == 1 and len(evaluator_rows) == 1 else "fail",
            "detail": f"fill_rows={len(BOUNDARY_FLUX_FILL_ROWS)};evaluator_rows={len(evaluator_rows)}",
        },
        {
            "check_id": "V549_6_no_claim_rows",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": f"claim_theorem={len(claim_theorem_rows)};claim_obstruction={len(claim_obstruction_rows)};claim_fill={len(claim_fill_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V549_7_no_overclaim",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": "boundary_certificates_signed=false; epsilon_B_flux_abs_filled=false; BRR545_filled=false; source_measure=false; Newton=false; PPN=false; local_GR=false",
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
    evaluator_rows: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 549 - Y5 Boundary Cohomology Nohair Certificate or Boundary Flux Bound Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The boundary cohomology/no-hair certificate does not close for current MTS.

The work still helps: it separates two things that were getting blurred:

```text
relative cohomology / scalar no-hair is a strong sufficient route;
current MTS does not yet parent-own that route.
```

So `epsilon_B_flux_abs` stays retained, and the first boundary-flux fallback row is now explicit.

## 2. Boundary Cohomology and No-Hair Theorem Attempt

{markdown_table(BOUNDARY_THEOREM_ROWS)}

## 3. Obstruction Ledger

{markdown_table(BOUNDARY_OBSTRUCTION_ROWS)}

## 4. Boundary Flux Bound Fill Row

{markdown_table(BOUNDARY_FLUX_FILL_ROWS)}

## 5. Boundary Flux Evaluator

{markdown_table(evaluator_rows)}

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
MTS has attempted the boundary cohomology/no-hair certificates.
MTS has identified why the current corpus cannot sign BRC547_1 or BRC547_2.
MTS has written the first fallback bound row for epsilon_B_flux_abs.
```

Forbidden:

```text
MTS has signed the boundary cohomology/no-hair certificates.
MTS has filled epsilon_B_flux_abs.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is a useful miss. We now know that local scalar volume silence and scalar boundary language cannot be used as a cheap boundary-flux zero. To make this route work, the parent action must select the trivial boundary class and forbid vector/tensor/derivative hair before readout.

## 12. Next Target

`{NEXT_TARGET}`

Next: attempt the projector symplectic silence certificate. If that fails, write the commutator/projector-stress bound row.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator_rows = boundary_flux_evaluator_rows()
    validations = validation_rows(sources, evaluator_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (BOUNDARY_THEOREM_PATH, BOUNDARY_THEOREM_ROWS),
        (BOUNDARY_OBSTRUCTIONS_PATH, BOUNDARY_OBSTRUCTION_ROWS),
        (BOUNDARY_FLUX_FILL_PATH, BOUNDARY_FLUX_FILL_ROWS),
        (BOUNDARY_FLUX_EVALUATOR_PATH, evaluator_rows),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, evaluator_rows, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
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
        "boundary_theorem": str(ROOT / BOUNDARY_THEOREM_PATH),
        "boundary_obstructions": str(ROOT / BOUNDARY_OBSTRUCTIONS_PATH),
        "boundary_flux_fill": str(ROOT / BOUNDARY_FLUX_FILL_PATH),
        "boundary_flux_evaluator": str(ROOT / BOUNDARY_FLUX_EVALUATOR_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "boundary_theorem_rows": len(BOUNDARY_THEOREM_ROWS),
        "obstruction_rows": len(BOUNDARY_OBSTRUCTION_ROWS),
        "boundary_flux_fill_rows": len(BOUNDARY_FLUX_FILL_ROWS),
        "boundary_cohomology_certificate_signed": False,
        "boundary_nohair_certificate_signed": False,
        "epsilon_B_flux_abs_filled": False,
        "BRR545_values_filled": False,
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
        "done\nprivate_no_github\nboundary_cohomology_nohair_certificates_failed_boundary_flux_bound_row_written_no_BRR545_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
