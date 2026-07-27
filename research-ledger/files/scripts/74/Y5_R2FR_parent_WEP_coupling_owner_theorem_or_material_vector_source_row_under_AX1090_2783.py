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
DOC = WORK / "2783-Y5-R2FR-parent-WEP-coupling-owner-theorem-or-material-vector-source-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2783_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2783_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
    "clauses": MTS / "P8_Y5_R2FR_2783_CLAUSE_SIGNATURE_MATRIX.csv",
    "counterexamples": MTS / "P8_Y5_R2FR_2783_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
    "material": MTS / "P8_Y5_R2FR_2783_MATERIAL_VECTOR_SOURCE_ROW_STATUS.csv",
    "finite": MTS / "P8_Y5_R2FR_2783_FINITE_ROUTE_REQUIREMENTS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2783_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2783_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2783_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2783_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2783_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2783_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2783_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2783_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2783_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2783_WEP_COUPLING_OWNER_THEOREM_NONCLAIM.csv",
    "finite_queue": RAB_QUEUE / "JR2783_FINITE_WEP_ROUTE_REQUIREMENTS_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_WEP_COUPLING_OWNER_2783_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_coupling_owner_2783_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2783_PARENT_ACTION_PROOF_STACK_NEXT.csv",
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
        ("SRC2783_00_2782_next", "2782_next", MTS / "P8_Y5_R2FR_2782_NEXT_TARGET.csv", "NEXT2782_0_2783", "current handoff into WEP coupling-owner theorem"),
        ("SRC2783_01_2782_validation", "2782_validation", MTS / "P8_Y5_BRR545_2782_VALIDATION.csv", "VAL2782_OVERALL", "current validation baseline"),
        ("SRC2783_02_2782_contract", "2782_contract", MTS / "P8_Y5_R2FR_2782_PARENT_PRODUCT_CONTRACT_UPDATE.csv", "PWC2782_2_theorem_zero", "current theorem-zero contract"),
        ("SRC2783_03_2782_derivation", "2782_derivation", MTS / "P8_Y5_R2FR_2782_PARENT_MAP_DERIVATION_ATTEMPT.csv", "DER2782_5_verdict", "current parent map not-derived verdict"),
        ("SRC2783_04_2782_owner", "2782_owner", MTS / "P8_Y5_R2FR_2782_COUPLING_OWNER_GATES.csv", "OWN2782_2_current_owner", "current owner gates"),
        ("SRC2783_05_2782_toy", "2782_toy", MTS / "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv", "MV2782_delta_TA6V_minus_PtRh10", "current toy finite material row"),
        ("SRC2783_06_1062_parent", "1062_parent", MTS / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "prior parent theorem attempt"),
        ("SRC2783_07_1066_scalar", "1066_scalar", MTS / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source scalar exclusion conditional"),
        ("SRC2783_08_1067_action", "1067_action", MTS / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner conditional"),
        ("SRC2783_09_1068_direct", "1068_direct", MTS / "P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv", "DPF1068_2_theorem_zero_route", "theorem-zero route unsigned"),
        ("SRC2783_10_708_map", "708_map", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "source/test charge vector missing"),
        ("SRC2783_11_1078_precedent", "1078_precedent", WORK / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md", "Theorem-zero demotion", "R10 proof-stack precedent for next handoff"),
        ("SRC2783_12_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"theorem_id": "WCO2783_0_target", "claim": "parent WEP coupling-owner theorem", "formal_statement": "ordinary matter couples to the observed coframe/metric through one species-blind parent action measure/current owner, so no source-only relative species weight exists", "proof_move": "show all WEP-sensitive variations factor through universal Hilbert stress before readout", "result": "TARGET_SHARPENED", "gap": "clauses must be signed from parent action syntax, not adopted as taste", "claim_allowed": False}),
        nonclaim({"theorem_id": "WCO2783_1_conditional_theorem", "claim": "conditional theorem-zero", "formal_statement": "if parent object language excludes inert source-only scalars, action measure is species blind, and current/source normalization has one owner, then P_WEP=0", "proof_move": "Lie_v S_matter=0 for species-only source selectors; delta S/delta e_obs gives common Hilbert source; readout difference cancels", "result": "EXACT_CONDITIONAL_THEOREM", "gap": "premises remain unsigned", "claim_allowed": False}),
        nonclaim({"theorem_id": "WCO2783_2_object_language", "claim": "no inert source-only parent argument", "formal_statement": "Arg(S_parent) contains geometry, matter fields, gauge/current data, representation constants, and universal constants only", "proof_move": "exclude species-indexed w_A unless it is carried by an observable field/current/representation object", "result": "CONDITIONAL_FROM_SSE1066", "gap": "parent object language not derived from MTS primitives", "claim_allowed": False}),
        nonclaim({"theorem_id": "WCO2783_3_action_measure", "claim": "species-blind action-scale/measure owner", "formal_statement": "S_parent/hbar_parent has one action scale and one measure/Jacobian for all ordinary matter species", "proof_move": "rule out S_A -> w_A S_A by quantum/statistical measure ownership", "result": "CONDITIONAL_FROM_ASO1067", "gap": "hbar/measure owner not parent-derived", "claim_allowed": False}),
        nonclaim({"theorem_id": "WCO2783_4_current_owner", "claim": "single current/source normalization owner", "formal_statement": "matter currents and source normalization descend from one parent current functor, not species-specific weights", "proof_move": "fix representation charges/currents before readout and disallow post-variation source selectors", "result": "NOT_DERIVED", "gap": "current functor/representation owner is still missing", "claim_allowed": False}),
        nonclaim({"theorem_id": "WCO2783_5_verdict", "claim": "WEP theorem-zero closure", "formal_statement": "P_WEP=0 follows only after WCO2783_2..4 and readout/source closure are parent-signed", "proof_move": "assemble conditional theorem and test for unsigned clauses", "result": "THEOREM_ZERO_NOT_CLOSED_CURRENT_CORPUS", "gap": "object-language, measure/current owner, source worldtube/common-mode, and official readout array gates remain unsigned", "claim_allowed": False}),
    ]


def build_clause_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"clause_id": "CLAUSE2783_0_object_language", "needed_clause": "parent object-language typing excludes source-only species scalar w_A", "status": "CONDITIONAL_UNSIGNED", "source_evidence": "SSE1066_5_verdict", "if_unsigned_effect": "finite WEP branch requires sourced material/source vectors"}),
        nonclaim({"clause_id": "CLAUSE2783_1_action_measure", "needed_clause": "single species-blind action measure/hbar owner", "status": "CONDITIONAL_UNSIGNED", "source_evidence": "ASO1067_5_verdict", "if_unsigned_effect": "species action weights remain legal counterexamples"}),
        nonclaim({"clause_id": "CLAUSE2783_2_current_owner", "needed_clause": "single current/source normalization owner", "status": "MISSING", "source_evidence": "THM1062_2_EM_source_owner; OWN2782_2_current_owner", "if_unsigned_effect": "source-only current normalization remains legal"}),
        nonclaim({"clause_id": "CLAUSE2783_3_source_worldtube", "needed_clause": "Earth/source leg is universal common mode or sourced finite vector", "status": "MISSING", "source_evidence": "SWT1068_5_verdict; OWN2782_4_source_worldtube", "if_unsigned_effect": "finite source response vector R_source is required"}),
        nonclaim({"clause_id": "CLAUSE2783_4_material_tensor", "needed_clause": "Ti/Pt response is universal zero or sourced finite tensor", "status": "TOY_ONLY", "source_evidence": "MV2782_delta_TA6V_minus_PtRh10; MAT1068_5_verdict", "if_unsigned_effect": "toy vector remains algebra-only"}),
        nonclaim({"clause_id": "CLAUSE2783_5_readout_kernel", "needed_clause": "official MICROSCOPE readout arrays or validated reconstruction", "status": "MISSING_OFFICIAL_ARRAYS", "source_evidence": "IMP2782_0_official_arrays; RG2781_0_official_arrays", "if_unsigned_effect": "surrogate-only tests remain nonclaim"}),
    ]


def build_counterexample_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"counterexample_id": "CE2783_0_species_action_weight", "legal_if_unsigned": "ASO/action measure owner", "form": "S_matter = sum_A w_A S_A with constant w_A", "why_dangerous": "classical equations can look unchanged while Hilbert stress/source normalization changes", "blocks": "theorem-zero WEP"}),
        nonclaim({"counterexample_id": "CE2783_1_current_rescaling", "legal_if_unsigned": "current owner", "form": "J_A -> c_A J_A or beta_source,A source marker", "why_dangerous": "creates species/source charge vector without changing geometry syntax", "blocks": "source-scalar exclusion"}),
        nonclaim({"counterexample_id": "CE2783_2_disconnected_material_components", "legal_if_unsigned": "object-language/naturality connectedness", "form": "ordinary matter category has disconnected simple-object components with natural constants per component", "why_dangerous": "naturality alone does not force universal weights", "blocks": "material universality proof"}),
        nonclaim({"counterexample_id": "CE2783_3_post_variation_selector", "legal_if_unsigned": "variation-before-readout/readout closure", "form": "readout projection applies F(T_A,A) after Hilbert stress variation", "why_dangerous": "species labels can re-enter after common stress derivation", "blocks": "readout theorem-zero"}),
    ]


def build_material_rows() -> list[dict[str, Any]]:
    toy_rows = read_csv_rows(MTS / "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv")
    delta = next((row for row in toy_rows if row.get("material_vector_id") == "MV2782_delta_TA6V_minus_PtRh10"), {})
    return [
        nonclaim({"material_source_id": "MVS2783_0_toy_delta_TA6V_minus_PtRh10", "route": "finite material vector fallback", "available_row": "MV2782_delta_TA6V_minus_PtRh10", "q_Z_over_A_toy": delta.get("q_Z_over_A_toy", ""), "status": "TOY_SOURCE_ROW_AVAILABLE_NONCLAIM", "missing_for_claim": "source-backed isotope/chemical/material tensor or parent response theorem"}),
        nonclaim({"material_source_id": "MVS2783_1_required_claim_material", "route": "finite material vector claim route", "available_row": "none", "q_Z_over_A_toy": "", "status": "MISSING_CLAIM_VALID_MATERIAL_VECTOR", "missing_for_claim": "R_TA6V and R_PtRh10 from parent action or sourced material model"}),
    ]


def build_finite_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"requirement_id": "FIN2783_0_R_material", "object": "R_TA6V - R_PtRh10", "required_evidence": "parent-derived material response tensor or source-backed material model", "current_status": "TOY_VECTOR_ONLY", "blocks": "finite P_WEP"}),
        nonclaim({"requirement_id": "FIN2783_1_R_source", "object": "R_source^Earth", "required_evidence": "Earth/source composition/worldtube or parent theorem proving source common mode", "current_status": "MISSING_SOURCE_VECTOR", "blocks": "finite P_WEP"}),
        nonclaim({"requirement_id": "FIN2783_2_C_parent", "object": "C_parent coupling owner", "required_evidence": "parent coefficient/coupling basis with units and normalization", "current_status": "MISSING_COUPLING_OWNER", "blocks": "finite and theorem-zero routes"}),
        nonclaim({"requirement_id": "FIN2783_3_K_readout", "object": "K_MICROSCOPE readout kernel", "required_evidence": "official CMSM arrays/masks or validated reconstruction", "current_status": "SURROGATE_ONLY", "blocks": "empirical scoring"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2783_0_WEP_coupling_owner_theorem_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_COUPLING_OWNER_THEOREM_OR_SOURCED_FINITE_VECTORS",
            "product_units": "dimensionless",
            "derivation_status": "THEOREM_ZERO_UNSIGNED_FINITE_ROUTE_MISSING",
            "notes": "conditional theorem is coherent, but its parent premises are unsigned; finite route lacks sourced vectors",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2783_0_MICROSCOPE_R1_eta_source_charge",
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
            "runner_id": "APR2783_0_WEP_coupling_owner_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject unsigned theorem/missing finite vectors and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2783_0_conditional_theorem", "claim_component": "conditional WEP theorem-zero", "gate_pass": True, "claim_allowed": False, "reason": "premises unsigned"}),
        nonclaim({"gate_id": "CG2783_1_parent_object_language", "claim_component": "parent object-language typing", "gate_pass": False, "claim_allowed": False, "reason": "CONDITIONAL_UNSIGNED"}),
        nonclaim({"gate_id": "CG2783_2_current_measure_owner", "claim_component": "species-blind measure/current owner", "gate_pass": False, "claim_allowed": False, "reason": "MEASURE_CONDITIONAL_CURRENT_MISSING"}),
        nonclaim({"gate_id": "CG2783_3_finite_vectors", "claim_component": "sourced finite material/source vectors", "gate_pass": False, "claim_allowed": False, "reason": "TOY_MATERIAL_ONLY_SOURCE_VECTOR_MISSING"}),
        nonclaim({"gate_id": "CG2783_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2783_0_conditional_theorem_kept", "decision": "keep theorem-zero route because the conditional theorem is coherent", "evidence": "WCO2783_1_conditional_theorem", "consequence": "next work should try to sign the parent premises"}),
        nonclaim({"decision_id": "DEC2783_1_no_WEP_claim", "decision": "do not claim WEP/local-GR pass", "evidence": "WCO2783_5_verdict; APR2783_0_WEP_coupling_owner_product_stub", "consequence": "P_WEP remains missing"}),
        nonclaim({"decision_id": "DEC2783_2_next_target", "decision": "attack the parent object-language/measure/current owner proof stack", "evidence": "CLAUSE2783_0_object_language; CLAUSE2783_1_action_measure; CLAUSE2783_2_current_owner", "consequence": "2784 should try to sign theorem-zero premises or demote to finite sourced route"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2783_0_2784",
            "next_target": "2784-Y5-R2FR-parent-action-object-language-measure-current-owner-proof-stack-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_action_object_language_measure_current_owner_proof_stack_under_AX1090_2784.py",
            "objective": "attempt to sign the three core premises of the WEP theorem-zero route: parent object-language typing, species-blind action measure, and single current/source normalization owner; if any remain unsigned, demote theorem-zero to closure-only and keep finite WEP as sourced-input route",
            "include": "parent action syntax; allowed argument types; hbar/measure owner; current functor owner; counterexample kill list; finite-route demotion gates; product-runner refusal",
            "exclude": "Delta_w=0 by taste; tau=1; cancellation tuning; toy material vector as evidence; measured-G absorption; public claim; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    material: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_rows = theorem + clauses + counterexamples + candidate + gates
    finite_rows = material + finite + candidate + gates
    beta_rows = theorem + clauses + next_rows
    microscope_rows = theorem + clauses + counterexamples + material + finite + candidate + next_rows
    specs = [
        ("BR2783_0_theorem_queue", "theorem", theorem_rows, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "WEP coupling-owner theorem nonclaim copy"),
        ("BR2783_1_finite_queue", "finite", finite_rows, OUTPUTS["finite"], BRANCH_OUTPUTS["finite_queue"], "finite WEP route requirements nonclaim copy"),
        ("BR2783_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["clauses"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing WEP theorem copy"),
        ("BR2783_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE WEP coupling-owner copy"),
        ("BR2783_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next parent action proof-stack route"),
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
    theorem = rows_by_name["theorem"]
    clauses = rows_by_name["clauses"]
    counterexamples = rows_by_name["counterexamples"]
    material = rows_by_name["material"]
    finite = rows_by_name["finite"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2783_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2783_1_conditional_theorem", any(row["theorem_id"] == "WCO2783_1_conditional_theorem" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), "conditional theorem-zero statement staged"),
        ("VAL2783_2_theorem_not_closed", any(row["theorem_id"] == "WCO2783_5_verdict" and row["result"] == "THEOREM_ZERO_NOT_CLOSED_CURRENT_CORPUS" for row in theorem), "theorem-zero remains unsigned"),
        ("VAL2783_3_clause_matrix_blocks", len(clauses) == 6 and any(row["clause_id"] == "CLAUSE2783_2_current_owner" and row["status"] == "MISSING" for row in clauses), "clause matrix captures current-owner and material gaps"),
        ("VAL2783_4_counterexamples", len(counterexamples) == 4 and all(row["valid_for_claim"] is False for row in counterexamples), "counterexample kill list staged"),
        ("VAL2783_5_material_source_row_nonclaim", any(row["material_source_id"] == "MVS2783_0_toy_delta_TA6V_minus_PtRh10" and row["status"] == "TOY_SOURCE_ROW_AVAILABLE_NONCLAIM" for row in material), "toy material source row demoted to nonclaim"),
        ("VAL2783_6_finite_route_requirements", len(finite) == 4 and any(row["requirement_id"] == "FIN2783_2_C_parent" and row["current_status"] == "MISSING_COUPLING_OWNER" for row in finite), "finite route requirements staged"),
        ("VAL2783_7_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row remains missing theorem or finite vectors"),
        ("VAL2783_8_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import is positive numeric"),
        ("VAL2783_9_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2783_10_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2783_0_conditional_theorem" and row["gate_pass"] is True for row in gates), "all claim gates deny WEP/local-GR claim"),
        ("VAL2783_11_next_target", any(row["row_id"] == "NEXT2783_0_2784" and "parent-action-object-language-measure-current-owner-proof-stack" in row["next_target"] for row in next_rows), "2784 handoff written"),
        ("VAL2783_12_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2783_13_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2783_14_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2783_15_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2783_16_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2783_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2783_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2783 stages a coherent conditional WEP theorem-zero route but does not close it. Object-language, action-measure, current-owner, source-worldtube, material tensor, and official readout array clauses remain unsigned or missing. The finite WEP route is kept as sourced-input only, the product runner refuses claims, and 2784 targets the parent action object-language/measure/current-owner proof stack.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2783 - Y5 R2/f(R): Parent WEP Coupling-Owner Theorem Or Material-Vector Source Row Under AX1090",
        "## Private Verdict\n\n2783 keeps the WEP theorem-zero route alive, but only as an exact conditional theorem. The conditional logic is clean: if parent object-language typing, species-blind action measure, and single current/source owner are signed, then P_WEP=0. They are not signed yet. The finite WEP route therefore remains sourced-input only.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Coupling-Owner Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["theorem_id", "claim", "formal_statement", "proof_move", "result", "gap", "claim_allowed", "valid_for_claim"]),
        "## Clause Signature Matrix\n\n" + markdown_table(rows_by_name["clauses"], ["clause_id", "needed_clause", "status", "source_evidence", "if_unsigned_effect", "valid_for_claim"]),
        "## Counterexample Audit\n\n" + markdown_table(rows_by_name["counterexamples"], ["counterexample_id", "legal_if_unsigned", "form", "why_dangerous", "blocks", "valid_for_claim"]),
        "## Material-Vector Source Row Status\n\n" + markdown_table(rows_by_name["material"], ["material_source_id", "route", "available_row", "q_Z_over_A_toy", "status", "missing_for_claim", "valid_for_claim"]),
        "## Finite Route Requirements\n\n" + markdown_table(rows_by_name["finite"], ["requirement_id", "object", "required_evidence", "current_status", "blocks", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is not a failure-failure; it is a clean fork in the road. Either the parent action really forbids species/source weights, in which case WEP can close elegantly by theorem-zero, or the finite WEP branch must earn its keep with sourced material/source vectors. No free lunch, no ghost coupling.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    theorem = build_theorem_rows()
    clauses = build_clause_rows()
    counterexamples = build_counterexample_rows()
    material = build_material_rows()
    finite = build_finite_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decision_rows()
    next_rows = build_next_rows()

    for key, rows in [
        ("sources", sources), ("theorem", theorem), ("clauses", clauses),
        ("counterexamples", counterexamples), ("material", material), ("finite", finite),
        ("candidate", candidate), ("bounds", bounds), ("runner", runner),
        ("comparisons", comparisons), ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(theorem, clauses, counterexamples, material, finite, candidate, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "theorem": theorem,
        "clauses": clauses,
        "counterexamples": counterexamples,
        "material": material,
        "finite": finite,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2783_OVERALL")
    print(f"2783 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
