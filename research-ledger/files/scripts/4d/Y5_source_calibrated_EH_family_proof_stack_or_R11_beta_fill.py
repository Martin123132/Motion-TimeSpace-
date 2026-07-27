from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_source_calibrated_EH_family_proof_stack_written_R11_beta_fill_matrix_active_no_beta_or_local_GR_promotion"
CLAIM_CEILING = "source_calibrated_EH_family_proof_stack_or_R11_beta_fill_only_no_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md"

DOC_PATH = Path("529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_SOURCE_REGISTER.csv")
PROOF_STACK_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv")
BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS.csv")
R11_BETA_FILL_MATRIX_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_FILL_MATRIX.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md",
        "role": "EH mass-parameter theorem target and beta fill queue",
    },
    {
        "source_file": "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md",
        "role": "beta demotion and clean route to B=A^2",
    },
    {
        "source_file": "526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md",
        "role": "beta coefficient runner and q_loc provisional bound",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "measured-GM source calibration chain",
    },
    {
        "source_file": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only exterior parent-premise ladder",
    },
    {
        "source_file": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "second-order metric-only/R11 blocker ledger",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "local-GR symbol placement and q_loc action debt",
    },
    {
        "source_file": "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "q_loc/Gamma/Khat stress-action candidate and residual branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EH_FAMILY_PREMISE_GATES.csv",
        "role": "528 premise gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_RESIDUAL_FILL_QUEUE.csv",
        "role": "528 beta fill queue",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv",
        "role": "523 Gauss/orbital calibration chain",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "523 source-normalization residual scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "R11 operator-family status",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
        "role": "R11 minimum executable vector skeleton",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local beta/gamma/PPN bound manifest",
    },
    {
        "source_file": "scripts/Y5_source_calibrated_EH_family_proof_stack_or_R11_beta_fill.py",
        "role": "this checkpoint generator",
    },
]


PROOF_STACK_ROWS = [
    {
        "rung_id": "SCEH529_0_observed_metric_branch",
        "required_identity": "one observed metric/coframe is used by matter, clocks, photons, source variation, and PPN readout",
        "math_form": "g_obs=g_matter=g_source=g_readout through O(U^2)",
        "if_passes": "PPN coefficients refer to the physical metric",
        "current_status": "conditional_not_derived_through_O_U2",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_1_EH_only_exterior",
        "required_identity": "compact exterior field equation is EH plus harmless Lambda/background subtraction",
        "math_form": "E_munu=G_munu+Lambda g_munu; c_nonEH_operator_vector=0",
        "if_passes": "local exterior can use GR mass-family theorem",
        "current_status": "not_derived_R11_template_only",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_2_one_parameter_nohair_family",
        "required_identity": "ordinary compact exterior is a one-parameter mass family with no scalar/vector/domain/memory/boundary hair",
        "math_form": "metric exterior = Schwarzschild/SdS(mu) + background; no independent hair charges",
        "if_passes": "one mu controls both U and U^2 terms",
        "current_status": "not_derived_extra_sectors_retained",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_3_measured_mu_calibration",
        "required_identity": "the EH mass parameter equals measured orbital GM and the Hilbert/projected source charge",
        "math_form": "mu_EH=mu_obs=G0 M_H[Pi_M J_H]",
        "if_passes": "the mass in the metric is the same mass read by slow orbits",
        "current_status": "not_derived_523_scorecard_unfilled",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_4_constant_source_normalization",
        "required_identity": "mu_EH has no time/radius/species/range/frame/domain derivative and no mu_extra channel",
        "math_form": "partial_{t,r,A,lambda,frame,domain} mu_EH=0; mu_extra=0",
        "if_passes": "A is a constant mass normalization, not a hidden force/source effect",
        "current_status": "not_derived_extra_mass_channels_unfilled",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_5_isotropic_PPN_expansion",
        "required_identity": "the EH family is expanded in the observed isotropic/PPN readout coordinate",
        "math_form": "g00=-1+2U/c^2-2U^2/c^4+...; gij=(1+2U/c^2)delta_ij+...",
        "if_passes": "beta=1 and gamma=1 for the metric core",
        "current_status": "conditional_on_prior_rungs",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_6_no_quadratic_leakage",
        "required_identity": "R11, q_loc, boundary/domain, and readout sectors contribute no independent O(U^2) term",
        "math_form": "delta_beta_R11=delta_beta_q_loc=delta_beta_boundary=delta_beta_readout=0",
        "if_passes": "B=A^2 survives full MTS sector split",
        "current_status": "not_derived_components_unfilled",
        "valid_for_claim": "false",
    },
    {
        "rung_id": "SCEH529_7_beta_local_GR_gate",
        "required_identity": "beta residual envelope and full PPN vector are zero or below locks without cancellation",
        "math_form": "Delta_beta_total_abs<=7.8e-5 and gamma/alpha_i/xi rows pass",
        "if_passes": "beta gate can be treated as scored/derived; still requires full local-GR vector",
        "current_status": "not_run",
        "valid_for_claim": "false",
    },
]


BLOCKER_ROWS = [
    {
        "blocker_id": "BL529_0_R11_operator",
        "blocks_rungs": "SCEH529_1;SCEH529_6;SCEH529_7",
        "current_evidence": "R11_EXECUTABLE_VECTOR_STATUS rows are template-only/no-claim",
        "repair": "derive EH-only theorem or fill executable R11 beta/gamma/preferred-frame vector",
        "priority": "highest",
    },
    {
        "blocker_id": "BL529_1_measured_GM",
        "blocks_rungs": "SCEH529_3;SCEH529_4",
        "current_evidence": "523 scorecard unfilled; measured_GM_parent_derived=false",
        "repair": "close charge-current/Gauss/orbital/extra-mass/source-normalization chain",
        "priority": "highest",
    },
    {
        "blocker_id": "BL529_2_q_loc",
        "blocks_rungs": "SCEH529_6;SCEH529_7",
        "current_evidence": "q_loc compact-shell beta comparison is provisional; U2 normalization not proved",
        "repair": "derive q_loc Ward-zero through O(U2) or fill physical delta_beta_q_loc profile",
        "priority": "high",
    },
    {
        "blocker_id": "BL529_3_boundary_domain_projector",
        "blocks_rungs": "SCEH529_2;SCEH529_4;SCEH529_6",
        "current_evidence": "boundary/domain/projector stress and mu_extra channels retained",
        "repair": "derive no-flux/no-hair theorem or fill beta/alpha3/xi coefficients",
        "priority": "high",
    },
    {
        "blocker_id": "BL529_4_readout_frame",
        "blocks_rungs": "SCEH529_0;SCEH529_5;SCEH529_6",
        "current_evidence": "same observed metric/readout through O(U2) not derived",
        "repair": "derive same-coframe/readout theorem through PPN order",
        "priority": "high",
    },
]


R11_BETA_FILL_ROWS = [
    {
        "operator_family": "R2_fR_scalar_mode",
        "beta_effect": "scalar quadratic g00 correction and finite-range beta/gamma slip",
        "required_fill": "c_R2_or_c_fR; scalar mass; source coupling; beta/gamma/alpha(lambda) map",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "beta_effect": "higher-curvature quadratic metric response and possible slip/location effects",
        "required_fill": "c_Ricci_or_c_Weyl; weak-field solution map; beta/gamma/xi map",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "beta_effect": "scalar/class-metric nonlinear completion or source-charge beta residual",
        "required_fill": "F(phi,C); local solution; source charge; B/A^2 map",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "boundary_topological_terms",
        "beta_effect": "boundary quadratic mass renormalization, beta, alpha3, xi leakage",
        "required_fill": "boundary coefficient or scalar/topological no-flux theorem",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "source_normalization_operator",
        "beta_effect": "A_source/B_source mismatch after measured-GM normalization",
        "required_fill": "A_source;B_source;proof B=A^2 or beta residual value",
        "current_status": "missing_A_B",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "projector_domain_stress",
        "beta_effect": "domain/projector quadratic stress and preferred-frame/location beta contamination",
        "required_fill": "projector/domain stress coefficient; beta/alpha_i/xi map",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "beta_effect": "history/nonlocal quadratic response, Gdot, alpha3, or beta leakage",
        "required_fill": "kernel norm/form; compact-local silence proof or beta/Gdot/fifth-force map",
        "current_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "q_loc_Gamma_Khat",
        "beta_effect": "O(U2) q_loc force/source projection",
        "required_fill": "Ward-zero through O(U2) or delta_beta_q_loc profile with normalization",
        "current_status": "provisional_budget_only",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D529_0_proof_stack_written",
        "status": "source_calibrated_EH_family_stack_written",
        "meaning": "the exact rung stack from observed metric to EH mass family to measured GM to beta=1 is explicit",
        "claim_status": "conditional_not_satisfied",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D529_1_R11_fill_matrix_active",
        "status": "R11_beta_fill_matrix_written",
        "meaning": "if EH-only no-hair cannot be derived, beta-relevant R11 families have fill requirements",
        "claim_status": "no_beta_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D529_2_current_MTS_not_promoted",
        "status": "all_claim_rungs_false",
        "meaning": "no proof-stack rung currently grants beta, PPN, or local GR claim credit",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D529_3_next_fork",
        "status": "derive_EH_nohair_or_fill_R11_beta",
        "meaning": "the next work must either close the EH/no-hair route or fill the executable beta component vector",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D529_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SOURCE_CALIBRATED_EH_FAMILY",
        "previous_status": "conditional_theorem_written_current_premises_open",
        "new_status": "full_proof_stack_written_all_claim_rungs_unpassed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_BETA_FILL",
        "previous_status": "must_be_EH_only_or_executable_before_mass_family_route_can_claim",
        "new_status": "operator_family_beta_fill_matrix_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "MEASURED_GM_CALIBRATION",
        "previous_status": "still_required_to_identify_EH_mass_parameter_with_measured_GM",
        "new_status": "central_blocker_in_EH_family_stack",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_U2",
        "previous_status": "retained_beta_component_until_U2_conversion_or_Ward_zero_derived",
        "new_status": "explicit_R11_beta_fill_matrix_row",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_mass_family_premises_open_and_beta_fill_queue_unscored",
        "new_status": "still_blocked_proof_stack_unpassed_and_R11_beta_matrix_unfilled",
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


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    family_gates = read_csv(Path("source-intake/mts_residuals/P8_Y5_EH_FAMILY_PREMISE_GATES.csv"))
    beta_queue = read_csv(Path("source-intake/mts_residuals/P8_Y5_BETA_RESIDUAL_FILL_QUEUE.csv"))
    r11_status = read_csv(Path("source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv"))
    claim_stack_rows = [row for row in PROOF_STACK_ROWS if row["valid_for_claim"] == "true"]
    claim_r11_rows = [row for row in R11_BETA_FILL_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V529_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V529_1_528_rows_loaded",
            "result": "pass" if len(family_gates) >= 6 and len(beta_queue) >= 6 else "fail",
            "detail": f"family_gates={len(family_gates)};beta_queue={len(beta_queue)}",
        },
        {
            "check_id": "V529_2_R11_status_loaded",
            "result": "pass" if len(r11_status) >= 10 else "fail",
            "detail": f"r11_status_rows={len(r11_status)}",
        },
        {
            "check_id": "V529_3_proof_stack_written",
            "result": "pass" if len(PROOF_STACK_ROWS) == 8 else "fail",
            "detail": f"proof_stack_rows={len(PROOF_STACK_ROWS)}",
        },
        {
            "check_id": "V529_4_R11_beta_fill_matrix_written",
            "result": "pass" if len(R11_BETA_FILL_ROWS) == 8 else "fail",
            "detail": f"r11_beta_rows={len(R11_BETA_FILL_ROWS)}",
        },
        {
            "check_id": "V529_5_no_claim_rows",
            "result": "pass" if not claim_stack_rows and not claim_r11_rows else "fail",
            "detail": f"claim_stack_rows={len(claim_stack_rows)};claim_r11_rows={len(claim_r11_rows)}",
        },
        {
            "check_id": "V529_6_no_overclaim",
            "result": "pass" if not claim_stack_rows and not claim_r11_rows else "fail",
            "detail": "source_calibrated_EH_family_derived=false; R11_beta_vector_filled=false; beta_equals_one_derived=false; local_GR_claim_allowed=false",
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
    validations: list[dict[str, str]],
) -> str:
    return f"""# 529 - Y5 Source-Calibrated EH Family Proof Stack or R11 Beta Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The local-GR/beta target is now a finite proof stack, not a vibe.

To get beta from derivation rather than closure, MTS must show:

```text
one observed metric
-> EH-only one-parameter exterior
-> measured mu = orbital GM
-> no quadratic leakage
-> PPN expansion gives beta = 1.
```

Current MTS does not yet pass the stack. The fallback is the R11/beta fill matrix.

## 2. Proof Stack

{markdown_table(PROOF_STACK_ROWS)}

## 3. Blocker Ledger

{markdown_table(BLOCKER_ROWS)}

## 4. R11 Beta Fill Matrix

{markdown_table(R11_BETA_FILL_ROWS)}

## 5. Decision

{markdown_table(DECISION_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
The source-calibrated EH-family proof stack is explicit.
The R11 beta fill matrix is explicit.
Current MTS has not passed the stack.
```

Forbidden:

```text
MTS has derived the source-calibrated EH family.
MTS has filled the R11 beta vector.
MTS has derived beta=1, PPN, or local GR.
```

## 10. Next Target

`{NEXT_TARGET}`

Next fork: either derive an EH/no-hair theorem for the retained operator families, or start filling the R11 beta component vector. That is where the next real progress lives.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (PROOF_STACK_PATH, PROOF_STACK_ROWS),
        (BLOCKER_LEDGER_PATH, BLOCKER_ROWS),
        (R11_BETA_FILL_MATRIX_PATH, R11_BETA_FILL_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
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
        "proof_stack": str(ROOT / PROOF_STACK_PATH),
        "blocker_ledger": str(ROOT / BLOCKER_LEDGER_PATH),
        "r11_beta_fill_matrix": str(ROOT / R11_BETA_FILL_MATRIX_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "proof_stack_rows": len(PROOF_STACK_ROWS),
        "blocker_rows": len(BLOCKER_ROWS),
        "r11_beta_fill_rows": len(R11_BETA_FILL_ROWS),
        "failed_validation_rows": len(failed_validations),
        "source_calibrated_EH_family_stack_written": True,
        "source_calibrated_EH_family_derived_for_MTS": False,
        "R11_beta_fill_matrix_written": True,
        "R11_beta_vector_filled": False,
        "measured_mu_equals_GM_derived": False,
        "B_equals_A_squared_derived_for_MTS": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
