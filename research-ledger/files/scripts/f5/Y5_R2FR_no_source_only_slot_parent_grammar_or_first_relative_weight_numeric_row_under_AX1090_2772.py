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
DOC = WORK / "2772-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2772_SOURCE_REGISTER.csv",
    "grammar": MTS / "P8_Y5_R2FR_2772_PARENT_GRAMMAR_AUDIT.csv",
    "allowed": MTS / "P8_Y5_R2FR_2772_ALLOWED_ACTION_GRAMMAR.csv",
    "field": MTS / "P8_Y5_R2FR_2772_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv",
    "charge": MTS / "P8_Y5_R2FR_2772_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
    "zero": MTS / "P8_Y5_R2FR_2772_WA_THEOREM_ZERO_CLAUSES.csv",
    "wep_schema": MTS / "P8_Y5_R2FR_2772_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
    "candidate": MTS / "P8_Y5_R2FR_2772_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2772_WEP_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2772_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2772_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2772_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2772_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2772_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2772_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2772_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "grammar_queue": RAB_QUEUE / "JR2772_NO_SOURCE_ONLY_SLOT_GRAMMAR_NONCLAIM.csv",
    "wep_queue": RAB_QUEUE / "JR2772_FIRST_WEP_RELATIVE_WEIGHT_ROW_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "NO_SOURCE_ONLY_SLOT_2772_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "first_wep_relative_weight_row_2772_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2772_SOURCE_SCALAR_EXCLUSION_NEXT.csv",
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
        ("SRC2772_00_2771_next", "2771_next", MTS / "P8_Y5_R2FR_2771_NEXT_TARGET.csv", "NEXT2771_0_2772", "current handoff into no-source-only-slot target"),
        ("SRC2772_01_2771_proof", "2771_proof", MTS / "P8_Y5_R2FR_2771_LABEL_FORGETTING_PROOF_ATTEMPT.csv", "PLF2771_5_verdict", "current label-forgetting proof verdict"),
        ("SRC2772_02_2771_slot", "2771_slot", MTS / "P8_Y5_R2FR_2771_NO_SOURCE_ONLY_SLOT_AUDIT.csv", "NSS2771_2_relative_weight", "current surviving relative source-weight countermodel"),
        ("SRC2772_03_2771_requirements", "2771_requirements", MTS / "P8_Y5_R2FR_2771_NUMERIC_SOURCE_REQUIREMENTS.csv", "REQ2771_0_WEP_species", "current WEP numeric/source requirement"),
        ("SRC2772_04_2771_guard", "2771_guard", MTS / "P8_Y5_R2FR_2771_COMMON_MODE_GUARD.csv", "CMG2771_0_common_absorption", "current measured-G common-mode guard"),
        ("SRC2772_05_2771_template", "2771_template", MTS / "P8_Y5_R2FR_2771_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv", "PRED2771_0_WEP_relative_source_weight", "current WEP relative-weight product placeholder"),
        ("SRC2772_06_2771_bound", "2771_bound", MTS / "P8_Y5_R2FR_2771_RELATIVE_WEIGHT_BOUND_IMPORT.csv", "BOUND2771_0_WEP_source_charge", "current WEP bound import"),
        ("SRC2772_07_1065_doc", "1065_doc", WORK / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md", "PGG1065_5_verdict", "prior R10 grammar template"),
        ("SRC2772_08_1065_grammar", "1065_grammar", MTS / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv", "PGG1065_5_verdict", "prior parent grammar audit"),
        ("SRC2772_09_1065_allowed", "1065_allowed", MTS / "P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv", "AAG1065_4_source_only_species_scalar", "prior allowed/prohibited action grammar"),
        ("SRC2772_10_1065_field", "1065_field", MTS / "P8_Y5_R10_1065_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv", "FNL1065_4_verdict", "prior field normalization loophole audit"),
        ("SRC2772_11_1065_charge", "1065_charge", MTS / "P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv", "CIN1065_4_verdict", "prior charge/current normalization audit"),
        ("SRC2772_12_1065_zero", "1065_zero", MTS / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv", "WTZ1065_4_verdict", "prior w_A theorem-zero clauses"),
        ("SRC2772_13_1065_wep", "1065_wep", MTS / "P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv", "WEP1065_2_delta_w", "prior first WEP row schema"),
        ("SRC2772_14_1065_prediction", "1065_prediction", MTS / "P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv", "PRED1065_0_WEP_relative_source_weight_first_row", "prior WEP product candidate"),
        ("SRC2772_15_1065_bound", "1065_bound", MTS / "P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_BOUND_IMPORT.csv", "BOUND1065_0_WEP_source_charge", "prior WEP bound import"),
        ("SRC2772_16_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound anchor"),
        ("SRC2772_17_393_common_mode", "393_common_mode", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "source-normalized measured-G guard"),
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


def build_grammar_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"audit_id": "PGG2772_0_parent_language", "claim": "define the parent matter action language before source coupling", "formal_clause": "S_matter is a local functional of e_obs, Psi_A, connections, and measured matter parameters theta_A; AX1090 quotient labels cannot appear as inert source-only selectors", "result": "CONDITIONAL_GRAMMAR_CANDIDATE", "gap": "the object language is sharp but still not forced from parent primitives", "parent_signed": False}),
        nonclaim({"audit_id": "PGG2772_1_no_inert_species_scalar", "claim": "forbid a dimensionless inert scalar w_A that only multiplies active source strength", "formal_clause": "w_A not in Obj(Language) if varying w_A changes T_source while changing no nongravitational observable, representation label, or measured matter parameter", "result": "EXACT_IF_PARENT_SYNTAX_ACCEPTED", "gap": "this is the desired no-source-only-slot rule, not yet a derived syntax theorem", "parent_signed": False}),
        nonclaim({"audit_id": "PGG2772_2_field_normalization_quotient", "claim": "classify removable w_A as field normalization when possible", "formal_clause": "Psi_A -> Z_A^(1/2) Psi_A with canonical kinetic term and transformed measured couplings", "result": "LOOPHOLE_AUDITED_NOT_CLOSED", "gap": "interactions, composite matter, quantum weights, and measure factors can keep an apparent source weight physical", "parent_signed": False}),
        nonclaim({"audit_id": "PGG2772_3_charge_interaction_owner", "claim": "source normalization cannot hide inside charge/current normalization", "formal_clause": "q_A, m_A, representation data, and J_A normalizations are measured matter-sector parameters rather than gravitational source-only switches", "result": "OWNER_CONDITIONAL", "gap": "Noether/current owner remains candidate-missing in the current branch", "parent_signed": False}),
        nonclaim({"audit_id": "PGG2772_4_measure_coframe_descent", "claim": "prevent measure/coframe factors from reintroducing species labels", "formal_clause": "sqrt(-g_obs), e_obs, connection descent, and boundary terms are species blind through the local limit", "result": "PARALLEL_PARENT_SIGNATURE_MISSING", "gap": "measure/coframe/hidden-spurion return is still a parallel unsigned gate", "parent_signed": False}),
        nonclaim({"audit_id": "PGG2772_5_verdict", "claim": "no-source-only-slot parent grammar theorem", "formal_clause": "Language(S_matter) excludes w_A; common w is calibration; all relative weights are measured matter parameters, removable field normalizations, or forbidden spurions", "result": "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED", "gap": "no derivation yet that the parent category object language must exclude inert species scalars", "parent_signed": False}),
    ]


def build_allowed_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"grammar_id": "AAG2772_0_observed_geometry", "slot": "observed coframe/metric", "allowed_status": "allowed", "grammar_rule": "one e_obs/g_obs supplies matter dynamics, Hilbert variation, clocks, photons, and readout", "signature_status": "conditional_from_source_side_spine"}),
        nonclaim({"grammar_id": "AAG2772_1_matter_fields", "slot": "ordinary matter fields Psi_A", "allowed_status": "allowed", "grammar_rule": "fields may carry representation labels and measured charges/masses", "signature_status": "ordinary_matter_language_allowed"}),
        nonclaim({"grammar_id": "AAG2772_2_measured_parameters", "slot": "theta_A measured matter parameters", "allowed_status": "allowed_if_observable", "grammar_rule": "masses, charges, representation data, and interaction coefficients must be readout-measurable", "signature_status": "requires Noether/current owner for full closure"}),
        nonclaim({"grammar_id": "AAG2772_3_common_normalization", "slot": "w_common", "allowed_status": "calibration_only", "grammar_rule": "single universal constant multiplier can be absorbed into kappa/G only if range/time/species/frame independent", "signature_status": "guarded_by_393_and_2771"}),
        nonclaim({"grammar_id": "AAG2772_4_source_only_species_scalar", "slot": "w_A", "allowed_status": "prohibited_by_candidate_grammar", "grammar_rule": "no inert dimensionless species scalar may multiply S_A while remaining invisible to nongravitational readout", "signature_status": "not_parent_signed"}),
        nonclaim({"grammar_id": "AAG2772_5_hidden_spurion", "slot": "w(m,D,boundary,A)", "allowed_status": "prohibited_or_retained_residual", "grammar_rule": "marker, domain, boundary, and post-readout masks cannot reweight source after variation", "signature_status": "parallel_open_gate"}),
        nonclaim({"grammar_id": "AAG2772_6_nonHilbert_current", "slot": "zeta_A J_NH,A", "allowed_status": "absent_exact_silent_or_residual", "grammar_rule": "spin/torsion/boundary/non-Hilbert current must be proved silent or bounded separately", "signature_status": "parallel_open_gate"}),
    ]


def build_field_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"loophole_id": "FNL2772_0_free_field_rescaling", "possible_escape": "w_A is only a field normalization", "audit_result": "not enough by itself", "reason": "canonical kinetic normalization can remove one factor, but interactions and composite observables fix relative normalizations", "required_closure": "field-redefinition quotient plus all measured couplings transformed with no leftover source-only factor"}),
        nonclaim({"loophole_id": "FNL2772_1_action_scale_quantum_weight", "possible_escape": "overall S_A multiplier is dynamically invisible classically", "audit_result": "dangerous_counterexample", "reason": "classical EOM may be unchanged while Hilbert stress and path-integral/statistical weight change", "required_closure": "parent quantum/statistical action normalization or theorem that such multipliers are gauge quotiented"}),
        nonclaim({"loophole_id": "FNL2772_2_mass_unit_convention", "possible_escape": "w_A is mass renormalization or unit choice", "audit_result": "not source-only if observable", "reason": "if it changes inertial mass or spectra, it belongs to theta_A and is not a hidden gravitational prefactor", "required_closure": "same parameter must enter dynamics, source, and readout through one owner"}),
        nonclaim({"loophole_id": "FNL2772_3_measure_jacobian", "possible_escape": "species-dependent measure/coframe Jacobian", "audit_result": "parallel_spurion_channel", "reason": "a Jacobian can multiply variation without appearing as explicit w_A", "required_closure": "species-blind measure/coframe descent and boundary silence"}),
        nonclaim({"loophole_id": "FNL2772_4_verdict", "possible_escape": "all w_A are normalization artifacts", "audit_result": "NOT_PROVED", "reason": "some apparent weights may be quotiented, but an inert source-only scalar is still legal unless the parent grammar forbids it", "required_closure": "parent action syntax exclusion or numeric WEP prior row"}),
    ]


def build_charge_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"audit_id": "CIN2772_0_charge_is_observable", "object": "electric/gauge charge q_A", "result": "not a hidden source prefactor", "reason": "charge enters interactions and currents, so it is measured matter data rather than a pure gravitational source weight", "closure_needed": "current normalization and representation owner"}),
        nonclaim({"audit_id": "CIN2772_1_neutral_rest_source", "object": "neutral/rest-mass source contribution", "result": "blocks charge-only escape", "reason": "source weight must apply to all stress-energy, not only EM charge channels", "closure_needed": "Hilbert source owner for total stress tensor"}),
        nonclaim({"audit_id": "CIN2772_2_current_owner", "object": "Noether/current normalization", "result": "candidate_missing", "reason": "current branch still marks the owner as not derived, so current normalization cannot force w_A absent", "closure_needed": "single parent current owner for charge, matter, and source readout"}),
        nonclaim({"audit_id": "CIN2772_3_interaction_renormalization", "object": "coupling and charge renormalization", "result": "loophole_not_closed", "reason": "renormalized interactions can hide normalization choices unless the parent identifies which constants are measured", "closure_needed": "operator-domain rule separating measured constants from source-only scalars"}),
        nonclaim({"audit_id": "CIN2772_4_verdict", "object": "interaction/charge normalization route to no w_A", "result": "CONDITIONAL_NOT_PARENT_SIGNED", "reason": "it supplies a good classification but not a proof that inert source-only scalars cannot exist", "closure_needed": "parent current owner or explicit source-scalar exclusion theorem"}),
    ]


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"zero_id": "WTZ2772_0_strict_no_slot", "target_quantity": "Delta_w_AB", "theorem_clause": "w_A is not a syntactic object in the parent matter action language", "would_imply": "Delta_w_AB = 0 for all material/source pairs", "current_status": "exact_clause_not_parent_signed", "blocks": "cannot score WEP relative-source row as theorem-zero"}),
        nonclaim({"zero_id": "WTZ2772_1_common_mode_only", "target_quantity": "Delta_w_AB", "theorem_clause": "w_A = w_common for every species/source and w_common is constant/range/time/frame independent", "would_imply": "Delta_w_AB = 0 after common calibration", "current_status": "common_mode_guarded_not_proved", "blocks": "relative weights cannot be absorbed into measured G"}),
        nonclaim({"zero_id": "WTZ2772_2_field_redefinition", "target_quantity": "Delta_w_AB", "theorem_clause": "all apparent w_A are field normalizations removed by canonical quotient with interactions preserved", "would_imply": "no residual source-only product", "current_status": "normalization_loophole_audited_not_closed", "blocks": "path-integral/action-scale counterexample survives"}),
        nonclaim({"zero_id": "WTZ2772_3_current_owner", "target_quantity": "Delta_w_AB", "theorem_clause": "one parent current/source owner fixes matter dynamics, Noether currents, and Hilbert source normalization", "would_imply": "source label has no independent coupling selector", "current_status": "owner_candidate_missing", "blocks": "relative source weights remain finite-branch debts"}),
        nonclaim({"zero_id": "WTZ2772_4_verdict", "target_quantity": "P_WEP_relative_source_weight", "theorem_clause": "Delta_w_AB=0 OR tau_WEP=0 from parent-signed grammar/projection", "would_imply": "P_WEP_relative_source_weight=0", "current_status": "THEOREM_ZERO_NOT_PARENT_SIGNED", "blocks": "first WEP numeric row must remain nonclaim/missing-input"}),
    ]


def build_wep_schema_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "WEP2772_0_bound_anchor", "quantity": "eta_AB source-charge bound", "symbol": "eta_TiPt_bound", "value_or_status": "2.8e-15", "units": "dimensionless", "source_row": "R1_WEP_source_charge", "runner_role": "bound", "refusal_gate": "bound alone is not an MTS prediction"}),
        nonclaim({"row_id": "WEP2772_1_material_pair", "quantity": "MICROSCOPE Ti/Pt material convention", "symbol": "AB", "value_or_status": "TA6V_minus_PtRh10", "units": "dimensionless convention", "source_row": "MCON1061_0_test_pair; WEP1065_1_material_pair", "runner_role": "context", "refusal_gate": "material convention does not supply Delta_w_AB"}),
        nonclaim({"row_id": "WEP2772_2_delta_w", "quantity": "relative source-weight difference for Ti/Pt", "symbol": "Delta_w_TiPt", "value_or_status": "MISSING_PARENT_GRAMMAR_ZERO_OR_NUMERIC_PRIOR", "units": "dimensionless", "source_row": "WTZ2772_4_verdict", "runner_role": "required_prediction_input", "refusal_gate": "no unity shortcut and no absorption into measured G"}),
        nonclaim({"row_id": "WEP2772_3_tau_WEP", "quantity": "local lab/source/orbit/readout projection", "symbol": "tau_WEP", "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "units": "dimensionless", "source_row": "REQ2771_0_WEP_species; WEP1065_3_tau_WEP", "runner_role": "required_prediction_input", "refusal_gate": "tau_WEP cannot be set to one"}),
        nonclaim({"row_id": "WEP2772_4_product", "quantity": "first scoreable WEP relative source product", "symbol": "P_WEP_relative_source_weight = abs(Delta_w_TiPt * tau_WEP)", "value_or_status": "MISSING_DELTA_W_TiPt_TIMES_TAU_WEP_PRODUCT", "units": "dimensionless", "source_row": "WEP2772_2_delta_w; WEP2772_3_tau_WEP", "runner_role": "prediction", "refusal_gate": "must be numeric, sourced, unit-matched, and <= 2.8e-15"}),
        nonclaim({"row_id": "WEP2772_5_no_cancellation", "quantity": "absolute-value no-cancellation guard", "symbol": "abs(Delta_w_TiPt * tau_WEP)", "value_or_status": "ENFORCED_AS_SCHEMA", "units": "dimensionless", "source_row": "WEP2772_4_product", "runner_role": "guard", "refusal_gate": "no signed-material cancellation accepted as evidence"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2772_0_WEP_relative_source_weight_first_row",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DELTA_W_TiPt_TIMES_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": rel(OUTPUTS["wep_schema"]),
            "inputs_present": "eta_TiPt_bound=2.8e-15; material_pair=TA6V_minus_PtRh10",
            "required_inputs": "Delta_w_TiPt theorem-zero or numeric prior; tau_WEP local projection; absolute product; source paths",
            "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT",
            "notes": "The first WEP row is structurally defined in the R2/f(R) branch, but it is not a prediction until Delta_w_TiPt and tau_WEP are derived or sourced.",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "bound_id": "BOUND2772_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": rel(LOCAL_BOUNDS / "local_bound_claims.csv"),
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_internal_runner_only",
            "bound_valid_for_internal_runner": True,
            "notes": "Source-backed WEP anchor; it does not create an MTS prediction without a numeric product row.",
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
            "issues": "no valid MTS WEP relative-weight product prediction rows",
        })
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2772_0_WEP_relative_weight_first_row",
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
        nonclaim({"gate_id": "CG2772_0_parent_grammar_theorem", "claim": "parent action grammar forbids source-only species scalar w_A", "gate_pass": False, "reason": "candidate grammar is exact but not parent signed", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2772_1_theorem_zero_Delta_w", "claim": "Delta_w_TiPt=0 by theorem", "gate_pass": False, "reason": "no-source-only-slot theorem-zero clauses remain unsigned", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2772_2_first_WEP_numeric_row", "claim": "first WEP relative-weight row is scoreable", "gate_pass": False, "reason": "Delta_w_TiPt and tau_WEP are missing; product runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2772_3_measured_G_absorption", "claim": "relative source weights can be absorbed into measured G", "gate_pass": False, "reason": "only common universal range/time/species/frame independent factors are absorbable", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2772_4_local_GR_WEP_claim", "claim": "local GR/WEP source coupling branch is derived", "gate_pass": False, "reason": "right source-side structure is isolated, but the grammar/current/projection signatures remain open", "claim_allowed": False}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2772_0_grammar_status", "decision": "no-source-only-slot grammar is the right theorem target but not closed", "because": "the grammar kills w_A if accepted, but acceptance is still a parent syntax/quotient contract", "next_action": "derive the source-scalar exclusion from parent object language or operator-domain rules"}),
        nonclaim({"decision_id": "DEC2772_1_first_WEP_row_status", "decision": "first WEP relative-source row is schema-complete but numerically empty", "because": "eta bound and material convention exist, while Delta_w_TiPt and tau_WEP are missing", "next_action": "either prove Delta_w_TiPt=0 or source a numeric prior width plus tau_WEP projection"}),
        nonclaim({"decision_id": "DEC2772_2_best_next", "decision": "next target is parent action syntax source-scalar exclusion or WEP Delta-w prior width", "because": "this is the smallest remaining fork between a derivation win and a bounded finite branch", "next_action": "2773-Y5-R2FR-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2772_0_2773",
            "next_target": "2773-Y5-R2FR-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_action_syntax_source_scalar_exclusion_or_WEP_Delta_w_prior_width_under_AX1090_2773.py",
            "objective": "derive the parent action syntax/operator-domain rule that excludes inert source-only species scalars; if it fails, fill the WEP Delta_w_TiPt prior-width row and tau_WEP projection requirements without claiming a pass",
            "include": "source-scalar exclusion lemma, object-language typing, field/measure normalization, quantum action-scale issue, WEP Delta_w_TiPt prior-width schema, tau_WEP projection contract",
            "exclude": "assuming minimality, setting Delta_w=0 by taste, setting tau_WEP=1, absorbing relative weights into measured G, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    grammar: list[dict[str, Any]],
    allowed: list[dict[str, Any]],
    field: list[dict[str, Any]],
    charge: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    wep_schema: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grammar_rows = grammar + allowed + field + charge + zero + gates
    wep_rows = wep_schema + candidate + bounds + gates
    beta_rows = allowed + field + charge + zero + next_rows
    microscope_rows = wep_schema + candidate + bounds + gates + next_rows
    specs = [
        ("BR2772_0_grammar_queue", "grammar", grammar_rows, OUTPUTS["grammar"], BRANCH_OUTPUTS["grammar_queue"], "no-source-only-slot grammar nonclaim copy"),
        ("BR2772_1_wep_queue", "wep_first_row", wep_rows, OUTPUTS["wep_schema"], BRANCH_OUTPUTS["wep_queue"], "first WEP relative-weight row nonclaim copy"),
        ("BR2772_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["allowed"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing source-scalar exclusion copy"),
        ("BR2772_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE first WEP row copy"),
        ("BR2772_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next source-scalar exclusion target"),
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
    grammar = rows_by_name["grammar"]
    allowed = rows_by_name["allowed"]
    field = rows_by_name["field"]
    charge = rows_by_name["charge"]
    zero = rows_by_name["zero"]
    wep_schema = rows_by_name["wep_schema"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2772_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2772_1_grammar_not_promoted", any(row["audit_id"] == "PGG2772_5_verdict" and row["result"] == "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED" for row in grammar), "parent grammar theorem remains conditional"),
        ("VAL2772_2_allowed_slots_written", len(allowed) >= 7 and any(row["grammar_id"] == "AAG2772_4_source_only_species_scalar" for row in allowed), "allowed/prohibited action grammar slots are recorded"),
        ("VAL2772_3_loopholes_audited", any(row["loophole_id"] == "FNL2772_4_verdict" and row["audit_result"] == "NOT_PROVED" for row in field) and any(row["audit_id"] == "CIN2772_4_verdict" for row in charge), "field normalization and charge/current loopholes are audited"),
        ("VAL2772_4_theorem_zero_unsigned", any(row["zero_id"] == "WTZ2772_4_verdict" and row["current_status"] == "THEOREM_ZERO_NOT_PARENT_SIGNED" for row in zero), "w_A theorem-zero is not promoted"),
        ("VAL2772_5_first_WEP_schema_written", all(any(row["row_id"] == required for row in wep_schema) for required in ["WEP2772_0_bound_anchor", "WEP2772_1_material_pair", "WEP2772_2_delta_w", "WEP2772_3_tau_WEP", "WEP2772_4_product", "WEP2772_5_no_cancellation"]), "first WEP row has bound, material context, Delta_w, tau_WEP, product, and no-cancellation guard"),
        ("VAL2772_6_prediction_template_nonclaim", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "first WEP prediction row remains missing-input/nonclaim"),
        ("VAL2772_7_bound_anchor_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True and bounds[0]["valid_for_claim"] is False, "WEP bound anchor is numeric and source-backed for internal runner only"),
        ("VAL2772_8_runner_refuses_missing_prediction", runner[0]["valid_prediction_rows"] == 0 and runner[0]["valid_bound_rows"] == 1 and runner[0]["claim_allowed"] is False, "strict product runner refuses the first WEP placeholder"),
        ("VAL2772_9_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all grammar/WEP/local-GR claim gates remain blocked"),
        ("VAL2772_10_next_target_written", any(row["row_id"] == "NEXT2772_0_2773" and "source-scalar-exclusion" in row["next_target"] for row in next_rows), "next target selects source-scalar exclusion or WEP Delta-w prior-width"),
        ("VAL2772_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2772_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2772_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2772_14_generated_files_in_post_checkpoint", generated_files_under_work(), "all generated files are under post-checkpoint-work"),
        ("VAL2772_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2772_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2772_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2772 ports the no-source-only-slot grammar into the current R2/f(R) branch, keeps the w_A theorem-zero unsigned, writes the first WEP relative-weight row schema, imports only the WEP bound as an internal runner anchor, refuses the missing MTS product, blocks all local-GR/WEP claims, and selects parent action syntax source-scalar exclusion or WEP Delta-w prior width as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2772 - Y5 R2/f(R): No-Source-Only-Slot Parent Grammar Or First Relative-Weight Numeric Row Under AX1090",
        "## Private Verdict\n\nThe route is sharp but not closed: if the parent matter language has no inert source-only species scalar `w_A`, then `Delta_w_AB=0` follows and the WEP relative-weight branch dies cleanly. That grammar rule is still not parent-derived, so this checkpoint does not claim local GR, WEP, R10, or universal coupling.\n\nRunner result: the first WEP row is schema-complete, but `Delta_w_TiPt` and `tau_WEP` remain missing. The strict runner therefore keeps `valid_prediction_rows=0`.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Parent Grammar Audit\n\n" + markdown_table(rows_by_name["grammar"], ["audit_id", "claim", "formal_clause", "result", "gap", "parent_signed", "valid_for_claim"]),
        "## Allowed Action Grammar\n\n" + markdown_table(rows_by_name["allowed"], ["grammar_id", "slot", "allowed_status", "grammar_rule", "signature_status", "valid_for_claim"]),
        "## Field Normalization Loopholes\n\n" + markdown_table(rows_by_name["field"], ["loophole_id", "possible_escape", "audit_result", "reason", "required_closure", "valid_for_claim"]),
        "## Charge And Interaction Normalization\n\n" + markdown_table(rows_by_name["charge"], ["audit_id", "object", "result", "reason", "closure_needed", "valid_for_claim"]),
        "## w_A Theorem-Zero Clauses\n\n" + markdown_table(rows_by_name["zero"], ["zero_id", "target_quantity", "theorem_clause", "would_imply", "current_status", "blocks", "valid_for_claim"]),
        "## First WEP Numeric Row Schema\n\n" + markdown_table(rows_by_name["wep_schema"], ["row_id", "quantity", "symbol", "value_or_status", "units", "source_row", "runner_role", "refusal_gate", "valid_for_claim"]),
        "## WEP Product Runner\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes"]),
        "## WEP Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim", "notes"]),
        "## Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc", "valid_for_claim"]),
        "## Runner Comparisons\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is the cleanest fork now. Either the parent syntax forbids `w_A`, and the source-coupling problem collapses beautifully; or it does not, and the honest path is to put a numeric prior width on `Delta_w_TiPt` plus a real `tau_WEP` projection. No hand-waving, no unity shortcut, no burying it in measured `G`.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    grammar = build_grammar_rows()
    allowed = build_allowed_rows()
    field = build_field_rows()
    charge = build_charge_rows()
    zero = build_zero_rows()
    wep_schema = build_wep_schema_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("grammar", grammar), ("allowed", allowed), ("field", field), ("charge", charge),
        ("zero", zero), ("wep_schema", wep_schema), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision),
        ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(grammar, allowed, field, charge, zero, wep_schema, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "grammar": grammar,
        "allowed": allowed,
        "field": field,
        "charge": charge,
        "zero": zero,
        "wep_schema": wep_schema,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2772_OVERALL")
    print(f"2772 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
