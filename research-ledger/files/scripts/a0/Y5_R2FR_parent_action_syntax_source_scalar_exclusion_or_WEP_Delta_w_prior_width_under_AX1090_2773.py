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
DOC = WORK / "2773-Y5-R2FR-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2773_SOURCE_REGISTER.csv",
    "lemma": MTS / "P8_Y5_R2FR_2773_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "typing": MTS / "P8_Y5_R2FR_2773_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "operator": MTS / "P8_Y5_R2FR_2773_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "normalization": MTS / "P8_Y5_R2FR_2773_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
    "prior": MTS / "P8_Y5_R2FR_2773_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
    "tau": MTS / "P8_Y5_R2FR_2773_TAU_WEP_PROJECTION_CONTRACT.csv",
    "candidate": MTS / "P8_Y5_R2FR_2773_WEP_DELTA_W_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2773_WEP_DELTA_W_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2773_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2773_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2773_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2773_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2773_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2773_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2773_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "exclusion_queue": RAB_QUEUE / "JR2773_SOURCE_SCALAR_EXCLUSION_LEMMA_NONCLAIM.csv",
    "wep_prior_queue": RAB_QUEUE / "JR2773_WEP_DELTA_W_PRIOR_WIDTH_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "SOURCE_SCALAR_EXCLUSION_2773_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "wep_delta_w_prior_width_2773_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2773_ACTION_SCALE_OR_TAU_NEXT.csv",
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
        ("SRC2773_00_2772_next", "2772_next", MTS / "P8_Y5_R2FR_2772_NEXT_TARGET.csv", "NEXT2772_0_2773", "current handoff into source-scalar exclusion"),
        ("SRC2773_01_2772_grammar", "2772_grammar", MTS / "P8_Y5_R2FR_2772_PARENT_GRAMMAR_AUDIT.csv", "PGG2772_5_verdict", "current no-source-only-slot grammar verdict"),
        ("SRC2773_02_2772_allowed", "2772_allowed", MTS / "P8_Y5_R2FR_2772_ALLOWED_ACTION_GRAMMAR.csv", "AAG2772_4_source_only_species_scalar", "current candidate syntax ban for w_A"),
        ("SRC2773_03_2772_field", "2772_field", MTS / "P8_Y5_R2FR_2772_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv", "FNL2772_1_action_scale_quantum_weight", "current action-scale field-normalization obstruction"),
        ("SRC2773_04_2772_charge", "2772_charge", MTS / "P8_Y5_R2FR_2772_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv", "CIN2772_2_current_owner", "current current-owner obstruction"),
        ("SRC2773_05_2772_zero", "2772_zero", MTS / "P8_Y5_R2FR_2772_WA_THEOREM_ZERO_CLAUSES.csv", "WTZ2772_4_verdict", "current theorem-zero failure"),
        ("SRC2773_06_2772_wep", "2772_wep", MTS / "P8_Y5_R2FR_2772_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv", "WEP2772_2_delta_w", "current first WEP row schema"),
        ("SRC2773_07_2772_candidate", "2772_candidate", MTS / "P8_Y5_R2FR_2772_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv", "PRED2772_0_WEP_relative_source_weight_first_row", "current WEP product placeholder"),
        ("SRC2773_08_1066_doc", "1066_doc", WORK / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md", "SSE1066_5_verdict", "prior R10 source-scalar exclusion template"),
        ("SRC2773_09_1066_lemma", "1066_lemma", MTS / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "prior source-scalar exclusion lemma"),
        ("SRC2773_10_1066_typing", "1066_typing", MTS / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv", "OLT1066_6_verdict", "prior object-language typing"),
        ("SRC2773_11_1066_operator", "1066_operator", MTS / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv", "ODR1066_4_verdict", "prior operator-domain obstruction"),
        ("SRC2773_12_1066_normalization", "1066_normalization", MTS / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_4_verdict", "prior action-scale/measure obstruction"),
        ("SRC2773_13_1066_tau", "1066_tau", MTS / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_7_verdict", "prior tau_WEP projection contract"),
        ("SRC2773_14_1055_parent", "1055_parent", MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_4_source_label_forgetting", "parent action contract candidate"),
        ("SRC2773_15_1055_counter", "1055_counter", MTS / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", "CE1055_3_relative_source_weight", "relative source-weight counterexample"),
        ("SRC2773_16_980_theorem", "980_theorem", MTS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_2_scalar_obstruction_lemma", "continuous scalar obstruction"),
        ("SRC2773_17_980_counter", "980_counter", MTS / "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv", "CEX980_2_species_kappa", "species kappa counterexample"),
        ("SRC2773_18_989_owner", "989_owner", MTS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "current/source owner gap"),
        ("SRC2773_19_1061_tau", "1061_tau", MTS / "P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv", "INF1061_4_tau_WEP", "tau_WEP missing input ledger"),
        ("SRC2773_20_1061_material", "1061_material", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention"),
        ("SRC2773_21_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound anchor"),
        ("SRC2773_22_393_common", "393_common", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard"),
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


def build_lemma_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"lemma_id": "SSE2773_0_target", "claim": "exclude inert source-only species scalars from the parent action syntax", "formal_statement": "If a scalar x_A changes only active gravitational source strength and has no observable/gauge/representation/geometry type, then x_A is not an admissible parent argument.", "attempt_result": "TARGET_SHARPENED", "gap": "typing principle must be parent-derived rather than adopted as minimality"}),
        nonclaim({"lemma_id": "SSE2773_1_object_language_route", "claim": "typed parent arguments are geometry, matter fields, gauge/current data, representation constants, or universal constants", "formal_statement": "Arg(S_parent) subset Gamma(E_geom) union Gamma(E_matter) union Conn union Theta_meas union Theta_univ.", "attempt_result": "CONDITIONAL_TYPING_LEMMA", "gap": "the exact parent object language is not yet derived from deeper MTS primitives"}),
        nonclaim({"lemma_id": "SSE2773_2_variation_before_readout", "claim": "post-variation source selectors cannot generate species weights", "formal_statement": "T_matter := delta S_matter/delta e_obs before readout/projector reduction; no F((T_A,A)) after variation.", "attempt_result": "CLEAN_IF_PARENT_VARIATION_ORDER_SIGNED", "gap": "readout/EFT backreaction closure remains unsigned"}),
        nonclaim({"lemma_id": "SSE2773_3_naturality_route", "claim": "natural source scalar across ordinary matter coproduct should be common", "formal_statement": "Nat(Obj(C_matter), R_+) = constants if the ordinary matter category is connected by allowed morphisms.", "attempt_result": "HELPFUL_CONDITIONAL_ONLY", "gap": "species components can be disconnected; a family w_A is natural on disconnected/simple-object components"}),
        nonclaim({"lemma_id": "SSE2773_4_quantum_action_scale_obstruction", "claim": "multiplying S_A by w_A is not guaranteed to be a harmless classical redundancy", "formal_statement": "S_A -> w_A S_A can leave classical EOM form invariant while changing Hilbert stress, path-integral weight, and source normalization.", "attempt_result": "OBSTRUCTION_SURVIVES", "gap": "needs parent quantum/statistical/action-scale normalization owner"}),
        nonclaim({"lemma_id": "SSE2773_5_verdict", "claim": "parent source-scalar exclusion lemma", "formal_statement": "typed object language + variation-before-readout + common action-scale normalization => no inert species source scalar w_A", "attempt_result": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED", "gap": "action-scale/measure normalization and parent object-language typing remain unsigned"}),
    ]


def build_typing_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"type_id": "OLT2773_0_geometry", "candidate": "e_obs, g_obs, connection", "type_status": "admissible", "why": "observable geometry and its connection determine matter dynamics and Hilbert variation", "wA_effect": "species blind if one observed coframe is signed", "signature_status": "conditional"}),
        nonclaim({"type_id": "OLT2773_1_matter_fields", "candidate": "Psi_A", "type_status": "admissible", "why": "ordinary species fields are dynamical variables", "wA_effect": "labels are bookkeeping unless source coupling can see them after variation", "signature_status": "allowed"}),
        nonclaim({"type_id": "OLT2773_2_measured_parameters", "candidate": "m_A, q_A, representation data, interaction couplings", "type_status": "admissible_if_observable", "why": "they affect spectra, scattering, charge/current, or representation labels", "wA_effect": "not source-only if measured in nongravitational channels", "signature_status": "current_owner_unsigned"}),
        nonclaim({"type_id": "OLT2773_3_universal_constant", "candidate": "single w_common or kappa_univ", "type_status": "calibration_only", "why": "a common multiplier can be absorbed into measured coupling only after universality guards", "wA_effect": "cannot absorb relative w_A/w_B", "signature_status": "guarded_by_common_mode_rule"}),
        nonclaim({"type_id": "OLT2773_4_inert_source_scalar", "candidate": "w_A multiplying only S_A/source strength", "type_status": "rejected_by_candidate_typing", "why": "it has no independent observable, gauge, representation, or geometry role", "wA_effect": "would create WEP-sensitive T_source=sum_A w_A T_A", "signature_status": "not_parent_signed"}),
        nonclaim({"type_id": "OLT2773_5_hidden_marker", "candidate": "w(m,D,boundary,A)", "type_status": "rejected_or_residual", "why": "marker/domain/boundary scalars can reintroduce labels under another name", "wA_effect": "must be theorem-forbidden or explicitly bounded", "signature_status": "obstruction_active_from_980"}),
        nonclaim({"type_id": "OLT2773_6_verdict", "candidate": "object-language typing proof", "type_status": "conditional_not_parent_derived", "why": "typing kills w_A if accepted, but acceptance still rests on parent syntax/measure axioms", "wA_effect": "Delta_w_TiPt not theorem-zero yet", "signature_status": "open"}),
    ]


def build_operator_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"rule_id": "ODR2773_0_allowed_coefficient_ring", "rule": "visible coefficients may depend only on q_loc and fixed representation/topological data", "formal_form": "Coeff(O_vis) in Alg[q_loc, Theta_rep, Level_EM]", "result": "POWERFUL_IF_SIGNED", "obstruction": "same rule remains a contract, not a parent theorem"}),
        nonclaim({"rule_id": "ODR2773_1_continuous_target_obstruction", "rule": "source scalar target R_+ is continuous", "formal_form": "nonconstant invariant I gives w=w0+epsilon I unless invariant algebra/action target is forbidden", "result": "OBSTRUCTION_FROM_980", "obstruction": "one untrivialized invariant scalar can feed continuous source weights"}),
        nonclaim({"rule_id": "ODR2773_2_species_component_obstruction", "rule": "species labels may form disconnected components", "formal_form": "Nat(C_disconnected,R_+) admits independent constants on components", "result": "OBSTRUCTION_SURVIVES", "obstruction": "need connected/rich morphism category or explicit no external source-label argument"}),
        nonclaim({"rule_id": "ODR2773_3_action_scale_target", "rule": "action-scale coefficients are not ordinary measured couplings unless parent measure owns them", "formal_form": "w_A S_A is a coefficient of the variational weight, not simply a field redefinition", "result": "REQUIRES_PARENT_MEASURE_OWNER", "obstruction": "quantum/statistical normalization of each matter sector is not signed"}),
        nonclaim({"rule_id": "ODR2773_4_verdict", "rule": "operator-domain source-scalar exclusion", "formal_form": "Hom(Arg_parent,R_+^species_source_only)=empty", "result": "EXACT_RULE_NOT_DERIVED", "obstruction": "requires invariant algebra triviality/no-extension plus parent action-scale ownership"}),
    ]


def build_normalization_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"audit_id": "FMQ2773_0_classical_EOM_rescaling", "issue": "overall S_A multiplier may not change isolated classical equations", "effect": "tempts false dismissal of w_A", "required_closure": "show same multiplier is gauge/quotient redundancy for source and quantum measure too", "status": "not_closed"}),
        nonclaim({"audit_id": "FMQ2773_1_Hilbert_source_rescaling", "issue": "overall S_A multiplier rescales Hilbert stress", "effect": "directly produces T_source=sum_A w_A T_A", "required_closure": "ban inert source scalars or prove universal common action normalization", "status": "active_obstruction"}),
        nonclaim({"audit_id": "FMQ2773_2_path_integral_weight", "issue": "action scale controls phase/statistical weight", "effect": "species-dependent hbar/effective action scale would be physically meaningful", "required_closure": "single parent hbar/action measure owner for all ordinary matter", "status": "parent_owner_missing"}),
        nonclaim({"audit_id": "FMQ2773_3_measure_jacobian", "issue": "species-dependent Jacobian can mimic w_A", "effect": "hidden measure/coframe descent can reopen source labels", "required_closure": "species-blind measure/coframe/boundary descent theorem", "status": "parallel_open_gate"}),
        nonclaim({"audit_id": "FMQ2773_4_verdict", "issue": "field/measure/quantum normalization closure", "effect": "blocks promotion of Delta_w_TiPt=0", "required_closure": "derive a universal parent action-scale normalization or retain finite Delta_w prior", "status": "NOT_PARENT_SIGNED"}),
    ]


def build_prior_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"prior_id": "DWP2773_0_WEP_bound", "quantity": "eta_TiPt_bound", "value_or_status": "2.8e-15", "units": "dimensionless", "formula_or_requirement": "abs(P_WEP_relative_source_weight) <= eta_TiPt_bound", "status": "bound_anchor_available"}),
        nonclaim({"prior_id": "DWP2773_1_material_pair", "quantity": "AB", "value_or_status": "TA6V_minus_PtRh10", "units": "convention", "formula_or_requirement": "Delta_w_TiPt := w_Ti_source - w_Pt_source in the MICROSCOPE convention", "status": "context_available"}),
        nonclaim({"prior_id": "DWP2773_2_theorem_zero_option", "quantity": "Delta_w_TiPt", "value_or_status": "MISSING_PARENT_SOURCE_SCALAR_EXCLUSION", "units": "dimensionless", "formula_or_requirement": "Delta_w_TiPt=0 only if SSE2773_5 is parent signed", "status": "not_available"}),
        nonclaim({"prior_id": "DWP2773_3_finite_prior_width", "quantity": "abs(Delta_w_TiPt)", "value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH", "units": "dimensionless", "formula_or_requirement": "if tau_WEP is numeric and nonzero, require abs(Delta_w_TiPt) <= 2.8e-15/abs(tau_WEP)", "status": "blocked_by_tau_WEP"}),
        nonclaim({"prior_id": "DWP2773_4_tau_WEP", "quantity": "tau_WEP", "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "units": "dimensionless", "formula_or_requirement": "derive from Earth/source worldtube, spacecraft orbit, observed coframe, and force readout", "status": "not_available"}),
        nonclaim({"prior_id": "DWP2773_5_product", "quantity": "P_WEP_relative_source_weight", "value_or_status": "MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP", "units": "dimensionless", "formula_or_requirement": "P = abs(Delta_w_TiPt * tau_WEP); no cancellation/sign trick accepted", "status": "not_scoreable"}),
    ]


def build_tau_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"contract_id": "TWP2773_0_source_worldtube", "input": "Earth/source worldtube and source stress profile", "required_form": "T_source^Earth(x) in observed local frame, with composition/source-weight convention", "current_status": "missing", "blocks": "tau_WEP normalization"}),
        nonclaim({"contract_id": "TWP2773_1_orbit_average", "input": "MICROSCOPE orbit and averaging convention", "required_form": "time/orbit average of differential acceleration channel in the same convention as eta_AB", "current_status": "missing", "blocks": "projection from local source profile to observed eta_AB"}),
        nonclaim({"contract_id": "TWP2773_2_observed_coframe", "input": "observed coframe/readout frame", "required_form": "same e_obs for force law, clocks, source variation, and readout", "current_status": "conditional_from_prior_spine", "blocks": "frame consistency of tau_WEP"}),
        nonclaim({"contract_id": "TWP2773_3_material_response", "input": "test-body material/source tensor", "required_form": "Ti/Pt material response to relative source-weight channel, not just alpha/Coulomb charge", "current_status": "material_pair_only", "blocks": "full Delta_w_TiPt mapping"}),
        nonclaim({"contract_id": "TWP2773_4_force_readout", "input": "differential acceleration readout map", "required_form": "map from parent source residual to eta_AB with units and sign/absolute convention", "current_status": "missing", "blocks": "scoreable WEP product"}),
        nonclaim({"contract_id": "TWP2773_5_no_unity_shortcut", "input": "tau_WEP value", "required_form": "numeric sourced value, theorem-zero, or explicit retained nuisance with prior", "current_status": "unity_forbidden", "blocks": "cannot set tau_WEP=1"}),
        nonclaim({"contract_id": "TWP2773_6_no_cancellation", "input": "sign/material cancellation", "required_form": "absolute product bound unless a signed material model is fully derived and sourced", "current_status": "absolute_guard_enforced", "blocks": "cannot hide product by cancellation"}),
        nonclaim({"contract_id": "TWP2773_7_verdict", "input": "tau_WEP projection", "required_form": "tau_WEP = functional[source worldtube, orbit average, e_obs, material tensor, force readout]", "current_status": "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED", "blocks": "finite Delta_w prior width and WEP runner scoring"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2773_0_WEP_Delta_w_prior_width_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": rel(OUTPUTS["prior"]),
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10",
            "required_inputs": "parent source-scalar theorem-zero OR numeric Delta_w_TiPt prior width;tau_WEP projection;absolute product source",
            "derivation_status": "MISSING_DELTA_W_TAUPROJECTION_PRODUCT",
            "notes": "The finite branch is explicit: if the theorem fails, Delta_w_TiPt and tau_WEP must be sourced before scoring.",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "bound_id": "BOUND2773_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": rel(LOCAL_BOUNDS / "local_bound_claims.csv"),
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_internal_runner_only",
            "bound_valid_for_internal_runner": True,
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; only a bound anchor, not a prediction.",
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
            "issues": "no valid MTS Delta_w/tau WEP product prediction rows",
        })
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2773_0_WEP_Delta_w_prior_width",
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
        nonclaim({"gate_id": "CG2773_0_source_scalar_exclusion", "claim": "inert source-only species scalars are parent-forbidden", "gate_pass": False, "reason": "object-language typing and action-scale ownership are not parent-derived", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2773_1_Delta_w_theorem_zero", "claim": "Delta_w_TiPt=0", "gate_pass": False, "reason": "source-scalar exclusion lemma remains conditional", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2773_2_finite_Delta_w_prior", "claim": "finite Delta_w_TiPt prior width is scoreable", "gate_pass": False, "reason": "tau_WEP projection is missing and no numeric Delta_w prior is sourced", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2773_3_WEP_product_runner", "claim": "first WEP relative-weight product passes bound", "gate_pass": False, "reason": "runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"gate_id": "CG2773_4_local_GR_source_branch", "claim": "local GR/Newton source coupling is derived", "gate_pass": False, "reason": "coupling source-side branch still needs parent action-scale/current/projection closure", "claim_allowed": False}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2773_0_lemma_status", "decision": "source-scalar exclusion is a strong conditional lemma, not a theorem", "because": "the proof needs parent object-language typing plus action-scale/measure ownership", "next_action": "attack the quantum/action-scale normalization owner"}),
        nonclaim({"decision_id": "DEC2773_1_finite_branch_status", "decision": "WEP finite branch is explicitly parameterized by Delta_w_TiPt and tau_WEP", "because": "bound and material convention exist, but both prediction inputs are missing", "next_action": "derive tau_WEP or source a numeric prior width only after tau is defined"}),
        nonclaim({"decision_id": "DEC2773_2_best_next", "decision": "next target is parent action-scale normalization or tau_WEP local projection", "because": "action-scale closure kills w_A cleanly; tau_WEP is the finite-branch bottleneck if the theorem fails", "next_action": "2774-Y5-R2FR-parent-quantum-action-scale-normalization-or-WEP-tau-projection-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2773_0_2774",
            "next_target": "2774-Y5-R2FR-parent-quantum-action-scale-normalization-or-WEP-tau-projection-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_quantum_action_scale_normalization_or_WEP_tau_projection_under_AX1090_2774.py",
            "objective": "derive the parent action-scale/measure normalization that forbids species-dependent S_A multipliers; if it fails, start filling tau_WEP as a real local source/orbit/readout projection instead of a unity shortcut",
            "include": "single hbar/action-measure owner, classical EOM vs Hilbert stress distinction, path-integral/action-scale typing, species-blind measure descent, tau_WEP source-worldtube/orbit/readout functional",
            "exclude": "setting w_A=1 by convention, setting tau_WEP=1, absorbing relative weights into measured G, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    lemma: list[dict[str, Any]],
    typing: list[dict[str, Any]],
    operator: list[dict[str, Any]],
    normalization: list[dict[str, Any]],
    prior: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    exclusion_rows = lemma + typing + operator + normalization + gates
    wep_rows = prior + tau + candidate + bounds + gates
    beta_rows = lemma + operator + normalization + next_rows
    microscope_rows = prior + tau + candidate + bounds + next_rows
    specs = [
        ("BR2773_0_exclusion_queue", "exclusion", exclusion_rows, OUTPUTS["lemma"], BRANCH_OUTPUTS["exclusion_queue"], "source-scalar exclusion lemma nonclaim copy"),
        ("BR2773_1_wep_prior_queue", "wep_prior", wep_rows, OUTPUTS["prior"], BRANCH_OUTPUTS["wep_prior_queue"], "WEP Delta-w prior-width nonclaim copy"),
        ("BR2773_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["operator"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing source-scalar exclusion copy"),
        ("BR2773_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE Delta-w/tau projection copy"),
        ("BR2773_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next action-scale or tau target"),
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
    lemma = rows_by_name["lemma"]
    typing = rows_by_name["typing"]
    operator = rows_by_name["operator"]
    normalization = rows_by_name["normalization"]
    prior = rows_by_name["prior"]
    tau = rows_by_name["tau"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2773_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2773_1_exclusion_not_promoted", any(row["lemma_id"] == "SSE2773_5_verdict" and row["attempt_result"] == "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED" for row in lemma), "source-scalar exclusion remains conditional"),
        ("VAL2773_2_object_typing_blocks_wA", any(row["type_id"] == "OLT2773_4_inert_source_scalar" and row["type_status"] == "rejected_by_candidate_typing" and row["signature_status"] == "not_parent_signed" for row in typing), "object-language typing rejects w_A only as candidate grammar"),
        ("VAL2773_3_operator_obstructions_written", any(row["rule_id"] == "ODR2773_1_continuous_target_obstruction" for row in operator) and any(row["rule_id"] == "ODR2773_4_verdict" and row["result"] == "EXACT_RULE_NOT_DERIVED" for row in operator), "operator-domain continuous/species obstructions are written"),
        ("VAL2773_4_action_scale_obstruction_written", any(row["audit_id"] == "FMQ2773_4_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in normalization), "field/measure/quantum action-scale obstruction is retained"),
        ("VAL2773_5_delta_w_schema_missing_inputs", any(row["prior_id"] == "DWP2773_2_theorem_zero_option" and "MISSING" in row["value_or_status"] for row in prior) and any(row["prior_id"] == "DWP2773_4_tau_WEP" and "MISSING" in row["value_or_status"] for row in prior), "Delta_w theorem-zero and tau_WEP inputs remain missing"),
        ("VAL2773_6_tau_contract_written", any(row["contract_id"] == "TWP2773_7_verdict" and row["current_status"] == "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED" for row in tau), "tau_WEP projection contract is written but not derived"),
        ("VAL2773_7_prediction_nonclaim", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "WEP Delta-w product prediction remains nonclaim"),
        ("VAL2773_8_bound_anchor_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True and bounds[0]["valid_for_claim"] is False, "WEP bound anchor is numeric and internal-runner only"),
        ("VAL2773_9_runner_refuses_placeholder", runner[0]["valid_prediction_rows"] == 0 and runner[0]["valid_bound_rows"] == 1 and runner[0]["claim_allowed"] is False, "strict runner refuses missing Delta_w/tau product"),
        ("VAL2773_10_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all source-scalar/WEP/local-GR claim gates remain blocked"),
        ("VAL2773_11_next_target_written", any(row["row_id"] == "NEXT2773_0_2774" and "action-scale" in row["next_target"] for row in next_rows), "next target selects action-scale normalization or tau projection"),
        ("VAL2773_12_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2773_13_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2773_14_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2773_15_generated_files_in_post_checkpoint", generated_files_under_work(), "all generated files are under post-checkpoint-work"),
        ("VAL2773_16_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2773_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2773_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2773 attempts the parent source-scalar exclusion route in the current R2/f(R) branch, finds the lemma exact but still conditional because action-scale/measure ownership is unsigned, writes the WEP Delta-w prior-width and tau_WEP projection contracts, refuses missing Delta_w/tau placeholders, blocks all WEP/local-GR claims, and selects parent action-scale normalization or WEP tau projection as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2773 - Y5 R2/f(R): Parent Action Syntax Source-Scalar Exclusion Or WEP Delta-w Prior Width Under AX1090",
        "## Private Verdict\n\nThe source-scalar exclusion lemma is exact as a conditional theorem, but still not parent-derived. The block is not ordinary classical field normalization; it is action-scale / Hilbert-stress / measure ownership. A species-dependent multiplier `w_A S_A` cannot be dismissed unless the parent owns one universal action measure for all ordinary matter.\n\nFinite branch: if the theorem fails, the WEP row needs both `Delta_w_TiPt` and `tau_WEP`. The MICROSCOPE bound and material convention alone are still not a prediction.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Source-Scalar Exclusion Lemma\n\n" + markdown_table(rows_by_name["lemma"], ["lemma_id", "claim", "formal_statement", "attempt_result", "gap", "valid_for_claim"]),
        "## Object-Language Typing\n\n" + markdown_table(rows_by_name["typing"], ["type_id", "candidate", "type_status", "why", "wA_effect", "signature_status", "valid_for_claim"]),
        "## Operator-Domain Rule Audit\n\n" + markdown_table(rows_by_name["operator"], ["rule_id", "rule", "formal_form", "result", "obstruction", "valid_for_claim"]),
        "## Field / Measure / Quantum Normalization\n\n" + markdown_table(rows_by_name["normalization"], ["audit_id", "issue", "effect", "required_closure", "status", "valid_for_claim"]),
        "## WEP Delta-w Prior Width Schema\n\n" + markdown_table(rows_by_name["prior"], ["prior_id", "quantity", "value_or_status", "units", "formula_or_requirement", "status", "valid_for_claim"]),
        "## tau_WEP Projection Contract\n\n" + markdown_table(rows_by_name["tau"], ["contract_id", "input", "required_form", "current_status", "blocks", "valid_for_claim"]),
        "## WEP Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes"]),
        "## WEP Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim", "notes"]),
        "## Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc", "valid_for_claim"]),
        "## Runner Comparisons\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is a useful failed kill-shot: `w_A` survives only because the parent has not yet proved a single universal action-scale/measure owner. That is good news structurally: the problem is now one gate, not a fog bank. Either close that gate and relative source weights vanish, or build `tau_WEP` properly and bound the finite branch like grown-ups.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    lemma = build_lemma_rows()
    typing = build_typing_rows()
    operator = build_operator_rows()
    normalization = build_normalization_rows()
    prior = build_prior_rows()
    tau = build_tau_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("lemma", lemma), ("typing", typing), ("operator", operator),
        ("normalization", normalization), ("prior", prior), ("tau", tau), ("candidate", candidate),
        ("bounds", bounds), ("runner", runner), ("comparisons", comparisons), ("gates", gates),
        ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(lemma, typing, operator, normalization, prior, tau, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "lemma": lemma,
        "typing": typing,
        "operator": operator,
        "normalization": normalization,
        "prior": prior,
        "tau": tau,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2773_OVERALL")
    print(f"2773 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
