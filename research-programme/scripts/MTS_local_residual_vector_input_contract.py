from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "MTS-local-residual-vector-input-contract"
CHECKPOINT_DOC = "428-MTS-local-residual-vector-input-contract.md"
STATUS = "MTS_local_residual_vector_input_contract_written_12_component_prediction_template_ready_no_MTS_residuals_loaded_no_local_GR_pass"
CLAIM_CEILING = "MTS_residual_vector_input_contract_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md"
RESIDUAL_INTAKE_DIR = ROOT / "source-intake" / "mts_residuals"
PREDICTION_TEMPLATE = RESIDUAL_INTAKE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv"


SOURCE_DOCS = [
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson bridge, source_residuals, mu_extra, and PPN-completion blockers",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH-operator/source-normalization retained rows and local-bound test matrix",
    },
    {
        "path": "427-source-normalization-bounds-csv-template-fill.md",
        "role": "verified external/internal source-bound rows",
    },
    {
        "path": "427-local-bound-runner-v4-evaluate-smoke.md",
        "role": "evaluate-mode result showing bounds loaded but MTS residual vector absent",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "sourced local-bound constraints for comparison",
    },
    {
        "path": "runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv",
        "role": "row IDs, observables, source locks, and symbolic/deferred status",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source and measured-GM normalization equations",
    },
]


RESIDUAL_SCHEMA = [
    {
        "column": "model_id",
        "required": "yes",
        "meaning": "short model/run name for the MTS branch being tested",
        "allowed_values": "nonempty string",
        "no_claim_guard": "a model_id alone is not evidence",
    },
    {
        "column": "branch_id",
        "required": "yes",
        "meaning": "specific closure/derivation branch, e.g. local_GR_parent_attempt_v1",
        "allowed_values": "nonempty string",
        "no_claim_guard": "branch must be reproducible",
    },
    {
        "column": "row_id",
        "required": "yes",
        "meaning": "runner-v4 row ID matching local_bound_claims.csv",
        "allowed_values": "R0_identity_coframe_direct through R11_EH_operator_ledger",
        "no_claim_guard": "unknown row IDs are rejected",
    },
    {
        "column": "observable",
        "required": "yes",
        "meaning": "observable name from the bound/evaluate table",
        "allowed_values": "must match row contract",
        "no_claim_guard": "prevents eta/gamma/beta row swaps",
    },
    {
        "column": "predicted_value",
        "required": "numeric rows yes; symbolic rows optional",
        "meaning": "signed central MTS residual in row units",
        "allowed_values": "float or blank for curve/vector rows",
        "no_claim_guard": "blank numeric rows cannot be evaluated",
    },
    {
        "column": "one_sigma",
        "required": "optional",
        "meaning": "theory/numerical uncertainty if available",
        "allowed_values": "float or blank",
        "no_claim_guard": "uncertainty cannot replace a central prediction",
    },
    {
        "column": "upper_envelope",
        "required": "yes",
        "meaning": "absolute upper envelope of the predicted residual used for bound comparison",
        "allowed_values": "float for R0-R9; curve/vector marker for R10/R11",
        "no_claim_guard": "this is what gets scored against the bound",
    },
    {
        "column": "units",
        "required": "yes",
        "meaning": "prediction units",
        "allowed_values": "dimensionless, yr^-1, range-dependent, operator family",
        "no_claim_guard": "unit mismatch blocks evaluation",
    },
    {
        "column": "curve_or_vector_file",
        "required": "R10/R11 yes; otherwise optional",
        "meaning": "path to alpha(lambda) curve or non-EH coefficient vector",
        "allowed_values": "workspace-relative path or blank",
        "no_claim_guard": "R10/R11 cannot pass on scalar placeholder text",
    },
    {
        "column": "derivation_status",
        "required": "yes",
        "meaning": "how the residual was obtained",
        "allowed_values": "derived_zero, derived_bound, fitted, phenomenological, closure_assumed, speculative",
        "no_claim_guard": "closure_assumed/speculative rows cannot support local-GR derivation",
    },
    {
        "column": "formula_reference",
        "required": "yes",
        "meaning": "equation label or derivation note producing the residual",
        "allowed_values": "nonempty string",
        "no_claim_guard": "no hidden black-box residuals",
    },
    {
        "column": "source_file",
        "required": "yes",
        "meaning": "file path containing the derivation or numerical run",
        "allowed_values": "workspace-relative path",
        "no_claim_guard": "source path must exist for claim-bearing rows",
    },
    {
        "column": "assumptions",
        "required": "yes",
        "meaning": "same-frame, EH, closure, fitted, boundary conditions, dataset, or gauge assumptions",
        "allowed_values": "nonempty string",
        "no_claim_guard": "assumptions determine whether this is derivation or closure",
    },
    {
        "column": "comparison_role",
        "required": "yes",
        "meaning": "how the row should be interpreted",
        "allowed_values": "GR_null_baseline, MTS_prediction, closure_control, symbolic_deferred",
        "no_claim_guard": "only MTS_prediction rows are empirical MTS tests",
    },
    {
        "column": "claim_request",
        "required": "yes",
        "meaning": "what the row asks the evaluator to allow",
        "allowed_values": "none, empirical_viability_only, derived_local_GR_candidate",
        "no_claim_guard": "derived_local_GR_candidate requires derived_zero/derived_bound on all non-symbolic rows",
    },
    {
        "column": "notes",
        "required": "optional",
        "meaning": "extra caveats or numerical details",
        "allowed_values": "free text",
        "no_claim_guard": "notes cannot override failed gates",
    },
]


RESIDUAL_COMPONENTS = [
    {
        "component_id": "r0_eta_geom",
        "row_id": "R0_identity_coframe_direct",
        "observable": "eta_WEP_direct_geometry",
        "MTS_output_name": "eta_geom_AB",
        "mathematical_definition": "eta_geom_AB = 2|a_geom(A)-a_geom(B)|/|a_geom(A)+a_geom(B)|, or the proven equivalent coframe-slip observable",
        "units": "dimensionless",
        "source_bound": "2.8e-15",
        "GR_null_value": "0",
        "current_MTS_status": "closure_control_only",
        "theorem_zero_condition": "single universal observed coframe for all freely falling material bodies with no species label",
        "numeric_input_required": "predicted eta_geom_AB or derived_zero proof",
        "failure_channel": "geometry/coframe WEP split",
        "claim_gate": "direct WEP geometry only; does not clear source charge R1",
    },
    {
        "component_id": "r1_eta_source",
        "row_id": "R1_WEP_source_charge",
        "observable": "eta_WEP_source_charge",
        "MTS_output_name": "eta_source_AB",
        "mathematical_definition": "eta_source_AB = 2|a_source(A)-a_source(B)|/|a_source(A)+a_source(B)|, equivalently a species derivative of mu_obs when reduced to measured acceleration",
        "units": "dimensionless",
        "source_bound": "2.8e-15",
        "GR_null_value": "0",
        "current_MTS_status": "retained_four_channel_budget",
        "theorem_zero_condition": "mu_obs has no species dependence and all source-charge/bulk/boundary/material-marker channels vanish or are forbidden",
        "numeric_input_required": "direct WEP subscore plus full source-normalization contribution",
        "failure_channel": "hidden source charge or material-marker coupling",
        "claim_gate": "must report direct and full R1 channels separately",
    },
    {
        "component_id": "r2_alpha_clock",
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "MTS_output_name": "alpha_clock",
        "mathematical_definition": "Delta nu/nu = (1 + alpha_clock) Delta U/c^2 after mapping the MTS clock variable to the observed metric frame",
        "units": "dimensionless",
        "source_bound": "2.48e-05",
        "GR_null_value": "0",
        "current_MTS_status": "retained_same_frame_clock_check",
        "theorem_zero_condition": "matter clocks couple to the same observed metric/coframe as the gravitational action",
        "numeric_input_required": "alpha_clock residual",
        "failure_channel": "clock/frame/nonmetricity split",
        "claim_gate": "clock success does not imply gamma/beta success",
    },
    {
        "component_id": "r3_gamma",
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "MTS_output_name": "gamma_minus_1",
        "mathematical_definition": "g_ij = delta_ij(1 + 2 gamma U/c^2) + O(c^-4); residual is gamma-1 in the observed frame",
        "units": "dimensionless",
        "source_bound": "2.3e-05",
        "GR_null_value": "0",
        "current_MTS_status": "EH_operator_slip_test",
        "theorem_zero_condition": "non-EH scalar/tensor/boundary/domain slip terms vanish or map below bound",
        "numeric_input_required": "gamma-1 residual from weak-field metric",
        "failure_channel": "spatial curvature slip or scalar mode",
        "claim_gate": "Poisson limit alone cannot supply gamma",
    },
    {
        "component_id": "r4_beta",
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "MTS_output_name": "beta_minus_1",
        "mathematical_definition": "g_00 = -1 + 2U/c^2 - 2 beta U^2/c^4 + O(c^-6); residual is beta-1 after source normalization",
        "units": "dimensionless",
        "source_bound": "7.8e-05",
        "GR_null_value": "0",
        "current_MTS_status": "source_normalization_beta_test",
        "theorem_zero_condition": "second-order weak-field equation closes with conserved measured GM and no nonlinear source residue",
        "numeric_input_required": "beta-1 residual",
        "failure_channel": "nonlinear source normalization or second-order metric mismatch",
        "claim_gate": "must separate beta from absorbed GM calibration",
    },
    {
        "component_id": "r5_alpha1",
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "MTS_output_name": "alpha1",
        "mathematical_definition": "PPN preferred-frame alpha1 extracted from g_0i/vector terms in the observed matter frame",
        "units": "dimensionless",
        "source_bound": "1e-04",
        "GR_null_value": "0",
        "current_MTS_status": "vector_preferred_frame_test",
        "theorem_zero_condition": "all vector/domain/projector preferred-frame terms are pure gauge, forbidden, or below retained lock",
        "numeric_input_required": "alpha1 residual or vector-to-PPN map",
        "failure_channel": "preferred-frame vector hair",
        "claim_gate": "requires same-pipeline GR/null baseline",
    },
    {
        "component_id": "r6_alpha2",
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "MTS_output_name": "alpha2",
        "mathematical_definition": "PPN alpha2 extracted from preferred-frame/vector-sector weak-field terms",
        "units": "dimensionless",
        "source_bound": "2e-09",
        "GR_null_value": "0",
        "current_MTS_status": "vector_preferred_frame_test",
        "theorem_zero_condition": "vector/domain/projector frame terms vanish with alpha2-level precision or by theorem",
        "numeric_input_required": "alpha2 residual or vector-to-PPN map",
        "failure_channel": "tight preferred-frame/vector leakage",
        "claim_gate": "engineering-small is not enough; 2e-09 lock applies",
    },
    {
        "component_id": "r7_alpha3",
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "MTS_output_name": "alpha3_or_flux_residual",
        "mathematical_definition": "alpha3-equivalent self-acceleration/momentum-nonconservation residual generated by unowned q_loc^nu, boundary flux, or domain exchange",
        "units": "dimensionless",
        "source_bound": "4e-20",
        "GR_null_value": "0",
        "current_MTS_status": "boundary_exchange_ultratight_test",
        "theorem_zero_condition": "Ward/Bianchi exchange ownership proves q_loc^nu=0 or maps it to a conserved internal current with no self-acceleration",
        "numeric_input_required": "alpha3-equivalent residual or exchange-flux-to-alpha3 map",
        "failure_channel": "unowned momentum flux or self-acceleration",
        "claim_gate": "ultratight row; closure language cannot pass it",
    },
    {
        "component_id": "r8_xi",
        "row_id": "R8_xi",
        "observable": "xi",
        "MTS_output_name": "xi",
        "mathematical_definition": "PPN preferred-location xi extracted from anisotropic/domain/shear coupling to external gravitational environment",
        "units": "dimensionless",
        "source_bound": "4e-09",
        "GR_null_value": "0",
        "current_MTS_status": "domain_shear_preferred_location_test",
        "theorem_zero_condition": "domain/projector/boundary shear terms vanish, are pure gauge, or are source-budgeted below xi lock",
        "numeric_input_required": "xi residual or anisotropy-to-PPN map",
        "failure_channel": "preferred-location/domain anisotropy",
        "claim_gate": "must not hide anisotropy inside isotropic Poisson source",
    },
    {
        "component_id": "r9_Gdot",
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "MTS_output_name": "dln_mu_obs_dt_or_dln_Geff_dt",
        "mathematical_definition": "d ln mu_obs/dt = d ln(G_eff M_eff)/dt, with d ln G_eff/dt reported separately when possible",
        "units": "yr^-1",
        "source_bound": "9.6e-15",
        "GR_null_value": "0",
        "current_MTS_status": "memory_source_drift_test",
        "theorem_zero_condition": "kappa_eff/G_eff and measured M_eff are constant, conserved, universal, and not memory-drifting locally",
        "numeric_input_required": "yr^-1 drift residual and decomposition into G_eff vs M_eff if available",
        "failure_channel": "memory drift or source-normalization drift",
        "claim_gate": "cosmological memory success cannot override local Gdot lock",
    },
    {
        "component_id": "r10_alpha_lambda",
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "MTS_output_name": "alpha_of_lambda_curve",
        "mathematical_definition": "V(r) = -G m1 m2/r [1 + alpha(lambda) exp(-r/lambda)] or an explicitly mapped non-Yukawa fifth-force envelope",
        "units": "range-dependent",
        "source_bound": "alpha(lambda)",
        "GR_null_value": "0 curve",
        "current_MTS_status": "symbolic_curve_required",
        "theorem_zero_condition": "finite-range force coefficient is identically zero, screened locally by theorem, or supplied as a curve below data",
        "numeric_input_required": "curve file with lambda, alpha_predicted, alpha_bound, units",
        "failure_channel": "range-dependent fifth force",
        "claim_gate": "no scalar placeholder pass; curve required",
    },
    {
        "component_id": "r11_nonEH",
        "row_id": "R11_EH_operator_ledger",
        "observable": "non_EH_operator_coefficients",
        "MTS_output_name": "c_nonEH_operator_vector",
        "mathematical_definition": "coefficient vector for retained non-EH operator families: R^2/f(R), Ricci^2, Weyl^2, scalar, vector, torsion/nonmetricity, bulk, boundary, nonlocal/memory, source-normalization",
        "units": "operator family",
        "source_bound": "symbolic",
        "GR_null_value": "all non-EH coefficients zero or pure topological/boundary class with no local variation",
        "current_MTS_status": "retained_EH_operator_ledger",
        "theorem_zero_condition": "parent action selects EH+Lambda as the only local second-order exterior metric operator and forbids/materially blinds all retained families",
        "numeric_input_required": "operator coefficient vector file plus maps to R3/R4/R5/R6/R8/R10 where applicable",
        "failure_channel": "non-EH operator residue",
        "claim_gate": "symbolic operator row cannot pass without coefficient/vector map",
    },
]


PREDICTION_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "row_id": row["row_id"],
        "observable": row["observable"],
        "predicted_value": "",
        "one_sigma": "",
        "upper_envelope": "",
        "units": row["units"],
        "curve_or_vector_file": "required_for_R10_R11" if row["row_id"].startswith(("R10", "R11")) else "",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": row["mathematical_definition"],
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_EH_source_normalization_or_closure_assumptions",
        "comparison_role": "MTS_prediction",
        "claim_request": "none",
        "notes": row["claim_gate"],
    }
    for row in RESIDUAL_COMPONENTS
]


LOCAL_GR_PASS_REQUIREMENTS = [
    {
        "requirement": "same_frame_source",
        "mathematical_condition": "matter clocks, rulers, and gravitational operator use the same observed metric/coframe",
        "rows_controlled": "R0;R2;R3;R4;R11",
        "empirical_pass_condition": "all affected residuals below bounds",
        "derived_GR_condition": "condition follows from parent action, not closure",
    },
    {
        "requirement": "EH_operator_selection",
        "mathematical_condition": "non-EH local operator coefficients are zero, pure boundary/topological, or Ward-owned with no local variation",
        "rows_controlled": "R3;R4;R5;R6;R8;R10;R11",
        "empirical_pass_condition": "mapped residuals below bounds and R11 vector supplied",
        "derived_GR_condition": "R11 theorem-zero or exact coefficient map from parent action",
    },
    {
        "requirement": "source_residuals_zero",
        "mathematical_condition": "nabla^2 Phi = 4 pi G_eff rho_eff with source_residuals=0",
        "rows_controlled": "R1;R4;R7;R9;R10",
        "empirical_pass_condition": "source, beta, flux, drift, and fifth-force residuals below bounds",
        "derived_GR_condition": "Ward/Bianchi exchange owner kills q_loc^nu and mu_extra without axiom",
    },
    {
        "requirement": "measured_GM_normalized",
        "mathematical_condition": "mu_obs = G_eff M_eff is conserved, universal, species-independent, and range-independent",
        "rows_controlled": "R1;R4;R9;R10",
        "empirical_pass_condition": "eta_source, beta, Gdot, alpha(lambda) below bounds",
        "derived_GR_condition": "partial_A mu_obs = partial_t mu_obs = partial_lambda mu_obs = 0 by theorem",
    },
    {
        "requirement": "PPN_completion",
        "mathematical_condition": "gamma=1, beta=1, alpha1=alpha2=alpha3=xi=0 in the observed local weak-field branch",
        "rows_controlled": "R3;R4;R5;R6;R7;R8",
        "empirical_pass_condition": "PPN residual vector below sourced bounds",
        "derived_GR_condition": "second-order weak-field expansion reduces to GR, not only Poisson/Newton",
    },
    {
        "requirement": "symbolic_rows_resolved",
        "mathematical_condition": "alpha(lambda) curve and non-EH coefficient vector are supplied or theorem-zero",
        "rows_controlled": "R10;R11",
        "empirical_pass_condition": "curve/vector evaluator can compare against sourced constraints",
        "derived_GR_condition": "finite-range and non-EH channels vanish or are parent-forbidden",
    },
]


COMPARISON_RULES = [
    {
        "rule_id": "numeric_abs_compare",
        "applies_to": "R0-R9 numeric rows",
        "algorithm": "compare max(abs(predicted_value), abs(upper_envelope if supplied)) to sourced upper_bound in matching units",
        "pass_label": "empirical_residual_below_bound_no_GR_claim",
        "fail_label": "empirical_residual_exceeds_bound",
    },
    {
        "rule_id": "symbolic_curve_compare",
        "applies_to": "R10 fifth-force row",
        "algorithm": "load curve_or_vector_file with lambda and alpha_predicted(lambda), compare to alpha_bound(lambda) over declared range",
        "pass_label": "curve_below_bound_no_scalar_placeholder",
        "fail_label": "curve_missing_or_exceeds_bound",
    },
    {
        "rule_id": "operator_vector_compare",
        "applies_to": "R11 non-EH operator row",
        "algorithm": "load coefficient vector and require maps to affected PPN/fifth-force rows or theorem-zero proof",
        "pass_label": "operator_vector_mapped_no_symbolic_pass",
        "fail_label": "operator_vector_missing_or_unmapped",
    },
    {
        "rule_id": "derivation_status_gate",
        "applies_to": "all rows",
        "algorithm": "closure_assumed/speculative rows can be empirical stress tests but cannot support derived_local_GR_candidate",
        "pass_label": "derivation_status_allowed_for_requested_claim",
        "fail_label": "claim_request_exceeds_derivation_status",
    },
    {
        "rule_id": "all_rows_or_no_local_GR",
        "applies_to": "full vector",
        "algorithm": "derived local GR requires all 12 rows resolved plus same-frame/EH/source-normalization proofs",
        "pass_label": "derived_local_GR_candidate_maybe",
        "fail_label": "partial_vector_no_local_GR",
    },
]


DECISION = [
    {
        "decision": "The MTS local residual vector is now defined as a 12-component object aligned to the sourced local-bound evaluator. No MTS predictions were loaded. The next physics bottleneck is to derive or estimate the components, especially q_loc^nu/source_residuals/mu_extra and the R10/R11 symbolic rows.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "MTS_residuals_loaded": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "task": "attempt to derive q_loc^nu=0/source_residuals=0/mu_extra=0 from Ward/Bianchi exchange ownership",
        "priority": "P0",
    },
    {
        "next_file": "429-MTS-local-residual-vector-evaluator.md",
        "task": "build an evaluator that compares a filled MTS residual prediction CSV against sourced local bounds",
        "priority": "P0",
    },
    {
        "next_file": "429-R10-R11-curve-and-operator-vector-contract.md",
        "task": "define file formats for alpha(lambda) and non-EH coefficient vectors so symbolic rows can be tested",
        "priority": "P1",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": path.exists(),
                "role": item["role"],
            }
        )
    return rows


def bound_alignment_rows() -> list[dict[str, Any]]:
    digest_rows = read_csv(ROOT / "runs" / "20260602-093000-local-bound-runner-v4-evaluate-smoke" / "results" / "evaluation_digest.csv")
    digest_by_row = {row["row_id"]: row for row in digest_rows if row.get("row_id")}
    rows = []
    for component in RESIDUAL_COMPONENTS:
        digest = digest_by_row.get(component["row_id"], {})
        rows.append(
            {
                "row_id": component["row_id"],
                "observable": component["observable"],
                "component_bound": component["source_bound"],
                "evaluate_upper_bound": digest.get("upper_bound", ""),
                "evaluate_source_lock": digest.get("source_lock", ""),
                "evaluate_status": digest.get("data_bound_status", ""),
                "alignment_status": "pass" if digest and component["source_bound"] == digest.get("upper_bound", "") else "review",
            }
        )
    return rows


def template_health_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "MTS_local_residual_predictions_TEMPLATE.csv",
            "path": str(PREDICTION_TEMPLATE),
            "exists": PREDICTION_TEMPLATE.exists(),
            "row_count": len(PREDICTION_TEMPLATE_ROWS),
            "purpose": "blank prediction template; not MTS evidence",
        },
        {
            "artifact": "README.md",
            "path": str(RESIDUAL_INTAKE_DIR / "README.md"),
            "exists": (RESIDUAL_INTAKE_DIR / "README.md").exists(),
            "row_count": "",
            "purpose": "rules for filling MTS residual predictions",
        },
    ]


def gate_rows(
    source_rows: list[dict[str, Any]],
    alignment_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    alignment_reviews = [row for row in alignment_rows if row["alignment_status"] != "pass"]
    symbolic_components = [
        row for row in RESIDUAL_COMPONENTS if row["row_id"].startswith(("R10", "R11"))
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "residual_schema_written",
            "status": "pass" if len(RESIDUAL_SCHEMA) == 16 else "fail",
            "evidence": f"{len(RESIDUAL_SCHEMA)} schema columns",
        },
        {
            "gate": "twelve_component_vector_written",
            "status": "pass" if len(RESIDUAL_COMPONENTS) == 12 else "fail",
            "evidence": f"{len(RESIDUAL_COMPONENTS)} residual components",
        },
        {
            "gate": "prediction_template_written",
            "status": "pass" if PREDICTION_TEMPLATE.exists() else "fail",
            "evidence": str(PREDICTION_TEMPLATE),
        },
        {
            "gate": "bound_alignment_checked",
            "status": "pass" if not alignment_reviews else "review",
            "evidence": f"{len(alignment_reviews)} row-bound alignments need review",
        },
        {
            "gate": "symbolic_components_marked",
            "status": "pass" if len(symbolic_components) == 2 else "fail",
            "evidence": f"{len(symbolic_components)} symbolic/curve/vector components",
        },
        {
            "gate": "local_GR_pass_requirements_written",
            "status": "pass" if len(LOCAL_GR_PASS_REQUIREMENTS) == 6 else "fail",
            "evidence": f"{len(LOCAL_GR_PASS_REQUIREMENTS)} all-row requirements",
        },
        {
            "gate": "comparison_rules_written",
            "status": "pass" if len(COMPARISON_RULES) == 5 else "fail",
            "evidence": f"{len(COMPARISON_RULES)} comparison rules",
        },
        {
            "gate": "MTS_residuals_loaded",
            "status": "not_run",
            "evidence": "template only; no MTS prediction values supplied",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "input contract only; no WEP/EH/Newton/PPN/fifth-force pass",
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


def write_readme() -> None:
    RESIDUAL_INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    (RESIDUAL_INTAKE_DIR / "README.md").write_text(
        "\n".join(
            [
                "# MTS Local Residual Predictions",
                "",
                "Use `MTS_local_residual_predictions_TEMPLATE.csv` to supply actual MTS residual predictions for local-bound testing.",
                "",
                "Do not edit this into a claim file by filling zeros unless a derivation source exists for each zero. Closure-assumed, speculative, or fitted rows can be useful stress tests, but they cannot support a derived local-GR claim.",
                "",
                "Rows R10 and R11 require external curve/vector files. A scalar `0` or `symbolic` placeholder is not a valid fifth-force or non-EH-operator pass.",
            ]
        ),
        encoding="utf-8",
    )


def write_checkpoint_markdown(
    run_dir: Path,
    source_rows: list[dict[str, Any]],
    alignment_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    source_table_rows = [
        {
            "source_file": row["source_file"],
            "exists": row["exists"],
            "role": row["role"],
        }
        for row in source_rows
    ]
    component_table_rows = [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "MTS_output_name": row["MTS_output_name"],
            "source_bound": row["source_bound"],
            "current_MTS_status": row["current_MTS_status"],
        }
        for row in RESIDUAL_COMPONENTS
    ]
    pass_requirement_rows = [
        {
            "requirement": row["requirement"],
            "rows_controlled": row["rows_controlled"],
            "empirical_pass_condition": row["empirical_pass_condition"],
            "derived_GR_condition": row["derived_GR_condition"],
        }
        for row in LOCAL_GR_PASS_REQUIREMENTS
    ]
    comparison_table_rows = [
        {
            "rule_id": row["rule_id"],
            "applies_to": row["applies_to"],
            "algorithm": row["algorithm"],
            "fail_label": row["fail_label"],
        }
        for row in COMPARISON_RULES
    ]
    alignment_table_rows = [
        {
            "row_id": row["row_id"],
            "component_bound": row["component_bound"],
            "evaluate_upper_bound": row["evaluate_upper_bound"],
            "alignment_status": row["alignment_status"],
        }
        for row in alignment_rows
    ]
    template_table_rows = template_health_rows()
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 428 - MTS Local Residual Vector Input Contract

Private residual-input checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 427 proved the sourced local-bound evaluator can run. This checkpoint defines the missing physics object: the MTS local residual vector.

From this point on, a local-GR/Newton claim is not allowed to mean "the bounds file exists" or "Poisson algebra looks clean." It must mean MTS supplies a 12-component residual vector, with formula sources and derivation status, and that vector is either theorem-zero for the right reason or empirically below sourced bounds.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/MTS_local_residual_vector_input_contract.py` |
| Run directory | `runs/{run_dir.name}` |
| Prediction template | `source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_table_rows, ["source_file", "exists", "role"])}

## 4. The 12-Component Residual Vector

{markdown_table(component_table_rows, ["row_id", "observable", "MTS_output_name", "source_bound", "current_MTS_status"])}

Compactly:

```text
r_local =
(eta_geom, eta_source, alpha_clock, gamma-1, beta-1,
 alpha1, alpha2, alpha3, xi, dln(mu_obs)/dt, alpha(lambda), c_nonEH)
```

The first ten entries can be numeric scalars once a branch is specified. The last two are not scalar placeholders: `alpha(lambda)` is a curve and `c_nonEH` is an operator-coefficient/vector map.

## 5. Local-GR Pass Requirements

{markdown_table(pass_requirement_rows, ["requirement", "rows_controlled", "empirical_pass_condition", "derived_GR_condition"])}

This is the key distinction:

```text
empirical viability: residuals are below sourced bounds
derived local GR: same-frame + EH + source-normalization + PPN + symbolic rows are parent-derived
```

The first is a good Mayweather round. The second is the title belt.

## 6. Comparison Rules

{markdown_table(comparison_table_rows, ["rule_id", "applies_to", "algorithm", "fail_label"])}

## 7. Bound Alignment

{markdown_table(alignment_table_rows, ["row_id", "component_bound", "evaluate_upper_bound", "alignment_status"])}

## 8. Prediction Intake Artifacts

{markdown_table(template_table_rows, ["artifact", "exists", "row_count", "purpose"])}

## 9. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 10. Decision

{DECISION[0]["decision"]}

Practical read: the project now has a real empirical spine for the local-GR question. The testing side is no longer the bottleneck. The bottleneck is derivation: can MTS produce `source_residuals=0`, `mu_extra=0`, no preferred-frame/domain leakage, and a resolved R10/R11 curve/vector story without sneaking in GR?

## 11. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    alignment_rows = bound_alignment_rows()

    write_readme()
    write_csv(PREDICTION_TEMPLATE, PREDICTION_TEMPLATE_ROWS)
    template_rows = template_health_rows()
    gate_result_rows = gate_rows(source_rows, alignment_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "residual_vector_schema.csv", RESIDUAL_SCHEMA)
    write_csv(results_dir / "residual_components.csv", RESIDUAL_COMPONENTS)
    write_csv(results_dir / "prediction_template_rows.csv", PREDICTION_TEMPLATE_ROWS)
    write_csv(results_dir / "local_GR_pass_requirements.csv", LOCAL_GR_PASS_REQUIREMENTS)
    write_csv(results_dir / "comparison_rules.csv", COMPARISON_RULES)
    write_csv(results_dir / "bound_alignment.csv", alignment_rows)
    write_csv(results_dir / "template_health.csv", template_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    failed_gates = [row["gate"] for row in gate_result_rows if row["status"] == "fail" and row["gate"] != "local_GR_promoted"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "prediction_template": str(PREDICTION_TEMPLATE),
        "residual_components": len(RESIDUAL_COMPONENTS),
        "schema_columns": len(RESIDUAL_SCHEMA),
        "local_GR_pass_requirements": len(LOCAL_GR_PASS_REQUIREMENTS),
        "comparison_rules": len(COMPARISON_RULES),
        "MTS_residuals_loaded": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, source_rows, alignment_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the MTS local residual-vector input contract and prediction template."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
