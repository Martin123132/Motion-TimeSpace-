from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1067-parent-quantum-action-scale-normalization" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1067_WEP_TAU_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1067_WEP_TAU_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1067_0_1066_next", "source-intake/mts_residuals/P8_Y5_R10_1066_NEXT_TARGET.csv", "1067-Y5-R10-parent-quantum-action-scale-normalization", "1066 handoff."),
        ("SRC1067_1_1066_exclusion", "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_4_quantum_action_scale_obstruction", "source-scalar action-scale obstruction."),
        ("SRC1067_2_1066_fmq", "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_4_verdict", "field/measure/quantum audit."),
        ("SRC1067_3_1066_tau", "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_7_verdict", "tau_WEP projection contract."),
        ("SRC1067_4_1066_delta", "source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv", "DWP1066_4_tau_WEP", "Delta_w/tau prior schema."),
        ("SRC1067_5_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "tau_WEP definition source."),
        ("SRC1067_6_1061_derivation", "source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_2_tau_WEP", "tau_WEP derivation attempt."),
        ("SRC1067_7_742_owner", "source-intake/mts_residuals/P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv", "TOA742_4_owner_verdict", "observed tau owner audit."),
        ("SRC1067_8_742_verdict", "source-intake/mts_residuals/P8_Y5_R10_742_TAU_PROOF_VERDICT.csv", "TPV742_3_tau_owner_result", "tau proof verdict."),
        ("SRC1067_9_1029_reqs", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_3_WEP_limit", "tau projection requirements."),
        ("SRC1067_10_1033_tauR10", "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_5_universal_cg_limit", "tau unity shortcut rejection."),
        ("SRC1067_11_1055_parent", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_6_single_parent_action", "single parent action contract."),
        ("SRC1067_12_989_current", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "current normalization owner."),
        ("SRC1067_13_1047_hbar", "source-intake/mts_residuals/P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_0_definition", "hbar/readout ownership."),
        ("SRC1067_14_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention."),
        ("SRC1067_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "WEP source-charge bound."),
        ("SRC1067_16_393_common", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "common-mode measured-G guard."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def action_scale_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "ASO1067_0_target",
            "claim": "one parent action-scale/measure owner for all ordinary matter",
            "formal_statement": "S_parent/hbar_parent contains sum_A S_A with one shared hbar_parent and no species-dependent action weights.",
            "attempt_result": "TARGET_SHARPENED",
            "missing_for_claim": "parent derivation of common action measure and hbar/readout descent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "ASO1067_1_classical_EOM_vs_source",
            "claim": "classical equation redundancy is not source redundancy",
            "formal_statement": "delta(w_A S_A)/delta Psi_A=0 may reduce to delta S_A/delta Psi_A=0, but delta(w_A S_A)/delta g_obs = w_A T_A.",
            "attempt_result": "OBSTRUCTION_EXPLICIT",
            "missing_for_claim": "cannot dismiss w_A by classical EOM scaling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "ASO1067_2_path_integral_measure",
            "claim": "species action-scale factors are physical unless the quantum measure quotients them",
            "formal_statement": "exp(i sum_A w_A S_A / hbar_parent) is not equivalent to exp(i sum_A S_A / hbar_parent) without a parent measure theorem.",
            "attempt_result": "MEASURE_OWNER_REQUIRED",
            "missing_for_claim": "no parent statistical/path-integral measure owner in current corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "ASO1067_3_field_redefinition_limit",
            "claim": "field normalization cannot automatically remove source-only action weights",
            "formal_statement": "canonical field rescaling must preserve interactions, composite material parameters, Hilbert source, and quantum measure simultaneously.",
            "attempt_result": "NOT_CLOSED_BY_RESCALING",
            "missing_for_claim": "field-redefinition quotient with current/measure/readout ownership",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "ASO1067_4_species_blind_measure",
            "claim": "measure/coframe/Jacobian descent must be species blind",
            "formal_statement": "D_A log mu_parent = D_A log sqrt(-g_obs) = D_A log J_measure = 0 for source-only species labels.",
            "attempt_result": "CONDITIONAL_CLAUSE",
            "missing_for_claim": "species-blind measure/coframe descent theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "ASO1067_5_verdict",
            "claim": "parent quantum action-scale normalization closes w_A",
            "formal_statement": "single hbar_parent/action measure + species-blind Jacobian + current owner => no w_A S_A and Delta_w_AB=0",
            "attempt_result": "CONDITIONAL_NOT_PARENT_DERIVED",
            "missing_for_claim": "hbar/action-measure owner, current owner, and species-blind measure descent remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def hbar_measure_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "HMO1067_0_hbar_parent",
            "object": "hbar_parent",
            "required_signature": "one action quantum/phase normalization for all ordinary matter sectors",
            "current_status": "not_parent_owned",
            "risk_if_missing": "species-dependent effective hbar_A is equivalent to action-scale w_A",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "HMO1067_1_measure_parent",
            "object": "Dmu_parent or path-integral/statistical measure",
            "required_signature": "measure factorizes without species-dependent source-only Jacobians",
            "current_status": "not_parent_owned",
            "risk_if_missing": "J_A measure factors mimic w_A S_A",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "HMO1067_2_current_owner",
            "object": "Noether/current normalization",
            "required_signature": "same parent owner fixes matter current, charge labels, and source normalization",
            "current_status": "candidate_missing",
            "risk_if_missing": "current/source normalization can reintroduce beta_source or w_A",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "HMO1067_3_readout_descent",
            "object": "dimensionless readout including hbar*c and clocks",
            "required_signature": "readout constants are quotient-fixed or owned by one parent sector",
            "current_status": "unsigned_from_1047_989",
            "risk_if_missing": "action scale and EM/readout normalizations drift separately",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "HMO1067_4_verdict",
            "object": "single action-scale owner",
            "required_signature": "HMO1067_0 through HMO1067_3 all signed",
            "current_status": "OWNER_NOT_DERIVED",
            "risk_if_missing": "cannot promote Delta_w_AB=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_weight_consequence_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "SWC1067_0_common_action_scale",
            "case": "w_A=w_common for every species",
            "source_effect": "common source normalization only",
            "claim_status": "calibration_possible_if_393_guards_pass",
            "WEP_effect": "Delta_w_AB=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "SWC1067_1_relative_action_scale",
            "case": "w_A=w_common(1+epsilon_A)",
            "source_effect": "T_source=sum_A w_A T_A",
            "claim_status": "live_countermodel",
            "WEP_effect": "Delta_w_AB survives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "SWC1067_2_quantum_measure_factor",
            "case": "Dmu = product_A J_A Dpsi_A",
            "source_effect": "measure factor can act like species action weight",
            "claim_status": "retained_residual",
            "WEP_effect": "could generate composition source normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "SWC1067_3_theorem_zero_consequence",
            "case": "single parent action-scale owner signed",
            "source_effect": "w_A slot absent or gauge-quotiented to common mode",
            "claim_status": "conditional_future_theorem",
            "WEP_effect": "Delta_w_TiPt=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "SWC1067_4_verdict",
            "case": "current corpus",
            "source_effect": "relative action-scale branch not eliminated",
            "claim_status": "nonclaim",
            "WEP_effect": "finite Delta_w*tau_WEP branch remains",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_wep_functional_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "TWF1067_0_definition",
            "component": "tau_WEP functional",
            "formal_role": "tau_WEP maps a parent source residual to MICROSCOPE eta_AB in the selected observed frame",
            "required_input": "tau_WEP = F_WEP[T_source^Earth, orbit, e_obs, material tensor, force readout, Xhat normalization]",
            "current_status": "definition_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_1_source_worldtube",
            "component": "Earth/source worldtube",
            "formal_role": "normalizes the source leg of the relative source-weight field",
            "required_input": "source stress profile, Earth composition/source convention, same Hilbert source used for G calibration",
            "current_status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_2_orbit_average",
            "component": "MICROSCOPE orbit/environment average",
            "formal_role": "projects the source residual onto the measured differential acceleration channel",
            "required_input": "time/orbit averaging kernel and environmental/readout convention",
            "current_status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_3_material_tensor",
            "component": "Ti/Pt material/source response",
            "formal_role": "turns source-weight residual into a differential test-body response",
            "required_input": "full material tensor or theorem reducing it to Delta_w_TiPt convention",
            "current_status": "material_pair_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_4_force_readout",
            "component": "eta_AB force/readout map",
            "formal_role": "sets dimensions, sign convention, and absolute-value scoring",
            "required_input": "observed coframe force law, calibration convention, no-cancellation rule",
            "current_status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_5_Xhat_normalization",
            "component": "parent Xhat/chi_X normalization",
            "formal_role": "keeps tau_WEP compatible with clock/R10 branches",
            "required_input": "shared parent normalization or declared separate finite branch",
            "current_status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "TWF1067_6_verdict",
            "component": "tau_WEP projection",
            "formal_role": "scoreable WEP projection factor",
            "required_input": "all components TWF1067_1 through TWF1067_5",
            "current_status": "NOT_DERIVED_DO_NOT_SET_TO_ONE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_acquisition_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "acquisition_id": "TAQ1067_0_tau_zero_option",
            "quantity": "tau_WEP",
            "accepted_evidence": "parent theorem showing WEP projection is exactly silent",
            "current_value": "MISSING_THEOREM_ZERO",
            "units": "dimensionless",
            "blocks": "finite WEP product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "TAQ1067_1_tau_numeric_option",
            "quantity": "tau_WEP",
            "accepted_evidence": "numeric local source/orbit/readout integral with source path and units",
            "current_value": "MISSING_NUMERIC_PROJECTION",
            "units": "dimensionless",
            "blocks": "Delta_w prior-width calculation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "TAQ1067_2_delta_w_width_if_tau",
            "quantity": "abs(Delta_w_TiPt)_max",
            "accepted_evidence": "2.8e-15 / abs(tau_WEP) after tau_WEP is numeric and nonzero",
            "current_value": "MISSING_TAU_WEP",
            "units": "dimensionless",
            "blocks": "finite relative-source prior",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "TAQ1067_3_direct_product_option",
            "quantity": "P_WEP_relative_source_weight",
            "accepted_evidence": "direct parent product without splitting Delta_w and tau_WEP",
            "current_value": "MISSING_DIRECT_PRODUCT",
            "units": "dimensionless",
            "blocks": "runner comparison",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "TAQ1067_4_refusal_rule",
            "quantity": "tau_WEP/product row",
            "accepted_evidence": "reject unity shortcuts, relative-G absorption, cancellation, or unsourced hand-picked factors",
            "current_value": "REFUSAL_ACTIVE",
            "units": "not_applicable",
            "blocks": "false positives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1067_0_WEP_tau_projection_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_TAU_WEP_AND_DELTA_W_OR_DIRECT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10",
            "required_inputs": "tau_WEP theorem-zero or numeric projection;Delta_w_TiPt theorem-zero/numeric width OR direct product;source paths",
            "derivation_status": "MISSING_TAU_WEP_PROJECTION_AND_DELTA_W_PRODUCT",
            "valid_for_claim": "false",
            "notes": "1067 refuses to score WEP until tau_WEP is a sourced projection or a direct parent product is derived.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1067_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_nonclaim",
            "valid_for_claim": "true",
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction.",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1067_0_WEP_tau_projection_product",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "blocked_or_failed_rows": str(status.get("blocked_or_failed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1067_0_action_scale_owner",
            "claim": "one parent action-scale/measure owner forbids w_A",
            "gate_pass": "false",
            "reason": "hbar/action measure/current/readout owner remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1067_1_Delta_w_zero",
            "claim": "Delta_w_TiPt=0",
            "gate_pass": "false",
            "reason": "action-scale theorem-zero is conditional only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1067_2_tau_WEP_defined",
            "claim": "tau_WEP is derived or sourced",
            "gate_pass": "false",
            "reason": "source worldtube, orbit average, material tensor, force readout, and Xhat normalization are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1067_3_WEP_runner_score",
            "claim": "WEP product can be scored",
            "gate_pass": "false",
            "reason": "strict runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1067_4_local_GR_coupling",
            "claim": "local GR/Newton coupling source branch is derived",
            "gate_pass": "false",
            "reason": "action-scale and tau/source projection closures remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1067_0_action_scale_status",
            "decision": "action-scale owner route is the cleanest theorem path but remains unsigned",
            "because": "species action-scale factors affect Hilbert source and quantum measure even if classical EOM look unchanged",
            "next_action": "either derive parent hbar/measure owner or stop using theorem-zero for Delta_w",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1067_1_tau_status",
            "decision": "tau_WEP must become a real projection functional",
            "because": "old tau files define it but do not provide source worldtube, orbit averaging, material tensor, force readout, or Xhat normalization",
            "next_action": "build the tau_WEP source-worldtube/orbit/readout acquisition pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1067_2_best_next",
            "decision": "next target is WEP tau source-worldtube/orbit/readout pack",
            "because": "if action-scale owner does not close immediately, tau_WEP is the first finite-branch bottleneck",
            "next_action": "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md",
            "objective": "build the tau_WEP acquisition pack: source worldtube, MICROSCOPE orbit/readout convention, material response tensor, observed-frame force map, and direct-product fallback, without setting tau_WEP to one.",
            "include": "Earth/source profile requirements, MICROSCOPE orbit averaging, eta_AB readout convention, Ti/Pt material response, Xhat normalization, direct P_WEP product option, strict refusal gates",
            "exclude": "unity tau, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    action_owner: list[dict[str, str]],
    hbar_owner: list[dict[str, str]],
    source_consequence: list[dict[str, str]],
    tau_functional: list[dict[str, str]],
    tau_schema: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if condition else "fail", "detail": detail, "generated_utc": stamp()})

    add("V1067_1_sources_exist_and_needles", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "every cited source path exists and every source needle was found")
    add("V1067_2_action_owner_not_promoted", any(row["owner_id"] == "ASO1067_5_verdict" and row["attempt_result"] == "CONDITIONAL_NOT_PARENT_DERIVED" for row in action_owner), "action-scale owner route remains conditional")
    add("V1067_3_hbar_owner_missing", any(row["audit_id"] == "HMO1067_4_verdict" and row["current_status"] == "OWNER_NOT_DERIVED" for row in hbar_owner), "single hbar/action-measure owner is not derived")
    add("V1067_4_relative_weight_retained", any(row["row_id"] == "SWC1067_1_relative_action_scale" and row["claim_status"] == "live_countermodel" for row in source_consequence), "relative action-scale countermodel is retained")
    add("V1067_5_tau_functional_missing", any(row["component_id"] == "TWF1067_6_verdict" and row["current_status"] == "NOT_DERIVED_DO_NOT_SET_TO_ONE" for row in tau_functional), "tau_WEP functional is not derived and unity shortcut is rejected")
    add("V1067_6_tau_acquisition_schema_written", len(tau_schema) >= 5 and any(row["acquisition_id"] == "TAQ1067_1_tau_numeric_option" and "MISSING" in row["current_value"] for row in tau_schema), "tau_WEP acquisition schema is written with missing numeric projection")
    add("V1067_7_prediction_nonclaim", len(predictions) == 1 and "MISSING" in predictions[0]["product_value"] and predictions[0]["valid_for_claim"] == "false", "WEP tau product prediction remains nonclaim")
    try:
        bound_numeric = len(bounds) == 1 and float(bounds[0]["bound_value"]) > 0
    except (KeyError, ValueError):
        bound_numeric = False
    add("V1067_8_bound_anchor_numeric", bound_numeric and bounds[0]["valid_for_claim"] == "true", "WEP bound anchor is numeric")
    add("V1067_9_runner_refuses_placeholder", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "strict runner refuses missing tau/Delta_w product")
    add("V1067_10_claim_gates_blocked", bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims), "all action-scale/tau/WEP claim gates remain blocked")
    add("V1067_11_next_target_written", bool(next_rows) and next_rows[0]["next_target"].startswith("1068-Y5-R10-WEP-tau-source-worldtube"), "next target selects tau_WEP acquisition pack")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1067_12_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1067_13_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")
    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1067_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1067 parent action-scale normalization / WEP tau projection validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    action_owner: list[dict[str, str]],
    hbar_owner: list[dict[str, str]],
    source_consequence: list[dict[str, str]],
    tau_functional: list[dict[str, str]],
    tau_schema: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1067 — Parent Quantum Action-Scale Normalization Or WEP tau Projection",
            "",
            "**Current verdict:** the action-scale route is clean but still unsigned. A species multiplier `w_A S_A` cannot be waved away by classical EOM scaling because it rescales Hilbert source and quantum/statistical weight.",
            "",
            "**Finite branch:** `tau_WEP` is still only a definition. To score WEP, it must become a sourced functional of Earth/source profile, orbit average, observed frame, material tensor, force readout, and Xhat normalization.",
            "",
            "**Runner result:** the WEP product row remains nonclaim and the strict runner refuses it with `valid_prediction_rows=0`.",
            "",
            "## Parent Action-Scale Owner Attempt",
            md_table(action_owner, ["owner_id", "claim", "formal_statement", "attempt_result", "missing_for_claim", "valid_for_claim"]),
            "",
            "## hbar / Measure Owner Audit",
            md_table(hbar_owner, ["audit_id", "object", "required_signature", "current_status", "risk_if_missing", "valid_for_claim"]),
            "",
            "## Source Weight Consequences",
            md_table(source_consequence, ["row_id", "case", "source_effect", "claim_status", "WEP_effect", "valid_for_claim"]),
            "",
            "## tau_WEP Functional Decomposition",
            md_table(tau_functional, ["component_id", "component", "formal_role", "required_input", "current_status", "valid_for_claim"]),
            "",
            "## tau_WEP Acquisition Schema",
            md_table(tau_schema, ["acquisition_id", "quantity", "accepted_evidence", "current_value", "units", "blocks", "valid_for_claim"]),
            "",
            "## WEP Product Candidate",
            md_table(predictions, PRODUCT_REQUIRED_COLUMNS),
            "",
            "## WEP Bound Import",
            md_table(bounds, BOUND_REQUIRED_COLUMNS),
            "",
            "## Runner Status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc"]),
            "",
            "## Runner Comparisons",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Source Register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle", "needle_found", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    action_owner = action_scale_owner_rows()
    hbar_owner = hbar_measure_owner_rows()
    source_consequence = source_weight_consequence_rows()
    tau_functional = tau_wep_functional_rows()
    tau_schema = tau_acquisition_schema_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1067_SOURCE_REGISTER.csv",
        "action_owner": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
        "hbar_owner": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
        "source_consequence": OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
        "tau_functional": OUT / "P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv",
        "tau_schema": OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1067_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1067_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1067_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1067_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1067_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1067_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["action_owner"], action_owner)
    write_csv(outputs["hbar_owner"], hbar_owner)
    write_csv(outputs["source_consequence"], source_consequence)
    write_csv(outputs["tau_functional"], tau_functional)
    write_csv(outputs["tau_schema"], tau_schema)
    write_csv(outputs["predictions"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bounds"], bounds, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claim_gates"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])

    validation = validate_outputs(
        outputs,
        sources,
        action_owner,
        hbar_owner,
        source_consequence,
        tau_functional,
        tau_schema,
        predictions,
        bounds,
        product_status,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        action_owner,
        hbar_owner,
        source_consequence,
        tau_functional,
        tau_schema,
        predictions,
        bounds,
        product_status_rows_,
        product_result["comparisons"],
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
