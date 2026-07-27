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
DOC = WORK / "2784-Y5-R2FR-parent-action-object-language-measure-current-owner-proof-stack-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2784_SOURCE_REGISTER.csv",
    "object_language": MTS / "P8_Y5_R2FR_2784_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "action_measure": MTS / "P8_Y5_R2FR_2784_ACTION_MEASURE_PROOF_ATTEMPT.csv",
    "current_owner": MTS / "P8_Y5_R2FR_2784_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "counterexamples": MTS / "P8_Y5_R2FR_2784_COUNTEREXAMPLE_KILL_MATRIX.csv",
    "demotion": MTS / "P8_Y5_R2FR_2784_THEOREM_ZERO_DEMOTION.csv",
    "finite_gates": MTS / "P8_Y5_R2FR_2784_FINITE_ROUTE_DEMOTION_GATES.csv",
    "candidate": MTS / "P8_Y5_R2FR_2784_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2784_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2784_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2784_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2784_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2784_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2784_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2784_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2784_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_queue": RAB_QUEUE / "JR2784_PARENT_ACTION_PROOF_STACK_NONCLAIM.csv",
    "finite_queue": RAB_QUEUE / "JR2784_FINITE_ROUTE_DEMOTION_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_WEP_THEOREM_ZERO_DEMOTION_2784_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_theorem_zero_demotion_2784_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2784_CURRENT_OWNER_NARROW_NEXT.csv",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2784_00_2783_next", "2783_next", MTS / "P8_Y5_R2FR_2783_NEXT_TARGET.csv", "NEXT2783_0_2784", "current handoff into parent action proof stack"),
        ("SRC2784_01_2783_validation", "2783_validation", MTS / "P8_Y5_BRR545_2783_VALIDATION.csv", "VAL2783_OVERALL", "current validation baseline"),
        ("SRC2784_02_2783_theorem", "2783_theorem", MTS / "P8_Y5_R2FR_2783_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv", "WCO2783_5_verdict", "current unsigned theorem-zero verdict"),
        ("SRC2784_03_2783_clauses", "2783_clauses", MTS / "P8_Y5_R2FR_2783_CLAUSE_SIGNATURE_MATRIX.csv", "CLAUSE2783_2_current_owner", "current unsigned clause matrix"),
        ("SRC2784_04_2783_counterexamples", "2783_counterexamples", MTS / "P8_Y5_R2FR_2783_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv", "CE2783_3_post_variation_selector", "current counterexample list"),
        ("SRC2784_05_2783_finite", "2783_finite", MTS / "P8_Y5_R2FR_2783_FINITE_ROUTE_REQUIREMENTS.csv", "FIN2783_2_C_parent", "current finite route requirements"),
        ("SRC2784_06_2783_material", "2783_material", MTS / "P8_Y5_R2FR_2783_MATERIAL_VECTOR_SOURCE_ROW_STATUS.csv", "MVS2783_0_toy_delta_TA6V_minus_PtRh10", "current toy material vector status"),
        ("SRC2784_07_1066_scalar", "1066_scalar", MTS / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "object-language scalar exclusion attempt"),
        ("SRC2784_08_1067_action", "1067_action", MTS / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner attempt"),
        ("SRC2784_09_1062_parent", "1062_parent", MTS / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "prior parent theorem attempt"),
        ("SRC2784_10_2782_owner", "2782_owner", MTS / "P8_Y5_R2FR_2782_COUPLING_OWNER_GATES.csv", "OWN2782_2_current_owner", "coupling owner gate source"),
        ("SRC2784_11_1078_precedent", "1078_precedent", WORK / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md", "Theorem-zero demotion", "R10 proof-stack precedent"),
        ("SRC2784_12_1079_current", "1079_current", MTS / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO1079_6_verdict", "R10 narrow current-owner precedent for next handoff"),
        ("SRC2784_13_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_object_language_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"object_language_id": "OL2784_0_target", "claim": "parent object-language typing signs allowed matter-action arguments", "allowed_argument_types": "observed geometry/coframe/metric; matter fields; gauge connections/currents; representation constants; universal constants", "forbidden_argument_types": "species-indexed inert source-only scalar w_A; disconnected label weight not carried by a field/current/representation", "proof_attempt": "promote 1066 from exclusion taste to a syntactic theorem of the parent action object language", "result": "TARGET_SHARPENED", "gap": "grammar exists as desired contract, not as a derived theorem from parent MTS primitives", "claim_allowed": False}),
        nonclaim({"object_language_id": "OL2784_1_positive_syntax", "claim": "positive syntax can list legitimate parent arguments", "allowed_argument_types": "fields, currents, representation data, orientation/measure data, and universal constants", "forbidden_argument_types": "bare species source weights outside those objects", "proof_attempt": "if every source term is a functorial expression of these objects, relative composition weights cannot be inserted after the fact", "result": "CONDITIONAL_FROM_1066", "gap": "the functorial-expression premise is still a parent axiom, not derived", "claim_allowed": False}),
        nonclaim({"object_language_id": "OL2784_2_forbidden_slot", "claim": "species-indexed inert w_A is forbidden", "allowed_argument_types": "observable species data only when carried by a field/current/representation", "forbidden_argument_types": "independent action multiplier w_A multiplying S_A", "proof_attempt": "show w_A has no transformation law, no current, no variation, and no representation owner in the parent category", "result": "NOT_PARENT_SIGNED", "gap": "absence of an owner is evidence of ugliness, not a proof of impossibility", "claim_allowed": False}),
        nonclaim({"object_language_id": "OL2784_3_counterexample", "claim": "disconnected species constants are impossible", "allowed_argument_types": "connected matter functor with one normalization", "forbidden_argument_types": "simple-object label constants c_A or w_A", "proof_attempt": "try to kill label constants by connectedness of the matter functor", "result": "COUNTEREXAMPLE_SURVIVES", "gap": "a direct-sum matter category can still carry independent constants unless the parent functor forbids them", "claim_allowed": False}),
        nonclaim({"object_language_id": "OL2784_4_verdict", "claim": "object-language proof closes theorem-zero premise", "allowed_argument_types": "positive list retained as contract", "forbidden_argument_types": "source-only scalar slot", "proof_attempt": "assemble positive syntax, forbidden-slot argument, and counterexample audit", "result": "OBJECT_LANGUAGE_NOT_SIGNED", "gap": "counterexample survives without a parent-derived object language", "claim_allowed": False}),
    ]


def build_action_measure_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"action_measure_id": "AM2784_0_target", "claim": "one hbar_parent/measure owner fixes ordinary matter normalization", "proof_attempt": "show S_parent/hbar_parent has a single integration measure and a single action scale for all ordinary matter sectors", "result": "TARGET_SHARPENED", "gap": "this would be the cleanest way to kill w_A S_A", "blocks_if_unsigned": "species action weights remain legal finite WEP branch inputs", "claim_allowed": False}),
        nonclaim({"action_measure_id": "AM2784_1_classical_eom", "claim": "classical equations alone fix action normalization", "proof_attempt": "use Euler-Lagrange equations to remove a constant multiplier per disconnected matter sector", "result": "OBSTRUCTION_ACKNOWLEDGED", "gap": "classical equations are insensitive to an overall sector multiplier until the sector couples as a source", "blocks_if_unsigned": "relative source strength can enter without changing isolated free-fall equations", "claim_allowed": False}),
        nonclaim({"action_measure_id": "AM2784_2_quantum_measure", "claim": "path-integral/statistical measure owner kills independent w_A S_A", "proof_attempt": "if all matter histories are weighted by the same parent hbar/measure, sector-specific action rescalings are not gauge-free choices", "result": "CONDITIONAL_FROM_1067", "gap": "1067 supplies a good conditional route but not a parent derivation", "blocks_if_unsigned": "finite WEP product must retain normalization coefficient C_parent", "claim_allowed": False}),
        nonclaim({"action_measure_id": "AM2784_3_missing_parent_measure", "claim": "parent corpus already contains a signed measure axiom", "proof_attempt": "search prior owner results for hbar/measure closure", "result": "NOT_PARENT_SIGNED", "gap": "no parent statistical/measure axiom is signed strongly enough to carry WEP theorem-zero", "blocks_if_unsigned": "species-blind action measure remains a closure requirement", "claim_allowed": False}),
        nonclaim({"action_measure_id": "AM2784_4_verdict", "claim": "action-measure proof closes theorem-zero premise", "proof_attempt": "assemble classical, quantum-measure, and source-coupling checks", "result": "ACTION_MEASURE_NOT_SIGNED", "gap": "the needed measure owner is plausible but currently an unsigned parent contract", "blocks_if_unsigned": "theorem-zero is closure-only", "claim_allowed": False}),
    ]


def build_current_owner_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"current_owner_id": "CO2784_0_target", "claim": "one current/source normalization owner fixes all ordinary matter source couplings", "proof_attempt": "derive the gravitational source and any gauge/Noether current from one parent current functor before readout", "result": "TARGET_SHARPENED", "gap": "current owner must be prior to material/readout projection", "blocks_if_unsigned": "J_A -> c_A J_A remains a legal source-normalization counterexample", "claim_allowed": False}),
        nonclaim({"current_owner_id": "CO2784_1_noether_route", "claim": "Noether/gauge representation data fix source normalization", "proof_attempt": "use representation charges to own gauge-current normalization", "result": "PARTIAL_FOR_GAUGE_ONLY", "gap": "gauge-current normalization does not by itself fix the Hilbert gravitational source normalization for WEP", "blocks_if_unsigned": "composition-dependent mass/source response can still enter", "claim_allowed": False}),
        nonclaim({"current_owner_id": "CO2784_2_hilbert_source_route", "claim": "Hilbert stress from variation before readout owns the gravitational source", "proof_attempt": "define T_mu_nu = delta S_matter / delta e_obs before any post-variation material selector is allowed", "result": "CONDITIONAL", "gap": "variation-before-readout is a strong contract, but the parent readout/order axiom is not signed here", "blocks_if_unsigned": "post-variation selector F(T_A,A) can mimic WEP residuals", "claim_allowed": False}),
        nonclaim({"current_owner_id": "CO2784_3_current_rescaling_counterexample", "claim": "current rescaling J_A -> c_A J_A is impossible", "proof_attempt": "try to absorb c_A into representation charge or field normalization", "result": "COUNTEREXAMPLE_SURVIVES", "gap": "without a single owner, source current normalization can be moved into a species coefficient", "blocks_if_unsigned": "finite route needs C_parent and source/material vectors", "claim_allowed": False}),
        nonclaim({"current_owner_id": "CO2784_4_verdict", "claim": "current-owner proof closes theorem-zero premise", "proof_attempt": "assemble Noether, Hilbert-source, and rescaling checks", "result": "CURRENT_OWNER_NOT_SIGNED", "gap": "Noether route is partial; Hilbert/readout route is conditional; rescaling counterexample survives", "blocks_if_unsigned": "WEP theorem-zero cannot be claimed", "claim_allowed": False}),
    ]


def build_counterexample_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"counterexample_id": "CEK2784_0_species_action_weight", "counterexample": "S_matter = sum_A w_A S_A", "kill_clause_required": "single parent hbar/action-measure owner plus no inert source-only scalar slot", "proof_status": "UNSIGNED", "result": "SURVIVES", "why_survives": "classical equations do not kill sector action multipliers before source coupling"}),
        nonclaim({"counterexample_id": "CEK2784_1_current_rescaling", "counterexample": "J_A -> c_A J_A", "kill_clause_required": "single current/source normalization owner", "proof_status": "UNSIGNED", "result": "SURVIVES", "why_survives": "current owner is not parent-signed; Noether route is gauge-only partial"}),
        nonclaim({"counterexample_id": "CEK2784_2_disconnected_material_components", "counterexample": "independent constants on disconnected material components", "kill_clause_required": "connected parent matter functor or no label-only constants theorem", "proof_status": "UNSIGNED", "result": "SURVIVES", "why_survives": "direct-sum matter sectors can carry label constants unless the parent object language forbids them"}),
        nonclaim({"counterexample_id": "CEK2784_3_post_variation_selector", "counterexample": "post-variation selector F(T_A,A)", "kill_clause_required": "variation-before-readout and official readout-kernel closure", "proof_status": "UNSIGNED", "result": "SURVIVES", "why_survives": "source/readout ordering remains a contract, not a signed theorem"}),
    ]


def build_demotion_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"demotion_id": "TZD2784_0_conditional", "statement": "the exact conditional theorem-zero from 2783 is retained", "status": "CONDITIONAL_THEOREM_RETAINED", "reason": "if object-language, action-measure, and current-owner premises are signed, P_WEP=0 follows", "claim_allowed": False}),
        nonclaim({"demotion_id": "TZD2784_1_missing_premises", "statement": "core premises remain unsigned", "status": "OBJECT_ACTION_CURRENT_UNSIGNED", "reason": "OL2784_4_verdict; AM2784_4_verdict; CO2784_4_verdict", "claim_allowed": False}),
        nonclaim({"demotion_id": "TZD2784_2_demote", "statement": "theorem-zero route is demoted to closure-only", "status": "CLOSURE_ONLY_UNSIGNED", "reason": "surviving counterexamples are legal until the parent action signs the owner clauses", "claim_allowed": False}),
        nonclaim({"demotion_id": "TZD2784_3_finite_route", "statement": "finite WEP route remains sourced-input route", "status": "FINITE_ROUTE_RETAINED_AS_SOURCED_INPUT_ONLY", "reason": "requires real material vector, Earth/source vector, C_parent owner, and official readout kernel", "claim_allowed": False}),
        nonclaim({"demotion_id": "TZD2784_4_verdict", "statement": "no WEP/local-GR product claim follows from 2784", "status": "NO_WEP_CLAIM", "reason": "conditional theorem is not parent-signed and finite product inputs are missing", "claim_allowed": False}),
    ]


def build_finite_gate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "FRD2784_0_material_vector", "object": "R_TA6V - R_PtRh10", "status": "TOY_ONLY_NONCLAIM", "required_to_unblock": "source-backed material response vector for actual MICROSCOPE composition/readout convention", "claim_allowed": False}),
        nonclaim({"gate_id": "FRD2784_1_source_vector", "object": "R_source^Earth", "status": "MISSING_SOURCE_VECTOR", "required_to_unblock": "source worldtube/current vector or common-mode theorem", "claim_allowed": False}),
        nonclaim({"gate_id": "FRD2784_2_coupling_owner", "object": "C_parent coupling owner", "status": "MISSING_COUPLING_OWNER", "required_to_unblock": "signed current/source normalization owner or sourced finite coefficient", "claim_allowed": False}),
        nonclaim({"gate_id": "FRD2784_3_readout_kernel", "object": "K_MICROSCOPE official readout kernel", "status": "MISSING_OFFICIAL_ARRAYS", "required_to_unblock": "official segment-level orbit/readout arrays or accepted reconstruction contract", "claim_allowed": False}),
        nonclaim({"gate_id": "FRD2784_4_product_runner", "object": "WEP product runner", "status": "MUST_REFUSE", "required_to_unblock": "numeric claim-valid prediction row and numeric sourced bound row", "claim_allowed": False}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2784_0_WEP_theorem_zero_or_finite_route_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_SIGNED_THEOREM_ZERO_OR_FINITE_SOURCED_VECTORS",
            "product_units": "dimensionless",
            "derivation_status": "THEOREM_ZERO_CLOSURE_ONLY_FINITE_ROUTE_MISSING",
            "notes": "object-language, action-measure, and current-owner proofs remain unsigned; finite route requires sourced vectors",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2784_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
            "bound_type": "source_backed_upper_bound_anchor",
            "source_row_id": "R1_WEP_source_charge",
            "bound_valid_for_internal_runner": True,
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
        nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS tau_WEP/direct-product prediction rows"})
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2784_0_WEP_parent_action_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject closure-only theorem-zero and missing finite vectors",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2784_0_conditional_theorem", "claim_component": "conditional theorem-zero", "gate_pass": True, "claim_allowed": False, "reason": "conditional theorem is retained but cannot be used as a claim until premises are signed"}),
        nonclaim({"gate_id": "CG2784_1_object_language", "claim_component": "parent object-language typing", "gate_pass": False, "claim_allowed": False, "reason": "OL2784_4_verdict=OBJECT_LANGUAGE_NOT_SIGNED"}),
        nonclaim({"gate_id": "CG2784_2_action_measure", "claim_component": "species-blind action measure", "gate_pass": False, "claim_allowed": False, "reason": "AM2784_4_verdict=ACTION_MEASURE_NOT_SIGNED"}),
        nonclaim({"gate_id": "CG2784_3_current_owner", "claim_component": "single current/source owner", "gate_pass": False, "claim_allowed": False, "reason": "CO2784_4_verdict=CURRENT_OWNER_NOT_SIGNED"}),
        nonclaim({"gate_id": "CG2784_4_finite_vectors", "claim_component": "finite WEP source/material vectors", "gate_pass": False, "claim_allowed": False, "reason": "FRD2784 gates retain toy/missing source, coupling, and official readout inputs"}),
        nonclaim({"gate_id": "CG2784_5_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2784_0_conditional_theorem", "decision": "retain conditional theorem-zero as a closure theorem", "because": "the algebraic logic is clean if object/action/current owner clauses are signed", "next_action": "do not use it as evidence until the premises are parent-derived"}),
        nonclaim({"decision_id": "DEC2784_1_demote_theorem_zero", "decision": "demote theorem-zero to closure-only unsigned", "because": "all three proof stacks leave counterexamples alive", "next_action": "route WEP through finite sourced inputs unless a narrow owner proof is found"}),
        nonclaim({"decision_id": "DEC2784_2_finite_route", "decision": "keep finite WEP as sourced-input route", "because": "material, source, coupling-owner, and official readout vectors are not complete", "next_action": "source real finite WEP vectors if the current-owner proof fails"}),
        nonclaim({"decision_id": "DEC2784_3_next_target", "decision": "try the narrow current/source normalization owner proof first", "because": "it is the least broad premise and the one that blocks both theorem-zero and finite coefficient ownership", "next_action": "write 2785 current-owner narrow proof or finite WEP source-vector contract"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2784_0_2785",
            "next_target": "2785-Y5-R2FR-parent-current-owner-narrow-proof-or-finite-WEP-source-vector-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_current_owner_narrow_proof_or_finite_WEP_source_vector_under_AX1090_2785.py",
            "objective": "try the narrow current/source normalization owner proof first; if it remains unsigned, begin finite WEP sourced-input acquisition with a real source vector/material tensor contract",
            "include": "current functor owner; Hilbert source variation-before-readout; representation/current normalization; source-vector contract; material-vector contract; runner refusal",
            "exclude": "tau=1; Delta_w=0 by taste; toy vector as evidence; measured-G absorption; public claim; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    object_language: list[dict[str, Any]],
    action_measure: list[dict[str, Any]],
    current_owner: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    finite_gates: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    proof_rows = object_language + action_measure + current_owner + counterexamples + demotion + candidate + gates
    finite_rows = finite_gates + candidate + gates
    beta_rows = object_language + action_measure + current_owner + demotion + next_rows
    microscope_rows = proof_rows + finite_gates + next_rows
    specs = [
        ("BR2784_0_proof_queue", "proof_stack", proof_rows, OUTPUTS["demotion"], BRANCH_OUTPUTS["proof_queue"], "parent action proof stack nonclaim copy"),
        ("BR2784_1_finite_queue", "finite", finite_rows, OUTPUTS["finite_gates"], BRANCH_OUTPUTS["finite_queue"], "finite route demotion nonclaim copy"),
        ("BR2784_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["demotion"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing theorem-zero demotion copy"),
        ("BR2784_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE theorem-zero demotion copy"),
        ("BR2784_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next narrow current-owner route"),
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
    object_language = rows_by_name["object_language"]
    action_measure = rows_by_name["action_measure"]
    current_owner = rows_by_name["current_owner"]
    counterexamples = rows_by_name["counterexamples"]
    demotion = rows_by_name["demotion"]
    finite_gates = rows_by_name["finite_gates"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2784_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2784_1_object_language_unsigned", any(row["object_language_id"] == "OL2784_4_verdict" and row["result"] == "OBJECT_LANGUAGE_NOT_SIGNED" for row in object_language), "object-language proof does not close"),
        ("VAL2784_2_action_measure_unsigned", any(row["action_measure_id"] == "AM2784_4_verdict" and row["result"] == "ACTION_MEASURE_NOT_SIGNED" for row in action_measure), "action-measure proof does not close"),
        ("VAL2784_3_current_owner_unsigned", any(row["current_owner_id"] == "CO2784_4_verdict" and row["result"] == "CURRENT_OWNER_NOT_SIGNED" for row in current_owner), "current-owner proof does not close"),
        ("VAL2784_4_counterexamples_survive", len(counterexamples) == 4 and all(row["result"] == "SURVIVES" for row in counterexamples), "all 2783 theorem-zero counterexamples still survive"),
        ("VAL2784_5_theorem_zero_demoted", any(row["demotion_id"] == "TZD2784_2_demote" and row["status"] == "CLOSURE_ONLY_UNSIGNED" for row in demotion), "theorem-zero is explicitly demoted to closure-only"),
        ("VAL2784_6_finite_route_blocks", len(finite_gates) == 5 and all(row["claim_allowed"] is False for row in finite_gates), "finite WEP route gates all block claims"),
        ("VAL2784_7_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row remains missing theorem or finite sourced vectors"),
        ("VAL2784_8_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import is positive numeric"),
        ("VAL2784_9_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2784_10_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2784_0_conditional_theorem" and row["gate_pass"] is True for row in gates), "all claim gates deny WEP/local-GR claim"),
        ("VAL2784_11_next_target", any(row["row_id"] == "NEXT2784_0_2785" and "parent-current-owner-narrow-proof" in row["next_target"] for row in next_rows), "2785 handoff written"),
        ("VAL2784_12_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2784_13_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2784_14_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2784_15_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2784_16_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2784_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2784_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2784 attempts to sign the WEP theorem-zero premises from the parent action proof stack. Object-language typing, action-measure ownership, and current/source ownership remain unsigned; all counterexamples survive; theorem-zero is demoted to closure-only; finite WEP remains a sourced-input route; product claims are refused; 2785 targets the narrow current/source normalization owner proof.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2784 - Y5 R2/f(R): Parent Action Object-Language, Measure, Current-Owner Proof Stack Under AX1090",
        "## Private Verdict\n\n2784 tries to close the WEP theorem-zero route from inside the parent action. It does not get the signatures: object-language typing, action-measure ownership, and current/source normalization ownership all remain unsigned. The conditional theorem is retained as a useful closure theorem, but theorem-zero is demoted to closure-only and finite WEP stays a sourced-input route.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Object-Language Proof Attempt\n\n" + markdown_table(rows_by_name["object_language"], ["object_language_id", "claim", "allowed_argument_types", "forbidden_argument_types", "proof_attempt", "result", "gap", "claim_allowed", "valid_for_claim"]),
        "## Action-Measure Proof Attempt\n\n" + markdown_table(rows_by_name["action_measure"], ["action_measure_id", "claim", "proof_attempt", "result", "gap", "blocks_if_unsigned", "claim_allowed", "valid_for_claim"]),
        "## Current-Owner Proof Attempt\n\n" + markdown_table(rows_by_name["current_owner"], ["current_owner_id", "claim", "proof_attempt", "result", "gap", "blocks_if_unsigned", "claim_allowed", "valid_for_claim"]),
        "## Counterexample Kill Matrix\n\n" + markdown_table(rows_by_name["counterexamples"], ["counterexample_id", "counterexample", "kill_clause_required", "proof_status", "result", "why_survives", "valid_for_claim"]),
        "## Theorem-Zero Demotion\n\n" + markdown_table(rows_by_name["demotion"], ["demotion_id", "statement", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Finite Route Demotion Gates\n\n" + markdown_table(rows_by_name["finite_gates"], ["gate_id", "object", "status", "required_to_unblock", "claim_allowed", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis was the proper theorem shot. It did not close, but it failed usefully: WEP-zero needs a signed parent grammar/measure/current owner, not vibes. The least broad remaining proof target is current/source normalization; if that also fails, we stop theorem hunting and start finite sourced-vector acquisition.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    object_language = build_object_language_rows()
    action_measure = build_action_measure_rows()
    current_owner = build_current_owner_rows()
    counterexamples = build_counterexample_rows()
    demotion = build_demotion_rows()
    finite_gates = build_finite_gate_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decision_rows()
    next_rows = build_next_rows()

    for key, rows in [
        ("sources", sources), ("object_language", object_language), ("action_measure", action_measure),
        ("current_owner", current_owner), ("counterexamples", counterexamples), ("demotion", demotion),
        ("finite_gates", finite_gates), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision),
        ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(object_language, action_measure, current_owner, counterexamples, demotion, finite_gates, candidate, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "object_language": object_language,
        "action_measure": action_measure,
        "current_owner": current_owner,
        "counterexamples": counterexamples,
        "demotion": demotion,
        "finite_gates": finite_gates,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2784_OVERALL")
    print(f"2784 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
