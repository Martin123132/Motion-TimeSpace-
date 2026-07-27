from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1722"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1722 - Parent Action-Density Edge Or CwH Current Norm Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1722_0_1721_doc",
        "source_key": "1721_doc",
        "source_path": ROOT / "1721-Y5-R2FR-source-prefactor-exclusion-or-wA-current-row.md",
        "needles": ["NEXT1721_0_primary", "C_wH"],
    },
    {
        "source_id": "SRC1722_1_1721_validation",
        "source_key": "1721_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1721_VALIDATION.csv",
        "needles": ["VAL1721_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1722_2_1721_no_prefactor",
        "source_key": "1721_no_prefactor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_NO_SOURCE_PREFACTOR_THEOREM_AUDIT.csv",
        "needles": ["NSP1721_4_verdict", "NO_SOURCE_PREFACTOR_NOT_DERIVED"],
    },
    {
        "source_id": "SRC1722_3_1721_wA_current",
        "source_key": "1721_wA_current",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_WA_CURRENT_NORM_SOURCE_ROWS.csv",
        "needles": ["WAC1721_1_weighted_current_norm_candidate", "MISSING_COMPONENT_TENSOR"],
    },
    {
        "source_id": "SRC1722_4_1720_jh_theorem",
        "source_key": "1720_jh_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
        "needles": ["JHT1720_2_norm_convention", "MISSING_NORM_CONVENTION_AND_VALUE"],
    },
    {
        "source_id": "SRC1722_5_1719_factor_bound",
        "source_key": "1719_factor_bound",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NDOMAIN_FACTOR_BOUND_CONTRACT.csv",
        "needles": ["NF1719_0_factorized_bound", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1722_6_1605_action_owner",
        "source_key": "1605_action_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["ADO1605_6_verdict", "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1722_7_1606_edges",
        "source_key": "1606_edges",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv",
        "needles": ["EDGE1606_7_verdict", "NOT_PARENT_CERTIFIED"],
    },
    {
        "source_id": "SRC1722_8_1606_component_pack",
        "source_key": "1606_component_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
        "needles": ["DWB1606_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"],
    },
    {
        "source_id": "SRC1722_9_1607_material_tensor",
        "source_key": "1607_material_tensor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_CONTEXT_AUDIT.csv",
        "needles": ["MTA1607_5_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    },
    {
        "source_id": "SRC1722_10_1608_tau",
        "source_key": "1608_tau",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles_present": yesno(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


def sources_for(keys: set[str]) -> str:
    return ";".join(str(item["source_path"]) for item in SOURCES if item["source_key"] in keys)


PARENT_EDGE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "edge_id": "PED1722_0_target",
        "claim_piece": "parent action-density edge owner",
        "formal_statement": "ordinary sectors are linked by nonzero parent-owned morphisms on one L_action line before source variation",
        "mathematical_effect": "naturality w_B F(e)=F(e) w_A forces w_A=w_B on each nonzero edge",
        "current_status": "TARGET_EXACT",
        "blocking_gap": "no imported parent action-density edge source",
        "edge_zero_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "edge_id": "PED1722_1_minimal_edge_set",
        "claim_piece": "source-relevant edge set",
        "formal_statement": "QED, QCD, mass/Yukawa, nuclear/atomic binding, measure/current, and readout edges must all be parent-owned",
        "mathematical_effect": "connected source graph collapses component delta_w_i to derivative-silent common w_star",
        "current_status": "PHYSICAL_TEMPLATE_ONLY",
        "blocking_gap": "1606 edge audit has NOT_PARENT_CERTIFIED verdict",
        "edge_zero_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "edge_id": "PED1722_2_no_Hom_plus_edge_zero_law",
        "claim_piece": "C_wH zero theorem",
        "formal_statement": "if no source-only Hom exists and the parent action-density graph is connected, then delta_w_A=0 modulo common calibration and C_wH=0",
        "mathematical_effect": "weighted-current correction vanishes before N_domain/J_H scoring",
        "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
        "blocking_gap": "no-Hom, common measure, edge ownership, readout no-reentry and non-Hilbert silence remain unsigned",
        "edge_zero_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "edge_id": "PED1722_3_false_routes",
        "claim_piece": "false edge proof routes",
        "formal_statement": "physical connectedness, same-action variation, classical EOM scaling, and measured-G absorption do not prove parent-owned edges",
        "mathematical_effect": "prevents hidden source-universality assumptions",
        "current_status": "GUARDRAIL_RETAINED",
        "blocking_gap": "none; guardrail remains active",
        "edge_zero_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "edge_id": "PED1722_4_verdict",
        "claim_piece": "parent edge proof status",
        "formal_statement": "C_wH cannot be theorem-zeroed by the current corpus because no parent-owned action-density edge certificate is sourced",
        "mathematical_effect": "finite C_wH operator-bound route remains mandatory",
        "current_status": "PARENT_EDGE_NOT_DERIVED",
        "blocking_gap": "source parent edge theorem or accept finite bound row",
        "edge_zero_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CWH_BOUND_LAW_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "law_id": "CWHL1722_0_definition",
        "quantity": "C_wH",
        "law": "C_wH := ||star(sum_i delta_w_i T_i_obs(tau,.))||_{A_ext,norm}",
        "status": "FORMAL_DEFINITION",
        "required_inputs": "component stress-current basis; delta_w vector; tau; annulus; norm; units",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "law_id": "CWHL1722_1_operator_bound",
        "quantity": "C_wH_bound",
        "law": "C_wH <= C_Tw(A_ext,norm,tau,basis) * ||delta_w||_Sigma",
        "status": "EXACT_NORM_BOUND_FORM",
        "required_inputs": "operator norm C_Tw; declared delta_w norm/covariance; same component basis",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "law_id": "CWHL1722_2_component_projection",
        "quantity": "C_Tw",
        "law": "C_Tw := ||L_Tw||_{Sigma->A}, L_Tw[delta_w]=star(sum_i delta_w_i T_i_obs(tau,.))",
        "status": "OPERATOR_NORM_TARGET_ONLY",
        "required_inputs": "T_i_obs decomposition; material/source tensor; annulus volume form; norm pair",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "law_id": "CWHL1722_3_zero_limit",
        "quantity": "C_wH_zero",
        "law": "C_wH=0 if delta_w=0 by no-Hom/parent-edge theorem or if L_Tw=0 by a parent source-current silence theorem",
        "status": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        "required_inputs": "no-Hom action-density owner theorem or current silence theorem",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "law_id": "CWHL1722_4_verdict",
        "quantity": "C_wH",
        "law": "C_wH has an exact bound shape, but all numerical/theorem inputs remain missing or proxy-only",
        "status": "BOUND_FORM_DERIVED_INPUTS_MISSING",
        "required_inputs": "C_Tw; ||delta_w||; tau; material tensor; norm; annulus; no shortcut provenance",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CWH_SOURCE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "CWH1722_0_CwH_current_norm_bound_candidate",
        "quantity": "C_wH",
        "definition": "weighted-current correction to the observed Hilbert current norm from surviving source/action weights",
        "bound_formula": "C_wH <= C_Tw * ||delta_w||_Sigma",
        "C_Tw": "MISSING_OPERATOR_NORM",
        "delta_w_norm": "MISSING_DELTA_W_VECTOR_OR_THEOREM_ZERO",
        "norm_type": "MISSING_NORM_TYPE",
        "A_ext": "MISSING_COMPACT_EXTERIOR_ANNULUS",
        "tau_obs": "MISSING_PARENT_SIGNED_TAU_OBS",
        "component_tensor": "MISSING_T_i_OBS_COMPONENT_DECOMPOSITION",
        "material_tensor": "MISSING_FULL_PARENT_MATERIAL_RESPONSE_TENSOR",
        "covariance": "MISSING_DELTA_W_COVARIANCE_OR_NO_CANCELLATION_ENVELOPE",
        "units": "MISSING_CURRENT_NORM_UNITS",
        "source_path": sources_for({"1721_wA_current", "1606_component_pack", "1607_material_tensor", "1608_tau", "1720_jh_theorem"}),
        "source_anchor": "WAC1721_1;DWB1606_*;MTA1607_5;TAU1608_4;JHT1720_2",
        "current_status": "SOURCE_ROW_TEMPLATE_ONLY_NOT_SCORE_READY",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "CWH1722_1_parent_edge_zero_candidate",
        "quantity": "C_wH_zero",
        "definition": "theorem-zero route through parent action-density edge/no-Hom proof",
        "bound_formula": "C_wH=0 if delta_w_A=0 modulo common derivative-silent w_star",
        "C_Tw": "not needed if delta_w zero theorem signed",
        "delta_w_norm": "ZERO_ONLY_IF_PARENT_EDGE_AND_NO_HOM_SIGNED",
        "norm_type": "not applicable if zero theorem signed",
        "A_ext": "not applicable if zero theorem signed",
        "tau_obs": "not applicable if zero theorem signed upstream",
        "component_tensor": "not applicable if zero theorem signed",
        "material_tensor": "not applicable if zero theorem signed",
        "covariance": "not applicable if zero theorem signed",
        "units": "not applicable if zero theorem signed",
        "source_path": sources_for({"1721_no_prefactor", "1605_action_owner", "1606_edges"}),
        "source_anchor": "NSP1721_4;ADO1605_6;EDGE1606_7",
        "current_status": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


INPUT_LEDGER_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "input_id": "IN1722_0_delta_w_vector",
        "needed_input": "delta_w component vector or theorem-zero",
        "current_status": "MISSING_OR_PROXY_NONCLAIM",
        "source_anchor": "1606 component pack",
        "blocks": "C_wH finite score",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "input_id": "IN1722_1_component_stress_tensor",
        "needed_input": "T_i_obs(tau,.) component decomposition on A_ext",
        "current_status": "MISSING_COMPONENT_DECOMPOSITION",
        "source_anchor": "1720/1721 J_H rows",
        "blocks": "operator norm C_Tw",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "input_id": "IN1722_2_material_tensor",
        "needed_input": "full parent material-response/source tensor",
        "current_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
        "source_anchor": "1607 material tensor audit",
        "blocks": "component projection and WEP/R10 finite route",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "input_id": "IN1722_3_tau_and_annulus",
        "needed_input": "parent-signed tau_obs plus compact exterior annulus/norm",
        "current_status": "TAU_WEP_NOT_EVALUATED_AND_NORM_MISSING",
        "source_anchor": "1608 tau contract;1720 norm convention",
        "blocks": "C_Tw and J_H norm",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "input_id": "IN1722_4_parent_edge",
        "needed_input": "parent-owned action-density edge certificate",
        "current_status": "PARENT_EDGE_NOT_DERIVED",
        "source_anchor": "1605 action owner;1606 edge audit",
        "blocks": "C_wH theorem-zero",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1722_0_parent_edge_zero",
        "quantity": "C_wH theorem-zero",
        "runner_decision": "REJECT_THEOREM_ZERO",
        "refusal_reasons": "PARENT_EDGE_NOT_DERIVED;NO_HOM_UNSIGNED;COMMON_MEASURE_UNSIGNED;READOUT_REENTRY_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1722_1_CwH_bound",
        "quantity": "C_wH <= C_Tw ||delta_w||",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_OPERATOR_NORM;MISSING_DELTA_W_VECTOR;MISSING_COMPONENT_STRESS_TENSOR;MISSING_TAU;MISSING_ANNULUS;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1722_2_JH_Ndomain",
        "quantity": "J_H norm and N_domain reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "C_wH_NOT_ZERO_OR_BOUNDED;JH_NORM_MISSING;DPIM_OPERATOR_AND_DELTA_D_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1722_3_Newton_GR",
        "quantity": "Newton/local-GR source-normalization reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "SOURCE_WEIGHT_CURRENT_UNBOUNDED;M_H_REF_MISSING;R_EQ_MISSING;PPN_VECTOR_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


DECISION_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1722_0_parent_edge_route",
        "decision": "do not promote parent-edge zero",
        "because": "the edge/naturality lemma is exact, but no parent action-density edge certificate is sourced",
        "next_action": "try a targeted parent edge proof only with a concrete source line; otherwise keep finite C_wH route",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1722_1_CwH_bound_route",
        "decision": "retain exact operator-bound law",
        "because": "C_wH <= C_Tw ||delta_w|| is the clean finite route if no-w_A remains unsigned",
        "next_action": "fill C_Tw, delta_w norm, tau, annulus, component tensor and covariance as separate nonclaim inputs",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1722_2_next",
        "decision": "build guarded J_H norm stack with C_wH dependency",
        "because": "the J_H norm is the next common choke point for N_domain and Newton/GR source normalization",
        "next_action": "1723 should merge JHN1720 and CWH1722 into one score-refusal schema, or source the first missing operator/tau/annulus input",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1722_0_primary",
        "next_target": "1723-Y5-R2FR-guarded-JH-norm-stack-or-CwH-input-source.md",
        "script": "scripts/Y5_R2FR_guarded_JH_norm_stack_or_CwH_input_source.py",
        "objective": "merge JHN1720 and CWH1722 into one guarded J_H norm stack; if possible, source the first missing C_Tw/tau/annulus input without claims",
        "selection_status": "selected",
        "success_condition": "J_H norm scoring refuses unless C_wH, tau, annulus, non-Hilbert and dPiM dependencies are zero-proved or source-backed",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1722_1_parallel_edge_source_hunt",
        "next_target": "1723b-Y5-R2FR-parent-action-density-edge-source-hunt.md",
        "script": "scripts/Y5_R2FR_parent_action_density_edge_source_hunt.py",
        "objective": "search the corpus for an explicit parent action-density edge/no-Hom source line rather than using physical connectedness",
        "selection_status": "held_parallel",
        "success_condition": "a concrete source path signs one parent-owned ordinary-matter edge, or the edge remains nonclaim",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1722_0_parent_edge",
        "claim": "parent action-density edge certificate theorem-zeroes delta_w",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "only physical/template edges exist; parent-owned edge source missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1722_1_CwH_bound",
        "claim": "C_wH finite bound is score-ready",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "C_Tw, delta_w norm, tau, annulus, component tensor, covariance and units are missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1722_2_JH_norm",
        "claim": "observed J_H norm can feed N_domain",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "C_wH and base J_H norm stack remain unbounded",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1722_3_Newton_local_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "source-weight current, M_H_ref, R_eq, dPiM and PPN vector remain open",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_SOURCE_REGISTER.csv",
    "parent_edge": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_PARENT_ACTION_DENSITY_EDGE_AUDIT.csv",
    "bound_law": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_BOUND_LAW.csv",
    "source_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_CURRENT_NORM_BOUND_ROWS.csv",
    "input_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_INPUT_LEDGER.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1722_VALIDATION.csv",
}


COPY_MAP = {
    "parent_edge": "R2FR_parent_action_density_edge_audit_1722.csv",
    "bound_law": "R2FR_CwH_bound_law_1722.csv",
    "source_rows": "R2FR_CwH_current_norm_bound_rows_1722.csv",
    "input_ledger": "R2FR_CwH_input_ledger_1722.csv",
    "runner_refusal": "R2FR_runner_refusal_1722.csv",
    "decision": "R2FR_decision_ledger_1722.csv",
    "next_target": "R2FR_next_target_1722.csv",
    "claim_gate": "R2FR_claim_gate_1722.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "parent_edge": PARENT_EDGE_ROWS,
        "bound_law": CWH_BOUND_LAW_ROWS,
        "source_rows": CWH_SOURCE_ROWS,
        "input_ledger": INPUT_LEDGER_ROWS,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "decision": DECISION_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1722_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1722_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "edge_zero_ready",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def source_row_paths_exist() -> bool:
    for row in CWH_SOURCE_ROWS:
        paths = [Path(item) for item in row["source_path"].split(";") if item]
        if not paths or any(not path.exists() for path in paths):
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1722_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1722_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1722*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_rows = rows_map["source_register"]
    edge_rows = rows_map["parent_edge"]
    bound_rows = rows_map["bound_law"]
    cwh_rows = rows_map["source_rows"]
    input_rows = rows_map["input_ledger"]
    runner_rows = rows_map["runner_refusal"]
    decision_rows = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1722_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1722_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1722_2_1721_handoff_preserved",
            any(row["source_key"] == "1721_doc" and row["needles_present"] == "True" for row in source_rows),
            "1721 selected parent-edge/CwH route",
            "1721 handoff missing",
        ),
        check(
            "VAL1722_3_parent_edge_not_derived",
            any(row["edge_id"] == "PED1722_4_verdict" and row["current_status"] == "PARENT_EDGE_NOT_DERIVED" for row in edge_rows),
            "parent action-density edge proof remains unproved",
            "parent edge verdict missing or promoted",
        ),
        check(
            "VAL1722_4_bound_law_present",
            any(row["law_id"] == "CWHL1722_1_operator_bound" and row["status"] == "EXACT_NORM_BOUND_FORM" for row in bound_rows),
            "exact CwH operator-bound law is present",
            "CwH operator-bound law missing",
        ),
        check(
            "VAL1722_5_bound_inputs_missing",
            any(row["law_id"] == "CWHL1722_4_verdict" and row["status"] == "BOUND_FORM_DERIVED_INPUTS_MISSING" for row in bound_rows),
            "CwH bound form remains input-missing",
            "CwH verdict missing or score-ready",
        ),
        check(
            "VAL1722_6_CwH_rows_nonclaim",
            len(cwh_rows) == 2 and all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in cwh_rows),
            "CwH source rows exist and remain nonclaim",
            "CwH source rows missing or claim-enabled",
        ),
        check(
            "VAL1722_7_CwH_source_paths_exist",
            source_row_paths_exist(),
            "all source paths listed in CwH rows exist",
            "one or more CwH source paths missing",
        ),
        check(
            "VAL1722_8_input_ledger_blocks",
            len(input_rows) == 5 and all(row["valid_for_claim"] == "False" for row in input_rows),
            "CwH input ledger names all open blockers as nonclaim",
            "CwH input ledger incomplete or claim-enabled",
        ),
        check(
            "VAL1722_9_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses parent-edge zero, CwH score, JH/Ndomain and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1722_10_decision_selects_guarded_stack",
            any(row["decision_id"] == "DEC1722_2_next" and "guarded J_H norm stack" in row["decision"] for row in decision_rows),
            "decision ledger selects guarded J_H norm stack route",
            "decision ledger does not select guarded stack route",
        ),
        check(
            "VAL1722_11_next_selected",
            any(row["route_id"] == "NEXT1722_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects guarded JH norm stack or CwH input source",
            "next target missing selected primary route",
        ),
        check(
            "VAL1722_12_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1722_13_csv_parse", parsed_ok, "all generated 1722 CSVs parse", "one or more generated 1722 CSVs failed to parse"),
        check("VAL1722_14_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1722_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1722_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1722_17_formalization_untouched", formalization_untouched(), "no 1722 outputs found under formalization-workbench", "1722 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1722_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1722 parent action-density edge and CwH current norm-bound validation" if overall else "one or more 1722 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1722 tries the derivation-first route for the `w_A` coupling problem: parent-owned action-density edges plus no source-only Hom would force `delta_w_A=0` modulo one derivative-silent common calibration.",
        "- The edge lemma is exact, but it is still conditional. The current corpus has physical/template ordinary-matter edges, not parent-owned `L_action` morphism certificates.",
        "- The finite fallback is now factorized instead of vague: `C_wH := ||star(sum_i delta_w_i T_i_obs(tau,.))||_{A_ext,norm}` and `C_wH <= C_Tw ||delta_w||_Sigma`.",
        "- That bound is not score-ready because `C_Tw`, the component stress tensor, `delta_w` norm/covariance, tau, annulus, norm type and units are missing or proxy-only.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, source-normalization, `J_H`-norm, `N_domain`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Parent Action-Density Edge Audit",
        markdown_table(rows_map["parent_edge"], ["edge_id", "claim_piece", "current_status", "mathematical_effect", "blocking_gap", "edge_zero_ready"]),
        "",
        "## CwH Bound Law",
        markdown_table(rows_map["bound_law"], ["law_id", "quantity", "law", "status", "required_inputs", "score_ready"]),
        "",
        "## CwH Current Norm Bound Rows",
        markdown_table(rows_map["source_rows"], ["row_id", "quantity", "bound_formula", "C_Tw", "delta_w_norm", "tau_obs", "material_tensor", "current_status", "score_ready", "valid_for_claim"]),
        "",
        "## CwH Input Ledger",
        markdown_table(rows_map["input_ledger"], ["input_id", "needed_input", "current_status", "source_anchor", "blocks"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1722 turns the coupling problem into a clean fork. The theorem route now needs an actual parent-owned action-density edge certificate, not physical connectedness. The finite route now has a real inequality, `C_wH <= C_Tw ||delta_w||`, but no one gets to score it until the operator norm, component basis, tau, annulus and covariance exist. This is useful because it makes the GR/Newton source-normalization path harder to fool and easier to finish.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1722-Y5-R2FR-parent-action-density-edge-or-CwH-current-norm-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1722_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1722 validation FAIL")
    print("1722 validation PASS")


if __name__ == "__main__":
    main()
