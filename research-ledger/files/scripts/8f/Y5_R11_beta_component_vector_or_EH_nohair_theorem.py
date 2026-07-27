from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R11_beta_component_vector_written_EH_nohair_target_explicit_no_R11_beta_or_local_GR_promotion"
CLAIM_CEILING = "R11_beta_component_vector_or_EH_nohair_theorem_only_no_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md"

DOC_PATH = Path("530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_COMPONENT_SOURCE_REGISTER.csv")
BETA_COMPONENT_VECTOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_COMPONENT_VECTOR.csv")
EH_NOHAIR_TARGETS_PATH = Path("source-intake/mts_residuals/P8_Y5_EH_NOHAIR_THEOREM_TARGETS.csv")
BETA_COMPONENT_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_COMPONENT_INPUT_TEMPLATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R11_BETA_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
        "role": "immediate proof stack and R11 beta fill matrix",
    },
    {
        "source_file": "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md",
        "role": "EH mass-parameter beta=1 theorem target",
    },
    {
        "source_file": "526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md",
        "role": "beta bound, beta evaluator, and provisional q_loc U2 comparison",
    },
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "second-order PPN residual vector and local-GR claim gate",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "measured-GM/orbital calibration chain",
    },
    {
        "source_file": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only parent-premise and Lovelock-style selection ladder",
    },
    {
        "source_file": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "sector-by-sector metric-only reduction attempt",
    },
    {
        "source_file": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 non-EH operator vector contract",
    },
    {
        "source_file": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "minimum executable R11 skeleton",
    },
    {
        "source_file": "496-R11-source-normalization-operator-vector-minimum-fill.md",
        "role": "source-normalization operator channels",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R11_BETA_FILL_MATRIX.csv",
        "role": "529 beta-relevant R11 fill matrix",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "current R11 operator-family claim status",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
        "role": "current R11 executable-vector skeleton",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_P6_metric_operator_rows_TEMPLATE.csv",
        "role": "higher-curvature/nonlocal metric operator subtemplate",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv",
        "role": "torsion/nonmetricity connection subtemplate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv",
        "role": "beta_eff=B/A^2 evaluator from 526",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv",
        "role": "provisional q_loc beta comparison from 526",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local PPN and equivalence-principle bound manifest",
    },
    {
        "source_file": "scripts/Y5_R11_beta_component_vector_or_EH_nohair_theorem.py",
        "role": "this checkpoint generator",
    },
]


EH_NOHAIR_TARGET_ROWS = [
    {
        "target_id": "EHNH530_0_parent_frame",
        "theorem_target": "one observed metric/coframe owns matter, clocks, source variation, photons, and PPN readout through O(U^2)",
        "math_contract": "g_obs=g_matter=g_source=g_readout+O(U^3/c^6)",
        "kills_or_controls": "readout beta leakage; frame redefinition loophole",
        "current_status": "not_derived_through_second_order",
        "valid_for_claim": "false",
    },
    {
        "target_id": "EHNH530_1_metric_only_local_exterior",
        "theorem_target": "compact local exterior has no independent scalar, vector, projector/domain, bulk, torsion, nonmetricity, boundary-stress, or nonlocal hair",
        "math_contract": "delta S_ext/dPhi_extra=0 implies Phi_extra=0/gauge/topological/no-stress in exterior",
        "kills_or_controls": "independent non-EH charges and extra source parameters",
        "current_status": "not_derived_R11_retained",
        "valid_for_claim": "false",
    },
    {
        "target_id": "EHNH530_2_second_order_4D_metric_operator",
        "theorem_target": "surviving bulk metric equation is local, four-dimensional, diffeomorphic, and second order",
        "math_contract": "E_mn=a G_mn+b g_mn with non-EH H_i_mn absent or theorem-zero",
        "kills_or_controls": "R2/f(R), Ricci/Weyl^2, and nonlocal metric operators",
        "current_status": "not_derived_P6_R11_open",
        "valid_for_claim": "false",
    },
    {
        "target_id": "EHNH530_3_harmless_boundary_class",
        "theorem_target": "boundary/class/topological sector has zero local stress, zero flux, and zero monopole/quadratic source shift",
        "math_contract": "delta S_boundary/dg_mn|exterior=0 and delta_mu_boundary=delta_beta_boundary=0",
        "kills_or_controls": "boundary beta, alpha3, xi, and source-normalization leakage",
        "current_status": "not_derived_boundary_rows_retained",
        "valid_for_claim": "false",
    },
    {
        "target_id": "EHNH530_4_measured_mass_lock",
        "theorem_target": "EH mass parameter equals measured orbital GM and has no derivative hair",
        "math_contract": "mu_EH=mu_obs=G0 M_H and partial_{t,r,A,lambda,frame,domain} mu_obs=0",
        "kills_or_controls": "source beta residual and Newtonian calibration loophole",
        "current_status": "not_derived_523_scorecard_unfilled",
        "valid_for_claim": "false",
    },
    {
        "target_id": "EHNH530_5_EH_family_PPN_readout",
        "theorem_target": "Schwarzschild/SdS exterior is expanded in observed isotropic PPN coordinates",
        "math_contract": "g00=-1+2U/c^2-2U^2/c^4+O(c^-6); gij=(1+2U/c^2)delta_ij+O(c^-4)",
        "kills_or_controls": "beta=1 and gamma=1 for the metric core",
        "current_status": "conditional_reference_only_prior_rungs_open",
        "valid_for_claim": "false",
    },
]


BETA_COMPONENT_ROWS = [
    {
        "component_id": "B530_0_source_AB",
        "operator_family": "source_normalization_operator",
        "component": "delta_beta_source",
        "formal_map": "delta_beta_source=B_source/A_source^2-1",
        "zero_or_safe_condition": "source equation or EH mass-family theorem gives B_source=A_source^2 after measured-GM normalization",
        "required_input": "A_source;B_source;measured_mu_lock;mu_extra=0",
        "bound_or_gate": "abs(delta_beta_source)<=7.8e-5 and no cancellation credit",
        "current_evidence": "A_source and B_source missing; measured-GM chain unfilled",
        "status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_1_R2_fR_scalar",
        "operator_family": "R2_fR_scalar_mode",
        "component": "delta_beta_R2_fR",
        "formal_map": "coefficient/scalar-mass/source-coupling -> gamma,beta,alpha(lambda) residual map",
        "zero_or_safe_condition": "c_R2=c_fR=0, scalar mass infinite, source coupling zero, or mapped residual below beta/gamma/R10 locks",
        "required_input": "c_R2_or_c_fR; scalar mass; matter/source coupling; weak-field solution",
        "bound_or_gate": "beta plus gamma and finite-range gates",
        "current_evidence": "R11 skeleton/template only",
        "status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_2_Ricci_Weyl",
        "operator_family": "Ricci_Weyl_squared",
        "component": "delta_beta_Ricci_Weyl",
        "formal_map": "c_Ricci,c_Weyl -> quadratic metric slip/location response",
        "zero_or_safe_condition": "coefficients zero, pure topological combination with harmless boundary, or weak-field map below beta/gamma/xi locks",
        "required_input": "c_Ricci_or_c_Weyl; units; topological/boundary status; weak-field map",
        "bound_or_gate": "beta/gamma/xi gate",
        "current_evidence": "R11 skeleton/template only",
        "status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_3_scalar_class",
        "operator_family": "scalar_tensor_class_metric",
        "component": "delta_beta_scalar_class",
        "formal_map": "scalar/class charge and nonlinear completion -> B/A^2 residual",
        "zero_or_safe_condition": "phi/C constant universal with zero stress/source charge, infinite mass, or mapped residual below locks",
        "required_input": "F(phi,C); scalar/class solution; source charge; beta/gamma/Gdot/R10 map",
        "bound_or_gate": "beta/gamma/clock/Gdot/fifth-force gate",
        "current_evidence": "retained; no local silence theorem",
        "status": "unfilled_retained",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_4_boundary",
        "operator_family": "boundary_topological_terms",
        "component": "delta_beta_boundary",
        "formal_map": "boundary stress/monopole/quadratic response -> beta, alpha3, xi shifts",
        "zero_or_safe_condition": "pure boundary/topological/class term has no exterior stress, no flux, no monopole shift, and no readout stress",
        "required_input": "boundary coefficient or no-flux/no-stress theorem",
        "bound_or_gate": "beta/alpha3/xi gate",
        "current_evidence": "boundary rows retained; no no-flux theorem promoted",
        "status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_5_projector_domain",
        "operator_family": "projector_domain_stress",
        "component": "delta_beta_projector_domain",
        "formal_map": "projector/domain stress coefficient -> beta plus preferred-frame/location vector",
        "zero_or_safe_condition": "projector/domain variables are metric-independent topological masks or first-class constraints with zero exterior stress",
        "required_input": "projector stress coefficient; domain no-hair theorem; alpha_i/xi map",
        "bound_or_gate": "beta plus alpha1/alpha2/alpha3/xi gates",
        "current_evidence": "domain/projector rows retained; alpha3 lock extremely tight",
        "status": "unfilled_retained",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_6_nonlocal_memory",
        "operator_family": "nonlocal_memory_kernel",
        "component": "delta_beta_nonlocal",
        "formal_map": "kernel norm/locality response -> beta, alpha3, Gdot, alpha(lambda)",
        "zero_or_safe_condition": "compact-local kernel silence, screening, zero norm, or residual map below local locks",
        "required_input": "kernel form/norm; local compact limit; Gdot/alpha3/R10 map",
        "bound_or_gate": "beta/alpha3/Gdot/fifth-force gate",
        "current_evidence": "template only; cosmology memory cannot be imported as local silence",
        "status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_7_q_loc",
        "operator_family": "q_loc_Gamma_Khat",
        "component": "delta_beta_q_loc",
        "formal_map": "P_loc(nabla^nu Gamma_eff-nabla_mu Khat^{mu nu}) projected to physical U^2 normalization",
        "zero_or_safe_condition": "Ward-zero through O(U^2) or compact profile maps below beta without violating alpha3/preferred-frame gates",
        "required_input": "physical q_loc profile; U^2 conversion; projection/readout normalization",
        "bound_or_gate": "beta bound 7.8e-5; alpha3 bound 4e-20 if same preferred-frame projection",
        "current_evidence": "provisional compact-shell budget only; U2 normalization not proved",
        "status": "provisional_budget_not_claim",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_8_torsion_nonmetricity",
        "operator_family": "torsion_nonmetricity",
        "component": "delta_beta_connection_readout",
        "formal_map": "independent connection residues -> source/light/clock/WEP and possible metric readout beta leakage",
        "zero_or_safe_condition": "Levi-Civita compatibility theorem or projective/spin modes are inert for all matter/readout sectors",
        "required_input": "P4 connection rows; compatibility theorem; WEP/clock/light map",
        "bound_or_gate": "WEP/clock/lightcone plus beta readout gate",
        "current_evidence": "P4 rows are template-only; metric compatibility not parent-derived",
        "status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_9_vector_preferred_frame",
        "operator_family": "vector_preferred_frame",
        "component": "delta_beta_vector_frame",
        "formal_map": "vector/domain/aether stress -> alpha1, alpha2, alpha3, xi and possible beta cross-term",
        "zero_or_safe_condition": "vector absent, pure gauge, dynamically aligned with zero stress, or mapped below preferred-frame locks",
        "required_input": "c_V; vector profile; alpha_i/xi map; beta cross-term map",
        "bound_or_gate": "alpha1/alpha2/alpha3/xi before beta promotion",
        "current_evidence": "retained; no zero theorem",
        "status": "unfilled_retained",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_10_bulk_X",
        "operator_family": "bulk_X_force_law",
        "component": "delta_beta_bulk_X",
        "formal_map": "bulk auxiliary force/source tail -> beta/gamma/source/fifth-force residuals",
        "zero_or_safe_condition": "positive source-free mass-gap no-hair or alpha_X(lambda_X) plus PPN/source map below locks",
        "required_input": "q_X,c_X,m_X; source/test normalization; alpha(lambda) curve",
        "bound_or_gate": "beta plus fifth-force/R10 gate",
        "current_evidence": "operator/source map not parent-derived",
        "status": "unfilled_retained",
        "valid_for_claim": "false",
    },
    {
        "component_id": "B530_11_readout_frame",
        "operator_family": "observed_readout_frame",
        "component": "delta_beta_readout",
        "formal_map": "coordinate/coframe/readout mismatch at O(U^2) -> apparent beta shift",
        "zero_or_safe_condition": "same observed metric/coframe theorem through second PPN order",
        "required_input": "readout map from parent variables to observed isotropic PPN coordinate",
        "bound_or_gate": "no beta claim until readout row is zero or bounded",
        "current_evidence": "same-readout theorem open",
        "status": "unfilled_retained",
        "valid_for_claim": "false",
    },
]


INPUT_TEMPLATE_ROWS = [
    {
        "component_id": row["component_id"],
        "operator_family": row["operator_family"],
        "input_kind": "derive_zero_or_fill_numeric",
        "required_columns": "coefficient_or_theorem,units,normalization,weak_field_map,source_file,assumptions,valid_for_claim",
        "acceptance_rule": row["zero_or_safe_condition"],
        "current_status": "awaiting_parent_derivation_or_numeric_vector",
    }
    for row in BETA_COMPONENT_ROWS
]


DECISION_ROWS = [
    {
        "decision_id": "D530_0_EH_nohair_target_written",
        "status": "EH_nohair_theorem_contract_explicit",
        "meaning": "the precise theorem needed to delete R11 beta components is now written rung by rung",
        "claim_status": "contract_only_not_satisfied",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D530_1_beta_component_vector_written",
        "status": "R11_beta_component_vector_written",
        "meaning": "every retained beta-relevant family now has a named component, formal map, zero condition, and required input",
        "claim_status": "no_beta_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D530_2_no_component_claim_rows",
        "status": "all_component_rows_invalid_for_claim",
        "meaning": "current MTS does not yet fill any R11 beta component as derived-zero or numeric-bounded",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D530_3_next_fork",
        "status": "source_Newton_beta_envelope_or_parent_nohair",
        "meaning": "next work should combine source beta, R11 beta, q_loc, boundary/domain, and readout into one no-cancellation envelope",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D530_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "EH_NOHAIR_ROUTE",
        "previous_status": "proof_stack_written_all_claim_rungs_unpassed",
        "new_status": "theorem_targets_explicit_but_not_satisfied",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_BETA_VECTOR",
        "previous_status": "operator_family_beta_fill_matrix_written",
        "new_status": "component_vector_written_all_rows_unfilled_or_template_only",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_U2",
        "previous_status": "provisional_beta_budget_only",
        "new_status": "explicit_beta_component_retained_until_physical_U2_map_or_Ward_zero",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BETA_ENVELOPE",
        "previous_status": "beta_fill_queue_unscored",
        "new_status": "ready_for_no_cancellation_envelope_after_component_inputs",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_proof_stack_unpassed_and_R11_beta_matrix_unfilled",
        "new_status": "still_blocked_R11_beta_components_unfilled_and_EH_nohair_not_derived",
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
    beta_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_R11_BETA_FILL_MATRIX.csv"))
    r11_status = read_csv(Path("source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv"))
    r11_skeleton = read_csv(Path("source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv"))
    beta_eval = read_csv(Path("source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv"))
    qloc_bound = read_csv(Path("source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv"))
    claim_component_rows = [row for row in BETA_COMPONENT_ROWS if row["valid_for_claim"] == "true"]
    claim_theorem_rows = [row for row in EH_NOHAIR_TARGET_ROWS if row["valid_for_claim"] == "true"]
    beta_lock_rows = [
        row
        for row in beta_eval
        if row.get("bound_id") == "BETA_LOCK" or row.get("observable", "") == "beta_minus_1"
    ]
    return [
        {
            "check_id": "V530_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V530_1_prior_beta_matrix_loaded",
            "result": "pass" if len(beta_fill) == 8 else "fail",
            "detail": f"beta_fill_rows={len(beta_fill)}",
        },
        {
            "check_id": "V530_2_R11_status_and_skeleton_loaded",
            "result": "pass" if len(r11_status) >= 10 and len(r11_skeleton) >= 10 else "fail",
            "detail": f"r11_status_rows={len(r11_status)};r11_skeleton_rows={len(r11_skeleton)}",
        },
        {
            "check_id": "V530_3_beta_evaluator_and_q_loc_loaded",
            "result": "pass" if len(beta_eval) >= 1 and len(qloc_bound) >= 1 else "fail",
            "detail": f"beta_eval_rows={len(beta_eval)};q_loc_rows={len(qloc_bound)};beta_lock_rows={len(beta_lock_rows)}",
        },
        {
            "check_id": "V530_4_EH_nohair_targets_written",
            "result": "pass" if len(EH_NOHAIR_TARGET_ROWS) == 6 else "fail",
            "detail": f"target_rows={len(EH_NOHAIR_TARGET_ROWS)}",
        },
        {
            "check_id": "V530_5_beta_component_vector_written",
            "result": "pass" if len(BETA_COMPONENT_ROWS) == 12 else "fail",
            "detail": f"component_rows={len(BETA_COMPONENT_ROWS)}",
        },
        {
            "check_id": "V530_6_no_claim_rows",
            "result": "pass" if not claim_component_rows and not claim_theorem_rows else "fail",
            "detail": f"claim_component_rows={len(claim_component_rows)};claim_theorem_rows={len(claim_theorem_rows)}",
        },
        {
            "check_id": "V530_7_no_overclaim",
            "result": "pass" if not claim_component_rows and not claim_theorem_rows else "fail",
            "detail": "EH_nohair_derived=false; R11_beta_vector_filled=false; beta_equals_one_derived=false; local_GR_claim_allowed=false",
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
    return f"""# 530 - Y5 R11 Beta Component Vector or EH Nohair Theorem

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The next fork has been made exact.

There are only two honest ways to make the local beta/GR route work:

```text
Route A: prove EH/no-hair strongly enough that every beta-relevant R11 component is zero.
Route B: fill every beta component as a numeric/theorem-bounded residual and pass the no-cancellation envelope.
```

Current MTS has neither route closed yet. This checkpoint writes the theorem target and the beta component vector, but it does not promote beta, PPN, or local GR.

## 2. EH Nohair Theorem Targets

{markdown_table(EH_NOHAIR_TARGET_ROWS)}

## 3. R11 Beta Component Vector

The total beta gate must eventually use a no-cancellation envelope:

```text
Delta_beta_total_abs
= |delta_beta_source|
+ sum_i |delta_beta_R11_i|
+ |delta_beta_q_loc|
+ |delta_beta_boundary_domain|
+ |delta_beta_readout|
<= 7.8e-5.
```

{markdown_table(BETA_COMPONENT_ROWS)}

## 4. Input Template

{markdown_table(INPUT_TEMPLATE_ROWS)}

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
The EH/no-hair target is explicit.
The R11 beta component vector is explicit.
Current MTS has not filled or theorem-zeroed the beta components.
```

Forbidden:

```text
MTS has derived EH/no-hair for local exteriors.
MTS has filled the R11 beta vector.
MTS has derived beta=1, PPN, or local GR.
```

## 10. Practical Read

This is the referee card for the local-GR route. If the parent action can really remove the retained sectors, beta follows cleanly from the EH mass family. If not, MTS must fight fairly as a residual branch with every component visible and bounded.

## 11. Next Target

`{NEXT_TARGET}`

Next: combine source A/B, R11 components, q_loc, boundary/domain, and readout into one no-cancellation beta envelope. If any component remains missing, beta stays demoted rather than smuggled in.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R11-beta-component-vector-or-EH-nohair-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (BETA_COMPONENT_VECTOR_PATH, BETA_COMPONENT_ROWS),
        (EH_NOHAIR_TARGETS_PATH, EH_NOHAIR_TARGET_ROWS),
        (BETA_COMPONENT_INPUT_TEMPLATE_PATH, INPUT_TEMPLATE_ROWS),
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
        "beta_component_vector": str(ROOT / BETA_COMPONENT_VECTOR_PATH),
        "eh_nohair_targets": str(ROOT / EH_NOHAIR_TARGETS_PATH),
        "input_template": str(ROOT / BETA_COMPONENT_INPUT_TEMPLATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "eh_nohair_target_rows": len(EH_NOHAIR_TARGET_ROWS),
        "beta_component_rows": len(BETA_COMPONENT_ROWS),
        "input_template_rows": len(INPUT_TEMPLATE_ROWS),
        "EH_nohair_theorem_targets_written": True,
        "EH_nohair_derived_for_MTS": False,
        "R11_beta_component_vector_written": True,
        "R11_beta_vector_filled": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nno_beta_PPN_or_local_GR_promotion\n", encoding="utf-8"
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
