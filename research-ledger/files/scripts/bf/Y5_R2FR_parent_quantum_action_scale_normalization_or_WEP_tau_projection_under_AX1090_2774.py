from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2774-Y5-R2FR-parent-quantum-action-scale-normalization-or-WEP-tau-projection-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2774_SOURCE_REGISTER.csv",
    "owner": MTS / "P8_Y5_R2FR_2774_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "hbar": MTS / "P8_Y5_R2FR_2774_HBAR_MEASURE_OWNER_AUDIT.csv",
    "consequence": MTS / "P8_Y5_R2FR_2774_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
    "tau_functional": MTS / "P8_Y5_R2FR_2774_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv",
    "tau_acquisition": MTS / "P8_Y5_R2FR_2774_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "candidate": MTS / "P8_Y5_R2FR_2774_WEP_TAU_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2774_WEP_TAU_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2774_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2774_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2774_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2774_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2774_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2774_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2774_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_queue": RAB_QUEUE / "JR2774_ACTION_SCALE_OWNER_NONCLAIM.csv",
    "tau_queue": RAB_QUEUE / "JR2774_WEP_TAU_ACQUISITION_SCHEMA_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "ACTION_SCALE_OWNER_2774_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "wep_tau_projection_2774_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2774_WEP_TAU_ACQUISITION_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2774_00_2773_next", "2773_next", MTS / "P8_Y5_R2FR_2773_NEXT_TARGET.csv", "NEXT2773_0_2774", "current handoff into action-scale/tau checkpoint"),
        ("SRC2774_01_2773_exclusion", "2773_exclusion", MTS / "P8_Y5_R2FR_2773_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE2773_4_quantum_action_scale_obstruction", "current action-scale obstruction"),
        ("SRC2774_02_2773_normalization", "2773_normalization", MTS / "P8_Y5_R2FR_2773_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ2773_4_verdict", "current normalization closure failure"),
        ("SRC2774_03_2773_tau", "2773_tau", MTS / "P8_Y5_R2FR_2773_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP2773_7_verdict", "current tau_WEP projection contract"),
        ("SRC2774_04_2773_delta", "2773_delta", MTS / "P8_Y5_R2FR_2773_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv", "DWP2773_4_tau_WEP", "current Delta_w/tau prior schema"),
        ("SRC2774_05_1067_doc", "1067_doc", WORK / "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md", "ASO1067_5_verdict", "prior R10 action-scale/tau template"),
        ("SRC2774_06_1067_owner", "1067_owner", MTS / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "prior parent action-scale owner attempt"),
        ("SRC2774_07_1067_hbar", "1067_hbar", MTS / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv", "HMO1067_4_verdict", "prior hbar/measure owner audit"),
        ("SRC2774_08_1067_tau", "1067_tau", MTS / "P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv", "TWF1067_6_verdict", "prior tau functional decomposition"),
        ("SRC2774_09_1053_tau", "1053_tau", MTS / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "tau_WEP definition-only source"),
        ("SRC2774_10_1061_derivation", "1061_derivation", MTS / "P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_2_tau_WEP", "tau derivation attempt"),
        ("SRC2774_11_742_owner", "742_owner", MTS / "P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv", "TOA742_4_owner_verdict", "observed tau owner audit"),
        ("SRC2774_12_742_verdict", "742_verdict", MTS / "P8_Y5_R10_742_TAU_PROOF_VERDICT.csv", "TPV742_3_tau_owner_result", "tau proof verdict"),
        ("SRC2774_13_1029_reqs", "1029_requirements", MTS / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_3_WEP_limit", "WEP tau projection requirement"),
        ("SRC2774_14_1033_tauR10", "1033_tauR10", MTS / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_5_universal_cg_limit", "unity tau shortcut rejection"),
        ("SRC2774_15_1055_parent", "1055_parent", MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_6_single_parent_action", "single parent action candidate"),
        ("SRC2774_16_989_current", "989_current", MTS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "current/source owner gap"),
        ("SRC2774_17_1047_hbar", "1047_hbar", MTS / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_0_definition", "hbar/readout normalization audit"),
        ("SRC2774_18_1061_material", "1061_material", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention"),
        ("SRC2774_19_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound anchor"),
        ("SRC2774_20_393_common", "393_common", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard"),
    ]
    rows = []
    for row_id, source_key, path, needle, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": exists and needle in text,
            "source_role": role,
        }))
    return rows


def build_owner_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"owner_id": "ASO2774_0_target", "claim": "one parent action-scale/measure owner for all ordinary matter", "formal_statement": "S_parent/hbar_parent contains sum_A S_A with one shared hbar_parent and no species-dependent action weights.", "attempt_result": "TARGET_SHARPENED", "missing_for_claim": "parent derivation of common action measure and hbar/readout descent"}),
        nonclaim({"owner_id": "ASO2774_1_classical_EOM_vs_source", "claim": "classical equation redundancy is not source redundancy", "formal_statement": "delta(w_A S_A)/delta Psi_A=0 may reduce to delta S_A/delta Psi_A=0, but delta(w_A S_A)/delta g_obs = w_A T_A.", "attempt_result": "OBSTRUCTION_EXPLICIT", "missing_for_claim": "cannot dismiss w_A by classical EOM scaling"}),
        nonclaim({"owner_id": "ASO2774_2_path_integral_measure", "claim": "species action-scale factors are physical unless the quantum measure quotients them", "formal_statement": "exp(i sum_A w_A S_A / hbar_parent) is not equivalent to exp(i sum_A S_A / hbar_parent) without a parent measure theorem.", "attempt_result": "MEASURE_OWNER_REQUIRED", "missing_for_claim": "no parent statistical/path-integral measure owner in current corpus"}),
        nonclaim({"owner_id": "ASO2774_3_field_redefinition_limit", "claim": "field normalization cannot automatically remove source-only action weights", "formal_statement": "canonical field rescaling must preserve interactions, composite material parameters, Hilbert source, and quantum measure simultaneously.", "attempt_result": "NOT_CLOSED_BY_RESCALING", "missing_for_claim": "field-redefinition quotient with current/measure/readout ownership"}),
        nonclaim({"owner_id": "ASO2774_4_species_blind_measure", "claim": "measure/coframe/Jacobian descent must be species blind", "formal_statement": "D_A log mu_parent = D_A log sqrt(-g_obs) = D_A log J_measure = 0 for source-only species labels.", "attempt_result": "CONDITIONAL_CLAUSE", "missing_for_claim": "species-blind measure/coframe descent theorem"}),
        nonclaim({"owner_id": "ASO2774_5_verdict", "claim": "parent quantum action-scale normalization closes w_A", "formal_statement": "single hbar_parent/action measure + species-blind Jacobian + current owner => no w_A S_A and Delta_w_AB=0", "attempt_result": "CONDITIONAL_NOT_PARENT_DERIVED", "missing_for_claim": "hbar/action-measure owner, current owner, and species-blind measure descent remain unsigned"}),
    ]


def build_hbar_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"audit_id": "HMO2774_0_hbar_parent", "object": "hbar_parent", "required_signature": "one action quantum/phase normalization for all ordinary matter sectors", "current_status": "not_parent_owned", "risk_if_missing": "species-dependent effective hbar_A is equivalent to action-scale w_A"}),
        nonclaim({"audit_id": "HMO2774_1_measure_parent", "object": "Dmu_parent or path-integral/statistical measure", "required_signature": "measure factorizes without species-dependent source-only Jacobians", "current_status": "not_parent_owned", "risk_if_missing": "J_A measure factors mimic w_A S_A"}),
        nonclaim({"audit_id": "HMO2774_2_current_owner", "object": "Noether/current normalization", "required_signature": "same parent owner fixes matter current, charge labels, and source normalization", "current_status": "candidate_missing", "risk_if_missing": "current/source normalization can reintroduce beta_source or w_A"}),
        nonclaim({"audit_id": "HMO2774_3_readout_descent", "object": "dimensionless readout including hbar*c and clocks", "required_signature": "readout constants are quotient-fixed or owned by one parent sector", "current_status": "unsigned_from_1047_989", "risk_if_missing": "action scale and EM/readout normalizations drift separately"}),
        nonclaim({"audit_id": "HMO2774_4_verdict", "object": "single action-scale owner", "required_signature": "HMO2774_0 through HMO2774_3 all signed", "current_status": "OWNER_NOT_DERIVED", "risk_if_missing": "cannot promote Delta_w_AB=0"}),
    ]


def build_consequence_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "SWC2774_0_common_action_scale", "case": "w_A=w_common for every species", "source_effect": "common source normalization only", "claim_status": "calibration_possible_if_393_guards_pass", "WEP_effect": "Delta_w_AB=0"}),
        nonclaim({"row_id": "SWC2774_1_relative_action_scale", "case": "w_A=w_common(1+epsilon_A)", "source_effect": "T_source=sum_A w_A T_A", "claim_status": "live_countermodel", "WEP_effect": "Delta_w_AB survives"}),
        nonclaim({"row_id": "SWC2774_2_quantum_measure_factor", "case": "Dmu = product_A J_A Dpsi_A", "source_effect": "measure factor can act like species action weight", "claim_status": "retained_residual", "WEP_effect": "could generate composition source normalization"}),
        nonclaim({"row_id": "SWC2774_3_theorem_zero_consequence", "case": "single parent action-scale owner signed", "source_effect": "w_A slot absent or gauge-quotiented to common mode", "claim_status": "conditional_future_theorem", "WEP_effect": "Delta_w_TiPt=0"}),
        nonclaim({"row_id": "SWC2774_4_verdict", "case": "current corpus", "source_effect": "relative action-scale branch not eliminated", "claim_status": "nonclaim", "WEP_effect": "finite Delta_w*tau_WEP branch remains"}),
    ]


def build_tau_functional_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"component_id": "TWF2774_0_definition", "component": "tau_WEP functional", "formal_role": "tau_WEP maps a parent source residual to MICROSCOPE eta_AB in the selected observed frame", "required_input": "tau_WEP = F_WEP[T_source^Earth, orbit, e_obs, material tensor, force readout, Xhat normalization]", "current_status": "definition_only"}),
        nonclaim({"component_id": "TWF2774_1_source_worldtube", "component": "Earth/source worldtube", "formal_role": "normalizes the source leg of the relative source-weight field", "required_input": "source stress profile, Earth composition/source convention, same Hilbert source used for G calibration", "current_status": "missing"}),
        nonclaim({"component_id": "TWF2774_2_orbit_average", "component": "MICROSCOPE orbit/environment average", "formal_role": "projects the source residual onto the measured differential acceleration channel", "required_input": "time/orbit averaging kernel and environmental/readout convention", "current_status": "missing"}),
        nonclaim({"component_id": "TWF2774_3_material_tensor", "component": "Ti/Pt material/source response", "formal_role": "turns source-weight residual into a differential test-body response", "required_input": "full material tensor or theorem reducing it to Delta_w_TiPt convention", "current_status": "material_pair_only"}),
        nonclaim({"component_id": "TWF2774_4_force_readout", "component": "eta_AB force/readout map", "formal_role": "sets dimensions, sign convention, and absolute-value scoring", "required_input": "observed coframe force law, calibration convention, no-cancellation rule", "current_status": "missing"}),
        nonclaim({"component_id": "TWF2774_5_Xhat_normalization", "component": "parent Xhat/chi_X normalization", "formal_role": "keeps tau_WEP compatible with clock/R10 branches", "required_input": "shared parent normalization or declared separate finite branch", "current_status": "missing"}),
        nonclaim({"component_id": "TWF2774_6_verdict", "component": "tau_WEP projection", "formal_role": "scoreable WEP projection factor", "required_input": "all components TWF2774_1 through TWF2774_5", "current_status": "NOT_DERIVED_DO_NOT_SET_TO_ONE"}),
    ]


def build_tau_acquisition_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"acquisition_id": "TAQ2774_0_tau_zero_option", "quantity": "tau_WEP", "accepted_evidence": "parent theorem showing WEP projection is exactly silent", "current_value": "MISSING_THEOREM_ZERO", "units": "dimensionless", "blocks": "finite WEP product scoring"}),
        nonclaim({"acquisition_id": "TAQ2774_1_tau_numeric_option", "quantity": "tau_WEP", "accepted_evidence": "numeric local source/orbit/readout integral with source path and units", "current_value": "MISSING_NUMERIC_PROJECTION", "units": "dimensionless", "blocks": "Delta_w prior-width calculation"}),
        nonclaim({"acquisition_id": "TAQ2774_2_delta_w_width_if_tau", "quantity": "abs(Delta_w_TiPt)_max", "accepted_evidence": "2.8e-15 / abs(tau_WEP) after tau_WEP is numeric and nonzero", "current_value": "MISSING_TAU_WEP", "units": "dimensionless", "blocks": "finite relative-source prior"}),
        nonclaim({"acquisition_id": "TAQ2774_3_direct_product_option", "quantity": "P_WEP_relative_source_weight", "accepted_evidence": "direct parent product without splitting Delta_w and tau_WEP", "current_value": "MISSING_DIRECT_PRODUCT", "units": "dimensionless", "blocks": "runner comparison"}),
        nonclaim({"acquisition_id": "TAQ2774_4_refusal_rule", "quantity": "tau_WEP/product row", "accepted_evidence": "reject unity shortcuts, relative-G absorption, cancellation, or unsourced hand-picked factors", "current_value": "REFUSAL_ACTIVE", "units": "not_applicable", "blocks": "false positives"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2774_0_WEP_tau_projection_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_TAU_WEP_AND_DELTA_W_OR_DIRECT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": rel(OUTPUTS["tau_acquisition"]),
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10",
            "required_inputs": "tau_WEP theorem-zero or numeric projection;Delta_w_TiPt theorem-zero/numeric width OR direct product;source paths",
            "derivation_status": "MISSING_TAU_WEP_PROJECTION_AND_DELTA_W_PRODUCT",
            "notes": "2774 refuses to score WEP until tau_WEP is a sourced projection or a direct parent product is derived.",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "bound_id": "BOUND2774_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": rel(LOCAL_BOUNDS / "local_bound_claims.csv"),
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_internal_runner_only",
            "bound_valid_for_internal_runner": True,
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction.",
        })
    ]


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if row.get("bound_valid_for_internal_runner") is True
        and is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [
        nonclaim({
            "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
            "arena": "",
            "product_symbol": "",
            "product_value": "",
            "bound_value": "",
            "comparison_status": "not_run",
            "pass_for_claim": False,
            "issues": "no valid MTS tau/Delta_w WEP product prediction rows",
        })
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2774_0_WEP_tau_projection_product",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "comparison_rows": len(comparisons),
            "passed_rows": 0,
            "blocked_or_failed_rows": len(comparisons),
            "claim_allowed": False,
            "generated_utc": ts(),
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2774_0_action_scale_owner", "claim": "one parent action-scale/measure owner forbids w_A", "gate_pass": False, "reason": "hbar/action measure/current/readout owner remains unsigned", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2774_1_Delta_w_zero", "claim": "Delta_w_TiPt=0", "gate_pass": False, "reason": "action-scale theorem-zero is conditional only", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2774_2_tau_WEP_defined", "claim": "tau_WEP is derived or sourced", "gate_pass": False, "reason": "source worldtube, orbit average, material tensor, force readout, and Xhat normalization are missing", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2774_3_WEP_runner_score", "claim": "WEP product can be scored", "gate_pass": False, "reason": "strict runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2774_4_local_GR_coupling", "claim": "local GR/Newton coupling source branch is derived", "gate_pass": False, "reason": "action-scale and tau/source projection closures remain open", "claim_allowed": False}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2774_0_action_scale_status", "decision": "action-scale owner route is the cleanest theorem path but remains unsigned", "because": "species action-scale factors affect Hilbert source and quantum measure even if classical EOM look unchanged", "next_action": "either derive parent hbar/measure owner or stop using theorem-zero for Delta_w"}),
        nonclaim({"decision_id": "DEC2774_1_tau_status", "decision": "tau_WEP must become a real projection functional", "because": "old tau files define it but do not provide source worldtube, orbit averaging, material tensor, force readout, or Xhat normalization", "next_action": "build the tau_WEP source-worldtube/orbit/readout acquisition pack"}),
        nonclaim({"decision_id": "DEC2774_2_best_next", "decision": "next target is WEP tau source-worldtube/orbit/readout pack", "because": "if action-scale owner does not close immediately, tau_WEP is the first finite-branch bottleneck", "next_action": "2775-Y5-R2FR-WEP-tau-source-worldtube-orbit-readout-acquisition-pack-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2774_0_2775",
            "next_target": "2775-Y5-R2FR-WEP-tau-source-worldtube-orbit-readout-acquisition-pack-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WEP_tau_source_worldtube_orbit_readout_acquisition_pack_under_AX1090_2775.py",
            "objective": "build the tau_WEP acquisition pack: source worldtube, MICROSCOPE orbit/readout convention, material response tensor, observed-frame force map, and direct-product fallback, without setting tau_WEP to one",
            "include": "Earth/source profile requirements, MICROSCOPE orbit averaging, eta_AB readout convention, Ti/Pt material response, Xhat normalization, direct P_WEP product option, strict refusal gates",
            "exclude": "unity tau, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    owner: list[dict[str, Any]],
    hbar: list[dict[str, Any]],
    consequence: list[dict[str, Any]],
    tau_functional: list[dict[str, Any]],
    tau_acquisition: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    owner_rows = owner + hbar + consequence + gates
    tau_rows = tau_functional + tau_acquisition + candidate + bounds + gates
    beta_rows = owner + hbar + next_rows
    microscope_rows = tau_functional + tau_acquisition + candidate + bounds + next_rows
    specs = [
        ("BR2774_0_owner_queue", "owner", owner_rows, OUTPUTS["owner"], BRANCH_OUTPUTS["owner_queue"], "action-scale owner nonclaim copy"),
        ("BR2774_1_tau_queue", "tau", tau_rows, OUTPUTS["tau_acquisition"], BRANCH_OUTPUTS["tau_queue"], "WEP tau acquisition schema nonclaim copy"),
        ("BR2774_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["hbar"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing action-scale owner copy"),
        ("BR2774_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE tau projection copy"),
        ("BR2774_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next tau acquisition target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    owner = rows_by_name["owner"]
    hbar = rows_by_name["hbar"]
    consequence = rows_by_name["consequence"]
    tau_functional = rows_by_name["tau_functional"]
    tau_acquisition = rows_by_name["tau_acquisition"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2774_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2774_1_action_owner_not_promoted", any(row["owner_id"] == "ASO2774_5_verdict" and row["attempt_result"] == "CONDITIONAL_NOT_PARENT_DERIVED" for row in owner), "action-scale owner route remains conditional"),
        ("VAL2774_2_hbar_owner_missing", any(row["audit_id"] == "HMO2774_4_verdict" and row["current_status"] == "OWNER_NOT_DERIVED" for row in hbar), "single hbar/action-measure owner is not derived"),
        ("VAL2774_3_relative_weight_retained", any(row["row_id"] == "SWC2774_1_relative_action_scale" and row["claim_status"] == "live_countermodel" for row in consequence), "relative action-scale countermodel is retained"),
        ("VAL2774_4_tau_functional_missing", any(row["component_id"] == "TWF2774_6_verdict" and row["current_status"] == "NOT_DERIVED_DO_NOT_SET_TO_ONE" for row in tau_functional), "tau_WEP functional is not derived and unity shortcut is rejected"),
        ("VAL2774_5_tau_acquisition_schema_written", any(row["acquisition_id"] == "TAQ2774_1_tau_numeric_option" and "MISSING" in row["current_value"] for row in tau_acquisition), "tau_WEP acquisition schema is written with missing numeric projection"),
        ("VAL2774_6_prediction_nonclaim", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "WEP tau product prediction remains nonclaim"),
        ("VAL2774_7_bound_anchor_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True and bounds[0]["valid_for_claim"] is False, "WEP bound anchor is numeric and internal-runner only"),
        ("VAL2774_8_runner_refuses_placeholder", runner[0]["valid_prediction_rows"] == 0 and runner[0]["valid_bound_rows"] == 1 and runner[0]["claim_allowed"] is False, "strict runner refuses missing tau/Delta_w product"),
        ("VAL2774_9_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all action-scale/tau/WEP claim gates remain blocked"),
        ("VAL2774_10_next_target_written", any(row["row_id"] == "NEXT2774_0_2775" and "tau-source-worldtube" in row["next_target"] for row in next_rows), "next target selects tau_WEP acquisition pack"),
        ("VAL2774_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2774_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2774_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2774_14_generated_files_in_post_checkpoint", generated_files_under_work(), "all generated files are under post-checkpoint-work"),
        ("VAL2774_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2774_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2774_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2774 ports the parent quantum action-scale normalization gate into the current R2/f(R) branch, shows w_A cannot be removed by classical EOM rescaling alone, keeps hbar/action-measure/current/readout ownership unsigned, writes the tau_WEP functional/acquisition schema, refuses missing tau/Delta_w placeholders, blocks WEP/local-GR claims, and selects the tau source-worldtube/orbit/readout acquisition pack as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2774 - Y5 R2/f(R): Parent Quantum Action-Scale Normalization Or WEP tau Projection Under AX1090",
        "## Private Verdict\n\nThe action-scale route remains the cleanest theorem path, but it is still unsigned. A species multiplier `w_A S_A` cannot be waved away by classical EOM scaling because it rescales Hilbert source and quantum/statistical weight.\n\nFinite branch: `tau_WEP` is still only a definition. To score WEP, it must become a sourced functional of Earth/source profile, orbit average, observed frame, material tensor, force readout, and Xhat normalization.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Parent Action-Scale Owner Attempt\n\n" + markdown_table(rows_by_name["owner"], ["owner_id", "claim", "formal_statement", "attempt_result", "missing_for_claim", "valid_for_claim"]),
        "## hbar / Measure Owner Audit\n\n" + markdown_table(rows_by_name["hbar"], ["audit_id", "object", "required_signature", "current_status", "risk_if_missing", "valid_for_claim"]),
        "## Source Weight Consequences\n\n" + markdown_table(rows_by_name["consequence"], ["row_id", "case", "source_effect", "claim_status", "WEP_effect", "valid_for_claim"]),
        "## tau_WEP Functional Decomposition\n\n" + markdown_table(rows_by_name["tau_functional"], ["component_id", "component", "formal_role", "required_input", "current_status", "valid_for_claim"]),
        "## tau_WEP Acquisition Schema\n\n" + markdown_table(rows_by_name["tau_acquisition"], ["acquisition_id", "quantity", "accepted_evidence", "current_value", "units", "blocks", "valid_for_claim"]),
        "## WEP Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes"]),
        "## WEP Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim", "notes"]),
        "## Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc", "valid_for_claim"]),
        "## Runner Comparisons\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThe win condition is crisp: prove one universal action-measure owner and `w_A` becomes a fake degree of freedom. Until then, the finite branch must be handled honestly through a real `tau_WEP` projection pack. No `tau=1`, no hiding relative weights in measured `G`, no cancellation fairy dust.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    owner = build_owner_rows()
    hbar = build_hbar_rows()
    consequence = build_consequence_rows()
    tau_functional = build_tau_functional_rows()
    tau_acquisition = build_tau_acquisition_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("owner", owner), ("hbar", hbar), ("consequence", consequence),
        ("tau_functional", tau_functional), ("tau_acquisition", tau_acquisition),
        ("candidate", candidate), ("bounds", bounds), ("runner", runner), ("comparisons", comparisons),
        ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(owner, hbar, consequence, tau_functional, tau_acquisition, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "owner": owner,
        "hbar": hbar,
        "consequence": consequence,
        "tau_functional": tau_functional,
        "tau_acquisition": tau_acquisition,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2774_OVERALL")
    print(f"2774 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
